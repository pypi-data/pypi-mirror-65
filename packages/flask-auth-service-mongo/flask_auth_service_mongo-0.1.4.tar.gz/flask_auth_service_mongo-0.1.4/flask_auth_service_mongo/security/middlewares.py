from ..constants.security import Roles
from .auth import current_user


class MutationMiddleware:
    """
    Args:
        access_control (List[Dict]): Example:
            ::
                [{
                    'mutation': 'login',
                    'roles': ['is_anonymously']
                }, {
                    'mutation': 'logout',
                    'roles': ['is_authenticated']
                }, {
                    'mutation': 'create_obj',
                    'roles': ['custom_role']
                }]
    """

    def __init__(self, access_control: list):
        self.access_control = access_control

    def resolve(self, next, root, info, **args):
        if root is not None or info.operation.operation != 'mutation':
            # Not a mutation, everything is allowed
            return next(root, info, **args)

        access_control = self.__get_access_control(info.field_name)
        if access_control is None:
            # No access rules were defined for this mutation
            return next(root, info, **args)

        user = current_user()
        if not user:
            if Roles.IS_AUTHENTICATED_ANONYMOUSLY in access_control['roles']:
                # user anonymously
                return next(root, info, **args)
            else:
                # Unauthorized
                return None

        if Roles.IS_AUTHENTICATED_FULLY in access_control['roles']:
            # Mutation usable by any authenticated user
            return next(root, info, **args)

        if user.role.name not in access_control['roles']:
            # Role not valid
            return None

        # Role ok
        return next(root, info, **args)

    def __get_access_control(self, field_name: str) -> dict:
        """Returns the first access_control when
        field_name == access_control.mutation

        Args:
            field_name (str):

        Returns:
            dict: Or None
        """
        access_control = list(filter(
            lambda d: d['mutation'] == field_name,
            self.access_control
        ))
        if access_control:
            return access_control[0]
        return None
