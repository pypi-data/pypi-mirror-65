from ... import config
from ...constants import responses
from ...constants.enums import HttpCode
from ...utils.use_case import Response, UseCaseInterface
from ...utils.validator import Validator
from ..auth import current_user
from ..utils import (
    password_match,
    token_generate,
    token_decode,
    refresh_token_decode,
    AccessTokens
)
from ..models import WhitelistToken
from ..repository import (
    UserRepository,
    WhitelistTokenRepository
)


__all__ = (
    'Login',
    'Logout',
    'RefreshToken',
    'AuthResponse',
)


class AuthResponse(Response):
    """Respuesta para los casos de uso de Auth

    Args:
        tokens (AccessTokens)
        change_password (bool): Indica si es necesario cambiar la contraseña
        http_code (int)
        message (str)
        errors (list)
    """
    def __init__(
        self,
        tokens: str = None,
        change_password: bool = None,
        *args,
        **kwargs
    ):
        self.tokens = tokens
        self.change_password = change_password

        super().__init__(*args, **kwargs)


class BaseAuth(UseCaseInterface):

    def _new_tokens(self, user) -> AccessTokens:
        """Crea un juego de tokens y lo registra en WhitelistToken

        Args:
            user (User)

        Returns:
            AccessTokens:
        """
        tokens, uuids = token_generate(user)

        if config.WHITE_LIST_TOKEN:
            WhitelistToken(
                uuid_access=uuids['uuid_access'],
                uuid_refresh=uuids['uuid_refresh'],
                user=user
            ).save()

        return tokens


class Login(BaseAuth):

    def handle(self, request: dict, role=None) -> AuthResponse:
        """
        Args:
            request (dict) Ejemplo:
                ::
                    {
                        'username': 'username',
                        'password': 'password'
                    }
            role (str|List[str]): or None. if not None: Allowed roles

        Returns:
            AuthResponse:
        """
        if isinstance(role, str):
            self._role = [role]
        else:
            self._role = role
        self._request = request

        valid, errors = self.__request_is_valid()
        if not valid:
            return AuthResponse(
                message=responses.BAD_REQUEST,
                http_code=HttpCode.BAD_REQUEST,
                errors=errors
            )

        username = self._request['username'].lower()
        self._user = UserRepository.find_one(username=username)
        if not self.__credential_conditions():
            return AuthResponse(
                message=responses.BAD_CREDENTIALS,
                http_code=HttpCode.BAD_REQUEST
            )

        return AuthResponse(
            message=responses.OK,
            tokens=self._new_tokens(self._user),
            change_password=self._user.change_password
        )

    def __credential_conditions(self) -> tuple:
        """Condiciones para verificar credenciales.
        Usuario, contraseña y role

        Returns:
            (tuple)
        """
        if self._role:
            return (
                self._user and
                self._user.role.name in self._role and
                password_match(self._request['password'], self._user.password)
            )
        return (
            self._user and
            password_match(self._request['password'], self._user.password)
        )

    def __request_is_valid(self) -> (bool, dict):
        """El request debe cumplir con la estructura,
        no debe tener key adicionales

        Returns:
            (bool, dict): (is_valid, errors)
        """
        v = Validator()
        v.schema = {
            "username": {
                "type": "string",
                "required": True,
                "no_spaces": True
            },
            "password": {
                "type": "string",
                "required": True,
                "no_spaces": True
            }
        }

        valid = v.validate(self._request)
        return valid, v.errors


class RefreshToken(BaseAuth):

    def handle(self, request: dict) -> AuthResponse:
        """
        Args:
            request (dict): Ejemplo:
                ::
                    {
                        'refresh_token': 'a_refresh_token'
                    }

        Returns:
            AuthResponse:
        """
        self.__request = request

        valid, response = self.__validate()
        if not valid:
            return response

        tokens = self._new_tokens(self.__user)
        return AuthResponse(
            message=responses.OK,
            tokens=tokens
        )

    def __validate(self) -> (bool, AuthResponse):
        """Valida el request y carga self.__portfolio y self.__payment

        Returns:
            (bool, AuthResponse): (True, None) Si es valido.
                (False, AuthResponse) Si no es valido.
        """
        valid, errors = self.__request_is_valid()
        if not valid:
            return False, AuthResponse(
                http_code=HttpCode.BAD_REQUEST,
                message=responses.BAD_REQUEST,
                errors=errors
            )

        payload = refresh_token_decode(
            self.__request['refresh_token']
        )
        if payload.error:
            return False, AuthResponse(
                http_code=HttpCode.UNAUTHORIZED,
                message=payload.error
            )

        self.__user = current_user()
        if config.WHITE_LIST_TOKEN:
            self.__whitelist = WhitelistTokenRepository.find_one(
                uuid_refresh=payload.uuid
            )
            if not self.__whitelist:
                return False, AuthResponse(
                    http_code=HttpCode.UNAUTHORIZED,
                    message=responses.UNAUTHORIZED
                )

            if self.__user.id != self.__whitelist.user.id:
                # El usuario autenticado no es propietario del refresh_token
                return False, AuthResponse(
                    http_code=HttpCode.UNAUTHORIZED,
                    message=responses.UNAUTHORIZED
                )

        return True, None

    def __request_is_valid(self) -> (bool, dict):
        """El request debe cumplir con la estructura,
        no debe tener key adicionales

        Returns:
            (bool, dict): (is_valid, errors)
        """
        v = Validator()
        v.schema = {
            "refresh_token": {
                "type": "string",
                "required": True
            }
        }

        valid = v.validate(self.__request)
        return valid, v.errors


class Logout(UseCaseInterface):

    def handle(self, token: str) -> Response:
        """
        Args:
            token (str)

        Returns:
            Response:
        """
        self.__token = token
        self.__delete_token()

        return Response(
            message=responses.OK
        )

    def __delete_token(self) -> None:
        """Borra el token de la WhitelistToken"""
        payload = token_decode(self.__token)
        token = WhitelistTokenRepository.find_one(
            uuid_access=payload.uuid
        )
        if token:
            token.delete()
