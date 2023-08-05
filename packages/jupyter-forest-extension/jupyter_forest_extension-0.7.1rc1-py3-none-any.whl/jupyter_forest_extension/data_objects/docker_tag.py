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

from typing import Iterable, Sequence, Optional

from dotmap import DotMap

from jupyter_forest_extension.data_objects.docker_tag_properties import DockerTagProperties
from jupyter_forest_extension.data_objects.serializable import Serializable


class DockerTag(Serializable['DockerTag']):
    @classmethod
    def build_from_serialized(cls, serialized_obj: DotMap) -> 'DockerTag':
        return DockerTag(
            (DockerTagProperties.build_from_serialized(image_dict) for image_dict in serialized_obj.images),
            serialized_obj.v2, serialized_obj.repository, serialized_obj.name,
            serialized_obj.creator, serialized_obj.full_size, serialized_obj.id, serialized_obj.image_id,
            serialized_obj.last_updater_username,
            serialized_obj.last_updated, serialized_obj.last_updater)

    def __init__(self, images: Iterable[DockerTagProperties],
                 v2: Optional[str] = None,
                 repository: Optional[str] = None,
                 name: Optional[str] = None,
                 creator: Optional[int] = None,
                 full_size: Optional[int] = None,
                 id: Optional[int] = None,
                 image_id: Optional[str] = None,
                 last_updater_username: Optional[str] = None,
                 last_updated: Optional[str] = None, last_updater: Optional[str] = None):
        self._image_id = image_id
        self._creator = creator
        self._full_size = full_size
        self._id = id
        self._image_id = image_id
        self._v2 = v2
        self._repository = repository
        self._name = name
        self._last_updater_username = last_updater_username
        self._last_updated = last_updated
        self._last_updater = last_updater
        self._images = tuple(images)

    @property
    def creator(self) -> Optional[int]:
        return self._creator

    @property
    def full_size(self) -> Optional[int]:
        return self._full_size

    @property
    def id(self) -> Optional[int]:
        return self._id

    @property
    def image_id(self) -> Optional[str]:
        return self._image_id

    @property
    def last_updater(self) -> Optional[str]:
        return self._last_updater

    @property
    def last_updated(self) -> Optional[str]:
        return self._last_updated

    @property
    def last_updater_username(self) -> Optional[str]:
        return self._last_updater_username

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def repository(self) -> Optional[str]:
        return self._repository

    @property
    def v2(self) -> Optional[str]:
        return self._v2

    @property
    def images(self) -> Sequence[DockerTagProperties]:
        return self._images
