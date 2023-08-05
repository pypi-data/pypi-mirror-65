"""
Pykrete repo testbed
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""

from pykrete.repo import Repo


class RepoTestbed(Repo):
    """Testbed class for tests which need a simulated repo"""

    def __init__(self, tags, change):
        """Initialize the testbed

        :param tags: simulated tags
        :param change: simulated change
        """
        self.tags = tags
        self.change = change
        self.added = []

    def get_all_tags(self):
        """simulation"""
        return self.tags

    def get_tags_from(self, pattern, is_must=False):
        """simulation"""
        if is_must:
            raise AssertionError('tags are fetched with is_must=True')
        if not pattern:
            raise AssertionError('no pattern was provider for fetching tags')
        return self.tags

    def get_head_change(self, branch=None):
        """simulation"""
        return self.change

    def add_tag(self, name, message):
        """simulation"""
        self.added.append((name, message))
        return name, message

    def remove_tag(self, name, is_must=True):
        """simulation"""
