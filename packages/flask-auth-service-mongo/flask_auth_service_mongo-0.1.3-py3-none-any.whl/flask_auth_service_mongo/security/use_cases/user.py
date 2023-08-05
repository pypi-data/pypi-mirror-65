import string
import random
from ... import config
from ...constants import responses
from ...constants.enums import HttpCode
from ...utils.use_case import Response, UseCaseInterface
from ...utils.validator import Validator
from ..utils import password_hash, password_match
from ..models import User
from ..repository import UserRepository, RoleRepository


class ResetPasswordResponse(Response):
    """Response from use case resetPassword

    Attributes:
        password (str)
        http_code (int)
        message (str)
        errors (list)
    """
    def __init__(
        self,
        password: str = None,
        *args,
        **kwargs
    ):
        self.password = password

        super().__init__(*args, **kwargs)


class SaveUserResponse(Response):
    """Respuesta para los casos de uso new y update user

    Attributes:
        user (User)
        http_code (int)
        message (str)
        errors (list)
    """
    def __init__(self, user: User = None, *args, **kwargs):
        self.user = user

        super(SaveUserResponse, self).__init__(*args, **kwargs)


class CreateUser(UseCaseInterface):
    """Crea usuario"""

    def handle(self, request: dict) -> SaveUserResponse:
        """
        Args:
            request (dict): Ejemplo:
                ::
                    {
                        'role': 'role_name',
                        'username': 'username',
                        'password': 'pass',
                        'password_confirmed': 'pass',
                        'identifier': '123' (Optional)
                    }
        Returns:
            SaveUserResponse:
        """
        self._request = request

        valid, response = self._validate()
        if not valid:
            return response

        try:
            self._create_user()
            response = SaveUserResponse(
                message=responses.CREATED,
                http_code=HttpCode.CREATED,
                user=self._user
            )
        except Exception:
            response = SaveUserResponse(
                message=responses.INTERNAL_SERVER_ERROR,
                http_code=HttpCode.INTERNAL_SERVER_ERROR
            )

        return response

    def _validate(self) -> (bool, SaveUserResponse):
        """Validaciones

        Returns:
            (bool, SaveUserResponse): (True, None): Request valido.
            (False, SaveUserResponse) Request no valido.
        """
        valid, errors = self.__request_is_valid()
        if not valid:
            return False, SaveUserResponse(
                message=responses.BAD_REQUEST,
                http_code=HttpCode.BAD_REQUEST,
                errors=errors
            )
        self._username = self._request['username'].lower()

        if (self._request.get('password') !=
                self._request.get('password_confirmed')):
            return False, SaveUserResponse(
                message="Passwords don't match",
                http_code=HttpCode.NOT_ACCEPTABLE
            )

        self._role = RoleRepository.find_one(name=self._request['role'])
        if not self._role:
            return False, SaveUserResponse(
                message="Role does not exist",
                http_code=HttpCode.NOT_ACCEPTABLE
            )

        user = UserRepository.find_one(username=self._username)
        if user:
            return False, SaveUserResponse(
                message="Username already exists",
                http_code=HttpCode.NOT_ACCEPTABLE
            )

        return True, None

    def _create_user(self):
        """ Crea User """
        self._user = User(
            username=self._username,
            password=password_hash(self._request['password']),
            role=self._role
        )

        self._user.save()

    def __request_is_valid(self) -> (bool, dict):
        """ El request debe cumplir con la estructura,
        no debe tener keys adicionales

        Returns:
            (bool, dict): (is_valid, errors)
        """
        v = Validator()
        v.schema = {
            "role": {
                "type": "string",
                "required": True,
            },
            "username": {
                "type": "string",
                "minlength": int(config.USERNAME_MIN_LENGTH),
                "required": True,
                "no_spaces": True
            },
            "password": {
                "type": "string",
                "minlength": int(config.PASSWORD_MIN_LENGTH),
                "required": True,
                "no_spaces": True
            },
            "password_confirmed": {
                "type": "string",
                "required": True,
                "no_spaces": True
            }
        }

        valid = v.validate(self._request)
        return valid, v.errors


class EditPasswordUser(UseCaseInterface):
    """Editar contraseña del usuario"""

    def handle(self, request: dict) -> SaveUserResponse:
        """
        Args:
            request (dict): Ejemplo:
                ::
                    {
                        'id': '5e404653d1c098c5177cc69d',
                        'current_password': 'pass',
                        'password': 'new_pass',
                        'password_confirmed': 'new_pass'
                    }

        Returns:
            SaveUserResponse:
        """
        self._request = request
        self._user = None

        valid, response = self._validate()
        if not valid:
            return response

        try:
            self._edit()
            response = SaveUserResponse(
                message=responses.OK,
                http_code=HttpCode.OK,
                user=self._user
            )
        except Exception:
            response = SaveUserResponse(
                message=responses.INTERNAL_SERVER_ERROR,
                http_code=HttpCode.INTERNAL_SERVER_ERROR
            )

        return response

    def _edit(self) -> None:
        """Edita la contraseña del usuario con los datos del request"""
        self._user.password = password_hash(self._request['new_password'])
        self._user.change_password = False
        self._user.save()

    def _validate(self) -> (bool, SaveUserResponse):
        """Validaciones

        Returns:
            (bool, SaveUserResponse): (True, None) = Si es válido
                (False, obj) = No es válido
        """
        valid, errors = self.__request_is_valid()
        if not valid:
            return False, SaveUserResponse(
                message=responses.BAD_REQUEST,
                http_code=HttpCode.BAD_REQUEST,
                errors=errors
            )

        if (self._request.get('new_password') !=
                self._request.get('password_confirmed')):
            return False, SaveUserResponse(
                message="Passwords don't match",
                http_code=HttpCode.BAD_REQUEST
            )

        self._user = UserRepository.find(self._request['id'])
        if not self._user:
            return False, SaveUserResponse(
                message=responses.NOT_FOUND,
                http_code=HttpCode.NOT_FOUND
            )

        if not password_match(
            self._request['current_password'],
            self._user.password
        ):
            return False, SaveUserResponse(
                message="Current password don't match",
                http_code=HttpCode.BAD_REQUEST
            )

        if (self._request.get('current_password') ==
                self._request.get('new_password')):
            return False, SaveUserResponse(
                message="The new password is equal as the current password",
                http_code=HttpCode.BAD_REQUEST
            )

        return True, None

    def __request_is_valid(self) -> (bool, dict):
        """ El request debe cumplir con la estructura,
        no debe tener keys adicionales

        Returns:
            (bool, dict): (is_valid, errors)
        """
        v = Validator()
        v.schema = {
            "id": {
                'type': 'string',
                'required': True,
                'mongo_id': True
            },
            "current_password": {
                "type": "string",
                "required": True
            },
            "new_password": {
                "type": "string",
                "minlength": int(config.PASSWORD_MIN_LENGTH),
                "required": True,
                "no_spaces": True
            },
            "password_confirmed": {
                "type": "string",
                "required": True
            }
        }

        valid = v.validate(self._request)
        return valid, v.errors


class DeleteUser(UseCaseInterface):
    """Elimina usuario"""

    def handle(self, request: dict) -> Response:
        """
        Args:
            request (dict): Ejemplo:
                ::
                    {
                        'id': '5e404653d1c098c5177cc69d'
                    }

        Returns:
            Response:
        """
        self._request = request
        self._user = None

        valid, response = self._validate()
        if not valid:
            return response

        try:
            self._user.delete()
            response = Response(
                message=responses.OK,
                http_code=HttpCode.OK
            )
        except Exception:
            response = Response(
                message=responses.INTERNAL_SERVER_ERROR,
                http_code=HttpCode.INTERNAL_SERVER_ERROR
            )

        return response

    def _validate(self) -> (bool, SaveUserResponse):
        """Validaciones

        Returns:
            (bool, SaveUserResponse): (True, None) = Si es válido
            (False, obj) = No es válido
        """
        valid, errors = self.__request_is_valid()
        if not valid:
            return False, SaveUserResponse(
                message=responses.BAD_REQUEST,
                http_code=HttpCode.BAD_REQUEST,
                errors=errors
            )

        self._user = UserRepository.find(self._request['id'])
        if not self._user:
            return False, SaveUserResponse(
                message=responses.NOT_FOUND,
                http_code=HttpCode.NOT_FOUND
            )

        return True, None

    def __request_is_valid(self) -> (bool, dict):
        """ El request debe cumplir con la estructura,
        no debe tener keys adicionales

        Returns:
            (bool, dict): (is_valid, errors)
        """
        v = Validator()
        v.schema = {
            "id": {
                'type': 'string',
                'required': True,
                'mongo_id': True
            }
        }

        valid = v.validate(self._request)
        return valid, v.errors


class EditUser(UseCaseInterface):

    def handle(self, request: dict) -> SaveUserResponse:
        """
        Args:
            request (dict): Example:
                ::
                    {
                        'id': '5e404653d1c098c5177cc69d',
                        'change_password': True
                    }

        Returns:
            SaveUserResponse:
        """
        self.__request = request
        self.__user = None

        valid, response = self.__validate()
        if not valid:
            return response

        self.__edit()

        return SaveUserResponse(
            message=responses.OK,
            http_code=HttpCode.OK,
            user=self.__user
        )

    def __edit(self) -> None:
        """Edit change_password field with request data"""
        self.__user.change_password = self.__request['change_password']
        self.__user.save()

    def __validate(self) -> (bool, SaveUserResponse):
        """Validations

        Returns:
            (bool, SaveUserResponse): (True, None) = Si es válido
            (False, obj) = No es válido
        """
        valid, errors = self.__request_is_valid()
        if not valid:
            return False, SaveUserResponse(
                message=responses.BAD_REQUEST,
                http_code=HttpCode.BAD_REQUEST,
                errors=errors
            )

        self.__user = UserRepository.find(self.__request['id'])
        if not self.__user:
            return False, SaveUserResponse(
                message=responses.NOT_FOUND,
                http_code=HttpCode.NOT_FOUND
            )

        return True, None

    def __request_is_valid(self) -> (bool, dict):
        """Request must have the structure,
        it must not have additional keys

        Returns:
            (bool, dict): (is_valid, errors)
        """
        v = Validator()
        v.schema = {
            "id": {
                "type": "string",
                "required": True,
                "mongo_id": True
            },
            "change_password": {
                "type": "boolean",
                "required": True
            }
        }

        valid = v.validate(self.__request)
        return valid, v.errors


class ResetPassword(UseCaseInterface):

    def handle(self, request) -> ResetPasswordResponse:
        """
        Args:
            role (str)
            request (dict): Example:
                ::
                    {
                        'id': '5e404653d1c098c5177cc69d'
                    }

        Returns:
            ResetPasswordResponse:
        """
        self.__request = request
        valid, response = self.__validate()
        if not valid:
            return response

        self.__edit_password()
        return ResetPasswordResponse(
            message=responses.OK,
            http_code=HttpCode.OK,
            password=self.__password
        )

    def __edit_password(self) -> None:
        """Update user password

        Attributes:
            __password (str): password generated
        """
        self.__password = self.__random_pass()
        self.__user.password = password_hash(
            self.__password
        )
        self.__user.change_password = True
        self.__user.save()

    def __random_pass(self) -> str:
        """Password Generator

        Returns:
            (str): Password generated
        """
        length = config.RESET_PASSWORD_LEN_GENERATOR
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))  # nosec

    def __validate(self) -> (bool, ResetPasswordResponse):
        """Execution of validators

        Attributes:
            __user (User):

        Returns:
            (bool, ResetPasswordResponse):
        """
        valid, errors = self.__request_is_valid()
        if not valid:
            return False, ResetPasswordResponse(
                message=responses.BAD_REQUEST,
                http_code=HttpCode.BAD_REQUEST,
                errors=errors
            )

        self.__user = UserRepository.find(self.__request['id'])
        if not self.__user:
            return False, ResetPasswordResponse(
                message=responses.NOT_FOUND,
                http_code=HttpCode.NOT_FOUND,
            )

        return True, None

    def __request_is_valid(self) -> (bool, dict):
        """The order must comply with the structure,
        must not have additional keys

        Returns:
            (bool, dict): (is_valid, errors)
        """
        v = Validator()
        v.schema = {
            'id': {
                'type': 'string',
                'required': True,
                'mongo_id': True
            }
        }
        valid = v.validate(self.__request)

        return valid, v.errors
