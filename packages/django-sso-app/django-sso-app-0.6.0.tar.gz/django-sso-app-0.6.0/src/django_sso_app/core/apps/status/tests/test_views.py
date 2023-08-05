import json
import responses
import jwt
from http.cookies import SimpleCookie
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.test import TestCase, Client
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress
from rest_framework.authtoken.models import Token

from django_sso_app.core import app_settings

from django_sso_app.core.apps.profiles.models import Profile
from django_sso_app.core.apps.groups.models import Group

User = get_user_model()


class TestStatus(TestCase):
    def setUp(self):
        self.client = Client()
        adapter = get_adapter()

        self.email = "pippo@disney.com"
        self.username = self.username = "pippo"
        self.password = self.password = "paperina"
        self.hashed_password = make_password(self.password)

        self.valid_login = {
            'login': self.username,
            'password': self.password,
            'fingerprint': '123456'
        }

        self.new_user = User.objects.create(username=self.username, email=self.email, password=self.hashed_password)
        self.new_user_email = EmailAddress.objects.create(user=self.new_user,
                                                          email=self.email,
                                                          primary=True,
                                                          verified=True)

        self.device0 = adapter.add_user_profile_device(self.new_user, '000000')

        self.valid_jwt = jwt.encode(
            self.device0.get_jwt_payload(),
            'secret',
            app_settings.JWT_ALGORITHM
        ).decode('utf-8')

        staff_user_email = 'staff@example.com'

        self.staff_user_username = 'staff'
        self.staff_user_password = 'abc123456'
        self.staff_user = User.objects.create_user(username=self.staff_user_username, email=staff_user_email,
                                                   password=self.staff_user_password, is_staff=True)
        self.staff_user_email = EmailAddress.objects.create(user=self.staff_user,
                                                            email=self.staff_user.email,
                                                            primary=True,
                                                            verified=True)
        self.staff_user_token = Token.objects.create(user=self.staff_user)

        self.staff_user_valid_token_headers = {
            'content_type': 'application/json',
            'HTTP_AUTHORIZATION': 'Token {}'.format(self.staff_user_token.key)
        }

        self.staff_user_valid_login = {
            'login': self.staff_user.username,
            'password': self.staff_user_password,
            'fingerprint': '123456'
        }

        np_uuid = 'new-profile-uuid'
        print('new profile uuid', np_uuid)
        self.valid_new_profile = {
            "url": "http://localhost:8000/api/v1/auth/users/{}/".format(np_uuid),
            "sso_id": np_uuid,
            "sso_rev": 5,
            "date_joined": "2018-12-31T00:00:00+0000",
            "is_active": True,
            "email_verified": True,
            "groups": ['users'],
            "profile": {
                "url": "http://localhost:8000/api/v1/auth/profiles/{}/".format(np_uuid),
                "created_at": "2019-12-05T19:56:41+0000",
                "sso_id": np_uuid,
                "sso_rev": 5,
                "subscriptions": [
                    {
                        "service_url": "http://example.com",
                        "is_unsubscribed": False
                    }
                ],
                "is_unsubscribed": False,
                "username": "new_profile",
                "email": "paiuolo@gmail.com",
                "user": "http://localhost:8000/api/v1/auth/users/{}/".format(np_uuid),
                "first_name": "new",
                "last_name": "profile",
                "description": None,
                "picture": None,
                "birthdate": None,
                "latitude": None,
                "longitude": None,
                "country": "IT",
                "address": None,
                "language": "it"
            },
            "username": "new_profile",
            "email": "new_profile@example.com",
            "password": "pwd"
        }

        self.valid_new_profile_jwt_payload = {
                'id':999,
                'fingerprint': 'xxx',
                'sso_id': np_uuid,
                'sso_rev': 5
            }

        self.valid_new_profile_jwt = jwt.encode(
            self.valid_new_profile_jwt_payload,
            'secret',
            app_settings.JWT_ALGORITHM
        ).decode('utf-8')


    @responses.activate
    def test_switch_between_statuses(self):
        with self.settings(DJANGO_SSO_APP_SHAPE='backend_only'):

            client = Client()
            response = client.post(
                reverse('rest_login'),
                data=json.dumps(self.valid_login),
                content_type='application/json'
            )

            user_user_object = response.data.get('user')
            setattr(user_user_object, 'password', self.hashed_password)
            user_user_object = json.dumps(user_user_object)

            self.assertEqual(response.status_code, status.HTTP_200_OK, 'new user can not login')

        with self.settings(DJANGO_SSO_APP_SHAPE='backend_app'):
            client = Client()
            response = client.post(
                reverse('rest_login'),
                data=json.dumps(self.valid_login),
                content_type='application/json'
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK, 'new user can not login')

        with self.settings(DJANGO_SSO_APP_SHAPE='app',
                           DJANGO_SSO_APP_SERVICE_URL='http://example.com'):

            profile_url = reverse('django_sso_app_profile:detail', args=(self.valid_new_profile['sso_id'],))
            print('profile_url', profile_url)

            client = Client()
            client.cookies = SimpleCookie({app_settings.JWT_COOKIE_NAME: self.valid_new_profile_jwt})

            response = client.get(
                profile_url,
                content_type='application/json'
            )
            print('response', response.data)

            self.assertEqual(response.status_code, status.HTTP_200_OK, 'profile not created')

            self.assertEqual(Profile.objects.filter(sso_id=self.valid_new_profile['sso_id']).count(), 1,
                             'no profile model')

            self.assertEqual(response.data.get('sso_id'), str(self.valid_new_profile['sso_id']), 'sso_id differs')

        with self.settings(DJANGO_SSO_APP_SHAPE='app_persistence',
                           DJANGO_SSO_APP_SERVICE_URL='http://example.com'):
            # deleting pre generated user
            User.objects.get(sso_app_profile__sso_id=self.valid_new_profile['sso_id']).delete()

            profile_url = reverse('django_sso_app_profile:detail', args=(self.valid_new_profile['sso_id'],))
            print('profile_url', profile_url)

            client = Client()

            mocked_url = app_settings.REMOTE_USER_URL.format(
                sso_id=self.valid_new_profile['sso_id'])  # + '?with_password=true'
            print('mocked_url', mocked_url)
            responses.add(responses.GET, mocked_url,
                          json=self.valid_new_profile, status=200)

            client.cookies = SimpleCookie({app_settings.JWT_COOKIE_NAME: self.valid_new_profile_jwt})

            response = client.get(
                profile_url,
                content_type='application/json'
            )

            self.assertEqual(Profile.objects.filter(sso_id=self.valid_new_profile['sso_id']).count(), 1,
                             'no profile model')

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data.get('sso_id'), str(self.valid_new_profile['sso_id']), 'sso_id differs')

            created_profile = Profile.objects.get(sso_id=self.valid_new_profile['sso_id'])
            self.assertEqual(created_profile.groups.count(), 1, 'group not created')
            self.assertEqual(created_profile.groups.filter(name='users').count(), 1, 'group not same')

        with self.settings(DJANGO_SSO_APP_SHAPE='app_apigateway',
                           DJANGO_SSO_APP_SERVICE_URL='http://example.com'):
            # deleting pre generated user
            User.objects.get(sso_app_profile__sso_id=self.valid_new_profile['sso_id']).delete()

            profile_url = reverse('django_sso_app_profile:detail', args=(self.valid_new_profile['sso_id'],))
            print('profile_url', profile_url)

            client = Client()

            client.cookies = SimpleCookie({app_settings.JWT_COOKIE_NAME: self.valid_new_profile_jwt})

            response = client.get(
                profile_url,
                content_type='application/json',
                HTTP_X_CONSUMER_USERNAME=self.valid_new_profile['sso_id'].replace('-', '_'),
                HTTP_X_CONSUMER_GROUPS='users'
            )
            print('response', response.data)
            self.assertEqual(Profile.objects.filter(sso_id=self.valid_new_profile['sso_id']).count(), 1,
                             'no profile model')

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data.get('sso_id'), str(self.valid_new_profile['sso_id']), 'sso_id differs')

            created_profile = Profile.objects.get(sso_id=self.valid_new_profile['sso_id'])
            self.assertEqual(created_profile.groups.count(), 1, 'group not created')
            self.assertEqual(created_profile.groups.filter(name='users').count(), 1, 'group not same')
