"""
GIT tag-based version bumper
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import logging
from .revision_type import RevisionType


class TagVersionBumper:
    """Handles version bump
    In the case of a release, a commit message containing '#major' will increment the major version,
     otherwise a commit message containing '#minor' will increment the minor version.
    Build is calculated as the current CI project-build# variable, minus a base build,
     or 0 if it is a release.
    """

    __major_part = 0
    __minor_part = 1
    __version_part_base = 0
    __version_bump_size = 1

    def __init__(self, repo, revision, base_build):
        """Initializes this instance from CI environment

        :param repo: project's repository (optional, defaults to git for the current folder)
        :param revision: Build revision
        :param base_build: base build for non-release versions
        """
        self._logger = logging.getLogger(__name__)
        self.__revision = revision
        self.__repo = repo
        self.__base_build = base_build
        self.__version_parts = []

    def advance_version(self, version_parts):
        """Advances the specified version

        :param version_parts: version to advance
        :return: advanced version
        """
        self.__version_parts = list(version_parts)
        if self.__revision.revision_type != RevisionType.Release:
            return self.__advance_build_relative_to_base_build()
        return self.__advance_major_minor_from_last_change_details()

    def __advance_build_relative_to_base_build(self):
        self.__version_parts[2] += self.__revision.build - self.__base_build
        self._logger.debug('Advanced version relative to base build: %s', self.__version_parts)
        return self.__version_parts

    def __advance_major_minor_from_last_change_details(self):
        change_details = self.__repo.get_head_change().details
        for key, value in {'#major': self.__major_part, '#minor': self.__minor_part}.items():
            if key in change_details:
                return self.__bump_version(value)
        return self.__advance_build_relative_to_base_build()

    def __bump_version(self, bump_part):
        self.__version_parts[bump_part] += self.__version_bump_size
        for i in range(bump_part + 1, len(self.__version_parts)):
            self.__version_parts[i] = self.__version_part_base
        self._logger.debug('Advanced version by bumping location %s: %s',
                           bump_part + 1, self.__version_parts)
        return self.__version_parts
