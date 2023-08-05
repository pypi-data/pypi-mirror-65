#  Copyright (c) 2019 Samsung, Inc. and its affiliates.
#
#  This source code is licensed under the RESTRICTED license found in the
#  LICENSE file in the root directory of this source tree.

import textwrap
import pytest
import time
import uuid
import disco
from time import sleep
from disco.core.constants import JobStatus, TaskStatus
from tests.base_test import BaseTest
from tests.live import env
from .env import LIVE_TESTS_TIMEOUT_SECONDS, LIVE_TESTS_JOB_START_WAIT_TIME, LIVE_TESTS_TASKS_RUNNING_WAIT_TIME
from .utils import get_non_running_tasks
from disco.core.exceptions import GraphQLRequestException


@pytest.mark.skipif(env.skip, reason=env.reason)
# TODO: Test with a non-default cluster
# TODO: Archive jobs on tear-down even if an exception was thrown
class TestJobsLive(BaseTest):

    def setup_class(self):
        BaseTest.disable_progress_bar()

    def test_start_job(self):
        self._start_job(None)

    def test_start_job_with_cost_instance(self):
        self._start_invalid_cost_type_job()
        self._start_job('guaranteed')

    def test_create_job_from_git_repository(self):
        input_file_id = disco.upload_file('input.txt', '13')
        constants_file_id = disco.upload_file('constants.txt', 'ZZZ')
        users_repositories = disco.Repository.list_repositories()
        if len(users_repositories) > 0:
            script_repo_id = users_repositories[0].id
            script_file_path = 'aaa'
            job_name = 'Automation Start Job %s' % uuid.uuid4()
            job = disco.Job.create(input_file_ids=[input_file_id],
                                   constants_file_ids=[constants_file_id],
                                   job_name=job_name,
                                   script_repo_id=script_repo_id,
                                   script_file_path_in_repo=script_file_path)

            job_details = job.get_details()
            job_id = job_details.id
            assert job_id
            assert job_details.name == job_name

            job.archive()

    def test_cancel_job(self):
        script_content = textwrap.dedent('''
        import time
        
        for i in range(120):
            print(i)
            time.sleep(1)
        ''')

        number_of_inputs = 30

        expected_outputs = [self.random_str(prefix=f"output{i}-") for i in range(number_of_inputs)]

        print(f'Uploading {number_of_inputs} input files...')

        input_file_ids = [disco.upload_file(f'input_{i}.txt', expected_outputs[i]) for i in range(number_of_inputs)]
        script_file_id = disco.upload_file('sleep.py', script_content)
        job_name = 'Automation Cancel Job %s' % uuid.uuid4()
        job = disco.Job.create(script_file_id=script_file_id,
                               input_file_ids=input_file_ids,
                               job_name=job_name)

        print(f'Starting job {job.job_id}...')

        job.start()

        print(f'Job {job.job_id} started, stopping job...')
        job.stop()

        assert job.get_status() in [JobStatus.stopping, JobStatus.stopped]

        print(f'Waiting for job {job.job_id} to stop...')
        job_status = job.wait_for_status(JobStatus.stopped, interval=10,
                                         timeout=LIVE_TESTS_TIMEOUT_SECONDS)
        assert job_status == JobStatus.stopped

        print(f'job {job.job_id} was stopped!')

        tasks = job.get_tasks()
        assert len(tasks) == number_of_inputs

        task_statuses = [task.status for task in tasks]
        expected_task_statuses = [TaskStatus.stopped.value for _ in tasks]

        assert task_statuses == expected_task_statuses

        job.archive()

    def test_auto_start_job(self):
        script_content = 'print(\'Hello from automation!\')'
        script_file_id = disco.upload_file('hello.py', script_content)

        job_name = 'Automation Auto Start Job %s' % uuid.uuid4()
        job = disco.Job.create(script_file_id=script_file_id,
                               job_name=job_name, auto_start=True)

        print(f'job {job.job_id} finished!')

        job.wait_for_finish(interval=10, timeout=LIVE_TESTS_TIMEOUT_SECONDS)
        assert job.get_status() == JobStatus.done

        job.archive()

    def test_list_jobs(self):
        jobs = disco.Job.list_jobs(1)
        assert isinstance(jobs, list)
        if jobs:
            assert len(jobs) == 1
            job_details = jobs[0]
            assert job_details.id is not None
            assert job_details.name is not None
            assert job_details.status is not None

    def test_exception_on_job(self):
        erroneous_script = '1 / 0'
        script_file_id = disco.upload_file('woof.py', erroneous_script)

        job_name = 'Automation Failing Job %s' % uuid.uuid4()
        job = disco.Job.create(script_file_id, job_name=job_name, auto_start=True)

        print(f'Waiting for job {job.job_id} to finish...')

        job.wait_for_finish(interval=10, timeout=LIVE_TESTS_TIMEOUT_SECONDS)
        assert job.get_status() == JobStatus.failed

        print(f'job {job.job_id} finished!')

        job_tasks = job.get_tasks()
        assert job_tasks[0].status == TaskStatus.failed.value

        job.archive()

    def _start_job(self, instance_cost):
        job_name = 'Automation Start Job %s' % uuid.uuid4()
        job = self._create_job_params(job_name, instance_cost, '000000000000000000000000')

        job.start()
        job_details = job.get_details()
        job_id = job_details.id

        assert job_id
        assert job_details.name == job_name

        print(f'Waiting for job {job.job_id} to finish...')

        job.wait_for_finish(interval=10, timeout=LIVE_TESTS_TIMEOUT_SECONDS)
        assert job.get_status() == JobStatus.done

        print(f'job {job.job_id} finished!')

        job_tasks = job.get_tasks()
        assert job_tasks[0].status == TaskStatus.success.value

        jobs_list = disco.Job.list_jobs()
        assert job_id in [job_details.id for job_details in jobs_list]

        job.archive()

    def _start_invalid_cost_type_job(self):
        job_name = 'Automation Start Job %s' % uuid.uuid4()

        try:
            self._create_job_params(job_name, 'lowCost', '000000000000000000000011')
        except GraphQLRequestException as ex:
            assert ex.errors[0]['message'] == 'Operation not supported: lowCost instance cost type on gcp cluster'

    def _create_job_params(self, job_name, instance_cost, cluster_id=None):
        script_content = 'print(\'Hello from automation!\')'
        script_file_id = disco.upload_file('hello.py', script_content)
        input_file_id = disco.upload_file('input.txt', '13')
        constants_file_id = disco.upload_file('constants.txt', 'ZZZ')

        return disco.Job.create(script_file_id=script_file_id,
                                input_file_ids=[input_file_id],
                                constants_file_ids=[constants_file_id],
                                job_name=job_name,
                                cluster_id=cluster_id,
                                instance_cost=instance_cost)
