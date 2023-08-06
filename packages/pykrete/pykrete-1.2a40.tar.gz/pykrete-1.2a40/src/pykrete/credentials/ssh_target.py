"""
Security credentials target
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
from abc import abstractmethod

from pykrete.patterns.visitor import Target


class SshTarget(Target):
    """Visitor pattern - base class for credential targets
    """

    @abstractmethod
    def set_ssh(self, private_key_file_path, ssh_port):
        """Set the SSH credentials from the supplied file

        :param private_key_file_path: path to private key file
        :param ssh_port: SSH port
        """
