"""
Pykrete credentials tests
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import os
import unittest
import logging
from uuid import uuid4
from pykrete.args import CiIo
from pykrete.credentials import CiSshPrivateKey, SshTarget
from .ci import PykreteCiEchoTestCase


class PykreteCredentialsUnitTests(PykreteCiEchoTestCase, SshTarget):
    """Test pykrete's credentials module"""

    _logger = logging.getLogger(__name__)
    _dummy_key = str(uuid4())
    _dummy_file = str(uuid4())
    _set_file = None

    def test_enable_disable_ci_ssh_private_key(self):
        """Verifies successful enabling and disabling of CI SSH private key credentials
        """
        ci_io = CiIo(self._echo, {'deploy key': self._dummy_key, 'ssh port': '1234'})
        with CiSshPrivateKey(ci_io, self._dummy_file) as target:
            self.accept(target)
            self.assertEqual(self._dummy_file + '1234', self._set_file,
                             'wrong file and port set on visit')
            self._assert_key_file()
        self.assertFalse(os.path.exists(self._dummy_file), 'key file still exists after exit')

    def _assert_key_file(self):
        with open(self._dummy_file, 'r') as file:
            key_in_file = file.read()
        self.assertEqual(self._dummy_key, key_in_file, 'wrong key written to file')

    def set_ssh(self, private_key_file_path, ssh_port):
        self._set_file = private_key_file_path + ssh_port


if __name__ == '__main__':
    unittest.main()
