import unittest
import os
import pytest
from unittest.mock import patch, MagicMock
import on_call_rotation
import importlib
import logging

class TestScript(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set the environment variables before importing the script
        os.environ['PAGERDUTY_API_TOKEN'] = 'pd_token'
        os.environ['OPSLEVEL_API_TOKEN'] = 'ol_token'
        os.environ['ENVIRONMENT'] = 'development'

    # Test the setup of environment variables
    @patch("on_call_rotation.os.getenv")
    @patch("on_call_rotation.requests.post")
    @patch("on_call_rotation.requests.get")
    def test_main_function(self, mock_get, mock_post, mocked_getenv):

        # Setup mocks for os.getenv
        mocked_getenv.side_effect = lambda x: {"PAGERDUTY_API_TOKEN": "pd_token", "OPSLEVEL_API_TOKEN": "ol_token", "ENVIRONMENT": "development"}.get(x)
    

        print("Mocked getenv:", mocked_getenv.side_effect("PAGERDUTY_API_TOKEN"))
        # Setup mocks for requests.get and requests.post
        mock_get.return_value = MagicMock(status_code=200, json=lambda: {"data": "some_data"})
        mock_post.return_value = MagicMock(status_code=200)

        # Call the main function
        on_call_rotation.main()

        # Assertions for requests.get and requests.post calls
        mock_get.assert_called_with(
            'https://api.pagerduty.com/escalation_policies',
            headers={'Accept': 'application/vnd.pagerduty+json;version=2', 'Authorization': 'Token token=pd_token'},
            timeout=5
        )
        mock_post.assert_called_with(
            f"https://app.opslevel.com/integrations/custom_event/ol_token", 
            headers={'Content-Type': 'application/json'},
            json={"data": "some_data"},
            timeout=5
        )

    # Test logging configuration based on the environment
    def test_logging_configuration(self):
        with patch("logging.basicConfig") as mock_logging:
            with patch("os.getenv", return_value="production"):
                on_call_rotation.main()
                mock_logging.assert_called_with(filename='app.log', level=logging.ERROR,
                                                format='%(asctime)s - %(levelname)s - %(message)s')

            with patch("os.getenv", return_value="development"):
                on_call_rotation.main()
                mock_logging.assert_called_with(level=logging.DEBUG,
                                                format='%(asctime)s - %(levelname)s - %(message)s')                                                    

    # Test API call failures
    @patch("on_call_rotation.requests.post")
    @patch("on_call_rotation.requests.get")
    def test_api_call_failures(self, mocked_post, mocked_get):
        mocked_get.side_effect = Exception("API failure")
        mocked_post.side_effect = Exception("API failure")

        with patch("on_call_rotation.handle_request_errors") as mocked_error_handler:
            on_call_rotation.main()
            assert mocked_error_handler.called

            mocked_error_handler.assert_called()

if __name__ == '__main__':
    unittest.main()

