from unittest import TestCase
from mongoengine import connect, disconnect
from flask_auth_service_mongo.security.models import User, Role


class TestRole(TestCase):
    @classmethod
    def setUpClass(cls):
        disconnect()
        connect('mongoenginetest', host='mongomock://localhost')

    @classmethod
    def tearDownClass(cls):
        disconnect()

    def test_save(self):
        params = dict(
            name='admin',
            permissions=dict(
                x=True
            )
        )

        role = Role(**params)
        role.save()

        result = Role.objects().first()

        self.assertIsInstance(result, Role)
        for key in params:
            self.assertEqual(getattr(result, key), params[key])


class TestUser(TestCase):
    @classmethod
    def setUpClass(cls):
        disconnect()
        connect('mongoenginetest', host='mongomock://localhost')

    @classmethod
    def tearDownClass(cls):
        disconnect()

    def test_save(self):
        # Prepara un role
        role = Role(name='admin', permissions={'a': 1})
        role.save()

        params = dict(
            username='a name',
            password='a pass'
        )
        user = User(**params)
        self.assertIsNone(user.role)

        user.role = role
        user.save()

        result = User.objects().first()

        self.assertIsInstance(result, User)
        self.assertIsInstance(result.role, Role)
