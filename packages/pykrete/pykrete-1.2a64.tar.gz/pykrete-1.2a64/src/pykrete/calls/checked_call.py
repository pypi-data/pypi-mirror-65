"""
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import logging
from subprocess import Popen, PIPE

from ._parse_command_into_call_vector import parse_command_into_call_vector


class CheckedCall:
    """Used to execute shell commands and hold the execution results"""

    @property
    def stdout(self):
        """
        :return: (string) command's standard output
        """
        return self._stdout

    @property
    def stderr(self):
        """
        :return: (string) command's standard error
        """
        return self._stderr

    @property
    def success(self):
        """
        :return: (bool) True if exit-code was 0, False otherwise
        """
        return self._success

    def __init__(self, cmd):
        """Initializes this instance with the specified command

        :param cmd: (string/list) shell command
        """
        logger = logging.getLogger(__name__)
        logger.debug('Running command: %s', cmd)
        command_vector = self.__get_vector_from_command(cmd)
        self._process = Popen(command_vector, shell=True, stdout=PIPE, stderr=PIPE)
        (self._stdout, self._stderr) = self._run_and_get_streams()
        self._success = self._process.returncode == 0
        logger.debug('Command result:\n--- >> start output << ---\n%s\n--- >> end output << ---',
                     self.get_output())

    def get_output(self):
        """Gets the command's output

        :return: stdout + stderr
        """
        return f'{self._stdout}\n{self._stderr}'

    def __str__(self):
        return f'{self._process.args}\n{self.get_output()}'

    def _run_and_get_streams(self):
        """
        :return (string, string): (stdout, stderr) strings
        """
        return tuple([stream.decode('ascii') for stream in self._process.communicate()])

    @staticmethod
    def __get_vector_from_command(cmd):
        return cmd if isinstance(cmd, list) else parse_command_into_call_vector(str(cmd))
