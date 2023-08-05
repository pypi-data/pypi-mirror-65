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

from jupyter_forest_extension.data_objects.serializable import Serializable


class ForestVersionToCheck(Serializable['ForestVersionToCheck']):
    @classmethod
    def build_from_serialized(cls, serialized_obj: DotMap) -> 'ForestVersionToCheck':
        return ForestVersionToCheck(serialized_obj.quilc,
                                    serialized_obj.qvm,
                                    serialized_obj.pyquil)

    def __init__(self, quilc: str, qvm: str, pyquil: str) -> None:
        self._quilc = quilc
        self._qvm = qvm
        self._pyquil = pyquil

    @property
    def quilc(self) -> str:
        return self._quilc

    @property
    def qvm(self) -> str:
        return self._qvm

    @property
    def pyquil(self) -> str:
        return self._pyquil
