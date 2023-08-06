"""
GIT repository SSH management
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import logging


class GitSsh:
    """Handles pushing to a git repo"""

    def __init__(self, environment_setter, urls, private_key_file_path, ssh_port):
        """Set SSH private key to the specified path

        :param environment_setter: sets a git repository's custom environment
        :param urls: branch url management
        :param private_key_file_path: Path to private key file
        :param ssh_port: SSH port (optional, defaults to 22)
        """
        self._logger = logging.getLogger(__name__)
        self._urls = urls
        self._path = private_key_file_path
        self._environment = self._set_environment(environment_setter, private_key_file_path)
        if not self._urls.configured_ssh_urls:
            self._original_urls = self._urls.configure_ssh_url_and_save_original(ssh_port)

    def unset(self, *args):
        """Unset the credentials

        :param args: exit arguments
        """
        self._logger.debug('Disabling GIT SSH')
        self._environment.__exit__(*args)
        if self._original_urls:
            http_url, old_url = self._original_urls
            self._urls.replace_url(http_url, old_url)

    def _set_environment(self, environment_setter, private_key_file_path):
        ssh_cmd = 'ssh -o StrictHostKeyChecking=no -i ' \
                  + private_key_file_path.replace('\\', '\\\\')
        self._logger.debug('Enabling GIT SSH with command [%s]', ssh_cmd)
        environment = environment_setter(GIT_SSH_COMMAND=ssh_cmd)
        environment.__enter__()
        return environment
