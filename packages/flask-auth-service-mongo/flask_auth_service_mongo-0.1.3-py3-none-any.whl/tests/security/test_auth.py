from unittest import TestCase
from unittest.mock import patch, Mock
from flask import Flask
from flask_auth_service_mongo.security.models import User
from flask_auth_service_mongo.security.utils import Payload
from flask_auth_service_mongo.security.auth import (
    required,
    current_user,
    set_current_user
)


def resolve_patch(path: str) -> str:
    return 'flask_auth_service_mongo.security.auth.{}'.format(path)


class TestCurrentUser(TestCase):
    def test_user(self):
        # Crea el contexto del app flask
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'not-secret'

        with app.app_context():
            user = current_user()
            self.assertIsNone(user)

            param = User()
            set_current_user(param)
            user = current_user()
            self.assertEqual(user, param)


class TestRequired(TestCase):

    @required('test')
    def with_required(self):
        """funcion que usa el decorador a probar"""
        return {'message': 'ok'}, 200

    @required(['test', 'other'])
    def with_required_roles(self):
        """funcion que usa el decorador a probar"""
        return {'message': 'ok'}, 200

    @required(['test', 'other'], True)
    def with_require_password_change(self):
        """funcion que usa el decorador a probar"""
        return {'message': 'ok'}, 200

    @patch(resolve_patch('decorators.request'))
    def test_header_without_authorization(self, mock_request):
        """# header sin "Authorization"""
        # mock request.header
        mock_request.headers.get = Mock(return_value=None)

        result = self.with_required()

        # Prueba header que se esta usando para obtener el token
        args, kwargs = mock_request.headers.get.call_args
        self.assertEqual(args, ('Authorization',))
        self.assertEqual(kwargs, {})

        self.assertEqual(result, ({'message': 'unauthorized'}, 401))

    @patch(resolve_patch('decorators.request'))
    def test_error_token_type(self, mock_request):
        """# Tipo de "Authorization" no valido"""
        # mock request.header
        mock_request.headers.get = Mock(return_value='BearerXD abc')

        result = self.with_required()

        self.assertEqual(result, ({'message': 'unauthorized'}, 401))

    @patch(resolve_patch('decorators.token_decode'))
    @patch(resolve_patch('decorators.request'))
    def test_error_token(self, mock_request, mock_token_decode):
        """# Error de token"""
        payload = Payload(error='error')
        # mocks
        mock_request.headers.get = Mock(return_value='Bearer abc')
        mock_token_decode.return_value = payload

        result = self.with_required()

        # Prueba header que se esta usando para obtener el token
        args, kwargs = mock_token_decode.call_args
        self.assertEqual(args, ('abc',))
        self.assertEqual(kwargs, {})

        self.assertEqual(result, ({'message': 'error'}, 401))

    @patch(resolve_patch('decorators.WhitelistTokenRepository.find_one'))
    @patch(resolve_patch('decorators.token_decode'))
    @patch(resolve_patch('decorators.request'))
    def test_token_in_whitelist_nod_found(
        self,
        mock_request,
        mock_token_decode,
        mock_whitelist_find
    ):
        """# Token no esta en WhitelistToken"""
        payload = Payload(user_id='a1', _uuid='U123')

        # mocks
        mock_request.headers.get = Mock(return_value='Bearer abc')
        mock_token_decode.return_value = payload
        mock_whitelist_find.return_value = None

        result = self.with_required()

        mock_whitelist_find.assert_called_with(uuid_access='U123')
        self.assertEqual(result, ({'message': 'unauthorized'}, 401))

    @patch(resolve_patch('decorators.UserRepository.find'))
    @patch(resolve_patch('decorators.WhitelistTokenRepository.find_one'))
    @patch(resolve_patch('decorators.token_decode'))
    @patch(resolve_patch('decorators.request'))
    def test_user_not_found(
        self,
        mock_request,
        mock_token_decode,
        mock_whitelist_find,
        mock_user_find
    ):
        """# Usuario no encontrado"""
        payload = Payload(user_id='a1')

        # mocks
        mock_request.headers.get = Mock(return_value='Bearer abc')
        mock_token_decode.return_value = payload
        mock_user_find.return_value = None
        mock_whitelist_find.return_value = Mock()

        result = self.with_required()

        self.assertEqual(result, ({'message': 'unauthorized'}, 401))

    @patch(resolve_patch('decorators.WhitelistTokenRepository.find_one'))
    @patch(resolve_patch('decorators.UserRepository.find'))
    @patch(resolve_patch('decorators.token_decode'))
    @patch(resolve_patch('decorators.request'))
    def test_error_role(
        self,
        mock_request,
        mock_token_decode,
        mock_user_find,
        mock_whitelist_find
    ):
        payload = Payload(user_id='a1')

        # mocks
        mock_request.headers.get = Mock(return_value='Bearer abc')
        mock_token_decode.return_value = payload
        user = Mock()
        user.role.name = 'other_role'
        mock_user_find.return_value = user
        mock_whitelist_find.return_value = Mock()

        result = self.with_required()

        self.assertEqual(result, ({'message': 'unauthorized'}, 401))

    @patch(resolve_patch('decorators.WhitelistTokenRepository.find_one'))
    @patch(resolve_patch('decorators.UserRepository.find'))
    @patch(resolve_patch('decorators.token_decode'))
    @patch(resolve_patch('decorators.request'))
    def test_error_roles(
        self,
        mock_request,
        mock_token_decode,
        mock_user_find,
        mock_whitelist_find
    ):
        payload = Payload(user_id='a1')

        # mocks
        mock_request.headers.get = Mock(return_value='Bearer abc')
        mock_token_decode.return_value = payload
        user = Mock()
        user.role.name = 'other_role'
        mock_user_find.return_value = user
        mock_whitelist_find.return_value = Mock()

        result = self.with_required_roles()

        self.assertEqual(result, ({'message': 'unauthorized'}, 401))

    @patch(resolve_patch('decorators.WhitelistTokenRepository.find_one'))
    @patch(resolve_patch('decorators.UserRepository.find'))
    @patch(resolve_patch('decorators.token_decode'))
    @patch(resolve_patch('decorators.request'))
    def test_error_password_change_required(
        self,
        mock_request,
        mock_token_decode,
        mock_user_find,
        mock_whitelist_find
    ):
        payload = Payload(user_id='a1')

        # mocks
        mock_request.headers.get = Mock(return_value='Bearer abc')
        mock_token_decode.return_value = payload
        user = Mock(change_password=True)
        user.role.name = 'test'
        mock_user_find.return_value = user
        mock_whitelist_find.return_value = Mock()

        result = self.with_require_password_change()

        self.assertEqual(
            result,
            ({'message': 'password_change_required'}, 401)
        )

    @patch(resolve_patch('decorators.WhitelistTokenRepository.find_one'))
    @patch(resolve_patch('decorators.set_current_user'))
    @patch(resolve_patch('decorators.UserRepository.find'))
    @patch(resolve_patch('decorators.token_decode'))
    @patch(resolve_patch('decorators.request'))
    def test_ok(
        self,
        mock_request,
        mock_token_decode,
        mock_user_find,
        mock_set_current_user,
        mock_whitelist_find
    ):
        """# Usuario no encontrado"""
        payload = Payload(user_id='a1')

        # mocks
        mock_request.headers.get = Mock(return_value='Bearer abc')
        mock_token_decode.return_value = payload
        user = Mock()
        user.role = Mock()
        user.role.name = 'test'
        mock_user_find.return_value = user
        mock_whitelist_find.return_value = Mock()

        result = self.with_required()

        # Prueba que se ejecute la funcion decorada
        self.assertEqual(result, ({'message': 'ok'}, 200))

        # Prueba que se haga el set_current_user
        args, kwargs = mock_set_current_user.call_args
        self.assertEqual(args, (user,))
        self.assertEqual(kwargs, {})

    @patch(resolve_patch('decorators.WhitelistTokenRepository.find_one'))
    @patch(resolve_patch('decorators.set_current_user'))
    @patch(resolve_patch('decorators.UserRepository.find'))
    @patch(resolve_patch('decorators.token_decode'))
    @patch(resolve_patch('decorators.request'))
    def test_ok_multi_roles(
        self,
        mock_request,
        mock_token_decode,
        mock_user_find,
        mock_set_current_user,
        mock_whitelist_find
    ):
        """# Usuario no encontrado"""
        payload = Payload(user_id='a1')

        # mocks
        mock_request.headers.get = Mock(return_value='Bearer abc')
        mock_token_decode.return_value = payload
        user = Mock()
        user.role = Mock()
        user.role.name = 'test'
        mock_user_find.return_value = user
        mock_whitelist_find.return_value = Mock()

        result = self.with_required_roles()

        # Prueba que se ejecute la funcion decorada
        self.assertEqual(result, ({'message': 'ok'}, 200))

        # Prueba que se haga el set_current_user
        args, kwargs = mock_set_current_user.call_args
        self.assertEqual(args, (user,))
        self.assertEqual(kwargs, {})

    @patch(resolve_patch('decorators.WhitelistTokenRepository.find_one'))
    @patch(resolve_patch('decorators.set_current_user'))
    @patch(resolve_patch('decorators.UserRepository.find'))
    @patch(resolve_patch('decorators.token_decode'))
    @patch(resolve_patch('decorators.request'))
    def test_ok_without_role(
        self,
        mock_request,
        mock_token_decode,
        mock_user_find,
        mock_set_current_user,
        mock_whitelist_find
    ):
        """# Usuario no encontrado"""
        payload = Payload(user_id='a1')

        # mocks
        mock_request.headers.get = Mock(return_value='Bearer abc')
        mock_token_decode.return_value = payload
        user = Mock()
        mock_user_find.return_value = user
        mock_whitelist_find.return_value = Mock()

        @required()  # Sin role
        def with_required():
            """funcion que usa el decorador a probar"""
            return {'message': 'created'}, 201

        result = with_required()

        # Prueba que se ejecute la funcion decorada
        self.assertEqual(result, ({'message': 'created'}, 201))

        # Prueba que se haga el set_current_user
        args, kwargs = mock_set_current_user.call_args
        self.assertEqual(args, (user,))
        self.assertEqual(kwargs, {})
