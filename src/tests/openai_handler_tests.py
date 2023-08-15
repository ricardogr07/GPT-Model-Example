import unittest
import openai
from unittest.mock import patch
from handlers.openai_handler import OpenAIApiHandler

class TestOpenAIApiHandler(unittest.TestCase):

    def setUp(self):
        # This method is called before each test. Here we create an instance of OpenAIApiHandler
        self.handler = OpenAIApiHandler()
        self.valid_messages = [{'role': 'system', 'content': 'You are a helpful assistant.'}]
        self.api_response = {'choices': [{'message': {'content': 'Generated completion'}}]}

    def test_configure_openai_valid_api_key_and_base_url(self):
        # Simulates having valid API key and base URL in environment variables
        with patch('os.environ.get', side_effect=['valid_api_key', 'valid_base_url']):
            self.handler.configure_openai()
            self.assertEqual(self.handler.OPENAI_API_KEY, 'valid_api_key')
            self.assertEqual(self.handler.OPENAI_API_BASE, 'valid_base_url')

    def test_configure_openai_missing_api_key_or_base_url(self):
        # Simulates missing API key and base URL in environment variables
        with patch('os.environ.get', side_effect=[None, None]):
            self.handler.configure_openai()
            self.assertIsNone(self.handler.OPENAI_API_KEY)
            self.assertIsNone(self.handler.OPENAI_API_BASE)

    def test_generate_chat_completion_valid_messages_array(self):
        # Simulates a valid API response when a valid messages array is provided
        with patch('openai.ChatCompletion.create', return_value=self.api_response):
            result = self.handler.generate_chat_completion(self.valid_messages)
            self.assertEqual(result, 'Generated completion')

    def test_generate_chat_completion_invalid_messages_array(self):
        with self.assertRaises(openai.error.InvalidRequestError) as context:
            self.handler.generate_chat_completion('invalid_messages')

        self.assertEqual(
            str(context.exception),
            "'invalid_messages' is not of type 'array' - 'messages'"
        )


    def test_generate_chat_completion_api_call_error(self):
        with patch('openai.ChatCompletion.create', side_effect=openai.error.OpenAIError('API call error')):
            with self.assertRaises(openai.error.OpenAIError) as context:
                self.handler.generate_chat_completion(self.valid_messages)

            self.assertEqual(str(context.exception), 'API call error')

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
