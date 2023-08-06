
class Roles:
    IS_AUTHENTICATED_FULLY = 'is_authenticated'
    IS_AUTHENTICATED_ANONYMOUSLY = 'is_anonymously'

    @staticmethod
    def values() -> list:
        return [
            Roles.IS_AUTHENTICATED_FULLY,
            Roles.IS_AUTHENTICATED_ANONYMOUSLY,
        ]
