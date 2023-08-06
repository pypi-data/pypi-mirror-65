""" Default config.py file"""
import os


TOKEN_TYPE = 'Bearer'  # nosec
WHITE_LIST_TOKEN = os.environ.get('WHITE_LIST_TOKEN', True)
SECRET_KEY = os.environ.get('SECRET_KEY', 'not-secret')
USERNAME_MIN_LENGTH = os.environ.get('USERNAME_MIN_LENGTH', 3)
PASSWORD_MIN_LENGTH = os.environ.get('PASSWORD_MIN_LENGTH', 3)
TOKEN_EXPIRE_MINUTES = os.environ.get('TOKEN_EXPIRE_MINUTES', 60)
RESET_PASSWORD_LEN_GENERATOR = os.environ.get(
    'RESET_PASSWORD_LEN_GENERATOR', 8)
REQUIRE_PASSWORD_CHANGE = os.environ.get('REQUIRE_PASSWORD_CHANGE', False)
