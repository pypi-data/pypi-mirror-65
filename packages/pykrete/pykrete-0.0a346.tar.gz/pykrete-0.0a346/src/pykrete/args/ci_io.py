"""
CI information manager
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import logging
from .environ import environ


class CiIo:
    """Handle CI environment IO
    """
    def __init__(self, ci_reader=environ, ci_spec=None):
        """Initializes this instance from CI environment

        :param ci_reader: (ci_variable, role)=>value function [see pykrete.args.environ behavior]
        :param ci_spec: dictionary of part to CI variable
         (parts are: 'major version', 'minor version', 'build version', 'branch name',
          'merge request title', 'job name', 'deploy key')
        """
        self._logger = logging.getLogger(__name__)
        self.__ci_reader = ci_reader
        self.__ci_spec = ci_spec if ci_spec else self.__get_default_ci_spec()

    def read_env(self, part, default=None):
        """Read a spec-part from the CI environment

        :param part: part name
        :param default: default value if not found,
         or None if there should be an exception if not found
        :return: Read value, or None if not found
        :exception: The part's variable is not defined in the environment and it should be
        """
        role = None if default is not None else f'CI\'s \'{part}\' value'
        var_name = self.__ci_spec[part]
        self._logger.debug('Reading CI environment %s [role: %s] from %s', part, role, var_name)
        value = self.__ci_reader(var_name, role)
        if default and not value:
            value_source = 'Used default'
            value = default
        else:
            value_source = 'Read'
        self._logger.debug('%s %s = %s', value_source, part, '[MASKED]' if 'key' in part else value)
        return value

    @staticmethod
    def __get_default_ci_spec():
        return {'major version': 'CI_VERSION_MAJOR',
                'minor version': 'CI_VERSION_MINOR',
                'build version': 'CI_PIPELINE_IID',
                'branch name': 'CI_COMMIT_REF_NAME',
                'merge request title': 'CI_MERGE_REQUEST_TITLE',
                'job name': 'CI_JOB_NAME',
                'deploy key': 'CI_DEPLOY_KEY',
                'ssh port': 'SSH_PORT',
                'upstream project ID': 'UPSTREAM_PROJECT_ID',
                'upstream pipeline ID': 'UPSTREAM_PIPELINE_ID',
                'upstream build job prefix': 'UPSTREAM_BUILD_JOB_PREFIX',
                'upstream key': 'UPSTREAM_TOKEN',
                'api url': 'CI_API_V4_URL'}
