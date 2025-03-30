import os
import json
import unittest
from unittest.mock import patch, mock_open
from config.settings import load_settings, Settings

class TestSettingsLoading(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open, read_data='DEBUG=True\nSECRET_KEY=mysecret\nDATABASE_URL=sqlite:///:memory:\nAPI_KEY=myapikey\n')
    def test_load_env_vars(self, mock_file):
        """Test loading settings from environment variables."""
        with patch.dict(os.environ, {
            'DEBUG': 'True',
            'SECRET_KEY': 'mysecret',
            'DATABASE_URL': 'sqlite:///:memory:',
            'API_KEY': 'myapikey'
        }):
            settings = load_settings()
            self.assertTrue(settings.debug)
            self.assertEqual(settings.secret_key, 'mysecret')
            self.assertEqual(settings.database_url, 'sqlite:///:memory:')
            self.assertEqual(settings.api_key, 'myapikey')

    @patch('builtins.open', new_callable=mock_open, read_data='{"debug": false, "secret_key": "mysecret", "database_url": "sqlite:///:memory:", "api_key": "myapikey"}')
    def test_load_json_config(self, mock_file):
        """Test loading settings from JSON configuration file."""
        with patch.dict(os.environ, {
            'DEBUG': '',
            'SECRET_KEY': '',
            'DATABASE_URL': '',
            'API_KEY': ''
        }):
            settings = load_settings()
            self.assertFalse(settings.debug)
            self.assertEqual(settings.secret_key, 'mysecret')
            self.assertEqual(settings.database_url, 'sqlite:///:memory:')
            self.assertEqual(settings.api_key, 'myapikey')

    @patch('builtins.open', new_callable=mock_open, read_data='{"debug": false, "secret_key": "", "database_url": "", "api_key": ""}')
    def test_validation_missing_secret_key(self, mock_file):
        """Test validation raises error for missing SECRET_KEY."""
        with self.assertRaises(ValueError) as context:
            load_settings()
        self.assertEqual(str(context.exception), "SECRET_KEY is required.")

    @patch('builtins.open', new_callable=mock_open, read_data='{"debug": false, "secret_key": "mysecret", "database_url": "", "api_key": ""}')
    def test_validation_missing_database_url(self, mock_file):
        """Test validation raises error for missing DATABASE_URL."""
        with self.assertRaises(ValueError) as context:
            load_settings()
        self.assertEqual(str(context.exception), "DATABASE_URL is required.")

    @patch('builtins.open', new_callable=mock_open, read_data='{"debug": false, "secret_key": "mysecret", "database_url": "sqlite:///:memory:", "api_key": ""}')
    def test_validation_missing_api_key(self, mock_file):
        """Test validation raises error for missing API_KEY."""
        with self.assertRaises(ValueError) as context:
            load_settings()
        self.assertEqual(str(context.exception), "API_KEY is required.")

if __name__ == '__main__':
    unittest.main()
