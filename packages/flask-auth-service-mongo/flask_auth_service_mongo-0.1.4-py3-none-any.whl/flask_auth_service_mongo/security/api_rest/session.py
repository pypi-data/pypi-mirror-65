from flask import request
from ..use_cases import Login, Logout


def login(role=None):
    """login for API Rest

    Args:
        role (str|List[str]): Nullable

    Returns:
        (dict, int): (data, http_code)
    """
    use_case = Login()
    result = use_case.handle(
        request=request.get_json(),
        role=role
    )

    response = dict(
        message=result.message
    )
    if result.tokens:
        response['data'] = dict(
            access_token=result.tokens.access_token,
            token_type=result.tokens.token_type,
            refresh_token=result.tokens.refresh_token,
            expires_in=result.tokens.expires_in,
            change_password=result.change_password
        )
    return response, result.http_code


def logout():
    """logout for API Rest

    Returns:
        (dict, int): (data, http_code)
    """
    authorization = request.headers.get('Authorization')
    _, token = authorization.split(' ')
    use_case = Logout()
    result = use_case.handle(token=token)

    response = dict(message=result.message)
    return response, result.http_code
