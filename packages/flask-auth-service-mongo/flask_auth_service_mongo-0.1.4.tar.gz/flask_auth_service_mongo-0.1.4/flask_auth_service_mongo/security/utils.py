import datetime
import bcrypt
import jwt
import uuid
from .models import User
from .. import config
from ..constants import responses


def password_hash(password: str) -> str:
    """
    Args:
        password (str)

    Returns:
        hashed (str)
    """
    password = password.encode()
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed.decode()


def password_match(password: str, hashed: str) -> bool:
    """
    Args:
        password (str)
        hashed (str)

    Returns:
        (bool)
    """
    password = password.encode()
    hashed = hashed.encode()
    return bcrypt.checkpw(password, hashed)


class Payload:
    """
    Attributes:
        error (str)
        user_id (str)
    """
    def __init__(
        self,
        error: str = None,
        user_id: str = None,
        _uuid: str = None
    ):
        self.error = error
        self.user_id = user_id
        self.uuid = _uuid


class AccessTokens:
    """
    Args:
        token_type (str)
        access_token (str)
        refresh_token (str)
        expires_in (int): Tiempo en minutos para que expire el token
    """
    def __init__(
        self,
        token_type: str = None,
        access_token: str = None,
        refresh_token: str = None,
        expires_in: int = None
    ):
        self.token_type = token_type
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_in = expires_in


def token_generate(user: User) -> (AccessTokens, dict):
    """Genera un juego de access token y refresh token

    Args:
        user (User)

    Returns:
        (AccessTokens, dict):
    """
    expires_in = config.TOKEN_EXPIRE_MINUTES

    def token(payload):
        return jwt.encode(
            payload,
            config.SECRET_KEY,
            algorithm='HS256'
        ).decode()

    now = datetime.datetime.utcnow()
    expire = now + datetime.timedelta(minutes=expires_in)

    # access_token
    access_payload = {
        'exp': expire,
        'iat': now,
        'sub': str(user.id),
        'uuid': str(uuid.uuid1())
    }
    access_token = token(access_payload)

    # refresh_token
    refresh_payload = {
        'exp': expire,
        'uuid': str(uuid.uuid1())
    }
    refresh_token = token(refresh_payload)

    return AccessTokens(
        token_type=config.TOKEN_TYPE,
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=expires_in
    ), {
        'uuid_access': access_payload['uuid'],
        'uuid_refresh': refresh_payload['uuid']
    }


def token_decode(token: str) -> Payload:
    """
    Args:
        token (str)

    Returns:
        Payload:
    """
    try:
        payload = jwt.decode(
            token,
            config.SECRET_KEY,
            algorithms=['HS256']
        )

        return Payload(
            user_id=payload['sub'],
            _uuid=payload['uuid']
        )
    except jwt.ExpiredSignatureError:
        return Payload(responses.SIGNATURE_EXPIRED)
    except Exception:
        return Payload(responses.INVALID_TOKEN)


def refresh_token_decode(refresh_token: str) -> Payload:
    """
    Args:
        refresh_token (str)

    Returns:
        Payload:
    """
    try:
        payload = jwt.decode(
            refresh_token,
            config.SECRET_KEY,
            algorithms=['HS256']
        )

        return Payload(
            _uuid=payload['uuid']
        )
    except jwt.ExpiredSignatureError:
        return Payload(responses.SIGNATURE_EXPIRED)
    except Exception:
        return Payload(responses.INVALID_TOKEN)
