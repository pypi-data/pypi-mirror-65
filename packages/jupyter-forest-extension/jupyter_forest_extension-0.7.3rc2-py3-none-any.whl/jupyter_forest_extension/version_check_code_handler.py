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

from typing import Optional, Awaitable

from notebook.base.handlers import IPythonHandler
from tornado import web
from pathlib import Path


class VersionCheckCodeHandler(IPythonHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def initialize(self):
        super().initialize()

    @web.authenticated
    async def get(self):
        self.log.info("Code requested")
        script_filename = Path(__file__)
        absolute_script_filename = script_filename.absolute()
        directory = absolute_script_filename.parent
        version_retrieval_filename = directory.joinpath('version_check.py')
        contents = version_retrieval_filename.read_text(encoding='UTF-8')
        self.log.info("Returning {}".format(contents))
        self.write(contents)
