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

from jupyter_forest_extension.jupyter_version_service import JupyterVersionService
from notebook.base.handlers import IPythonHandler
from tornado import web
import json


class JupyterVersionCheckHandler(IPythonHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def initialize(self):
        super().initialize()

    @web.authenticated
    async def get(self):
        self.log.info("JupyterVersionCheckHandler - Check requested")
        try:
            version_checker = JupyterVersionService(logger=self.log)

            version_state = version_checker.get_state()
            up_to_date = all(version_state.values())

            if up_to_date:
                state = {"versionStatus": "OK",
                         "longVersionStatus": "The JupyterLab Forest extension is up to date.",
                         "state": "OK"}
            else:
                state = {"versionStatus": "Out of date",
                         "longVersionStatus": "The JupyterLab Forest extension is out to date.",
                         "state": "OK"}
        except BaseException:
            self.log.exception("Couldn't determine state")
            state = {"versionStatus": "Unknown",
                     "longVersionStatus": "The JupyterLab Forest extension status couldn't be determined.",
                     "state": "Unknown"}

        self.log.debug("get: state %s", state)
        json_state = json.dumps(state)
        self.log.debug("get: json_state %s", json_state)
        self.write(json_state)
