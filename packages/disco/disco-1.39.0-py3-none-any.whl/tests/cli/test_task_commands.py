from tests.base_test import BaseTest
from disco_cli import cli, setup_cli
from mock import patch
from click.testing import CliRunner
from .cli_test_utils import output_message_includes
from disco.models import TaskAuditEvent

class TestTaskCommands(BaseTest):

    def setup_class(self):
        setup_cli()

    @patch('disco.gql.authentication.Authentication.is_logged_in')
    @patch('disco.Task.get_task_events_log')
    def test_show(self, get_task_events_log_mock, is_logged_in_mock):
        is_logged_in_mock.return_value = True
        list_task_events = [
            TaskAuditEvent({'time': '2020-02-25T12:28:03.630Z', 'displayMessage': 'Agent received task',
                            'type': 'Received'}),
            TaskAuditEvent({'time': '2020-02-25T12:28:03.633Z', 'displayMessage': 'Task setup', 'type': 'TaskSetup'}),
            TaskAuditEvent({'time': '2020-02-25T12:28:03.753Z', 'displayMessage': 'Artifacts Downloaded',
                            'type': 'DownloadingArtifacts'}),
            TaskAuditEvent({'time': '2020-02-25T12:28:18.418Z', 'displayMessage': 'Started running', 'type': 'Started'}),
            TaskAuditEvent({'time': '2020-02-25T12:28:35.997Z', 'displayMessage': 'Task completed successfully',
                            'type': 'Completed'})
        ]

        get_task_events_log_mock.return_value = list_task_events
        runner = CliRunner()
        result = runner.invoke(cli, ['task', 'show', 'task_id'])
        assert result.exit_code == 0
        get_task_events_log_mock.assert_called()
        assert output_message_includes(result, '| Agent received task         |')
        assert output_message_includes(result, '| Task completed successfully |')

    @patch('disco.gql.authentication.Authentication.is_logged_in')
    @patch('disco.Task.get_task_events_log')
    def test_show_empty(self, get_task_events_log_mock, is_logged_in_mock):
        is_logged_in_mock.return_value = True
        list_task_events = []

        get_task_events_log_mock.return_value = list_task_events
        runner = CliRunner()
        result = runner.invoke(cli, ['task', 'show', 'task_id'])
        assert result.exit_code == 0
        get_task_events_log_mock.assert_called()
        assert result.output == 'No logs available yet.\n'




