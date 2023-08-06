from unittest import TestCase
from flask_auth_service_mongo.security.commands import (
    role_new,
    user_new,
    clear_tokens
)


class TestRoleNew(TestCase):

    def test_params(self):
        context = role_new.make_context(
            'role-new', [
                '-n', 'a name',
                '-p', '{"key": "value"}'
            ]
        )

        self.assertEqual(context.params['name'], 'a name')
        self.assertEqual(context.params['permissions'], '{"key": "value"}')


class TestUserNew(TestCase):

    def test_params(self):
        context = user_new.make_context(
            'new', [
                '-r', 'a role',
                '-u', 'an username',
                '--password', 'a pass'
            ]
        )

        self.assertEqual(context.params['role'], 'a role')
        self.assertEqual(context.params['username'], 'an username')
        self.assertEqual(context.params['password'], 'a pass')


class TestClearTokens(TestCase):

    def test_params(self):
        context = clear_tokens.make_context('clear-tokens', ['-f'])
        self.assertEqual(context.params['forced'], True)

        context = clear_tokens.make_context('clear-tokens', [])
        self.assertEqual(context.params['forced'], False)
