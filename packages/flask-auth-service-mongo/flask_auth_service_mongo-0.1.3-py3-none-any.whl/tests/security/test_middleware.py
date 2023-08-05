from unittest import TestCase
from unittest.mock import patch, Mock
from flask_auth_service_mongo.security.models import User, Role
from flask_auth_service_mongo.security.middlewares import MutationMiddleware


def resolve_patch(path: str) -> str:
    return f'flask_auth_service_mongo.security.middlewares.{path}'


class TestMutationMiddleware(TestCase):

    def middleware(self):
        return MutationMiddleware([
            {
                'mutation': 'login',
                'roles': ['is_anonymously']
            },
            {
                'mutation': 'logout',
                'roles': ['is_authenticated']
            },
            {
                'mutation': 'create_obj',
                'roles': ['custom_role']
            }
        ])

    def test_not_mutation(self):
        # Mocks
        mock_next = Mock(return_value='not_mutation')
        mock_info = Mock(
            operation=Mock(
                operation='other'
            )
        )

        # Exec
        middleware = self.middleware()
        result = middleware.resolve(mock_next, None, mock_info)

        # Asserts
        self.assertEqual(result, 'not_mutation')
        mock_next.assert_called_with(None, mock_info)

    def test_root_is_defined(self):
        # Mocks
        mock_next = Mock(return_value='root_is_defined')
        mock_info = Mock(
            operation=Mock(
                operation='mutation'
            )
        )

        # Exec
        middleware = self.middleware()
        result = middleware.resolve(mock_next, 'root', mock_info)

        # Asserts
        self.assertEqual(result, 'root_is_defined')
        mock_next.assert_called_with('root', mock_info)

    def test_access_control_nod_found(self):
        # Mocks
        mock_next = Mock(return_value='nod_found')
        mock_info = Mock(
            field_name='delete_obj',
            operation=Mock(
                operation='mutation'
            )
        )

        # Exec
        middleware = self.middleware()
        result = middleware.resolve(mock_next, None, mock_info)

        # Asserts
        self.assertEqual(result, 'nod_found')
        mock_next.assert_called_with(None, mock_info)

    @patch(resolve_patch('current_user'))
    def test_user_anonymously(self, mock_current_user):
        # Mocks
        mock_next = Mock(return_value='user_anonymously')
        mock_info = Mock(
            field_name='login',
            operation=Mock(
                operation='mutation'
            )
        )
        mock_current_user.return_value = None

        # Exec
        middleware = self.middleware()
        result = middleware.resolve(mock_next, None, mock_info)

        # Asserts
        self.assertEqual(result, 'user_anonymously')
        mock_next.assert_called_with(None, mock_info)

    @patch(resolve_patch('current_user'))
    def test_unauthorized(self, mock_current_user):
        # Mocks
        mock_next = Mock(return_value='unauthorized')
        mock_info = Mock(
            field_name='logout',
            operation=Mock(
                operation='mutation'
            )
        )
        mock_current_user.return_value = None

        # Exec
        middleware = self.middleware()
        result = middleware.resolve(mock_next, None, mock_info)

        # Asserts
        self.assertEqual(result, None)
        mock_next.assert_not_called()

    @patch(resolve_patch('current_user'))
    def test_is_authenticated(self, mock_current_user):
        # Mocks
        mock_next = Mock(return_value='is_authenticated')
        mock_info = Mock(
            field_name='logout',
            operation=Mock(
                operation='mutation'
            )
        )
        mock_current_user.return_value = User()

        # Exec
        middleware = self.middleware()
        result = middleware.resolve(mock_next, None, mock_info)

        # Asserts
        self.assertEqual(result, 'is_authenticated')
        mock_next.assert_called_with(None, mock_info)

    @patch(resolve_patch('current_user'))
    def test_role_not_valid(self, mock_current_user):
        # Mocks
        mock_next = Mock(return_value='role_not_valid')
        mock_info = Mock(
            field_name='create_obj',
            operation=Mock(
                operation='mutation'
            )
        )
        mock_current_user.return_value = User(
            role=Role(
                name='other_role'
            )
        )

        # Exec
        middleware = self.middleware()
        result = middleware.resolve(mock_next, None, mock_info)

        # Asserts
        self.assertEqual(result, None)
        mock_next.assert_not_called()

    @patch(resolve_patch('current_user'))
    def test_role_ok(self, mock_current_user):
        # Mocks
        mock_next = Mock(return_value='role_ok')
        mock_info = Mock(
            field_name='create_obj',
            operation=Mock(
                operation='mutation'
            )
        )
        mock_current_user.return_value = User(
            role=Role(
                name='custom_role'
            )
        )

        # Exec
        middleware = self.middleware()
        result = middleware.resolve(mock_next, None, mock_info)

        # Asserts
        self.assertEqual(result, 'role_ok')
        mock_next.assert_called_with(None, mock_info)
