from unittest.mock import patch, mock_open, MagicMock, Mock

import unittest
import requests
import subprocess
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# excluding following line for linter as it complains that
# from import is supposed to be at the top of the file
from smarsy.parse import (perform_get_request, validate_title,
                       get_user_credentials,
                       open_json_file,
                       perform_post_request,
                       validate_object_keys,
                       get_headers,
                       login,
                       Urls)  # noqa


class TestsGetPage(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch('requests.get')
    def test_perform_get_request_uses_provided_url_for_request(
            self,
            mock_request):
        mock_request.return_value.status_code = 200
        exepted_url = 'https://smarsy.ua/'
        perform_get_request(exepted_url)
        mock_request.assert_called_with(exepted_url)

    @patch('requests.get')
    def test_perform_get_request_returns_expected_text_on_valid_request(
            self,
            mock_response):
        url = 'https://smarsy.ua/'
        mock_response.return_value.status_code = 200
        expected_text = 'This is login Page'
        mock_response(url).text = expected_text
        self.assertEqual(perform_get_request(url), expected_text)

    @patch('requests.get')
    def test_perform_get_requestresponse_with_status_code_404_raises_exception(
            self,
            mock_response):
        url = 'https://smarsy.ua/'
        mock_response.return_value.status_code = 404
        self.assertRaises(requests.HTTPError, perform_get_request, url)

    def test_login_page_has_expected_title(self):
        html = '<html><title>Smarsy - Смарсі - Україна</title></html>'
        actual = validate_title(html)
        self.assertTrue(actual)

    def test_perform_post_request_uses_provided_url_for_request(
            self):
        session = Mock(
            post=MagicMock(
                return_value=Mock(status_code=200)
            )
        )
        exepted_url = 'https://smarsy.ua/'
        perform_post_request(session, exepted_url)
        session.post.assert_called_with(
            url=exepted_url, data=None, headers=None)

    def test_perform_post_request_returns_expected_text_on_valid_request(
            self):
        expected_text = 'some_text'
        session = Mock(
            post=MagicMock(
                return_value=Mock(text=expected_text, status_code=200)
            )
        )
        self.assertEqual(perform_post_request(session, 'url'), expected_text)

    def test_perform_post_request_uses_provided_data_for_post_request(
            self):
        expected_data = 'data'
        expected_url = 'url'
        session = Mock(
            post=MagicMock(
                return_value=Mock(status_code=200,
                                  data=expected_data,
                                  text=expected_url)
            )
        )
        perform_post_request(session, expected_url, data=expected_data)
        session.post.assert_called_with(url=expected_url,
                                        data=expected_data,
                                        headers=None)

    def test_perform_post_request_uses_provided_headers_for_post_request(
            self):
        expected_headers = {"a": 1}
        expected_url = 'url'
        session = Mock(
            post=MagicMock(
                return_value=Mock(status_code=200,
                                  data=None,
                                  text=expected_url,
                                  headers=expected_headers)
            )
        )
        perform_post_request(session, expected_url, headers=expected_headers)
        session.post.assert_called_with(
            url=expected_url, data=None, headers=expected_headers)

    def test_perform_post_request_resp_with_status_code_404_raises_exception(
            self):
        expected_text = 'some_text'
        s = Mock(
            post=MagicMock(
                return_value=Mock(text=expected_text, status_code=404)
            )
        )
        self.assertRaises(requests.HTTPError, perform_post_request, s, 'url')


class TestsFileOperations(unittest.TestCase):
    @patch('smarsy.parse.open_json_file')
    def test_user_credentials_object_is_the_same_like_in_file(self,
                                                              mock_json_load):
        expected = {
            'language': 'UA',
            'username': 'user',
            'password': 'pass'
        }
        mock_json_load.return_value = expected
        actual = get_user_credentials()
        self.assertEqual(actual, expected)

    @patch('smarsy.parse.open_json_file')
    def test_user_credentials_fails_if_there_is_no_user(self,
                                                        mock_json_load):
        creds = {
            'language': 'UA',
            'notuser': 'user',
            'password': 'pass'
        }
        mock_json_load.return_value = creds
        with self.assertRaises(Exception) as ue:
            get_user_credentials()
        self.assertEqual(
            'Credentials are in the wrong format (username is missing)',
            str(ue.exception))

    @patch('smarsy.parse.open_json_file')
    def test_user_credentials_fails_if_there_is_no_language(self,
                                                            mock_json_load):
        creds = {
            'nolanguage': 'UA',
            'username': 'user',
            'password': 'pass'
        }
        mock_json_load.return_value = creds
        with self.assertRaises(Exception) as ue:
            get_user_credentials()
        self.assertEqual(
            'Credentials are in the wrong format (language is missing)',
            str(ue.exception))

    @patch('smarsy.parse.open_json_file')
    def test_user_credentials_fails_if_there_is_no_password(self,
                                                            mock_json_load):
        creds = {
            'language': 'UA',
            'username': 'user',
            'nopassword': 'pass'
        }
        mock_json_load.return_value = creds
        with self.assertRaises(Exception) as ue:
            get_user_credentials()
        self.assertEqual(
            'Credentials are in the wrong format (password is missing)',
            str(ue.exception))

    @patch('builtins.open')
    @patch('json.load')
    def test_json_load_gets_content_from_provided_file(self,
                                                       stream_mock,
                                                       mock_json_load):
        expected = 'some_path_to_file'
        stream_mock = MagicMock()
        stream_mock.__enter__.Name = MagicMock(get=MagicMock(Name=expected))
        open_json_file(expected)
        mock_json_load.assert_called_with(expected)

    def test_open_json_file_returns_object_from_provided_file(self):
        read_data = mock_open(read_data=json.dumps({'a': 1, 'b': 2, 'c': 3}))
        with patch('builtins.open', read_data):
            result = open_json_file('filename')
        self.assertEqual({'a': 1, 'b': 2, 'c': 3}, result)

    def test_open_json_file_raise_exception_with_non_existing_path(self):
        # test file does not exist
        with self.assertRaises(IOError) as context:
            open_json_file('null')
        self.assertEqual(
            'null does not exist.', str(context.exception))

    def test_open_json_file_raise_exception_when_invalid_json_in_file(self):
        # test file does not exist
        read_data = mock_open(read_data='')
        with patch("builtins.open", read_data):
            with self.assertRaises(ValueError) as context:
                open_json_file('filename')
            self.assertEqual(
                'filename is not valid JSON.', str(context.exception))

    def test_validate_object_keys_all_keys_exists(self):
        keys_list = ('language', 'username', 'password')
        creds = {
            'language': 'UA',
            'username': 'user',
            'password': 'pass'
        }
        self.assertTrue(validate_object_keys(keys_list, creds))

    def test_validate_object_keys_raise_exception_with_wrong_key(self):
        keys_list = ('language', 'username', 'password')
        creds = {
            'language': 'UA',
            'username': 'user',
            'nopassword': 'pass'
        }
        with self.assertRaises(Exception) as ke:
            validate_object_keys(keys_list, creds)
        self.assertEqual('Key is missing', str(ke.exception))

    @patch('smarsy.parse.open_json_file')
    def test_user_headers_object_is_the_same_like_in_file(self,
                                                          mock_json_load):
        expected = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }
        mock_json_load.return_value = expected
        actual = get_headers()
        self.assertEqual(actual, expected)


@patch('smarsy.parse.perform_post_request', return_value='Smarsy Login')
@patch('smarsy.parse.get_user_credentials', return_value={'u': 'name'})
@patch('smarsy.parse.get_headers', return_value={'h': '123'})
class TestsParse(unittest.TestCase):
    def test_login_gets_headers(self,
                                mock_headers,
                                user_credentials,
                                mock_request):
        login()
        self.assertTrue(mock_headers.called)

    def test_login_gets_credentials(self,
                                    mock_headers,
                                    user_credentials,
                                    mock_request):
        login()
        self.assertTrue(user_credentials.called)

    @patch('requests.Session', return_value='session')
    def test_login_uses_login_page_in_request(self,
                                              mock_session,
                                              mock_headers,
                                              user_credentials,
                                              mock_request):
        login()
        mock_request.assert_called_with(mock_session.return_value,
                                        Urls.LOGIN.value,
                                        user_credentials.return_value,
                                        mock_headers.return_value)

    @patch('requests.Session', return_value='session')
    def test_login_returns_post_request_text(self,
                                             mock_session,
                                             mock_headers,
                                             user_credentials,
                                             mock_request):
        self.assertEqual(login(), 'Smarsy Login')

    def test_if_empty_keys_raise_exception_with_empty_key(self,
                                                          mock_headers,
                                                          user_credentials,
                                                          mock_request):
        keys_list = ()
        creds = {
            'language': 'UA',
            'username': 'user',
            'nopassword': 'pass'
        }
        with self.assertRaises(Exception) as ke:
            validate_object_keys(keys_list, creds)
        self.assertEqual('Key is empty', str(ke.exception))


if __name__ == '__main__':
    if '--unittest' in sys.argv:
        subprocess.call([sys.executable, '-m', 'unittest', 'discover'])
