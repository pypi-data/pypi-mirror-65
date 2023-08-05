from disco.core.config import Config
from tests.base_test import BaseTest
from mock import patch


class TestConfig(BaseTest):

    @patch('pathlib.Path.exists', return_value=True)
    @patch('pathlib.Path.read_text', return_value='{"some_key": "some_value"}')
    def test_get(self, read_text_mock, exists_mock):
        config = Config()
        value = config.get('some_key')
        assert value == 'some_value'

    @patch('pathlib.Path.exists', return_value=False)
    @patch('pathlib.Path.read_text', return_value='{"some_key": "some_value"}')
    def test_get_no_file(self, read_text_mock, exists_mock):
        config = Config()
        value = config.get('some_key')
        assert value is None

    @patch('pathlib.Path.exists', return_value=True)
    @patch('pathlib.Path.read_text', return_value='{}')
    @patch('pathlib.Path.write_text')
    def test_set(self, write_text_mock, read_text_mock, exists_mock):
        config = Config()
        config.set('some_key', 'some_value')
        write_text_mock.assert_called_with('{"some_key": "some_value"}')
        assert config.get('some_key') == 'some_value'

    @patch('pathlib.Path.exists', return_value=True)
    @patch('pathlib.Path.read_text', return_value='{"some_key": "some_value", "other_key": "other_value"}')
    @patch('pathlib.Path.write_text')
    def test_reset(self, write_text_mock, read_text_mock, exists_mock):
        config = Config()
        value = config.get('other_key')
        assert value == 'other_value'
        config.reset('other_key')
        write_text_mock.assert_called_with('{"some_key": "some_value"}')
        value = config.get('other_key')
        assert value is None

