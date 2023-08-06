"""
GITLAB Upstream artifact downloader
Author: Shai Bennathan - shai.bennathan@gmail.com
(C) 2020
"""
import logging
from zipfile import ZipFile
from .gitlab_str import project_str, job_str, project_pipeline_str


class GitlabUpstreamArtifacts:
    """Manage upstream artifacts"""

    def __init__(self, server, upstream_env):
        """Initialize this instance for a specific job's artifacts

        :param server: GitLab server
        :param upstream_env: upstream environment
        """
        self._logger = logging.getLogger(__name__)
        self._server = server
        self._upstream_env = upstream_env

    def download(self, target_path=None):
        """Download artifacts from last successful build job in the upstream pipeline

        :param target_path: Target path for downloads
        """
        job = self._get_upstream_build_artifacts()
        self._extract_job_artifacts(job, target_path)

    def _get_upstream_build_artifacts(self):
        project = self._get_upstream_project()
        pipeline = self._get_pipeline_by_id(project, self._upstream_env.pipeline_id)
        jobs = self._get_jobs_via_pipeline(
            pipeline, project,
            lambda x: x.attributes['name'].startswith(self._upstream_env.build_job_prefix))
        return jobs[-1]

    def _get_upstream_project(self):
        self._logger.debug('Locating project ID %s on GitLab', self._upstream_env.project_id)
        project = self._server.projects.get(self._upstream_env.project_id)
        self._logger.debug('Got GitLab project %s', project_str(project))
        return project

    def _get_pipeline_by_id(self, project, pipeline_id):
        self._logger.debug('Getting pipeline ID %s from GitLab project %s',
                           pipeline_id, project_str(project))
        pipeline = project.pipelines.get(pipeline_id)
        self._logger.debug('Got GitLab %s', project_pipeline_str(project, pipeline))
        return pipeline

    def _get_jobs_via_pipeline(self, pipeline, project, job_filter):
        pipeline_msg = project_pipeline_str(project, pipeline)
        self._logger.debug('Getting jobs from %s', pipeline_msg)
        jobs = [project.jobs.get(pipeline_job.id)
                for pipeline_job in pipeline.jobs.list() if job_filter(pipeline_job)]
        if not jobs:
            raise IOError('No matching jobs found in ' + pipeline_msg)
        self._logger.debug('Got GitLab jobs: [%s] from %s',
                           ",".join([job_str(job) for job in jobs]), pipeline_msg)
        return jobs

    def _extract_job_artifacts(self, job, target_path):
        zip_path = self._download_artifacts_zip(job)
        self._unzip(zip_path, target_path)

    def _download_artifacts_zip(self, job):
        zip_path = 'artifacts.zip'
        self._logger.debug('Downloading artifacts from job into %s', zip_path)
        with open(zip_path, 'wb') as file:
            job.artifacts(streamed=True, action=file.write)
        return zip_path

    def _unzip(self, zip_path, target_path):
        unzip_path = target_path if target_path else 'artifacts'
        self._logger.debug('Unzipping artifacts into %s', unzip_path)
        with ZipFile(zip_path, 'r') as zip_file:
            zip_file.extractall(unzip_path)
