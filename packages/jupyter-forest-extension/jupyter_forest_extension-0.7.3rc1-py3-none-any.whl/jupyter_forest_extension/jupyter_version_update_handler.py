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
import os
from logging import INFO
from typing import Optional, Awaitable

import tornado
from jupyter_forest_extension.jupyter_version_service import JupyterVersionService
from jupyter_forest_extension.process_executor import ProcessExecutor
from notebook.base.handlers import IPythonHandler
from tornado import web
from tornado.ioloop import IOLoop
from jupyterlab import commands


class JupyterVersionUpdateHandler(IPythonHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def initialize(self):
        super().initialize()

    def upgrade(self):
        try:
            if JupyterVersionService.update_in_progress():
                raise ValueError("Update in progress")

            JupyterVersionService.set_update_in_progress(True)
            version_checker = JupyterVersionService(logger=self.log)

            release_candidate_mode = (os.getenv('JUPYTER_FOREST_RC', 0) == '1')

            jupyter_forest_extension_version = os.getenv('JUPYTER_FOREST_EXTENSION_VERSION', None)
            if jupyter_forest_extension_version is not None:
                version_checker.install_python_package_version('jupyter_forest_extension',
                                                               version=jupyter_forest_extension_version)
            else:
                version_checker.install_python_package_version('jupyter_forest_extension',
                                                               pre=release_candidate_mode)

            jupyterlab_forest_extension_tag = os.getenv('JUPYTERLAB_FOREST_EXTENSION_TAG', None)

            if jupyterlab_forest_extension_tag is not None:
                version = '@qcs/jupyterlab_forest_extension@{}'.format(jupyterlab_forest_extension_tag)
                build_required = version_checker.install_jupyterlab_extension(version)
            elif release_candidate_mode:
                build_required = version_checker.install_jupyterlab_extension('@qcs/jupyterlab_forest_extension@rc')
            else:
                build_required = version_checker.install_jupyterlab_extension('@qcs/jupyterlab_forest_extension')

            if build_required:
                commands.build()

            restart_command = os.getenv('JUPYTER_EXTENSIONS_RESTART_COMMAND', 'sudo systemctl restart jupyter')
            result = ProcessExecutor(self.log).check_output(restart_command, log_level=INFO)
            self.log.debug("result %s", result)
        finally:
            JupyterVersionService.set_update_in_progress(False)

    @web.authenticated
    async def post(self):
        self.log.info("Jupyter Update requested")

        if JupyterVersionService.update_in_progress():
            raise tornado.web.HTTPError(status_code=409, log_message="An upgrade is in process")

        # See: http://www.tornadoweb.org/en/stable/guide/coroutines.html#how-to-call-a-coroutine
        IOLoop.current().spawn_callback(lambda: self.upgrade())
        self.write("Update request received")
