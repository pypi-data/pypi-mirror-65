from flask import request
from ...config import WHITE_LIST_TOKEN, REQUIRE_PASSWORD_CHANGE
from ...constants import responses
from ...constants.enums import HttpCode
from ..utils import token_decode
from ..repository import UserRepository, WhitelistTokenRepository
from .user import set_current_user


def _response_unauthorized(message: str = None) -> (dict, int):
    """Crea una respuesta de "unauthorized"

    Args:
        message (str): Default None

    Returns:
        body (dict)
        http_code (int)
    """
    return dict(
        message=message if message else responses.UNAUTHORIZED
    ), HttpCode.UNAUTHORIZED.value


def required(role: str = None, require_password_change: bool = None):
    """Decorador para validar token jwt.
    Si role es diferente de None, verifica tambien el role

    Args:
        role (str): Or List[str]
        require_password_change (bool):
            Default = config.REQUIRE_PASSWORD_CHANGE.
            Si esta activo y User.change_password es True rechaza la petición.

    Returns:
        (dict, int): (body, http_code)
    """
    if isinstance(role, str):
        role = [role]

    if require_password_change is None:
        require_password_change = REQUIRE_PASSWORD_CHANGE

    def decorator(func):
        def wrapper(*args, **kwargs):
            authorization = request.headers.get('Authorization')
            if not authorization:
                # header sin "Authorization"
                return _response_unauthorized()

            auth_type, token = authorization.split(' ')
            if auth_type != 'Bearer':
                # Tipo de "Authorization" no valido
                return _response_unauthorized()

            payload = token_decode(token)
            if payload.error:
                # Error de token
                return _response_unauthorized(payload.error)

            if WHITE_LIST_TOKEN:
                in_whitelist = WhitelistTokenRepository.find_one(
                    uuid_access=payload.uuid
                )
                if not in_whitelist:
                    # El token no esta en la lista blanca
                    return _response_unauthorized()

            user = UserRepository.find(payload.user_id)
            if not user:
                # Usuario no encontrado
                return _response_unauthorized()

            if role and user.role.name not in role:
                # Role incorrecto
                return _response_unauthorized()

            if require_password_change and user.change_password:
                # El usuario debe cambiar de contraseña
                return _response_unauthorized('password_change_required')

            set_current_user(user)

            return func(*args, **kwargs)
        wrapper.__doc__ = func.__doc__
        return wrapper
    return decorator
