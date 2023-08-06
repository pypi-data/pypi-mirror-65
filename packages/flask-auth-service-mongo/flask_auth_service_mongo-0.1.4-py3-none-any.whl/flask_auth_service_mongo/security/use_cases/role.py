from ...constants import responses
from ...constants.enums import HttpCode
from ...utils.use_case import Response, UseCaseInterface
from ...utils.validator import Validator
from ..models import Role
from ..repository import RoleRepository


class SaveRoleResponse(Response):
    """Respuesta para los casos de uso new y update role

    Attributes:
        role (security.models.Role)
        http_code (int)
        message (str)
        errors (dict)
    """
    def __init__(self, role: Role = None, *args, **kwargs):
        self.role = role

        super(SaveRoleResponse, self).__init__(*args, **kwargs)


class NewRole(UseCaseInterface):
    """Caso de uso: Crear un Role"""

    def handle(self, request: dict) -> SaveRoleResponse:
        """
        Args:
            request (dict): Ejemplo:
                ::
                    {
                        'name': 'roleName',
                        'permissions': {'a':'b'}
                    }

        Returns:
            SaveRoleResponse:
        """
        self._request = request

        valid, response = self.__validate()
        if not valid:
            return response

        role = self._create_role()
        return SaveRoleResponse(
            message=responses.CREATED,
            http_code=HttpCode.CREATED,
            role=role
        )

    def __validate(self) -> (bool, SaveRoleResponse):
        """Execution of validators

        Returns:
            (bool, SaveRoleResponse):
        """
        valid, errors = self.__request_is_valid()
        if not valid:
            return False, SaveRoleResponse(
                message=responses.BAD_REQUEST,
                http_code=HttpCode.BAD_REQUEST,
                errors=errors
            )

        exists = RoleRepository.find_one(name=self._request['name'])
        if exists:
            return False, SaveRoleResponse(
                message=responses.EXISTING_RESOURCE,
                http_code=HttpCode.BAD_REQUEST
            )

        return True, None

    def _create_role(self) -> Role:
        """Crea un Role con los datos del self._request

        Returns:
            Role:
        """
        role = Role(**self._request)
        role.save()

        return role

    def __request_is_valid(self) -> (bool, dict):
        """ El request debe cumplir con la estructura,
        no debe tener keys adicionales

        Returns:
            (bool, dict): (is_valid, errors)
        """
        v = Validator()
        v.schema = {
            'name': {
                'type': 'string',
                'required': True
            },
            'permissions': {
                'type': 'dict'
            }
        }

        valid = v.validate(self._request)
        return valid, v.errors
