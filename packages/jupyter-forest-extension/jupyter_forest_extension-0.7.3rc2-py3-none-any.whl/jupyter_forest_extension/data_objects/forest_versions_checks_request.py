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

from dotmap import DotMap

from jupyter_forest_extension.data_objects.forest_docker_images import ForestDockerImages
from jupyter_forest_extension.data_objects.forest_version_to_check import ForestVersionToCheck
from jupyter_forest_extension.data_objects.serializable import Serializable


class ForestVersionsChecksRequest(Serializable['ForestVersionsChecksRequest']):
    @classmethod
    def build_from_serialized(cls, serialized_obj: DotMap) -> 'ForestVersionsChecksRequest':
        forest_versions_checks = ForestVersionToCheck.build_from_serialized(serialized_obj.forest_versions_checks)
        forest_docker_versions_checks = ForestDockerImages.build_from_serialized(
            serialized_obj.forest_docker_versions_checks)
        return ForestVersionsChecksRequest(forest_versions_checks, forest_docker_versions_checks)

    def __init__(self, forest_versions_checks: ForestVersionToCheck,
                 forest_docker_versions_checks: ForestDockerImages) -> None:
        self._forest_versions_checks = forest_versions_checks
        self._forest_docker_versions_checks = forest_docker_versions_checks

    @property
    def forest_versions_checks(self) -> ForestVersionToCheck:
        return self._forest_versions_checks

    @property
    def forest_docker_versions_checks(self) -> ForestDockerImages:
        return self._forest_docker_versions_checks
