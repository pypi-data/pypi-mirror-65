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

from typing import Iterable

from dotmap import DotMap

from jupyter_forest_extension.data_objects.forest_version import ForestVersion
from jupyter_forest_extension.data_objects.serializable import Serializable


class ForestVersions(Serializable['ForestVersions']):
    @classmethod
    def build_from_serialized(cls, serialized_obj: DotMap) -> 'ForestVersions':
        return ForestVersions([ForestVersion.build_from_serialized(version) for version in serialized_obj.versions],
                              ForestVersion.build_from_serialized(serialized_obj.latest))

    def __init__(self, versions: Iterable[ForestVersion], latest: ForestVersion) -> None:
        self._versions = versions
        self._latest = latest

    @property
    def versions(self) -> Iterable[ForestVersion]:
        return self._versions

    @property
    def latest(self) -> ForestVersion:
        return self._latest
