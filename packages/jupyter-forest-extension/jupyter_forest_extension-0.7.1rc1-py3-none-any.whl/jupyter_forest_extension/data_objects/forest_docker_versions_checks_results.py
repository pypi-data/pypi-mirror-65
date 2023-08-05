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

from typing import Optional, Dict, Any

from dotmap import DotMap

from jupyter_forest_extension.data_objects.docker_image_check_result import DockerImageCheckResult
from jupyter_forest_extension.data_objects.serializable import Serializable


class ForestDockerVersionsChecksResults(Serializable['ForestDockerVersionsChecksResults']):
    def __init__(self, quilc: Optional[DockerImageCheckResult] = None, qvm: Optional[DockerImageCheckResult] = None):
        self._qvm = qvm
        self._quilc = quilc

    @classmethod
    def build_from_serialized(cls, serialized_obj: DotMap) -> 'ForestDockerVersionsChecksResults':
        quilc_result = DockerImageCheckResult(serialized_obj.quilc) if serialized_obj.quilc else None
        qvm_result = DockerImageCheckResult(serialized_obj.qvm) if serialized_obj.qvm else None
        return ForestDockerVersionsChecksResults(quilc_result, qvm_result)

    @property
    def qvm(self) -> Optional[DockerImageCheckResult]:
        return self._qvm

    @property
    def quilc(self) -> Optional[DockerImageCheckResult]:
        return self._quilc

    def __getstate__(self) -> Dict[str, Any]:
        state = {}
        if self._qvm is not None:
            state['qvm'] = self._qvm.value
        if self._quilc is not None:
            state['quilc'] = self._quilc.value
        return state
