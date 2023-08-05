"""
CI environment-based revision information manager
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
from .revision_type import RevisionType


class CiRevisionAndBuild:
    """Handle revision in CI environment
    Revision is read from CI_COMMIT_REF_NAME, CI_MERGE_REQUEST_TITLE and CI_JOB_NAME:
        Release (4) - master branch on a job who'se name doesn't contain '_rc_'
        RC (3) - non-WIP merge request, master branch on a job who'se name contains '_rc_'
        Beta (2) - merge request with 'WIP' in the title
        Alpha (1) - none of the above
    Build is read from CI_PIPELINE_IID.
    """

    @property
    def revision_type(self):
        """
        :return: Revision type of the version
        """
        return self._revision_type

    @property
    def build(self):
        """
        :return: Build part of the version
        """
        return self._build

    def __init__(self, ci_io):
        """Initializes this instance from CI environment

        :param ci_io: CI IO for 'branch name', 'merge request title'
        """
        self.__ci_io = ci_io
        self._revision_type = self.__get_revision_type()
        self._build = int(self.__ci_io.read_env('build version'))

    def __get_revision_type(self):
        if self.__is_master():
            return self.__revision_from_master()

        revision = self.__revision_from_merge_request()
        return revision if revision else RevisionType.Alpha

    def __is_master(self):
        branch_name = self.__ci_io.read_env('branch name')
        return branch_name == 'master'

    def __revision_from_merge_request(self):
        merge_request_title = self.__ci_io.read_env('merge request title', False)
        if merge_request_title:
            return RevisionType.Beta if 'WIP' in merge_request_title else RevisionType.RC
        return None

    def __revision_from_master(self):
        job_name = self.__ci_io.read_env('job name')
        return RevisionType.RC if '_rc_' in job_name else RevisionType.Release
