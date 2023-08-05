# /**
#  * Copyright (c) Samsung, Inc. and its affiliates.
#  *
#  * This source code is licensed under the RESTRICTED license found in the
#  * LICENSE file in the root directory of this source tree.
#  */
import dill

from . import job_file_handler
import os
from disco import Job
from disco.core.constants import JobStatus


def add_job(job_name, func, args, args_types, wait=False):
    job_files = job_file_handler.upload_job_files(job_name, func, args, args_types)
    job = add_job_request(job_name, job_files[0], job_files[1], wait)
    return job


def start_job(job):
    job.start()


def wait_for_job_done(job):
    job.wait_for_finish(timeout=(24 * 60 * 60))


def get_results(job):
    task_results = get_job_results(job)
    results = []
    if task_results and len(task_results) > 0:
        for task_result in task_results:
            for file in task_result.raw_result:
                if file[0] == 'result.pickle':
                    results.append(dill.loads(file[1]))
    return results


def add_job_request(job_name, script_module_and_req_ids, input_files_ids, wait=False):
    machine_size = os.environ.get('DISCO_MACHINE_SIZE')
    cluster_id = os.environ.get('DISCO_CLUSTER_ID')
    job = Job.create(script_file_id=script_module_and_req_ids[0],
                     input_file_ids=input_files_ids,
                     constants_file_ids=[script_module_and_req_ids[1], script_module_and_req_ids[2]],
                     job_name=job_name,
                     cluster_id=cluster_id,
                     cluster_instance_type=machine_size if machine_size is not None else 's',
                     upload_requirements_file=False)
    if wait:
        job.start()
        job.wait_for_finish()
    return job


def get_job_results(job):
    job_status = job.get_status()

    # Job is done
    if job_status == JobStatus.done:
        # Download the results
        task_results = job.get_results()
        return task_results
    return False
