"""
GITLAB object stringify
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import logging


def project_str(project):
    """Stringify project
    :param project: GitLab project
    :return: Project name with namespace
    """
    return project.attributes['name_with_namespace']


def pipeline_str(pipeline):
    """Stringify pipeline
    :param pipeline: GitLab pipeline
    :return: pipeline reference with status
    """
    p_attr = pipeline.attributes
    return f'{p_attr["ref"]}[{p_attr["sha"][0:8]}/{p_attr["id"]} - {p_attr["status"]}]'


def project_pipeline_str(project, pipeline):
    """Stringify project pipeline
    :param project: GitLab project
    :param pipeline: GitLab pipeline
    :return: pipeline with project
    """
    return f'pipeline {pipeline_str(pipeline)} in GitLab project {project_str(project)}'


def job_str(job):
    """Stringify job
    :param job: GitLab job
    :return: job reference with commit info
    """
    j_attr = job.attributes
    logger = logging.getLogger(__name__)
    logger.info('job type: %s', type(job))
    for key, value in j_attr.items():
        logger.info('Attribute: key %s; type: %s, value: %s', key, type(value), value)
    logger.info('job dir: %s', dir(job))
    j_commit = j_attr['commit']
    j_commit_str = f'{j_commit["title"]} by {j_commit["committer_name"]}' if j_commit else ""
    return f'{j_attr["ref"]}/{j_attr["name"]}/{j_attr["id"]}[{j_commit_str}]'
