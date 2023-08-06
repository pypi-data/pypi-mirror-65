from .models import (
    Role,
    User,
    WhitelistToken
)


class RoleRepository:
    """Clase para búsquedas dentro del modelo Role"""

    @staticmethod
    def find(id: str) -> Role:
        """Busca un Role por id

        Args:
            id (str)

        Returns:
            security.models.Role: o None
        """
        return Role.objects(id=id).first()

    @staticmethod
    def find_one(**kwargs) -> Role:
        """Busca un Role por parámetros dados

        Args:
            kwargs

        Returns:
            security.models.Role: o None
        """
        return Role.objects(**kwargs).first()

    @staticmethod
    def find_all(**kwargs) -> Role:
        """Busca Roles por parámetros dados

        Args:
            kwargs

        Returns:
            security.models.Role: o None
        """
        return Role.objects(**kwargs)


class UserRepository:
    """Clase para búsquedas dentro del modelo User"""

    @staticmethod
    def find(id: str) -> User:
        """Busca un User por id

        Args:
            id (str)

        Returns:
            security.models.User: o None
        """
        return User.objects(id=id).first()

    @staticmethod
    def find_one(**kwargs) -> User:
        """Busca un User

        Args:
            kwargs: Atributos del modelo

        Returns:
            security.models.User: o None
        """
        return User.objects(**kwargs).first()

    @staticmethod
    def find_all(**kwargs) -> list:
        """Busca Users

        Args:
            kwargs: Atributos del modelo

        Returns:
            list[security.models.User]
        """
        return User.objects(**kwargs)


class WhitelistTokenRepository:
    """Clase para búsquedas dentro del modelo WhitelistToken"""

    @staticmethod
    def find(id: str) -> WhitelistToken:
        """Busca un WhitelistToken por id

        Args:
            id (str)

        Returns:
            security.models.WhitelistToken: o None
        """
        return WhitelistToken.objects(id=id).first()

    @staticmethod
    def find_one(**kwargs) -> WhitelistToken:
        """Busca un WhitelistToken

        Args:
            kwargs: Atributos del modelo

        Returns:
            security.models.WhitelistToken: o None
        """
        return WhitelistToken.objects(**kwargs).first()

    @staticmethod
    def find_all(**kwargs) -> list:
        """Busca WhitelistTokens

        Args:
            kwargs: Atributos del modelo

        Returns:
            list[security.models.WhitelistToken]
        """
        return WhitelistToken.objects(**kwargs)
