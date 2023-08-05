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
from typing import Iterable, Optional, List

from dotmap import DotMap

from jupyter_forest_extension.data_objects.link import Link
from jupyter_forest_extension.data_objects.serializable import Serializable


class ForestVersion(Serializable['ForestVersion']):
    @classmethod
    def build_from_serialized(cls, serialized_obj: DotMap) -> 'ForestVersion':
        if serialized_obj.links:
            links = [Link(link.text, link.url) for link in serialized_obj.links]  # type: Optional[List[Link]]
        else:
            links = None

        return ForestVersion(serialized_obj.quilc,
                             serialized_obj.qvm,
                             serialized_obj.sdk,
                             serialized_obj.notes,
                             serialized_obj.title,
                             links)

    def __init__(self, quilc: str, qvm: str, sdk: str, notes: Optional[str] = None, title: Optional[str] = None,
                 links: Optional[Iterable[Link]] = None) -> None:
        self._title = title
        self._notes = notes
        self._quilc = quilc
        self._qvm = qvm
        self._sdk = sdk

        self._links = tuple(links) if links else None

    @property
    def notes(self) -> Optional[str]:
        return self._notes

    @property
    def links(self) -> Optional[Iterable[Link]]:
        return self._links

    @property
    def quilc(self) -> str:
        return self._quilc

    @property
    def qvm(self) -> str:
        return self._qvm

    @property
    def sdk(self) -> str:
        return self._sdk

    @property
    def title(self) -> Optional[str]:
        return self._title
