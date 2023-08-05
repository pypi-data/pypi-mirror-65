##############################################################################
# Copyright 2019-2020 Rigetti Computing
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
##############################################################################

import json
import sys
from logging import Logger, INFO
from typing import Dict, Optional, Iterable
import re

from cachetools import TTLCache

from jupyter_forest_extension.logging_service import LoggingService
from jupyter_forest_extension.process_executor import ProcessExecutor

from pypi_simple import PyPISimple

from jupyterlab import commands
from packaging.version import Version

DEFAULT_JUPYTER_EXTENSION = 'jupyter_forest_extension'
DEFAULT_JUPYTERLAB_EXTENSION = '@qcs/jupyterlab-forest-extension'


class JupyterVersionService:
    _update_in_progress = False

    @classmethod
    def update_in_progress(cls) -> bool:
        return cls._update_in_progress

    @classmethod
    def set_update_in_progress(cls, value: bool) -> None:
        cls._update_in_progress = value

    def __init__(self, logger: Optional[Logger] = None, cache_ttl: Optional[int] = 60):
        if logger:
            self._logger = logger
        else:
            self._logger = LoggingService.get_named_logger(__name__)

        self._installed_version_cache = TTLCache(10, ttl=60)
        self._process_executor = ProcessExecutor(self._logger)

        if cache_ttl:
            # Use a cache instance rather than decorators to allow dynamic setting the ttl
            self._cache = TTLCache(1, cache_ttl)
        else:
            self._cache = None

    @staticmethod
    def read_version_from_pip_show_output(pip_show_output: str) -> Version:
        for line in pip_show_output.splitlines():
            match = re.match(r"^\s*Version:\s*(.*)\s*$", line, re.IGNORECASE)
            if match:
                return Version(match.group(1))

        raise ValueError("Version not found in output {}".format(pip_show_output))

    def get_installed_python_version(self, package: str = DEFAULT_JUPYTER_EXTENSION) -> Version:
        pip_show_output = self._process_executor.check_output([sys.executable, '-m', 'pip', 'show', package])
        return JupyterVersionService.read_version_from_pip_show_output(pip_show_output)

    @staticmethod
    def get_available_python_versions(package: str = DEFAULT_JUPYTER_EXTENSION) -> Iterable[Version]:
        client = PyPISimple()
        packages = client.get_project_files(package)
        return tuple([Version(python_package.version) for python_package in packages])

    def get_latest_compatible_python_version(self, package: str = DEFAULT_JUPYTER_EXTENSION) -> Version:
        pip_show_output = self._process_executor.check_output(args=[sys.executable, '-m', 'pip', 'list',
                                                                    '--outdated', '--format', 'json'])

        packages = json.loads(pip_show_output)

        for outdated_package in packages:
            if outdated_package['name'] == package:
                return Version(outdated_package['latest_version'])

        # No update necessary
        return self.get_installed_python_version(package)

    def install_jupyterlab_extension(self, package: str) -> bool:
        # If package is a tgz path, it will be installed from the tarball
        build_required = commands.install_extension(package)
        build_required |= commands.update_extension(package)
        return build_required

    def install_python_package_version(self, package: str, version: str = None, pre: bool = False) -> None:
        version_suffix = "=={}".format(version) if version else ""
        install_command = [sys.executable, '-m', 'pip', 'install']

        if pre:
            install_command.append("--pre")

        if not version:
            install_command.append("--upgrade")

        install_command.append("{}{}".format(package, version_suffix))

        self._process_executor.check_output(install_command, log_level=INFO)

    @staticmethod
    def get_latest_compatible_jupyterlab_extension_version(package: str
                                                           = DEFAULT_JUPYTERLAB_EXTENSION) -> Optional[Version]:
        extensions = commands.get_latest_compatible_package_versions([package])
        version = extensions.get(package)
        return Version(version) if version else None

    @staticmethod
    def get_installed_jupyterlab_extensions() -> Dict:
        info = commands.get_app_info()
        return info['extensions']

    @staticmethod
    def get_installed_jupyterlab_extension_version(package: str
                                                   = DEFAULT_JUPYTERLAB_EXTENSION) -> Optional[Version]:
        extensions = JupyterVersionService.get_installed_jupyterlab_extensions()
        extension = extensions.get(package)
        if extension:
            return Version(extension['version'])
        else:
            return None

    def python_package_is_current(self, package: str = DEFAULT_JUPYTER_EXTENSION) -> bool:
        installed_version = self.get_installed_python_version(package)
        latest_version = self.get_latest_compatible_python_version(package)

        return installed_version >= latest_version

    @staticmethod
    def jupyterlab_extension_is_current(package: str = DEFAULT_JUPYTERLAB_EXTENSION) -> bool:
        installed_version = JupyterVersionService.get_installed_jupyterlab_extension_version(package)

        if installed_version is None:
            raise ValueError("Extension {} is not installed".format(package))

        latest_compatible_version = \
            JupyterVersionService.get_latest_compatible_jupyterlab_extension_version(package)

        if latest_compatible_version is None:
            raise ValueError("Latest compatible version couldn't be determined")

        return installed_version >= latest_compatible_version

    def get_state(self, python_package: str = DEFAULT_JUPYTER_EXTENSION,
                  jupyterlab_extension: str = DEFAULT_JUPYTERLAB_EXTENSION) -> Dict[str, bool]:
        if self._cache is None:
            return self.build_state(python_package, jupyterlab_extension)

        cache_key = 'get_state'

        if cache_key in self._cache:
            return self._cache[cache_key]
        else:
            state = self.build_state(python_package, jupyterlab_extension)
            self._cache[cache_key] = state
            return state

    def build_state(self, python_package: str = DEFAULT_JUPYTER_EXTENSION,
                    jupyterlab_extension: str = DEFAULT_JUPYTERLAB_EXTENSION) -> Dict[str, bool]:
        jupyter_forest_extension_ok = self.python_package_is_current(python_package)
        jupyterlab_extension_is_ok = self.jupyterlab_extension_is_current(jupyterlab_extension)
        state = {python_package: jupyter_forest_extension_ok,
                 jupyterlab_extension: jupyterlab_extension_is_ok}
        return state
