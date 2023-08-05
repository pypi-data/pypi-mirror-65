import subprocess
from typing import Sequence, Union
from logging import Logger, DEBUG


class ProcessExecutor:
    def __init__(self, logger: Logger, default_log_level: int = DEBUG, default_log_command: bool = False) -> None:
        self._logger = logger
        self._default_log_level = default_log_level
        self._default_log_command = default_log_command

    def check_output(self, args: Union[str, Sequence[str]], log_level: int = None, log_command: bool = None) -> str:
        if log_level is None:
            log_level = self._default_log_level

        if log_command is None:
            log_command = self._default_log_command

        if log_command:
            command = " ".join(args)
            self._logger.log(msg="Running command: {}".format(command), level=log_level)

        result = subprocess.check_output(args).decode('UTF-8')
        self._logger.log(msg="Result:\n {}".format(result), level=log_level)
        return result
