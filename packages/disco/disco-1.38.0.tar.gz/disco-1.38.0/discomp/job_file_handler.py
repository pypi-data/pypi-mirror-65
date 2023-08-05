# /**
#  * Copyright (c) Samsung, Inc. and its affiliates.
#  *
#  * This source code is licensed under the RESTRICTED license found in the
#  * LICENSE file in the root directory of this source tree.
#  */
import inspect, sys
import os
import glob
import dill
from zipfile import ZipFile
from . import utils
from disco import upload_file, Job


def upload_job_files(job_name, func, args, args_types):
    script_module_ids_tuple = upload_script_module_and_req_files(job_name, func, args_types)
    input_files_ids_array = upload_input_files(args, args_types)
    return script_module_ids_tuple, input_files_ids_array


def upload_script_module_and_req_files(job_name, func, args_types):
    if (func):
        script_name = utils.get_script_file_name(job_name)
        multiple = '' if args_types == utils.get_map_args_type() else '*'
        module_file_name = utils.get_module_file_name()
        module = dill.dumps(inspect.getmodule(func))
        script_content = '#!/usr/bin/python3.6\n'
        script_content += """
import sys, dill
with open(sys.argv[1], "rb") as f_arg:
    arg = dill.load(f_arg)
with open('customer-module.pickle', 'rb') as f_module:
    module = dill.load(f_module)
"""
        script_content += 'func = getattr(module, "' + func.__name__ + '")\n'
        script_content += 'result = func(' + multiple + 'arg)'
        script_content += """
with open('run-result/result.pickle', 'wb') as f_result:
    dill.dump(result, f_result)   
"""
        script_id = upload_file(script_name, script_content, show_progress_bar=False)
        module_id = upload_file(module_file_name, module, show_progress_bar=False)
        requirements = Job.generate_requirements()
        requirements = requirements + "\ndiscomp"
        req_id = upload_file("requirements.txt", requirements, show_progress_bar=False)

        return script_id, module_id, req_id


def upload_input_files(args, args_types):
    if args_types == utils.get_process_args_type():
        return [upload_input_file(args)]
    else:
        file_ids = []
        for i, arg in enumerate(args):
            arg_to_dump = tuple(arg) if (args_types == utils.get_starmap_args_type()) else arg
            file_ids.append(upload_input_file(arg_to_dump, i))
        return file_ids


def upload_input_file(arg, i=0):
    input_filename = utils.get_input_file_name_prefix() + str(i) + '.pickle'
    dilled_arg = dill.dumps(arg)
    return upload_file(input_filename, dilled_arg, show_progress_bar=False)


def get_results(job):
    task_results = job.get_task_results()
    return [dill.loads(result['result.pickle']) for result in task_results]
