"""
GITLAB Upstream CI environment
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
from pykrete.args import CiIo


class GitLabUpstreamEnv:
    """GitLab upstream environment"""

    @property
    def project_id(self):
        """
        :return: Upstream project ID
        """
        return self._project_id

    @property
    def pipeline_id(self):
        """
        :return: Upstream pipeline ID
        """
        return self._pipeline_id

    @property
    def build_job_prefix(self):
        """
        :return: Upstream build job prefix
        """
        return self._build_job_prefix

    @property
    def key(self):
        """
        :return: Upstream token key
        """
        return self._key

    def __init__(self, ci_io=None):
        """Initialize this instance

        :param ci_io: CI environment's IO manager (optional, defaults to pykrete.args.CiIo)
        """
        self.__ci_io = ci_io if ci_io else CiIo()
        (self._project_id, self._pipeline_id, self._build_job_prefix, self._key) =\
            self.__get_upstream_parts()

    def __get_upstream_parts(self):
        return tuple(
            [self.__get_upstream(part) for part in
             ['project ID', 'pipeline ID', 'build job prefix', 'key']])

    def __get_upstream(self, part):
        return self.__ci_io.read_env(f'upstream {part}')
