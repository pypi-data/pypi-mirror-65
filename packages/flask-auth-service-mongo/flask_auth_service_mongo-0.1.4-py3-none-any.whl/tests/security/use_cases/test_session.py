from unittest import TestCase
from unittest.mock import patch, Mock
from flask_auth_service_mongo.security.utils import AccessTokens
from flask_auth_service_mongo.security.use_cases import (
    Response,
    AuthResponse,
    Login,
    Logout,
    RefreshToken
)
from flask_auth_service_mongo.security.models import User, WhitelistToken


def resolve_patch(path: str) -> str:
    return f'flask_auth_service_mongo.security.use_cases.session.{path}'


class TestLogin(TestCase):

    def test_request_not_valid(self):
        use_case = Login()
        result = use_case.handle({'key': 'value'}, 'role')
        expected = {
            'key': ['unknown field'],
            'password': ['required field'],
            'username': ['required field']
        }

        self.assertIsInstance(result, AuthResponse)
        self.assertEqual(result.message, 'bad_request')
        self.assertEqual(result.errors, expected)
        self.assertEqual(result.http_code, 400)

    @patch(resolve_patch('UserRepository.find_one'))
    def test_user_not_found(self, mock_user_find):
        # Mocks
        mock_user_find.return_value = None

        use_case = Login()
        request = dict(
            username='test_name',
            password='test_pass'
        )
        result = use_case.handle(request, 'role')

        # asserts
        mock_user_find.assert_called_with(
            username='test_name'
        )
        self.assertIsInstance(result, AuthResponse)
        self.assertEqual(result.message, 'bad_credentials')
        self.assertEqual(result.http_code, 400)

    @patch(resolve_patch('UserRepository.find_one'))
    def test_incorrect_role(self, mock_user_find):
        # Mocks
        mock_user_find.return_value = Mock(name='other_role')

        use_case = Login()
        request = dict(
            username='test_name',
            password='test_pass'
        )
        result = use_case.handle(request, 'role')

        # asserts
        mock_user_find.assert_called_with(
            username='test_name'
        )
        self.assertIsInstance(result, AuthResponse)
        self.assertEqual(result.message, 'bad_credentials')
        self.assertEqual(result.http_code, 400)

    @patch(resolve_patch('password_match'))
    @patch(resolve_patch('UserRepository.find_one'))
    def test_incorrect_password(self, mock_user_find, mock_password_match):
        # Mocks
        user = Mock(password='pass')
        user.role.name = 'role'
        mock_user_find.return_value = user
        mock_password_match.return_value = False

        use_case = Login()
        request = dict(
            username='test_name',
            password='test_pass'
        )
        result = use_case.handle(request, 'role')

        # asserts
        mock_user_find.assert_called_with(
            username='test_name'
        )
        mock_password_match.assert_called_with(request['password'], 'pass')
        self.assertIsInstance(result, AuthResponse)
        self.assertEqual(result.message, 'bad_credentials')
        self.assertEqual(result.http_code, 400)

    @patch(resolve_patch('config.WHITE_LIST_TOKEN'), True)
    @patch(resolve_patch('WhitelistToken'))
    @patch(resolve_patch('token_generate'))
    @patch(resolve_patch('password_match'))
    @patch(resolve_patch('UserRepository.find_one'))
    def test_ok_with_whitelist_token(
        self,
        mock_user_find,
        mock_password_match,
        mock_token_generate,
        mock_whitelist
    ):
        # Mocks
        uuids = {
            'uuid_access': 'abc123',
            'uuid_refresh': 'abc456'
        }
        tokens = AccessTokens(
            token_type='Bearer',
            access_token='__access_token',
            refresh_token='__refresh_token',
            expires_in=10
        )
        user = Mock(
            password='hash_pass',
            change_password=False
        )
        user.role.name = 'role'
        mock_user_find.return_value = user
        mock_password_match.return_value = True
        mock_token_generate.return_value = tokens, uuids

        # Exec
        use_case = Login()
        request = dict(
            username='test_name',
            password='test_pass'
        )
        result = use_case.handle(request, 'role')

        # asserts
        mock_whitelist.assert_called_with(
            uuid_access='abc123',
            uuid_refresh='abc456',
            user=user
        )
        mock_password_match.assert_called_with('test_pass', 'hash_pass')
        self.assertIsInstance(result, AuthResponse)
        self.assertEqual(result.message, 'ok')
        self.assertEqual(result.http_code, 200)
        self.assertIsInstance(result.tokens, AccessTokens)
        self.assertEqual(result.tokens.access_token, '__access_token')
        self.assertEqual(result.tokens.refresh_token, '__refresh_token')
        self.assertEqual(result.change_password, False)

    @patch(resolve_patch('config.WHITE_LIST_TOKEN'), False)
    @patch(resolve_patch('WhitelistToken'))
    @patch(resolve_patch('token_generate'))
    @patch(resolve_patch('password_match'))
    @patch(resolve_patch('UserRepository.find_one'))
    def test_ok_without_whitelist_token(
        self,
        mock_user_find,
        mock_password_match,
        mock_token_generate,
        mock_whitelist
    ):
        # Mocks
        uuids = {
            'uuid_access': 'abc123',
            'uuid_refresh': 'abc456'
        }
        tokens = AccessTokens(
            token_type='Bearer',
            access_token='__access_token',
            refresh_token='__refresh_token',
            expires_in=10
        )
        user = Mock(
            password='hash_pass',
            change_password=False
        )
        user.role.name = 'role'
        mock_user_find.return_value = user
        mock_password_match.return_value = True
        mock_token_generate.return_value = tokens, uuids

        # Exec
        use_case = Login()
        request = dict(
            username='test_name',
            password='test_pass'
        )
        result = use_case.handle(request, 'role')

        # asserts
        mock_whitelist.assert_not_called()
        mock_password_match.assert_called_with('test_pass', 'hash_pass')
        self.assertIsInstance(result, AuthResponse)
        self.assertEqual(result.message, 'ok')
        self.assertEqual(result.http_code, 200)
        self.assertIsInstance(result.tokens, AccessTokens)
        self.assertEqual(result.tokens.access_token, '__access_token')
        self.assertEqual(result.tokens.refresh_token, '__refresh_token')
        self.assertEqual(result.change_password, False)

    @patch(resolve_patch('config.WHITE_LIST_TOKEN'), False)
    @patch(resolve_patch('WhitelistToken'))
    @patch(resolve_patch('token_generate'))
    @patch(resolve_patch('password_match'))
    @patch(resolve_patch('UserRepository.find_one'))
    def test_ok_list_roles(
        self,
        mock_user_find,
        mock_password_match,
        mock_token_generate,
        mock_whitelist
    ):
        # Mocks
        uuids = {
            'uuid_access': 'abc123',
            'uuid_refresh': 'abc456'
        }
        tokens = AccessTokens(
            token_type='Bearer',
            access_token='__access_token',
            refresh_token='__refresh_token',
            expires_in=10
        )
        user = Mock(
            password='hash_pass',
            change_password=False
        )
        user.role.name = 'role'
        mock_user_find.return_value = user
        mock_password_match.return_value = True
        mock_token_generate.return_value = tokens, uuids

        # Exec
        use_case = Login()
        request = dict(
            username='test_name',
            password='test_pass'
        )
        result = use_case.handle(request, ['role2', 'role'])

        # asserts
        mock_whitelist.assert_not_called()
        mock_password_match.assert_called_with('test_pass', 'hash_pass')
        self.assertIsInstance(result, AuthResponse)
        self.assertEqual(result.message, 'ok')
        self.assertEqual(result.http_code, 200)
        self.assertIsInstance(result.tokens, AccessTokens)
        self.assertEqual(result.tokens.access_token, '__access_token')
        self.assertEqual(result.tokens.refresh_token, '__refresh_token')
        self.assertEqual(result.change_password, False)

    @patch(resolve_patch('config.WHITE_LIST_TOKEN'), False)
    @patch(resolve_patch('WhitelistToken'))
    @patch(resolve_patch('token_generate'))
    @patch(resolve_patch('password_match'))
    @patch(resolve_patch('UserRepository.find_one'))
    def test_ok_without_roles(
        self,
        mock_user_find,
        mock_password_match,
        mock_token_generate,
        mock_whitelist
    ):
        # Mocks
        uuids = {
            'uuid_access': 'abc123',
            'uuid_refresh': 'abc456'
        }
        tokens = AccessTokens(
            token_type='Bearer',
            access_token='__access_token',
            refresh_token='__refresh_token',
            expires_in=10
        )
        user = Mock(
            password='hash_pass',
            change_password=False
        )
        user.role.name = 'role'
        mock_user_find.return_value = user
        mock_password_match.return_value = True
        mock_token_generate.return_value = tokens, uuids

        # Exec
        use_case = Login()
        request = dict(
            username='test_name',
            password='test_pass'
        )
        result = use_case.handle(request)

        # asserts
        mock_whitelist.assert_not_called()
        mock_password_match.assert_called_with('test_pass', 'hash_pass')
        self.assertIsInstance(result, AuthResponse)
        self.assertEqual(result.message, 'ok')
        self.assertEqual(result.http_code, 200)
        self.assertIsInstance(result.tokens, AccessTokens)
        self.assertEqual(result.tokens.access_token, '__access_token')
        self.assertEqual(result.tokens.refresh_token, '__refresh_token')
        self.assertEqual(result.change_password, False)


class TestLogout(TestCase):

    @patch(resolve_patch('token_decode'))
    @patch(resolve_patch('WhitelistTokenRepository.find_one'))
    def test_ok(self, mock_find, mock_decode):
        # Mocks
        mock_token = Mock()
        mock_token.delete.return_value = True
        mock_find.return_value = mock_token
        mock_result = Mock(
            user_id='user1',
            uuid='u123'
        )
        mock_decode.return_value = mock_result

        use_case = Logout()
        result = use_case.handle('a_token')

        # Asserts
        self.assertIsInstance(result, Response)
        self.assertEqual(result.http_code, 200)
        self.assertEqual(result.message, 'ok')
        mock_find.assert_called_with(uuid_access='u123')
        mock_token.delete.assert_called_with()


class TestRefreshToken(TestCase):

    def test_request_not_valid(self):
        # Exec
        use_case = RefreshToken()
        result = use_case.handle({'key': 'value'})

        # Asserts
        self.assertIsInstance(result, AuthResponse)
        self.assertEqual(result.message, 'bad_request')
        self.assertEqual(result.http_code, 400)
        self.assertEqual(result.errors, {
            'key': ['unknown field'],
            'refresh_token': ['required field']
        })

    def test_payload_error(self):
        # Exec
        use_case = RefreshToken()
        result = use_case.handle({
            'refresh_token': 'a_refresh_token'
        })

        # Asserts
        self.assertIsInstance(result, AuthResponse)
        self.assertEqual(result.message, 'invalid_token')
        self.assertEqual(result.http_code, 401)

    @patch(resolve_patch('current_user'))
    @patch(resolve_patch('refresh_token_decode'))
    @patch(resolve_patch('WhitelistTokenRepository.find_one'))
    def test_refresh_token_not_saved(
        self,
        mock_find,
        mock_decode,
        mock_current_user
    ):
        # Mocks
        mock_decode.return_value = Mock(
            uuid='u123',
            error=None
        )
        mock_find.return_value = None
        mock_current_user.return_value = User(
            id='5e6a9440a3d71505cc416ed6'
        )

        # Exec
        use_case = RefreshToken()
        result = use_case.handle({
            'refresh_token': 'a_refresh_token'
        })

        # Asserts
        self.assertIsInstance(result, AuthResponse)
        self.assertEqual(result.message, 'unauthorized')
        self.assertEqual(result.http_code, 401)
        mock_find.assert_called_with(uuid_refresh='u123')
        mock_decode.assert_called_with('a_refresh_token')

    @patch(resolve_patch('current_user'))
    @patch(resolve_patch('refresh_token_decode'))
    @patch(resolve_patch('WhitelistTokenRepository.find_one'))
    def test_current_user_not_is_user_refresh_token(
        self,
        mock_find,
        mock_decode,
        mock_current_user
    ):
        # Mocks
        mock_decode.return_value = Mock(
            uuid='u123',
            error=None
        )
        mock_find.return_value = WhitelistToken(
            user=User(
                id='5e6a93b924beeae45a431af3'
            )
        )
        mock_current_user.return_value = User(
            id='5e6a9440a3d71505cc416ed6'
        )

        # Exec
        use_case = RefreshToken()
        result = use_case.handle({
            'refresh_token': 'a_refresh_token'
        })

        # Asserts
        self.assertIsInstance(result, AuthResponse)
        self.assertEqual(result.message, 'unauthorized')
        self.assertEqual(result.http_code, 401)
        mock_current_user.assert_called_with()

    @patch(resolve_patch('WhitelistToken'))
    @patch(resolve_patch('token_generate'))
    @patch(resolve_patch('current_user'))
    @patch(resolve_patch('refresh_token_decode'))
    @patch(resolve_patch('WhitelistTokenRepository.find_one'))
    def test_ok(
        self,
        mock_find,
        mock_decode,
        mock_current_user,
        mock_token_generate,
        mock_whitelist
    ):
        # Mocks
        mock_decode.return_value = Mock(
            uuid='u123',
            error=None
        )
        user = User(
            id='5e6a93b924beeae45a431af3'
        )
        mock_find.return_value = WhitelistToken(
            user=user
        )
        mock_current_user.return_value = user
        uuids = {
            'uuid_access': 'abc123',
            'uuid_refresh': 'abc456'
        }
        tokens = AccessTokens(
            token_type='Bearer',
            access_token='__access_token',
            refresh_token='__refresh_token',
            expires_in=10
        )
        mock_token_generate.return_value = tokens, uuids

        # Exec
        use_case = RefreshToken()
        result = use_case.handle({
            'refresh_token': 'a_refresh_token'
        })

        # Asserts
        self.assertIsInstance(result, AuthResponse)
        self.assertEqual(result.message, 'ok')
        self.assertEqual(result.http_code, 200)
        self.assertIsInstance(result.tokens, AccessTokens)
        self.assertEqual(result.tokens.access_token, '__access_token')
        self.assertEqual(result.tokens.refresh_token, '__refresh_token')
        mock_whitelist.assert_called_with(
            uuid_access='abc123',
            uuid_refresh='abc456',
            user=user
        )
