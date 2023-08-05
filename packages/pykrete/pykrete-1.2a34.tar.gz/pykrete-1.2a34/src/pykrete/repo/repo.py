"""
Repository management interface
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
from abc import ABCMeta, abstractmethod


class Repo(metaclass=ABCMeta):
    """Repository interface"""

    @abstractmethod
    def get_all_tags(self):
        """Gets all tags from the current branch in the repo

        :return: A list of tag info tuples (name, message)
        """

    @abstractmethod
    def get_tags_from(self, pattern, is_must=False):
        """Gets all tags from the current branch in the repo, from the tag whose name matches the
         supplied pattern.

        :param pattern: name pattern to match
        :param is_must: True to raise an error if no match is found, False to return all tags in
        that case (with the first tuple as None).
        :return: A list of tag info tuples (name, message)
        """

    @abstractmethod
    def add_tag(self, name, message):
        """Adds a tag to the repo

        :param name: tag name
        :param message: tag message
        :return: the new tag's info tuple (name, message)
        """

    @abstractmethod
    def remove_tag(self, name, is_must):
        """Removes a tag from the repo

        :param name: tag name
        :param is_must: True to raise an error tag doesn't exist, False to just skip in that case.
        :exception: KeyError - tag not found
        """

    @abstractmethod
    def get_head_change(self, branch=None):
        """Gets the last change in the branch

        :param branch: branch name (optional, defaults to the current branch)
        :return: (pykrete.repo.Change) last change in the branch
        """
