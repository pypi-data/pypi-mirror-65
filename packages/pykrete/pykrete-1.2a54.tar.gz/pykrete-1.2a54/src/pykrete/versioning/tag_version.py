"""
GIT tag-based version information manager
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import logging
import re
from pykrete.args import CiIo
from pykrete.repo import Git
from .revision_type import RevisionType
from .version import Version
from .ci_revision_and_build import CiRevisionAndBuild
from .tag_version_bumper import TagVersionBumper


class TagVersion(Version):
    """Handle version in CI environment
    A version is constructed from the last version tag (tag name format '<major>.<minor>.<build>'
     indicating a release version, with a message format of 'ci_base_build <build>' indicating the
     CI build number for the first release with this major-minor combo). In the case of a release,
     a commit message containing '#major' will increment the major version, otherwise a commit
     message containing '#minor' will increment the minor version.
    Build is calculated as the current CI project-build# variable, minus the build specified in the
     last version tag's message if this isn't a release, or 0 if it is a release.
    Revision is read from the CI environment variables CI_COMMIT_REF_NAME, CI_MERGE_REQUEST_TITLE
     and CI_JOB_NAME:
        Release (4) - master branch on a job who'se name doesn't contain '_rc_'
        RC (3) - non-WIP merge request, master branch on a job who'se name contains '_rc_'
        Beta (2) - merge request with 'WIP' in the title
        Alpha (1) - none of the above
    """

    _empty_version = [0, 0, 0], 0

    def __init__(self, repo=Git(), ci_io=None):
        """Initializes this instance from CI environment

        :param repo: project's repository (optional, defaults to git for the current folder)
        :param ci_io: CI environment's IO manager (optional, defaults to pykrete.args.CiIo)
        """
        self._logger = logging.getLogger(__name__)
        self.__revision = CiRevisionAndBuild(ci_io if ci_io else CiIo())
        self.__repo = repo
        self.__tags = self.__read_tags()
        # pylint: disable=unbalanced-tuple-unpacking
        (major, minor, build) = self.__read_version_from_tags()
        super().__init__(major=major,
                         minor=minor,
                         revision=self.__revision.revision_type.value,
                         build=build,
                         revision_type=self.__revision.revision_type)

    def apply(self):
        """Apply this version to the relevant environment
        """
        if self.__revision.revision_type != RevisionType.Release:
            raise ValueError('Cannot apply non-release version')
        self.__repo.add_tag(f'{self.major}.{self.minor}.{self.build}',
                            f'ci_base_build {self.__revision.build}')

    def __read_tags(self):
        return self.__repo.get_tags_from(pattern=r'(\d+\.){2}\d+', is_must=False)

    def __read_version_from_tags(self):
        last_version_tag = self.__tags[0] if self.__tags else None
        version_parts, base_build =\
            self.__get_version_parts_and_base_build_from(last_version_tag)
        version_parts = self.__advance_version(version_parts, base_build)
        return tuple(version_parts)

    def __get_version_parts_and_base_build_from(self, tag):
        return self.__make_version_parts_and_base_build_from(tag) if tag else self._empty_version

    def __make_version_parts_and_base_build_from(self, tag):
        version_parts = [int(part) for part in tag[0].split('.')]
        message_build = re.findall(r'ci_base_build (\d+)', tag[1]) if tag[1] else None
        base_build = int(message_build[0]) if message_build else 0
        self._logger.debug('Read version parts: %s [base build %s]', version_parts, base_build)
        return version_parts, base_build

    def __advance_version(self, version_parts, base_build):
        return TagVersionBumper(self.__repo, self.__revision, base_build)\
            .advance_version(version_parts)
