from unittest import TestCase
from unittest.mock import patch, Mock
from flask_auth_service_mongo import api_rest
from flask_auth_service_mongo.security.use_cases import AuthResponse
from flask_auth_service_mongo.security.utils import AccessTokens


def resolve_patch(path: str) -> str:
    return f'flask_auth_service_mongo.security.api_rest.session.{path}'


class TestLogin(TestCase):

    @patch(resolve_patch('request'))
    @patch(resolve_patch('Login'))
    def test_error(self, mock_use_case, mock_request):
        # Mocks
        mock_request.get_json.return_value = {'data': 'ok'}
        mock_handle = Mock()
        mock_handle.handle.return_value = AuthResponse(
            message='error',
            http_code=400
        )
        mock_use_case.return_value = mock_handle

        # Exec
        result = api_rest.login('test')

        # Asserts
        self.assertEqual(result, ({'message': 'error'}, 400))
        mock_handle.handle.assert_called_with(
            role='test',
            request={'data': 'ok'}
        )

    @patch(resolve_patch('request'))
    @patch(resolve_patch('Login'))
    def test_ok(self, mock_use_case, mock_request):
        # Mocks
        mock_request.get_json.return_value = {'data': 'ok'}
        mock_handle = Mock()
        mock_handle.handle.return_value = AuthResponse(
            message='ok',
            http_code=200,
            change_password=False,
            tokens=AccessTokens(
                access_token='Abc123',
                token_type='Bearer',
                refresh_token='Abc',
                expires_in=60
            )
        )
        mock_use_case.return_value = mock_handle

        # Exec
        result = api_rest.login('test')

        # Asserts
        self.assertEqual(
            result,
            ({
                'data': {
                    'access_token': 'Abc123',
                    'change_password': False,
                    'expires_in': 60,
                    'refresh_token': 'Abc',
                    'token_type': 'Bearer'
                },
                'message': 'ok'
            }, 200)
        )
        mock_handle.handle.assert_called_with(
            role='test',
            request={'data': 'ok'}
        )


class TestLogout(TestCase):

    @patch(resolve_patch('request'),
           headers={'Authorization': 'Bearer token_test'})
    @patch(resolve_patch('Logout'))
    def test_ok(self, mock_use_case, mock_request):
        # Mocks
        mock_handle = Mock()
        mock_handle.handle.return_value = AuthResponse(
            message='ok',
            http_code=200
        )
        mock_use_case.return_value = mock_handle

        # Exec
        result = api_rest.logout()

        # Asserts
        self.assertEqual(result, ({'message': 'ok'}, 200))
        mock_handle.handle.assert_called_with(
            token='token_test'
        )
