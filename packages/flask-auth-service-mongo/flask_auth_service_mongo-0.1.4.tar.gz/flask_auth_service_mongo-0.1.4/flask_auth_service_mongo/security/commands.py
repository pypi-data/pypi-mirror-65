import json
import click
from flask import Blueprint
from .use_cases import NewRole, CreateUser
from .models import WhitelistToken

command_auth_mongo = Blueprint(
    'command_auth_mongo',
    __name__,
    cli_group='auth_mongo'
)


@command_auth_mongo.cli.command(
    'role-new',
    help="Create a Role"
)
@click.option('-n', '--name', 'name', required=True, prompt=True)
@click.option('-p', '--permissions', 'permissions',
              help='''JSON example: '{"key": "value"}' ''')
def role_new(**kwargs):
    request = dict()
    for (key, value) in kwargs.items():
        if value is not None:
            request[key] = value
    try:
        if 'permissions' in request:
            request['permissions'] = json.loads(request['permissions'])

        use_case = NewRole()
        result = use_case.handle(request)

        click.echo("Result of Role creation: {}. {}".format(
            result.message,
            result.errors if result.errors else ''
        ))
    except Exception as e:
        click.echo("Create a Role ERROR: {}".format(e))


@command_auth_mongo.cli.command(
    'user-new',
    help='Create User'
)
@click.option('-r', '--role', required=True, prompt='Role',
              help='User role')
@click.option('-u', '--username', required=True, prompt='Username',
              help='Your username to login')
@click.option('--password', required=True, prompt=True,
              hide_input=True, confirmation_prompt=True,
              help='Your password to login')
def user_new(
    role: str,
    username: str,
    password: str
):
    click.echo('Creation of user started.')
    use_case = CreateUser()
    request = dict(
        role=role,
        username=username,
        password=password,
        password_confirmed=password
    )
    result = use_case.handle(request)

    click.echo("Result of User creation: {}. {}".format(
        result.message,
        result.errors if result.errors else ''
    ))


@command_auth_mongo.cli.command(
    'clear-tokens',
    help='Clear all tokens of the WhitelistToken'
)
@click.option('-f', '--forced', is_flag=True)
def clear_tokens(forced):
    if forced:
        WhitelistToken.drop_collection()
    else:
        try:
            _ = WhitelistToken.objects().first()
        except Exception:
            # There are changes in the model
            # Delete collection to avoid problems
            WhitelistToken.drop_collection()

    click.echo('Token cleanup completed')
