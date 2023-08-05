import logging
import json

from allauth.account.models import (
    EmailAddress,
)
from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import authenticate

from django_sso_app.backend.tests.factories import UserTestCase
from django_sso_app.core import app_settings

User = get_user_model()
logger = logging.getLogger('django_sso_app.core.tests')


class TestLogin(UserTestCase):

    def test_can_login_with_email(self):
        response = self.client.post(
            reverse('account_login'),
            data=self.valid_email_login
        )

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/profile/')

    def test_can_login_with_username(self):
        response = self.client.post(
            reverse('account_login'),
            data=self.valid_username_login
        )

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/profile/')

    def test_login_returns_jwt_cookie(self):
        response = self.client.post(
            reverse('account_login'),
            data=self.valid_email_login
        )

        cookies = response.client.cookies.items()

        has_jwt_cookie = False
        for (key, val) in cookies:
            if key == "jwt":
                has_jwt_cookie = True
                break

        self.assertTrue(has_jwt_cookie)

    def test_migrated_can_login_without_updating_rev(self):
        self.client.logout()

        migrated_user = User.objects.create(
            username=self.migrated_user_username,
            email=self.migrated_user_email,
            password=self.migrated_user_hashed_password
        )
        migrated_user_email = EmailAddress.objects.create(user=migrated_user,
                                                          email=self.migrated_user_email,
                                                          primary=True,
                                                          verified=True)
        migrated_profile = migrated_user.sso_app_profile

        logger.info('User created "{}"'.format(migrated_profile))

        previus_rev = migrated_profile.sso_rev

        logger.info('Calling Login with credentials "{}"'.format(self.valid_migrated_user_login))
        response = self.client.post(
            reverse('account_login'),
            data=self.valid_migrated_user_login
        )

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.url, '/profile/')

        migrated_profile.refresh_from_db()
        second_rev = migrated_profile.sso_rev
        self.assertEqual(previus_rev, second_rev)


    def test_admin_user_do_not_receives_jwt_on_login(self):
        response = self.client.post(
            '/admin/login/',
            data=self.valid_admin_login
        )

        cookies = response.client.cookies.items()

        jwt_cookie = None
        has_jwt_cookie = False
        for (key, val) in cookies:
            if key == "jwt":
                has_jwt_cookie = True
                jwt_cookie = val
                break

        self.assertFalse(has_jwt_cookie, 'admin receives jwt')
        self.assertEqual(jwt_cookie, None, 'jwt is still valid')


class TestLogout(UserTestCase):

    def test_logout_deletes_jwt_and_removes_devices(self):
        response = self.client.post(
            reverse('account_login'),
            data=self.valid_username_login
        )

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        response = self.client.post(
            reverse('account_logout'),
            content_type='application/json'
        )

        cookies = response.client.cookies.items()
        jwt_cookie = None
        has_valid_jwt_cookie = False
        for (key, val) in cookies:
            if key == "jwt":
                jwt_cookie = val
                if getattr(val, '_value') != 'None':
                    has_valid_jwt_cookie = True
                break

        self.assertFalse(has_valid_jwt_cookie, 'logout keeps jwt cookie')

        user_devices = self.user.sso_app_profile.devices.all()
        self.assertEqual(user_devices.count(), 0, 'Logout is not deleting all user devices')


class TestRegister(UserTestCase):

    def test_can_register(self):
        response = self.client.post(
            reverse('account_signup'),
            data=self.valid_new_profile
        )

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        new_user = User.objects.filter(email=self.valid_new_profile['email']).first()

        self.assertEqual(new_user.email, self.valid_new_profile['email'])

        email_address = EmailAddress.objects.filter(user=new_user, email=self.valid_new_profile['email']).first()

        self.assertNotEqual(email_address, None)

    def test_cannot_register_on_invalid_registration_data(self):
        response = self.client.post(
            reverse('account_signup'),
            data=self.invalid_new_profile,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_sends_confirmation_email(self):
        response = self.client.post(
            reverse('account_signup'),
            data=self.valid_new_profile
        )

        self.assertEqual(len(mail.outbox), 1)

    def test_registration_creates_subscription(self):
        response = self.client.post(
            reverse('account_signup'),
            data=self.valid_new_profile
        )

        new_user = User.objects.filter(username=self.valid_new_profile['username']).first()
        self.assertNotEqual(new_user, None, 'no new user created')

        self.assertEqual(new_user.sso_app_profile.subscriptions.filter(service__service_url=self.service.service_url).count(), 1)
