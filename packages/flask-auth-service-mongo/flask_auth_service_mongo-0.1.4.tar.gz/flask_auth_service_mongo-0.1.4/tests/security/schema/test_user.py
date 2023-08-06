import json
import graphene
from unittest import TestCase
from unittest.mock import patch, Mock
from flask_auth_service_mongo.security.schema import (
    UpdatePassword,
    UpdateUser,
    ResetPassword,
)
from flask_auth_service_mongo.security.models import User


def resolve_patch(patch: str) -> str:
    return 'flask_auth_service_mongo.security.schema.user.{}'.format(patch)


class Mutation(graphene.ObjectType):
    updatePassword = UpdatePassword.Field()
    updateUser = UpdateUser.Field()
    resetPassword = ResetPassword.Field()


class TestMutationUpdatePassword(TestCase):

    __query = '''
        mutation {
            updatePassword (input: {
                currentPassword: "currentPass"
                newPassword: "newPass"
                passwordConfirmed: "newPass"
            }) {
                ok
            }
        }
    '''

    @patch(resolve_patch('EditPasswordUser'))
    @patch(resolve_patch('auth.current_user'))
    def test_error(self, mock_auth, mock_use_case):
        # Mocks
        mock_auth.return_value = Mock(id='abc123')
        mock_handle = Mock()
        mock_handle.handle.return_value = Mock(
            http_code=400,
            message='error'
        )
        mock_use_case.return_value = mock_handle

        # Execution
        schema = graphene.Schema(mutation=Mutation)
        result = schema.execute(self.__query)

        # Asserts
        self.assertIsNotNone(result.errors)
        self.assertEqual(
            json.dumps(result.data),
            '''{"updatePassword": null}'''
        )
        mock_handle.handle.assert_called_with({
            'current_password': 'currentPass',
            'new_password': 'newPass',
            'password_confirmed': 'newPass',
            'id': 'abc123'
        })

    @patch(resolve_patch('EditPasswordUser'))
    @patch(resolve_patch('auth.current_user'))
    def test_ok(self, mock_auth, mock_use_case):
        # Mocks
        mock_auth.return_value = Mock(id='abc123')
        mock_handle = Mock()
        mock_handle.handle.return_value = Mock(
            http_code=200
        )
        mock_use_case.return_value = mock_handle

        # Execution
        schema = graphene.Schema(mutation=Mutation)
        result = schema.execute(self.__query)

        # Asserts
        self.assertIsNone(result.errors)
        self.assertEqual(
            json.dumps(result.data),
            '''{"updatePassword": {"ok": true}}'''
        )


class TestMutationUpdateUser(TestCase):

    __query = '''
        mutation {
            updateUser (input: {
                id: "VXNlcjo1ZTY2NmZmYTYyMjUzZTgyZjVjYWVhNDE="
                changePassword: false
            }) {
                user {
                    username
                }
            }
        }
    '''

    @patch(resolve_patch('EditUserUseCase'))
    def test_error(self, mock_use_case):
        # Mocks
        mock_handle = Mock()
        mock_handle.handle.return_value = Mock(
            http_code=400,
            message='error'
        )
        mock_use_case.return_value = mock_handle

        # Execution
        schema = graphene.Schema(mutation=Mutation)
        result = schema.execute(self.__query)

        # Asserts
        self.assertIsNotNone(result.errors)
        self.assertEqual(
            json.dumps(result.data),
            '''{"updateUser": null}'''
        )
        mock_handle.handle.assert_called_with({
            'id': '5e666ffa62253e82f5caea41',
            'change_password': False
        })

    @patch(resolve_patch('EditUserUseCase'))
    def test_ok(self, mock_use_case):
        # Mocks
        mock_handle = Mock()
        mock_handle.handle.return_value = Mock(
            http_code=200,
            user=User(
                username='user_name'
            )
        )
        mock_use_case.return_value = mock_handle

        # Execution
        schema = graphene.Schema(mutation=Mutation)
        result = schema.execute(self.__query)

        # Asserts
        self.assertIsNone(result.errors)
        self.assertEqual(
            json.dumps(result.data),
            '''{"updateUser": {"user": {"username": "user_name"}}}'''
        )
        mock_handle.handle.assert_called_with({
            'id': '5e666ffa62253e82f5caea41',
            'change_password': False
        })


class TestMutationResetPassword(TestCase):
    __query = '''
        mutation {
            resetPassword (input: {
                id: "VXNlcjo1ZTY2NmZmYTYyMjUzZTgyZjVjYWVhNDE="
            }) {
                password
            }
        }
    '''

    @patch(resolve_patch('ResetPasswordUseCase'))
    def test_ok(self, mock_case):
        # mocks
        mock_result = Mock()
        mock_response = Mock(
            message='ok',
            http_code=200,
            password='qwer'
        )
        mock_result.handle.return_value = mock_response
        mock_case.return_value = mock_result
        # Execution
        schema = graphene.Schema(mutation=Mutation)
        result = schema.execute(self.__query)
        self.assertIsNone(result.errors)
        self.assertEqual(
            json.dumps(result.data),
            '''{"resetPassword": {"password": "qwer"}}'''
        )
        mock_result.handle.assert_called_with(
            {'id': '5e666ffa62253e82f5caea41'})

    @patch(resolve_patch('ResetPasswordUseCase'))
    def test_error(self, mock_case):
        # mocks
        mock_result = Mock()
        mock_response = Mock(
            message='not_found',
            http_code=404,
            password=None
        )
        mock_result.handle.return_value = mock_response
        mock_case.return_value = mock_result
        # Execution
        schema = graphene.Schema(mutation=Mutation)
        result = schema.execute(self.__query)

        self.assertIsNotNone(result.errors)
        self.assertEqual(
            json.dumps(result.data),
            '''{"resetPassword": null}'''
        )
        mock_result.handle.assert_called_with(
            {'id': '5e666ffa62253e82f5caea41'})
