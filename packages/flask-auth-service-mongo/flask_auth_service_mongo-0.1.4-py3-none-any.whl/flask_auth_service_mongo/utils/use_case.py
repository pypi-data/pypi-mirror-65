import abc
from ..constants.enums import HttpCode
from .contract import LoggingInterface


class Response:
    """Respuesta Genérica para los casos de uso

    Attributes:
        _http_code (constants.enums.HttpCode):
            Garantiza que el codigo sea valido. Default HttpCode.OK
        message (str)
        errors (list)
    """

    def __init__(
        self,
        http_code: int = None,
        message: str = None,
        errors: list = None
    ):
        # Default HttpCode
        self._http_code: HttpCode = HttpCode.OK

        self.http_code = http_code
        self.message = message
        self.errors = errors

    @property
    def http_code(self) -> int:
        """int: Código http"""
        if self._http_code:
            return self._http_code.value
        return None

    @http_code.setter
    def http_code(self, http_code) -> None:
        if isinstance(http_code, HttpCode):
            self._http_code = http_code
        elif http_code:
            self._http_code = HttpCode(http_code)

    def __json__(self):
        return {
            'http_code': self.http_code,
            'message': self.message,
            'errors': self.errors,
        }


class UseCaseInterface(metaclass=abc.ABCMeta):
    """Contrato para los casos de uso
    Attributes:
        _path (str)
        _logger (utils.contract.LoggingInterface)
    """
    _path = None
    _logger: LoggingInterface = None

    def _debugger(self, message):
        """Se ejecuta solo si esta activo el debug

        Args:
            message (str)
        """
        self._logger.debug(
            '{}: {}'.format(self._path, message)
            )

    @abc.abstractmethod
    def handle(self, *args, **kwargs) -> Response:
        """Único método público, este debe recibir el request
        y retornar el resultado de todo el caso de uso

        Nota:
            Cualquier otro parámetro que el caso de uso necesite,
            que no llegue en el request de la petición

        Args:
            request (dict): (Opcional) Recomendado
            args: other positional arguments
            kwargs: other keyword arguments

        Returns:
            response (utils.use_case.Response): Instancia de Response o\
            de una clase hija (recomendado si se requiere retornar\
            datos que no sean atributos de Response)
        """
        pass
