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

from jupyter_forest_extension.data_objects.docker_tag import DockerTag
from jupyter_forest_extension.data_objects.serializable import Serializable


class DockerTags(Serializable):
    @classmethod
    def build_from_serialized(cls, serialized_obj: DotMap) -> 'DockerTags':
        return DockerTags(DockerTag.build_from_serialized(serialized_obj.latest),
                          DockerTag.build_from_serialized(serialized_obj.stable),
                          DockerTag.build_from_serialized(serialized_obj.edge))

    def __init__(self, latest: DockerTag, stable: DockerTag, edge: DockerTag):
        self._edge = edge
        self._stable = stable
        self._latest = latest

    @property
    def edge(self):
        return self._edge

    @property
    def stable(self):
        return self._stable

    @property
    def latest(self):
        return self._latest
