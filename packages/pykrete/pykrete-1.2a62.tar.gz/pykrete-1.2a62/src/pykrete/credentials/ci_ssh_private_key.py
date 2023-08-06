"""
Handle SSH private key
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import logging
from os import remove, getcwd, path
from uuid import uuid4
from pykrete.args import CiIo
from pykrete.patterns.visitor import Visitor
from .state import State


class CiSshPrivateKey(Visitor):
    """Handle SSH private key specifid in the CI environment"""

    @property
    def is_enabled(self):
        """
        :return: True if the key is enabled, False otherwise
        """
        return self._state == State.Enabled

    @property
    def ssh_port(self):
        """
        :return: the CI-configured SSH port
        """
        if not self._ssh_port:
            self._ssh_port = self.__ci_io.read_env('ssh port', '22')
        return self._ssh_port

    def __init__(self, ci_io=None, key_file=None):
        """Initialize this instance

        :param ci_io: CI environment reader override
        """
        self._logger = logging.getLogger(__name__)
        self.__ci_io = ci_io if ci_io else CiIo()
        self._state = State.NotInitialized
        self._key_file = key_file
        self._ssh_port = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.disable()

    def visit(self, target):
        """Visit this instance

        :param target: visited target
        """
        self._enable()
        target.set_ssh(self._key_file, self.ssh_port)

    def disable(self):
        """Disables the private key

        :exception: PermissionError - key already disabled
        """
        if self._must_not_be_disabled_but_is(State.NotInitialized):
            return
        self._logger.debug('Disabling SSH from key-file=%s', self._key_file)
        remove(self._key_file)
        self._state = State.Disabled

    def _enable(self):
        if self._must_not_be_disabled_but_is(State.Enabled):
            return
        self._make_key_file()
        self._state = State.Enabled

    def _make_key_file(self):
        if not self._key_file:
            self._key_file = path.join(getcwd(), str(uuid4()))
        key = self.__ci_io.read_env('deploy key')
        self._logger.debug('Enabling SSH with key-file=%s', self._key_file)
        with open(self._key_file, 'w') as key_file:
            key_file.write(key)

    def _must_not_be_disabled_but_is(self, other_state):
        if self._state == State.Disabled:
            self._logger.error('Trying to operate disabled SSH key-file')
            raise PermissionError('Credentials were disabled')
        return self._state == other_state
