# app only accetta jwt, la valida via secret in setting file
# app persistence accetta jwt, valida e
"""
DJANGO_SSO_APP_SHAPES = ('app',
                         'app_persistence',
                         'app_apigateway',
                         'app_persistence_apigateway')
"""
import json
import uuid
import jwt
import responses

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

from http.cookies import SimpleCookie

from rest_framework import status

from django_sso_app.backend.tests.factories import UserTestCase

from django_sso_app.core import app_settings

User = get_user_model()


class TestTokens(UserTestCase):
    def setUp(self):
        super(TestTokens, self).setUp()

        self.valid_jwt = jwt.encode(
            self.device0.get_jwt_payload(),
            'secret',
            app_settings.JWT_ALGORITHM
        ).decode('utf-8')

        self.invalid_jwt = jwt.encode(
            self.device0.get_jwt_payload(),
            'invalid_secret',
            app_settings.JWT_ALGORITHM
        ).decode('utf-8')

        self.valid_device_jwt = jwt.encode(
            self.device2.get_jwt_payload(),
            self.device2.apigw_jwt_secret,
            app_settings.JWT_ALGORITHM
        ).decode('utf-8')

    def test_app_shape_uses_settings_secret(self):
        client = Client()
        with self.settings(DJANGO_SSO_APP_SHAPE='app', DJANGO_SSO_APP_SERVICE_URL='http://example.com'):
            client.cookies = SimpleCookie({app_settings.JWT_COOKIE_NAME: self.valid_jwt})

            response = client.get(
                reverse('django_sso_app_profile:detail', args=(self.profile.sso_id,)),
                content_type='application/json'
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data.get('sso_id'), str(self.profile.sso_id))

        client = Client()
        with self.settings(DJANGO_SSO_APP_SHAPE='app', DJANGO_SSO_APP_SERVICE_URL='http://example.com'):
            client.cookies = SimpleCookie({app_settings.JWT_COOKIE_NAME: self.invalid_jwt})

            response = client.get(
                reverse('django_sso_app_profile:detail', args=(self.profile.sso_id,)),
                content_type='application/json'
            )

            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, 'invalid_jwt is valid')

    def test_app_apigateway_shape_uses_device_secret(self):
        with self.settings(DJANGO_SSO_APP_SHAPE='app_apigateway', DJANGO_SSO_APP_SERVICE_URL='http://example.com'):
            client = Client()
            client.cookies = SimpleCookie({app_settings.JWT_COOKIE_NAME: self.valid_device_jwt})

            response = client.get(
                reverse('django_sso_app_profile:detail', args=(self.profile.sso_id,)),
                content_type='application/json',
                HTTP_X_CONSUMER_USERNAME=self.profile.sso_id
            )
            print('test_app_apigateway_shape_uses_device_secret RESP', response.data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data.get('sso_id'), str(self.profile.sso_id))
