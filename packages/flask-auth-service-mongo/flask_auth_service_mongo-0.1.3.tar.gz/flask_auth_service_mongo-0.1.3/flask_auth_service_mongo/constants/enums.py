from enum import Enum, unique


@unique
class HttpCode(Enum):
    # 2xx Success
    OK = 200
    CREATED = 201
    ACCEPTED = 202

    # 4xx Client Error
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_ACCEPTABLE = 406
    NOT_FOUND = 404

    # 5xx Server Error
    INTERNAL_SERVER_ERROR = 500
