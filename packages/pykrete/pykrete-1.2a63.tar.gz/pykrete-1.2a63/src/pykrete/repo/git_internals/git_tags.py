"""
GIT repository tag reading management
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import re
import logging


class GitTagsReader:
    """Manage reading git tags"""

    @property
    def tags(self):
        """
        :return: all tags in the repo
        """
        tag_refs = self._get_tag_refs_by_date_ascending()
        return self.__name_message_tuples_from_tag_refs(tag_refs)

    def __init__(self, repo):
        """Initialize this instance

        :param repo: target repository
         subset (optional, defaults to getting all tags)
        """
        self._logger = logging.getLogger(__name__)
        self._repo = repo
        self._repo.remotes['origin'].fetch('--tags')

    def get_last_tag_ref_named(self, name, is_must=True):
        """Gets the last tag reference with the specified name

        :param name: tag name
        :param is_must: True to raise an error tag doesn't exist,
         False to just return None in that case.
        :return: tag reference
        :exception: KeyError - tag not found
        """
        tag_ref = self.__get_last_tag_ref_named(name, is_must)
        tag_tuple = self.name_message_tuple_from_tag_ref(tag_ref)
        self._logger.debug('Read tag from repo [%s]: %s', self._repo, tag_tuple)
        return tag_ref

    def get_tags_from(self, pattern, is_must):
        """Gets all tags from the current branch in the repo, from the tag whose name matches the
         supplied pattern.

        :param pattern: name pattern to match
        :param is_must: True to raise an error if no match is found, False to return all tags in
        that case (with the first tuple as None).
        :return: A list of tag info tuples (name, message)
        :exception: KeyError - tag not found
        """
        tag_refs = self.__get_tag_refs_from(pattern, is_must)
        return self.__name_message_tuples_from_tag_refs(tag_refs)

    @staticmethod
    def name_message_tuple_from_tag_ref(tag):
        """Convert a tag reference to a (name, message) tuple

        :param tag: tag reference
        :return: (name, message) tuple
        """
        return (tag.name, tag.tag.message if tag.tag else None) if tag else None

    def _get_tag_refs_by_date_ascending(self):
        tag_refs = list(self._repo.tags)
        tag_refs.sort(key=lambda x: x.tag.tagged_date if x and x.tag else 0)
        return tag_refs

    def __get_last_tag_ref_named(self, name, is_must):
        tag_refs = self._get_tag_refs_by_date_ascending()
        index = GitTagsReader.__find_last_tag_index(name.__eq__, tag_refs)
        return tag_refs[index] if \
            self.__is_found(index, is_must, f'No tag named {name} was found in repo') else \
            None

    def __get_tag_refs_from(self, pattern, is_must):
        tag_refs = self._get_tag_refs_by_date_ascending()
        from_index = GitTagsReader.__find_last_tag_index_by_name_pattern(pattern, tag_refs)
        return tag_refs[from_index:] if \
            self.__is_found(from_index, is_must, "No tag found to match pattern " + pattern) else \
            [None] + tag_refs

    def __name_message_tuples_from_tag_refs(self, tags):
        tag_tuples = [GitTagsReader.name_message_tuple_from_tag_ref(tag) for tag in tags]
        self._logger.debug('Read tags from repo [%s]: %s', self._repo, tag_tuples)
        return tag_tuples

    @staticmethod
    def __is_found(index, is_must, error):
        if index == -1:
            if is_must:
                raise KeyError(error)
            return False
        return True

    @staticmethod
    def __find_last_tag_index_by_name_pattern(pattern, tag_refs):
        compiled_pattern = re.compile(pattern)
        return GitTagsReader.__find_last_tag_index(compiled_pattern.match, tag_refs)

    @staticmethod
    def __find_last_tag_index(matcher, tag_refs):
        for i in range(len(tag_refs) - 1, -1, -1):
            if matcher(tag_refs[i].name):
                return i
        return -1
