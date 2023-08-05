from tests.base_test import BaseTest
from mock import patch
import mock
import disco


class TestTask(BaseTest):

    @BaseTest.with_config_and_env(authenticated=True)
    @patch('disco.gql.authentication.Authentication.get_current_user_id')
    def test_get_task_events_log(self, get_current_user_id_mock):
        get_current_user_id_mock.return_value = '123'
        with mock.patch('disco.gql.authentication.Authentication.query') as graphql_mock:
            graphql_mock.return_value = {'fetchTaskAuditEvents': [
                {'time': '2020-02-25T12:28:03.630Z', 'displayMessage': 'Agent received task', 'type': 'Received'},
                {'time': '2020-02-25T12:28:03.633Z', 'displayMessage': 'Task setup', 'type': 'TaskSetup'},
                {'time': '2020-02-25T12:28:03.753Z', 'displayMessage': 'Artifacts Downloaded',
                 'type': 'DownloadingArtifacts'},
                {'time': '2020-02-25T12:28:18.418Z', 'displayMessage': 'Started running', 'type': 'Started'},
                {'time': '2020-02-25T12:28:35.997Z', 'displayMessage': 'Task completed successfully',
                 'type': 'Completed'}]}

            task_id = self.random_str('task-id')
            task = disco.Task(task_id)
            result = task.get_task_events_log()

        assert isinstance(result, list)
        assert len(result) == 5
        assert result[0].time == '2020-02-25T12:28:03.630Z'
        assert result[0].display_message == 'Agent received task'
        assert result[0].type == 'Received'
        assert result[4].time == '2020-02-25T12:28:35.997Z'
        assert result[4].display_message == 'Task completed successfully'
        assert result[4].type == 'Completed'


