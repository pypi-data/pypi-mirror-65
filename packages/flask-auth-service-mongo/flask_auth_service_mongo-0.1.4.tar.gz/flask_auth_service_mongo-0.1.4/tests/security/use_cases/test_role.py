from unittest import TestCase
from unittest.mock import patch
from flask_auth_service_mongo.security.models import Role
from flask_auth_service_mongo.security.use_cases import (
    NewRole,
    SaveRoleResponse
)


def resolve_patch(path: str) -> str:
    return f'flask_auth_service_mongo.security.use_cases.role.{path}'


class TestNew(TestCase):

    __request = dict(
        name='a_name',
        permissions={'a': 'b'}
    )

    def test__request_not_valid(self):
        use_case = NewRole()
        request = dict(
            key='value'
        )
        result = use_case.handle(request)

        self.assertIsInstance(result, SaveRoleResponse)
        self.assertEqual(result.message, 'bad_request')
        self.assertEqual(result.http_code, 400)

    @patch(resolve_patch('RoleRepository.find_one'))
    def test_role_exists(self, mock_role):

        use_case = NewRole()
        result = use_case.handle(self.__request)

        self.assertIsInstance(result, SaveRoleResponse)
        self.assertEqual(result.message, 'existing_resource')
        self.assertEqual(result.http_code, 400)

    @patch(resolve_patch('Role.save'))
    @patch(resolve_patch('RoleRepository.find_one'))
    def test_role_save(self, mock_find, mock_role_save):
        # Mocks
        mock_find.return_value = None

        use_case = NewRole()
        result = use_case.handle(self.__request)

        self.assertIsInstance(result, SaveRoleResponse)
        self.assertEqual(result.message, 'created')
        self.assertEqual(result.http_code, 201)
        self.assertIsInstance(result.role, Role)
