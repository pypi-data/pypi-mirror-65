import abc


class LoggingInterface:
    """Contrato para el logging"""
    debug_on = False

    @abc.abstractmethod
    def debug(self, msg: str):
        pass

    @abc.abstractmethod
    def info(self, msg: str):
        pass

    @abc.abstractmethod
    def error(self, msg: str):
        pass
