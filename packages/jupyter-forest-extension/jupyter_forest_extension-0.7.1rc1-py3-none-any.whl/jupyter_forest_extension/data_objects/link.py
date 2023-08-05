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


class Link(Serializable['Link']):
    @classmethod
    def build_from_serialized(cls, serialized_obj: DotMap) -> 'Link':
        return Link(serialized_obj.text, serialized_obj.url)

    def __init__(self, text: str, url: str) -> None:
        self._url = url
        self._text = text

    @property
    def url(self) -> str:
        return self._url

    @property
    def text(self) -> str:
        return self._text
