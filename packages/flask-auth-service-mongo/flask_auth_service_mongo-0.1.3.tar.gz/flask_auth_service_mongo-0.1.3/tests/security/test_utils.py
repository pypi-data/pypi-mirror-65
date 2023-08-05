from unittest import TestCase
from flask import Flask
from flask_auth_service_mongo import config
from flask_auth_service_mongo.security.models import User
from flask_auth_service_mongo.security.utils import (
    Payload,
    password_hash,
    password_match,
    token_decode,
    token_generate,
    refresh_token_decode,
    AccessTokens
)


class TestPayload(TestCase):
    def test_new_full(self):
        params = ('error', 'user_id', 'uuid')
        payload = Payload(*params)
        self.assertEqual(params[0], payload.error)
        self.assertEqual(params[1], payload.user_id)
        self.assertEqual(params[2], payload.uuid)

    def test_new_nullable(self):
        payload = Payload()
        self.assertIsNone(payload.error)
        self.assertIsNone(payload.user_id)
        self.assertIsNone(payload.uuid)


class TestPassword(TestCase):
    """Pruebas del generador del hash y el match para la contraseña"""

    def test_hash_and_match(self):
        param = 'password'
        hashpw = password_hash(param)

        self.assertIsInstance(hashpw, str)
        self.assertNotEqual(hashpw, param)

        matchpw = password_match(param, hashpw)

        self.assertIsInstance(matchpw, bool)
        self.assertTrue(matchpw)

        matchpw = password_match('param', hashpw)

        self.assertIsInstance(matchpw, bool)
        self.assertFalse(matchpw)


class TestToken(TestCase):
    """Pruebas para el generador y el decode del token"""

    def test_generate_and_decode(self):
        # Crea el contexto del app flask
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'not-secret'

        with app.app_context():
            user = User(id='id')

            # generar tokens
            tokens, uuids = token_generate(user)
            self.assertIsInstance(tokens, AccessTokens)
            self.assertEqual(tokens.token_type, 'Bearer')
            self.assertEqual(tokens.expires_in, config.TOKEN_EXPIRE_MINUTES)
            self.assertIsInstance(uuids['uuid_access'], str)
            self.assertIsInstance(uuids['uuid_refresh'], str)
            self.assertNotEqual(uuids['uuid_access'], uuids['uuid_refresh'])

            # Decode Ok access_token
            payload = token_decode(tokens.access_token)
            self.assertIsInstance(payload, Payload)
            self.assertIsNone(payload.error)
            self.assertEqual(payload.user_id, 'id')
            self.assertEqual(payload.uuid, uuids['uuid_access'])

            # Decode Ok refresh_token
            payload = refresh_token_decode(tokens.refresh_token)
            self.assertIsInstance(payload, Payload)
            self.assertIsNone(payload.error)
            self.assertEqual(payload.uuid, uuids['uuid_refresh'])

            # Decode expired token
            token = ('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzYwMjE'
                     '5NzYsImlhdCI6MTU3NjAxODM3Niwic3ViIjoiNWRmMDIxYmU1Y2I0Y2Z'
                     'hZDgyMzM5MTg4Iiwicm9sIjoiYWRtaW4ifQ.PYY_7TRhSyd0_H_tXGBt'
                     'WCSm2K_pPuNjyOk4NERgNrk')
            payload = token_decode(token)
            self.assertIsInstance(payload, Payload)
            self.assertEqual(payload.error, 'signature_expired')
            self.assertIsNone(payload.user_id)

            # Decode expired token
            token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NzYwMjE'
            payload = token_decode(token)
            self.assertIsInstance(payload, Payload)
            self.assertEqual(payload.error, 'invalid_token')
            self.assertIsNone(payload.user_id)
