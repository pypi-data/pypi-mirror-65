from disco import Job
from mock import patch, ANY
import unittest
from discomp import Process
from discomp.tests import func_examples


class TestProcess(unittest.TestCase):

    @patch('disco.job.Job.create')
    @patch('disco.job.Job.start')
    @patch('disco.job.Job.wait_for_finish')
    @patch('disco.job.Job.get_results')
    @patch('disco.job.Job.get_status')
    @patch('disco.asset.Asset.upload', return_value='file_id')
    def test_create_process_start_join(self, asset_upload_mock, get_status_mock, get_results_mock, wait_for_finish_mock,
                                       start_mock,
                                       create_mock):
        args = (3, 7)
        create_mock.return_value = Job('some_job_id')
        p1 = Process(
            name='abcdjob',
            target=func_examples.mult,
            args=args)
        create_mock.assert_called_with(cluster_id=None, cluster_instance_type='s',
                                       constants_file_ids=['file_id', 'file_id'],
                                       input_file_ids=['file_id'],
                                       job_name=ANY, script_file_id='file_id', upload_requirements_file=False)

        p1.start()
        assert p1.job_status == 'JobStatus.started'
        start_mock.assert_called()

        p1.join()
        wait_for_finish_mock.assert_called()
