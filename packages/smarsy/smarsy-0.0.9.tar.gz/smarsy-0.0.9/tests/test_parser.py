from unittest.mock import patch, mock_open, MagicMock, Mock

import unittest
import requests
import subprocess
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '..',
                                             'smarsy')))
# excluding following line for linter as it complains that
# from import is supposed to be at the top of the file
from smarsy.parse import (perform_get_request, validate_title,
                       get_user_credentials, open_json_file,
                       perform_post_request, validate_object_keys,
                       get_headers, login, Urls,
                       childs_page_return_right_login)  # noqa


class TestsGetPage(unittest.TestCase):
    @patch('requests.Session')
    def setUp(self, mocked_session):
        self.default_url = 'http://www.smarsy.ua'
        self.default_text = 'Informative text'
        self.default_status_code = 200
        mocked_session.get.return_value = Mock(
            status_code=self.default_status_code,
            text=self.default_text)
        self.mocked_session = mocked_session

    def test_perform_get_request_uses_provided_url_for_request_with_class(
            self):
        perform_get_request(self.mocked_session, self.default_url)
        self.mocked_session.get.assert_called_with(url=self.default_url,
                                                   params=None, headers=None)

    def test_perform_get_request_uses_provided_url_for_request(self):
        perform_get_request(self.mocked_session, self.default_url)
        self.mocked_session.get.assert_called_with(url=self.default_url,
                                                   params=None, headers=None)

    def test_perform_get_request_returns_expected_text_on_valid_request(
            self):
        expected_text = 'This is login Page'
        self.mocked_session.get(self.default_url).text = expected_text
        self.assertEqual(perform_get_request(self.mocked_session,
                                             self.default_url),
                         expected_text)

    def test_perform_get_request_resp_with_status_code_404_raises_exception(
            self):
        self.mocked_session.get.return_value.status_code = 404
        self.assertRaises(requests.HTTPError, perform_get_request,
                          self.mocked_session, self.default_url)

    def test_perform_get_request_uses_provided_data_for_get_request(
            self):
        expected_params = 'params'
        perform_get_request(self.mocked_session, self.default_url,
                            params=expected_params)
        self.mocked_session.get.assert_called_with(url=self.default_url,
                                                   params=expected_params,
                                                   headers=None)

    def test_perform_get_request_uses_provided_headers_for_get_request(
            self):
        expected_headers = {"a": 1}
        perform_get_request(self.mocked_session, self.default_url,
                            headers=expected_headers)
        self.mocked_session.get.assert_called_with(url=self.default_url,
                                                   params=None,
                                                   headers=expected_headers)


class TestsPostRequest(unittest.TestCase):

    @patch('requests.Session')
    def setUp(self, mocked_session):
        self.default_url = 'http://www.smarsy.ua'
        self.default_text = 'Informative text'
        self.default_status_code = 200
        mocked_session.post.return_value = Mock(
            status_code=self.default_status_code,
            text=self.default_text)
        self.mocked_session = mocked_session

    def test_perform_post_request_uses_provided_url_for_request(
            self):
        perform_post_request(self.mocked_session, self.default_url)
        self.mocked_session.post.assert_called_with(url=self.default_url,
                                                    data=None, headers=None)

    def test_perform_post_request_returns_expected_text_on_valid_request(
            self):
        expected_text = 'some_text'
        self.mocked_session.post(self.default_url).text = expected_text
        self.assertEqual(perform_post_request(self.mocked_session,
                                              self.default_url),
                         expected_text)

    def test_perform_post_request_uses_provided_data_for_post_request(
            self):
        expected_data = 'data'
        perform_post_request(self.mocked_session, self.default_url,
                             data=expected_data)
        self.mocked_session.post.assert_called_with(url=self.default_url,
                                                    data=expected_data,
                                                    headers=None)

    def test_perform_post_request_uses_provided_headers_for_post_request(
            self):
        expected_headers = {"a": 1}
        perform_post_request(self.mocked_session, self.default_url,
                             headers=expected_headers)
        self.mocked_session.post.assert_called_with(url=self.default_url,
                                                    data=None,
                                                    headers=expected_headers)

    def test_perform_post_request_resp_with_status_code_404_raises_exception(
            self):
        self.mocked_session.post.return_value.status_code = 404
        self.assertRaises(requests.HTTPError, perform_post_request,
                          self.mocked_session, self.default_url)

    def test_perform_post_request_changes_response_encoding_to_provided(self):
        expected_encoding = 'utf8'
        perform_post_request(self.mocked_session, self.default_url,
                             encoding=expected_encoding)
        self.assertEqual(self.mocked_session.post.return_value.encoding, 
                         expected_encoding)


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


class TestPageContent(unittest.TestCase):

    def test_login_page_has_expected_title(self):
        html = '<html><title>Smarsy - Смарсі - Україна</title></html>'
        actual = validate_title(html)
        self.assertTrue(actual)

    def test_childs_page_has_expected_username(self):
        response_string = '\n<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" \
                     "http://www.w3.org/TR/html4/strict.dtd">\n<HTML>\n \
                     <HEAD>\n<TITLE>login</TITLE>\n'
        self.assertTrue(childs_page_return_right_login(response_string,
                                                       'login'))

    def test_childs_page_raise_exception_with_unexpected_username(self):
        response_string = '\n<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" \
                     "http://www.w3.org/TR/html4/strict.dtd">\n<HTML>\n \
                     <HEAD>\n<TITLE>login</TITLE>\n'
        with self.assertRaises(ValueError) as error:
            childs_page_return_right_login(response_string, 'nologin')
        self.assertEqual('Invalid Smarsy Login', str(error.exception))


if __name__ == '__main__':
    if '--unittest' in sys.argv:
        subprocess.call([sys.executable, '-m', 'unittest', 'discover'])
