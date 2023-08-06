from flask import g
from ..models import User


def current_user() -> User:
    """Retorna el usuario autenticado actual

    Returns:
        security.models.User: `None` or :class:`security.models.User` object
    """
    return g.get('user')


def set_current_user(user: User) -> None:
    """Define el usuario actual,
    para poder usar security.auth.current_user()

    Args:
        user (security.models.User):
    """
    g.user = user
