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

import inspect
from abc import abstractmethod
from typing import Dict, Any, TypeVar, Type, Generic, Optional

import simplejson as simplejson
from dotmap import DotMap

T = TypeVar('T', bound='Serializable')


class Serializable(Generic[T]):
    @staticmethod
    def remove_nulls(d: Dict) -> Dict:
        return {k: v for k, v in d.items() if v is not None}

    @staticmethod
    def normalize_json(json: str, indent: Optional[int] = 2, remove_nulls: bool = True) -> str:
        """
        Take a json string, deserialize it, apply formatting and null conventions and then serialize it
        """
        if remove_nulls:
            simplejson_deserialized = simplejson.loads(json, object_hook=Serializable.remove_nulls)
        else:
            simplejson_deserialized = simplejson.loads(json)

        return simplejson.dumps(simplejson_deserialized, indent=indent, sort_keys=True)

    @classmethod
    def deserialize(cls: Type[T], serialized: str) -> T:
        return cls.build_from_serialized(DotMap(simplejson.loads(serialized, object_hook=Serializable.remove_nulls)))

    @classmethod
    @abstractmethod
    def build_from_serialized(cls, serialized_obj: DotMap) -> T:
        raise NotImplementedError

    @staticmethod
    def has_member(obj, name):
        return any(name == _name for _name, member in inspect.getmembers(obj))

    @staticmethod
    def getstate_if_possible(obj):
        if isinstance(obj, Serializable):
            return obj.__getstate__()
        elif isinstance(obj, (tuple, list)):
            elements = []
            for element in obj:
                element_state = Serializable.getstate_if_possible(element)
                if element_state is not None:
                    elements.append(element_state)
            return elements or None
        elif isinstance(obj, (dict, DotMap)):
            state = {}
            for k in obj.keys():
                if k.startswith('__'):
                    # DotMap will add empty values for things like __bases__ if code tries to access such keys
                    # This causes infinite recursion behavior so these properties are skipped from serialization
                    continue

                value = obj[k]
                if value is None:
                    continue

                entry_state = Serializable.getstate_if_possible(value)
                if entry_state is None:
                    continue

                state[k] = entry_state

            if not state:
                return None

            return state
        else:
            return obj

    def __getstate__(self) -> Optional[Dict[str, Any]]:
        properties = [x for x in inspect.getmembers(type(self), lambda member: isinstance(member, property))
                      if not (x[0].startswith('_'))]

        state = {}

        for prop in properties:
            # print("Looking at {}".format(prop[0]))
            property_name = prop[0]
            value = self.__getattribute__(property_name)
            if value is not None:
                property_state = self.getstate_if_possible(value)

                if property_state is not None:
                    state[property_name] = property_state

        if not state:
            return None

        return state

    def dumps(self, indent: Optional[int] = 2) -> str:
        """
        Return a JSON representation of this object based upon public properties only
        """
        state = self.__getstate__()
        return simplejson.dumps(state, indent=indent, sort_keys=True)
