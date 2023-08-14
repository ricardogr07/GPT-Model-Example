from unittest import mock
import os
import openai


import unittest

class TestConfigureOpenai(unittest.TestCase):
    # Test that load_dotenv() successfully loads environment variables
    def test_load_dotenv_success(self):
        with mock.patch('dotenv.load_dotenv') as mock_load_dotenv:
            self.handler.configure_openai()
            mock_load_dotenv.assert_called_once()

    # Test that the OPENAI_API_KEY is successfully retrieved from environment variables
    def test_retrieve_api_key_success(self):
        with mock.patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'}):
            self.handler.configure_openai()
            self.assertEqual(self.handler.OPENAI_API_KEY, 'test_key')

    # Test that the OPENAI_API_BASE is successfully retrieved from environment variables
    def test_retrieve_api_base_success(self):
        with mock.patch.dict(os.environ, {'OPENAI_API_BASE': 'test_base'}):
            self.handler.configure_openai()
            self.assertEqual(self.handler.OPENAI_API_BASE, 'test_base')

    # Test that openai.api_type is set to 'azure'
    def test_set_api_type(self):
        self.handler.configure_openai()
        self.assertEqual(openai.api_type, 'azure')

    # Test that openai.api_key is set to the retrieved OPENAI_API_KEY
    def test_set_api_key(self):
        with mock.patch.dict(os.environ, {'OPENAI_API_KEY': 'test_key'}):
            self.handler.configure_openai()
            self.assertEqual(openai.api_key, 'test_key')

    # Test that openai.api_base is set to the retrieved OPENAI_API_BASE
    def test_set_api_base(self):
        with mock.patch.dict(os.environ, {'OPENAI_API_BASE': 'test_base'}):
            self.handler.configure_openai()
            self.assertEqual(openai.api_base, 'test_base')