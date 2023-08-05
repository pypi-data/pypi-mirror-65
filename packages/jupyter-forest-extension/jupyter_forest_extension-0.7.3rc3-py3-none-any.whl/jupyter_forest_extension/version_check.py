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

import pkg_resources
import json
import sys
import platform


def retrieve_versions():
    """
    This function is expected to be called against a remote python kernel to
    retrieve versions of installed software and running services.
    """
    python_executable = sys.executable
    python_version = platform.python_version()

    packages = [{"key": p.key, "version": p.version, "location": p.location}
                for p in sorted(list(pkg_resources.working_set), key=lambda x: x.key + x.version)
                if p.key == "pyquil"]

    qvm_info = None
    quilc_info = None

    try:
        from pyquil import get_qc
        from pyquil.api._qvm import QVM
        qc = get_qc('2q-qvm')

        if isinstance(qc.qam, QVM):
            qvm_info = qc.qam.get_version_info()
        else:
            qvm_info = None

        quilc_info = qc.compiler.get_version_info()
    except BaseException:
        # Do nothing for exceptions getting quil or quilc information
        pass

    results = {"pythonExecutable": python_executable,
               "pythonVersion": python_version,
               "packages": packages,
               "qvmInfo": qvm_info,
               "quilcInfo": quilc_info}

    return results


results = retrieve_versions()
print(json.dumps(results, sort_keys=True, indent=4, separators=(",", ": ")))
