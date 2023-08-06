"""
GIT repository URL management
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import re
import logging


class GitUrls:
    """Handles the URLs attached to a remote"""

    __ssh_prefix = 'ssh://git@'

    @property
    def configured_ssh_urls(self):
        """
        :return SSH urls configured for this remote
        """
        return [url for url in
                self._remote.urls if url.startswith(self.__ssh_prefix)]

    def __init__(self, remote):
        """Initialize this instance

        :param remote: git remote
        """
        self._logger = logging.getLogger(__name__)
        self._remote = remote

    def configure_ssh_url_and_save_original(self, ssh_port):
        """Configures an SSH url instead of existing HTTP url

        :param ssh_port: SSH port
        :return: (original, new) URLs
        """
        http_url, server, project = self._get_http_url_server_and_project_for_remote()
        ssh_url = self._make_ssh_url(server, project, ssh_port)
        self.replace_url(ssh_url, http_url)
        return http_url, ssh_url

    def replace_url(self, new, old):
        """Replace remote URL

        :param new: new URL to use
        :param old: old URL to replace
        """
        self._logger.debug('replacing URLS, new=%s, old=%s', new, old)
        self._remote.set_url(new, old)

    def _get_http_url_server_and_project_for_remote(self):
        pattern = re.compile(r'http.?://.*?([^:@/]+)/(.*)')
        matches = [(url, ) + tuple(match.groups()) for url, match in
                   [(url, pattern.match(url)) for url in self._remote.urls]
                   if match]
        if not matches:
            raise IOError(f'No HTTP* URLs found in {self._remote}')
        return matches[0]

    def _make_ssh_url(self, server, project, port):
        port_spec = '' if str(port) == '22' else f':{port}'
        return f'{self.__ssh_prefix}{server}{port_spec}/{project}'
