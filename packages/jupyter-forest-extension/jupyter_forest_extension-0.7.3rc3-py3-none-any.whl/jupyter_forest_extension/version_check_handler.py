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

import json
from typing import Optional, Awaitable, Dict

from notebook.base.handlers import IPythonHandler
from tornado import web, escape

from jupyter_forest_extension.version_check_service import VersionCheckService


class VersionCheckHandler(IPythonHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def initialize(self):
        super().initialize()

    @web.authenticated
    async def post(self):

        if self.request.body:
            self.log.debug("post: body received")
            data = escape.json_decode(self.request.body)
            self.log.debug("post: body %s", data)

            docker_info = None  # type: Optional[Dict]
            version_checker = VersionCheckService(logger=self.log)

            try:
                docker_info = version_checker.get_docker_information()
            except BaseException:
                self.log.error("Couldn't retrieve docker information")

            state = await version_checker.get_state(data, docker_info)

        else:
            raise ValueError("Missing body")

        self.log.debug("post: state %s", state)
        json_state = json.dumps(state)
        self.log.debug("post: json_state %s", json_state)
        self.write(json_state)
