"""
Security credentials management
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
from .ssh_target import SshTarget
from .ci_ssh_private_key import CiSshPrivateKey

__all__ = ['SshTarget', 'CiSshPrivateKey']
