from unittest import TestCase
from flask_auth_service_mongo.constants.security import Roles


class TestRoles(TestCase):

    def test_values(self):
        roles = Roles.values()

        self.assertEqual(roles, [
            'is_authenticated',
            'is_anonymously'
        ])
