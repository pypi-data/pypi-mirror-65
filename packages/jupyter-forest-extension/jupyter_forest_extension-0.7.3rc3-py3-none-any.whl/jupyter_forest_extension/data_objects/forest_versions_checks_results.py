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

from typing import Optional

from dotmap import DotMap

from jupyter_forest_extension.data_objects.serializable import Serializable


class ForestVersionsChecksResults(Serializable['ForestVersionsChecksResults']):
    @classmethod
    def build_from_serialized(cls, serialized_obj: DotMap) -> 'ForestVersionsChecksResults':
        return ForestVersionsChecksResults(serialized_obj.quilc,
                                           serialized_obj.qvm,
                                           serialized_obj.pyquil)

    def __init__(self, quilc: Optional[bool] = None,
                 qvm: Optional[bool] = None,
                 pyquil: Optional[bool] = None):
        self._qvm = qvm
        self._quilc = quilc
        self._pyquil = pyquil

    @property
    def qvm(self) -> Optional[bool]:
        return self._qvm

    @property
    def quilc(self) -> Optional[bool]:
        return self._quilc

    @property
    def pyquil(self) -> Optional[bool]:
        return self._pyquil
