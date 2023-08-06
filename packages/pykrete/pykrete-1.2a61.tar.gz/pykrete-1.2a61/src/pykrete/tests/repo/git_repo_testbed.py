"""
Pykrete repo testbed
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import logging


class GitUrlsTestbed:
    """simulated"""

    _logger = logging.getLogger(__name__)

    @property
    def configured_ssh_urls(self):
        """simulated"""
        return []

    def __init__(self):
        """simulated"""
        self.replaced_urls = []
        self.ssh_replaced = False

    def configure_ssh_url_and_save_original(self, ssh_port):
        """simulated"""
        self._logger.debug('configure_ssh_url_and_save_original called with port=%s', ssh_port)
        self.ssh_replaced = True
        return 'http', 'ssh'

    def replace_url(self, new, old):
        """simulated"""
        self._logger.debug('replace_url called, new=%s, old=%s', new, old)
        self.replaced_urls.append((new, old))


class WithTestbed:
    """simulated"""

    def __init__(self):
        """simulated"""
        self.entered = False
        self.exited = False
        self.args = None

    def __enter__(self):
        """simulated"""
        self.entered = True

    def __exit__(self, *args):
        """simulated"""
        self.exited = True
        self.args = args


class GitRepoRemoteTestbed:
    """simulated"""

    def __init__(self, urls):
        """simulated"""
        self.urls = urls
        self.urls_set = []

    def set_url(self, new, old):
        """simulated"""
        self.urls_set.append((new, old))
        self.urls[self.urls.index(old)] = new
