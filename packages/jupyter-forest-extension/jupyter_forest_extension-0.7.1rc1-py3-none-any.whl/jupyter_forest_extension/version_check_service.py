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
from logging import Logger, DEBUG
from typing import Dict, Optional

import docker
import docker.errors

import re
import aiohttp

from docker.models.images import Image
from dotmap import DotMap

from jupyter_forest_extension.data_objects.docker_image import DockerImage
from jupyter_forest_extension.data_objects.forest_docker_images import ForestDockerImages
from jupyter_forest_extension.data_objects.forest_versions_checks_request import ForestVersionsChecksRequest
from jupyter_forest_extension.data_objects.forest_version_to_check import ForestVersionToCheck
from jupyter_forest_extension.data_objects.post_forest_versions_checks_response import \
    PostForestVersionsChecksResponse
from jupyter_forest_extension.logging_service import LoggingService
from urllib import parse

DOCKER_DIGEST_REGEX = re.compile(r'rigetti/([^@]+)@(.+)')


class Failure:
    def __init__(self, component: str, short_description: str, long_description: str = None):
        self.component = component
        self.short_description = short_description
        self.long_description = long_description or short_description


class VersionCheckService:
    def __init__(self, forest_host: Optional[str] = None, logger: Optional[Logger] = None):
        if logger:
            self._logger = logger
        else:
            self._logger = LoggingService.get_named_logger(__name__)

        if forest_host:
            self._forest_host = forest_host
            return

        try:
            # Dynamically load pyquil. The extension should be able to operate with or without pyquil
            # Without pyquil, it is not able to read the configuration for the forest_url
            # and must fall back to a default value

            # noinspection PyProtectedMember, PyUnresolvedReferences
            from pyquil.api._config import PyquilConfig
            host = PyquilConfig().forest_url
        except ImportError:
            default_host = "https://forest-server.qcs.rigetti.com"
            self._logger.debug("pyquil package not available to read forest_url configuration, "
                               "defaulting to %s", default_host)
            host = default_host

        self._forest_host = host

    async def get_state(self, data_dict: Dict, docker_info_dict: Optional[Dict]) -> Dict:
        if self._logger.isEnabledFor(DEBUG):
            data_dict_string = json.dumps(data_dict)
            docker_info_dict_string = json.dumps(docker_info_dict)
            self._logger.debug("get_state: data_dict: %s docker_info_dict %s", data_dict_string,
                               docker_info_dict_string)

        docker_info = DotMap(docker_info_dict)
        data = DotMap(data_dict)
        failures = []

        python_executable = data.pythonExecutable
        python_version = data.pythonVersion
        packages = data.packages
        qvm_info = data.qvmInfo
        quilc_info = data.quilcInfo
        version_statuses = []
        pyquil_package = None

        for python_package in packages:
            self._logger.debug(json.dumps(python_package))
            if python_package["key"] == "pyquil":
                pyquil_package = python_package

        if pyquil_package:
            version_statuses.append("pyquil: {}".format(pyquil_package.version))

            if qvm_info:
                version_statuses.append("qvm: {}".format(qvm_info))
                if quilc_info:
                    version_statuses.append("quilc: {}".format(quilc_info.quilc))
                else:
                    failures.append(Failure("quilc", "quilc not installed or accessible"))
            else:
                failures.append(Failure("qvm", "QVM not installed or accessible"))
        else:
            failures.append(Failure("pyquil", "pyQuil needs to be installed"))
            version_statuses.append("pyquil: missing")
            version_statuses.append("qvm: N/A (pyQuil missing)")
            version_statuses.append("quilc: N/A (pyQuil missing)")

        long_version_statuses = version_statuses.copy()

        if python_executable:
            long_version_statuses.append("Interpreter:{}".format(python_executable))
        else:
            # This means that the JupyterLab extension failed
            raise ValueError("Python Executable not provided")

        if python_version:
            long_version_statuses.append("Python Version:{}".format(python_version))
        else:
            # This means that the JupyterLab extension failed
            raise ValueError("Python version not provided")

        if docker_info.qvm:
            qvm_service_tags = docker_info.qvm.tags
            if qvm_service_tags:
                long_version_statuses.append("Docker service tags: {}".format(", ".join(qvm_service_tags)))
        else:
            failures.append(Failure("qvm", "qvm docker service not found"))

        if docker_info.quilc:
            quilc_service_tags = docker_info.quilc.tags
            if quilc_service_tags:
                long_version_statuses.append("Docker service tags: {}".format(", ".join(quilc_service_tags)))
        else:
            failures.append(Failure("quilc", "quilc docker service not found"))

        if len(failures) > 0:
            short_status = "Forest services misconfigured or not running"
            state = "Error"
        else:
            url = parse.urljoin("{}".format(self._forest_host), "v1/forest_versions/check")
            self._logger.debug("url: %s", url)
            forest_version = ForestVersionToCheck(quilc=quilc_info.quilc,
                                                  qvm=qvm_info,
                                                  pyquil=pyquil_package.version)
            forest_docker_images = ForestDockerImages(quilc=DockerImage(docker_info.quilc.digest),
                                                      qvm=DockerImage(docker_info.qvm.digest))

            request = ForestVersionsChecksRequest(forest_versions_checks=forest_version,
                                                  forest_docker_versions_checks=forest_docker_images)

            self._logger.debug("request: %s", request.dumps())

            async with aiohttp.ClientSession() as session:
                result = await session.post(url=url, data=request.dumps())

            try:
                result.raise_for_status()
                self._logger.debug("status: %s", result.status)

                text = await result.text()
                self._logger.debug("result: %s", text)
                try:
                    deserialized_result = PostForestVersionsChecksResponse.deserialize(
                        text)  # type: Optional[PostForestVersionsChecksResponse]
                except BaseException:
                    self._logger.exception("Exception deserializing result")
                    deserialized_result = None
            except BaseException:
                failures.append(Failure("general", "Unable to check versions",
                                        "Unable to check versions ({})".format(result.status)))
                self._logger.exception("Exception checking versions")
                deserialized_result = None

            if not deserialized_result:
                state = "Error"
                failures.append(
                    Failure("general", "Unable to check versions", "Unable to check versions (deserialization)"))
                short_status = ", ".join(failure.short_description for failure in failures)
            else:
                ok_version_pattern = "{}: v{} Up to date"
                ok_service_pattern = "{}: Docker service up to date"

                stale_version_long_pattern = "{}: v{} Out of date"
                stale_version_short_pattern = "{}: Out of date"

                stale_service_short_pattern = "{}: Docker service out of date"
                stale_service_long_pattern = "{}: Docker service with digest {} out of date"

                version = qvm_info
                service_version = docker_info.qvm.digest

                key = 'qvm'
                version_result = deserialized_result.forest_versions_checks_results.qvm
                if not version_result:
                    failures.append(Failure(key, stale_version_short_pattern.format(key, version),
                                            stale_version_long_pattern.format(key, version)))
                else:
                    long_version_statuses.append(ok_version_pattern.format(key, version))

                docker_result = deserialized_result.forest_docker_versions_checks_results.qvm

                if not docker_result:
                    failures.append(Failure(key, stale_service_short_pattern.format(key),
                                            stale_service_long_pattern.format(key, service_version[:13])))
                else:
                    long_version_statuses.append(ok_service_pattern.format(key))

                version = pyquil_package.version
                key = 'pyquil'
                version_result = deserialized_result.forest_versions_checks_results.pyquil
                if not version_result:
                    failures.append(Failure(key, stale_version_short_pattern.format(key, version),
                                            stale_version_long_pattern.format(key, version)))
                else:
                    long_version_statuses.append(ok_version_pattern.format(key, version))

                version = quilc_info.quilc
                service_version = docker_info.quilc.digest

                key = 'quilc'
                version_result = deserialized_result.forest_versions_checks_results.quilc
                if not version_result:
                    failures.append(Failure(key, stale_version_short_pattern.format(key, version),
                                            stale_version_long_pattern.format(key, version)))
                else:
                    long_version_statuses.append(ok_version_pattern.format(key, version))

                docker_result = deserialized_result.forest_docker_versions_checks_results.quilc
                if not docker_result:
                    failures.append(Failure(key, stale_service_short_pattern.format(key),
                                            stale_service_long_pattern.format(key, service_version[:13])))
                else:
                    long_version_statuses.append(ok_service_pattern.format(key))

                if not failures:
                    state = "OK"
                    short_status = "Up to date"
                else:
                    state = "Out of date"
                    short_status = ", ".join(failure.short_description for failure in failures)

        if failures:
            long_version_statuses.append("Failures:")
            long_version_statuses.extend(failure.long_description for failure in failures)

        overall_state = {"versionStatus": short_status,
                         "longVersionStatus": "\n".join(long_version_statuses),
                         "state": state}

        self._logger.debug(overall_state)

        return overall_state

    @staticmethod
    def get_digest(image: Image, expected_repo: str) -> Optional[str]:
        repo_digests = image.attrs.get('RepoDigests')
        if not repo_digests:
            return None

        return VersionCheckService.parse_digest_string(expected_repo, repo_digests)

    @staticmethod
    def parse_digest_string(expected_repo, repo_digests):
        if not repo_digests:
            return None

        if len(repo_digests) != 1:
            # Only know how to deal with a single digest
            return None

        match = DOCKER_DIGEST_REGEX.match(repo_digests[0])
        if not match:
            return None
        if not match.groups() or len(match.groups()) != 2:
            return None
        if match.groups()[0] != expected_repo:
            return None
        return match.groups()[1]

    def get_docker_information(self) -> Dict:
        forest_containers = {"qvm": "qcs_qvm",
                             "quilc": "qcs_quilc"}

        forest_container_info = {}
        service_responsive = False
        client = None
        try:
            client = docker.from_env()
            service_responsive = client.ping()
        except docker.errors.APIError:
            self._logger.exception("Unable to communicate with Docker service")

        self._logger.debug("Able to communicate with docker service")

        if service_responsive and client:
            for container in client.containers.list():
                for key, container_name in forest_containers.items():
                    if container.name == container_name:
                        self._logger.debug("Found %s", container_name)
                        client.images.get(container.image.id)

                        repo_digest = VersionCheckService.get_digest(container.image, key)
                        forest_container_info[key] = {"image_id": container.image.id,
                                                      "tags": container.image.tags,
                                                      "digest": repo_digest}

        self._logger.debug(json.dumps(forest_container_info))
        return forest_container_info
