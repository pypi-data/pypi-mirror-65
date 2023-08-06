from unittest import TestCase
from unittest.mock import patch
from flask_auth_service_mongo.security.repository import (
    RoleRepository,
    UserRepository,
    WhitelistTokenRepository
)


def resolve_patch(path: str) -> str:
    return 'flask_auth_service_mongo.security.repository.{}'.format(path)


class TestRoleRepository(TestCase):

    @patch(resolve_patch('Role.objects'))
    def test_find(self, mock_obj):
        # Mocks
        mock_obj.return_value.first.return_value = 'test'

        result = RoleRepository.find(id='abc123')

        # Asserts
        self.assertEqual(result, 'test')
        mock_obj.assert_called_with(id='abc123')

    @patch(resolve_patch('Role.objects'))
    def test_find_one(self, mock_obj):
        # Mocks
        mock_obj.return_value.first.return_value = 'test'

        result = RoleRepository.find_one(key='abc123', other=123)

        # Asserts
        self.assertEqual(result, 'test')
        mock_obj.assert_called_with(key='abc123', other=123)

    @patch(resolve_patch('Role.objects'))
    def test_find_all(self, mock_obj):
        # Mocks
        mock_obj.return_value = ['test']

        result = RoleRepository.find_all(key='abc123', other=123)

        # Asserts
        self.assertEqual(result, ['test'])
        mock_obj.assert_called_with(key='abc123', other=123)


class TestUserRepository(TestCase):

    @patch(resolve_patch('User.objects'))
    def test_find(self, mock_obj):
        # Mocks
        mock_obj.return_value.first.return_value = 'test'

        result = UserRepository.find(id='abc123')

        # Asserts
        self.assertEqual(result, 'test')
        mock_obj.assert_called_with(id='abc123')

    @patch(resolve_patch('User.objects'))
    def test_find_one(self, mock_obj):
        # Mocks
        mock_obj.return_value.first.return_value = 'test'

        result = UserRepository.find_one(key='abc123', other=123)

        # Asserts
        self.assertEqual(result, 'test')
        mock_obj.assert_called_with(key='abc123', other=123)

    @patch(resolve_patch('User.objects'))
    def test_find_all(self, mock_obj):
        # Mocks
        mock_obj.return_value = ['test']

        result = UserRepository.find_all(key='abc123', other=123)

        # Asserts
        self.assertEqual(result, ['test'])
        mock_obj.assert_called_with(key='abc123', other=123)


class TestWhitelistTokenRepository(TestCase):

    @patch(resolve_patch('WhitelistToken.objects'))
    def test_find(self, mock_obj):
        # Mocks
        mock_obj.return_value.first.return_value = 'test'

        result = WhitelistTokenRepository.find(id='abc123')

        # Asserts
        self.assertEqual(result, 'test')
        mock_obj.assert_called_with(id='abc123')

    @patch(resolve_patch('WhitelistToken.objects'))
    def test_find_one(self, mock_obj):
        # Mocks
        mock_obj.return_value.first.return_value = 'test'

        result = WhitelistTokenRepository.find_one(key='abc123', other=123)

        # Asserts
        self.assertEqual(result, 'test')
        mock_obj.assert_called_with(key='abc123', other=123)

    @patch(resolve_patch('WhitelistToken.objects'))
    def test_find_all(self, mock_obj):
        # Mocks
        mock_obj.return_value = ['test']

        result = WhitelistTokenRepository.find_all(key='abc123', other=123)

        # Asserts
        self.assertEqual(result, ['test'])
        mock_obj.assert_called_with(key='abc123', other=123)
