from unittest import TestCase
from unittest.mock import patch, Mock
from flask_auth_service_mongo.security.use_cases import (
    CreateUser,
    SaveUserResponse,
    EditUser,
    EditPasswordUser,
    DeleteUser,
    ResetPassword,
    Response,
    ResetPasswordResponse
)
from flask_auth_service_mongo.security.models import User, Role


def resolve_patch(path: str) -> str:
    return 'flask_auth_service_mongo.security.use_cases.user.{}'.format(path)


class TestCreateUser(TestCase):

    def test_request_not_valid(self):
        use_case = CreateUser()
        result = use_case.handle({'key': 'value'})

        expected = {
            'key': ['unknown field'],
            'password': ['required field'],
            'password_confirmed': ['required field'],
            'role': ['required field'],
            'username': ['required field']
        }

        self.assertIsInstance(result, SaveUserResponse)
        self.assertEqual(result.message, 'bad_request')
        self.assertEqual(result.errors, expected)
        self.assertEqual(result.http_code, 400)

    def test_username_not_valid(self):
        use_case = CreateUser()
        request = {
            'username': '12',
            'password': '1234',
            'password_confirmed': '1234',
            'role': 'any'
        }
        result = use_case.handle(request)

        expected = {'username': [
            'min length is 3']
        }

        self.assertIsInstance(result, SaveUserResponse)
        self.assertEqual(result.message, 'bad_request')
        self.assertEqual(result.errors, expected)
        self.assertEqual(result.http_code, 400)

    def test_passwords_not_match(self):
        request = dict(
            username='str',
            role='str',
            password='pass',
            password_confirmed='1234'
        )
        use_case = CreateUser()
        result = use_case.handle(request)

        self.assertIsInstance(result, SaveUserResponse)
        self.assertEqual(result.message, "Passwords don't match")
        self.assertEqual(result.http_code, 406)

    @patch(resolve_patch('RoleRepository.find_one'))
    def test_rol_not_found(self, mock_role_find):
        # Mocks
        mock_role_find.return_value = None

        request = dict(
            username='str',
            role='notExists',
            password='pass',
            password_confirmed='pass'
        )
        use_case = CreateUser()
        result = use_case.handle(request)

        # asserts
        self.assertIsInstance(result, SaveUserResponse)
        self.assertEqual(result.message, "Role does not exist")
        self.assertEqual(result.http_code, 406)
        mock_role_find.assert_called_with(name='notExists')

    @patch(resolve_patch('UserRepository.find_one'))
    @patch(resolve_patch('RoleRepository.find_one'))
    def test_user_repeated(self, mock_role_find, mock_user_find):
        request = dict(
            username='exisTs',
            role='rol',
            password='pass',
            password_confirmed='pass'
        )
        use_case = CreateUser()
        result = use_case.handle(request)

        # asserts
        self.assertIsInstance(result, SaveUserResponse)
        self.assertEqual(result.message, "Username already exists")
        self.assertEqual(result.http_code, 406)
        mock_user_find.assert_called_with(username='exists')

    @patch(resolve_patch('User.save'))
    @patch(resolve_patch('UserRepository.find_one'))
    @patch(resolve_patch('RoleRepository.find_one'))
    def test_ok(self, mock_role_find, mock_user_find, mock_user_save):
        # Mocks
        mock_user_find.return_value = None
        mock_role_find.return_value = Role()

        request = dict(
            username='str',
            role='a role',
            password='pass',
            password_confirmed='pass'
        )
        use_case = CreateUser()
        result = use_case.handle(request)

        # asserts
        self.assertIsInstance(result, SaveUserResponse)
        self.assertEqual(result.message, "created")
        self.assertEqual(result.http_code, 201)
        self.assertIsInstance(result.user, User)
        mock_user_save.assert_called_with()

    @patch(resolve_patch('User.save'), *{
        'return_value.objects.side_effect': Exception()
    })
    @patch(resolve_patch('UserRepository.find_one'))
    @patch(resolve_patch('RoleRepository.find_one'))
    def test_except(self, mock_role_find, mock_user_find):
        # Mocks
        mock_user_find.return_value = None
        mock_role_find.return_value = Role()

        request = dict(
            username='str',
            role='aRole',
            password='pass',
            password_confirmed='pass'
        )
        use_case = CreateUser()
        result = use_case.handle(request)

        # asserts
        self.assertIsInstance(result, SaveUserResponse)
        self.assertEqual(result.message, "internal_server_error")
        self.assertEqual(result.http_code, 500)
        self.assertIsNone(result.user)


class TestEditPassword(TestCase):

    ID = '5e615cd4ec0af8597065055d'
    PASS = '$2b$12$umfFAKhJSKiB0jjP/a.yJeCdurFQNyWik3Cdg.ccLf4iJYD09zQ7e'

    def test_request_not_valid(self):
        use_case = EditPasswordUser()
        result = use_case.handle({'key': 'value'})

        self.assertIsInstance(result, SaveUserResponse)
        self.assertEqual(result.message, 'bad_request')
        self.assertEqual(result.http_code, 400)
        self.assertEqual(result.errors, {
            'key': ['unknown field'],
            'id': ['required field'],
            'current_password': ['required field'],
            'new_password': ['required field'],
            'password_confirmed': ['required field']
        })

    def test_passwords_not_valid(self):
        use_case = EditPasswordUser()
        # pass con espacios
        request = dict(
            id=self.ID,
            current_password='currentP',
            new_password=' d',
            password_confirmed='123'
        )
        result = use_case.handle(request=request)

        self.assertIsInstance(result, SaveUserResponse)
        self.assertEqual(result.message, 'bad_request')
        self.assertEqual(result.http_code, 400)
        self.assertEqual(result.errors, {
            'new_password': [
                'Must not contain spaces',
                'min length is 3'
            ]
        })

    def test_passwords_not_match(self):
        request = dict(
            id=self.ID,
            current_password='currentP',
            new_password='pass',
            password_confirmed='1234'
        )
        use_case = EditPasswordUser()
        result = use_case.handle(request=request)

        self.assertIsInstance(result, SaveUserResponse)
        self.assertEqual(result.message, "Passwords don't match")
        self.assertEqual(result.http_code, 400)

    @patch(resolve_patch('UserRepository.find'))
    def test_not_found(self, mock_user_find):
        # Mocks
        mock_user_find.return_value = None

        request = dict(
            id=self.ID,
            current_password='currentP',
            new_password='pass',
            password_confirmed='pass'
        )
        use_case = EditPasswordUser()
        result = use_case.handle(request=request)

        self.assertIsInstance(result, SaveUserResponse)
        self.assertEqual(result.message, 'not_found')
        self.assertEqual(result.http_code, 404)
        mock_user_find.assert_called_with(self.ID)

    @patch(resolve_patch('UserRepository.find'))
    def test_current_password_not_match(self, mock_user_find):
        # Mocks
        mock_user_find.return_value = User(
            password=self.PASS
        )

        request = dict(
            id=self.ID,
            current_password='otherPass',
            new_password='newPass',
            password_confirmed='newPass'
        )
        use_case = EditPasswordUser()
        result = use_case.handle(request=request)

        self.assertIsInstance(result, SaveUserResponse)
        self.assertEqual(result.message, "Current password don't match")
        self.assertEqual(result.http_code, 400)

    @patch(resolve_patch('UserRepository.find'))
    def test_new_password_is_current(self, mock_user_find):
        # Mocks
        mock_user_find.return_value = User(
            password=self.PASS
        )

        request = dict(
            id=self.ID,
            current_password='pass',
            new_password='pass',
            password_confirmed='pass'
        )
        use_case = EditPasswordUser()
        result = use_case.handle(request=request)

        self.assertIsInstance(result, SaveUserResponse)
        self.assertEqual(
            result.message,
            'The new password is equal as the current password'
        )
        self.assertEqual(result.http_code, 400)

    @patch(resolve_patch('User.save'))
    @patch(resolve_patch('UserRepository.find'))
    def test_ok(self, mock_user_find, mock_user_save):
        # Mocks
        user = User(
            password=self.PASS,
            change_password=True
        )
        mock_user_find.return_value = user

        request = dict(
            id=self.ID,
            current_password='pass',
            new_password='newPass',
            password_confirmed='newPass'
        )
        use_case = EditPasswordUser()
        result = use_case.handle(request=request)

        # asserts
        self.assertIsInstance(result, SaveUserResponse)
        self.assertEqual(result.message, "ok")
        self.assertEqual(result.http_code, 200)
        self.assertEqual(result.user, user)
        self.assertNotEqual(user.password, self.PASS)
        self.assertFalse(user.change_password)
        mock_user_save.assert_called_with()

    @patch(resolve_patch('User.save'), *{
        'return_value.objects.side_effect': Exception()
    })
    @patch(resolve_patch('UserRepository.find'))
    def test_except(self, mock_user_find):
        # Mocks
        mock_user_find.return_value = User(
            password=self.PASS
        )

        request = dict(
            id=self.ID,
            current_password='pass',
            new_password='newPass',
            password_confirmed='newPass'
        )
        use_case = EditPasswordUser()
        result = use_case.handle(request=request)

        # asserts
        self.assertIsInstance(result, SaveUserResponse)
        self.assertEqual(result.message, "internal_server_error")
        self.assertEqual(result.http_code, 500)
        self.assertIsNone(result.user)


class TestDeleteUser(TestCase):

    ID = '5e404653d1c098c5177cc69d'

    def test_request_not_valid(self):
        use_case = DeleteUser()
        result = use_case.handle({'key': 'value'})

        self.assertIsInstance(result, SaveUserResponse)
        self.assertEqual(result.message, 'bad_request')
        self.assertEqual(result.http_code, 400)
        self.assertEqual(result.errors, {
            'key': ['unknown field'],
            'id': ['required field']
        })

    @patch(resolve_patch('UserRepository.find'))
    def test_not_found(self, mock_user_find):
        # Mocks
        mock_user_find.return_value = None

        # Exec
        use_case = DeleteUser()
        result = use_case.handle({'id': self.ID})

        # Asserts
        self.assertIsInstance(result, Response)
        self.assertEqual(result.message, 'not_found')
        self.assertEqual(result.http_code, 404)
        mock_user_find.assert_called_with(self.ID)

    @patch(resolve_patch('User.delete'))
    @patch(resolve_patch('UserRepository.find'))
    def test_ok(self, mock_user_find, mock_user_delete):
        # Mocks
        mock_user_find.return_value = User()

        # Exec
        use_case = DeleteUser()
        result = use_case.handle({'id': self.ID})

        # asserts
        self.assertIsInstance(result, Response)
        self.assertEqual(result.message, "ok")
        self.assertEqual(result.http_code, 200)
        mock_user_delete.assert_called_with()

    @patch(resolve_patch('User.delete'), *{
        'return_value.objects.side_effect': Exception()
    })
    @patch(resolve_patch('UserRepository.find'))
    def test_except(self, mock_user_find):
        # Mocks
        mock_user_find.return_value = User()

        # Exec
        use_case = DeleteUser()
        result = use_case.handle({'id': self.ID})

        # asserts
        self.assertIsInstance(result, Response)
        self.assertEqual(result.message, "internal_server_error")
        self.assertEqual(result.http_code, 500)


class TestEditUser(TestCase):

    ID = '5e615cd4ec0af8597065055d'

    def test_request_not_valid(self):
        use_case = EditUser()
        result = use_case.handle({'key': 'value'})

        self.assertIsInstance(result, SaveUserResponse)
        self.assertEqual(result.message, 'bad_request')
        self.assertEqual(result.http_code, 400)
        self.assertEqual(result.errors, {
            'key': ['unknown field'],
            'id': ['required field'],
            'change_password': ['required field']
        })

    @patch(resolve_patch('UserRepository.find'))
    def test_not_found(self, mock_user_find):
        # Mocks
        mock_user_find.return_value = None

        request = dict(
            id=self.ID,
            change_password=True,
        )
        use_case = EditUser()
        result = use_case.handle(request=request)

        self.assertIsInstance(result, SaveUserResponse)
        self.assertEqual(result.message, 'not_found')
        self.assertEqual(result.http_code, 404)
        mock_user_find.assert_called_with(self.ID)

    @patch(resolve_patch('User.save'))
    @patch(resolve_patch('UserRepository.find'))
    def test_ok(self, mock_user_find, mock_user_save):
        # Mocks
        user = User(
            username='user',
            change_password=True
        )
        mock_user_find.return_value = user

        request = dict(
            id=self.ID,
            change_password=False,
        )
        use_case = EditUser()
        result = use_case.handle(request=request)

        # asserts
        self.assertIsInstance(result, SaveUserResponse)
        self.assertEqual(result.message, "ok")
        self.assertEqual(result.http_code, 200)
        self.assertEqual(result.user, user)
        self.assertFalse(user.change_password)
        mock_user_save.assert_called_with()


class TestResetPassword(TestCase):

    def test_bad_request(self):
        use_case = ResetPassword()
        result = use_case.handle({
            'key': 'value'
        })

        self.assertIsInstance(result, ResetPasswordResponse)
        self.assertEqual(result.message, 'bad_request')
        self.assertEqual(result.errors, {
            'id': ['required field'],
            'key': ['unknown field']
        })
        self.assertEqual(result.http_code, 400)

    @patch(resolve_patch('UserRepository.find'))
    def test_not_found(self, mock_repo):
        mock_repo.return_value = None

        use_case = ResetPassword()
        request = {'id': '5e404653d1c098c5177cc69d'}
        result = use_case.handle(request)

        self.assertIsInstance(result, ResetPasswordResponse)
        self.assertEqual(result.message, 'not_found')
        self.assertIsNone(result.errors)
        self.assertEqual(result.http_code, 404)

    @patch(resolve_patch('UserRepository.find'))
    def test_ok(self, mock_repo):
        mock_result = Mock()
        mock_result.return_value = User(
            password='something', change_password=False)
        mock_result.save.return_value = None
        mock_repo.return_value = mock_result

        use_case = ResetPassword()
        request = {'id': '5e404653d1c098c5177cc69d'}
        result = use_case.handle(request)

        self.assertIsInstance(result, ResetPasswordResponse)
        self.assertEqual(result.message, 'ok')
        self.assertIsNone(result.errors)
        self.assertEqual(result.http_code, 200)
        mock_result.save.assert_called_with()
        self.assertNotEqual(mock_result.password, 'something')
        self.assertEqual(mock_result.change_password, True)
