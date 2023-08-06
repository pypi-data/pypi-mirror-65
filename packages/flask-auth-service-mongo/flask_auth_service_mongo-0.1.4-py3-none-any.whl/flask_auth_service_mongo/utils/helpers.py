from functools import reduce
import re


def recursive_get(d: dict, keys, default=None):
    """Aplica un get recursivo al dict parametro

    Args:
        d (dict)
        keys (str|list|tuple): Si es un str keyA.keyB => [keyA, keyB]
        default (mixed): No requerido
    """
    if isinstance(keys, str):
        keys = keys.split('.')
    result = reduce(lambda c, k: c.get(k, {}), keys, d)
    if default is not None and result == {}:
        return default
    return result


def dict_keys_to_snake(data: dict) -> dict:
    """Convierte las keys de un diccionario de camel case a snake
    Args:
        data (dict)
    Returns:
        dict
    """
    return dict(
        zip([camel_to_snake(k) for k in data.keys()], list(data.values()))
    )


def camel_to_snake(msg: str):
    """Convierte un string camel case a snake
    Args:
        msg (str)
    Returns:
        str
    """
    msg = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', msg)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', msg).lower()
