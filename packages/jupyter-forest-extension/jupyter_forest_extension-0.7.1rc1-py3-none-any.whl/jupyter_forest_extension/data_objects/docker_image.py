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


class DockerImage(Serializable['DockerImage']):
    @classmethod
    def build_from_serialized(cls, serialized_obj: DotMap) -> 'DockerImage':
        return DockerImage(serialized_obj.Image)

    def __init__(self, image: str) -> None:
        self._image = image

    @property
    def image(self) -> str:
        return self._image

    def __getstate__(self):
        return {"Image": self._image}
