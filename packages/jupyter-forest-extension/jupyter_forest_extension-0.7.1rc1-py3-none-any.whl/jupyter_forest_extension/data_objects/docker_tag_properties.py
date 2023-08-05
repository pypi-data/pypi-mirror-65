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


class DockerTagProperties(Serializable['DockerTagProperties']):
    @classmethod
    def build_from_serialized(cls, serialized_obj: DotMap) -> 'DockerTagProperties':
        return DockerTagProperties(serialized_obj.digest,
                                   serialized_obj.architecture,
                                   serialized_obj.features,
                                   serialized_obj.variant,
                                   serialized_obj.os,
                                   serialized_obj.os_features,
                                   serialized_obj.os_version,
                                   serialized_obj.size)

    def __init__(self, digest: str, architecture: Optional[str] = None, features: Optional[str] = None,
                 variant: Optional[str] = None,
                 os: Optional[str] = None,
                 os_features: Optional[str] = None,
                 os_version: Optional[str] = None,
                 size: Optional[int] = None):
        self._digest = digest
        self._variant = variant
        self._os = os
        self._os_features = os_features
        self._size = size
        self._architecture = architecture
        self._features = features
        self._os_version = os_version

    @property
    def architecture(self) -> Optional[str]:
        return self._architecture

    @property
    def digest(self) -> str:
        return self._digest

    @property
    def features(self) -> Optional[str]:
        return self._features

    @property
    def variant(self) -> Optional[str]:
        return self._variant

    @property
    def os(self) -> Optional[str]:
        return self._os

    @property
    def os_features(self) -> Optional[str]:
        return self._os_features

    @property
    def os_version(self) -> Optional[str]:
        return self._os_version

    @property
    def size(self) -> Optional[int]:
        return self._size
