##############################################################################
# Copyright 2018-2020 Rigetti Computing
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

import logging
import sys
from typing import Type

from jupyter_forest_extension.utc_logging_formatter import UTCFormatter

LOG_FORMAT = '%(asctime)sZ|%(name)-20s|Thread: %(thread)d|PID: %(process)d|%(levelname)-8s|%(message)s'


class LoggingService:
    initialized = False

    @classmethod
    def initialize(cls) -> None:
        if not cls.initialized:
            level = 'INFO'
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.DEBUG)
            formatter = UTCFormatter(LOG_FORMAT)
            handler.setFormatter(formatter)
            logging.basicConfig(handlers=[handler], level=level)
            cls.initialized = True

    @classmethod
    def get_global_logger(cls) -> logging.Logger:
        return cls.get_named_logger("Global")

    @classmethod
    def get_logger_for_class(cls, class_to_log: Type) -> logging.Logger:
        if not cls.initialized:
            cls.initialize()

        return cls.get_named_logger(class_to_log.__name__)

    @classmethod
    def get_named_logger(cls, name: str) -> logging.Logger:
        if not cls.initialized:
            cls.initialize()

        return logging.getLogger(name)
