import json

import jwt
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.core import mail

from rest_framework import status

from django_sso_app.backend.tests.factories import UserTestCase

from .... import app_settings

User = get_user_model()


class TestUserCreate(UserTestCase):

    def test_staff_user_can_create_user_with_profile_with_unverified_email(self):
        print('HEADERS', self.staff_user_valid_token_headers, type(self.staff_user_valid_token_headers))
        response = self.client.post(
            reverse('django_sso_app_user:list'),
            data=json.dumps(self.valid_new_external_user),
            **self.staff_user_valid_token_headers
        )

        new_user_sso_id = response.data.get('sso_id')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response2 = self.client.get(
            reverse('django_sso_app_user:detail', args=(new_user_sso_id,)),
            **self.staff_user_valid_token_headers
        )

        self.assertEqual(response2.status_code, status.HTTP_200_OK)

        self.assertEqual(response2.data['email'], self.valid_new_external_user['email'])

        self.assertEqual(response2.data['email_verified'], False)

    def test_staff_user_can_create_user_with_profile_and_validated_email(self):
        print('HEADERS', self.staff_user_valid_token_headers, type(self.staff_user_valid_token_headers))

        response = self.client.post(
            reverse('django_sso_app_user:list') + '?skip_confirmation=true',
            data=json.dumps(self.valid_new_external_user),
            **self.staff_user_valid_token_headers
        )

        new_user_sso_id = response.data.get('sso_id')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response2 = self.client.get(
            reverse('django_sso_app_user:detail', args=(new_user_sso_id,)),
            **self.staff_user_valid_token_headers
        )

        self.assertEqual(response2.status_code, status.HTTP_200_OK)


        self.assertEqual(response2.data['email'], self.valid_new_external_user['email'])

        self.assertEqual(response2.data['email_verified'], True)

    def test_non_staff_user_can_create_profile_without_validated_mail(self):
        response0 = self.client.post(
            reverse('rest_login'),
            data=json.dumps(self.valid_login),
            content_type='application/json'
        )

        response = self.client.post(
            reverse('django_sso_app_user:list') + '?skip_confirmation=true',
            data=json.dumps(self.valid_new_external_user),
            content_type='application/json'
        )

        print('RESP', response.json())

        new_user_sso_id = response.data.get('sso_id')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response2 = self.client.get(
            reverse('django_sso_app_user:detail', args=(new_user_sso_id,)),
            **self.staff_user_valid_token_headers
        )

        self.assertEqual(response2.status_code, status.HTTP_200_OK)

        self.assertEqual(response2.data['email'], self.valid_new_external_user['email'])

        self.assertEqual(response2.data['email_verified'], False)

        new_user = User.objects.get(sso_app_profile__sso_id=new_user_sso_id)
        print('USER SUBSCRIPT', new_user.sso_app_profile.subscriptions.all(), self.service2.__dict__)

        self.assertEqual(new_user.sso_app_profile.subscriptions.first().service, self.service2 ,
                         'no subscription created')

        profile_object = self.valid_new_external_user['profile']
        for f in app_settings.PROFILE_FIELDS:
            model_val = getattr(new_user.sso_app_profile, f, None)
            object_val = profile_object.get(f, None)

            if f == 'birthdate':
                model_val = str(model_val)
            elif f == 'country':
                object_val = object_val.upper()
                model_val = str(model_val).upper()

            self.assertEqual(model_val, object_val)


class TestUserRetrieve(UserTestCase):

    def test_user_can_retrieve_user(self):
        response = self.client.post(
            reverse('rest_login'),
            data=json.dumps(self.valid_login),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response2 = self.client.get(
            reverse('django_sso_app_user:detail', args=(self.profile.sso_id,)),
            content_type='application/json'
        )
        print('RESP', response2.data)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

    def test_staff_user_can_retrieve_user_with_token(self):

        response2 = self.client.get(
            reverse('django_sso_app_user:detail', args=(self.profile.sso_id,)),
            **self.staff_user_valid_token_headers
        )
        print('RESP', response2.data)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)


class TestUserUpdate(UserTestCase):

    def test_user_email_update_deletes_all_devices_and_waits_for_confirmation(self):
        """
        User update refreshes caller jwt and deletes all but caller devices
        """
        print('\n logging in with user', self.user, 'and fingerprint', self.valid_login.get('fingerprint'))

        first_rev = self.profile.sso_rev
        response = self.client.post(
            reverse('rest_login'),
            data=json.dumps(self.valid_login),
            content_type='application/json'
        )
        cookies = response.cookies

        print('\n sending patch from user', self.user, 'with new email', self.valid_email_update)
        response2 = self.client.patch(
            reverse('django_sso_app_user:detail', args=[self.profile.sso_id]),
            data=json.dumps(self.valid_email_update),
            content_type='application/json'
        )
        cookies2 = response2.cookies

        self.profile.refresh_from_db()
        second_rev = self.profile.sso_rev

        self.assertEqual(second_rev, first_rev + 1, 'rev not incremented')

        devices = self.profile.devices.all()
        self.assertEqual(devices.count(), 0, 'devices not deleted')

        self.assertEqual(len(mail.outbox), 1)

    def test_user_password_update_refreshes_and_returns_current_device_jwt_and_deletes_all_devices_but_the_caller(self):
        """
        User password update refreshes caller jwt and deletes all but caller devices
        """

        first_rev = self.profile.sso_rev
        response = self.client.post(
            reverse('rest_login'),
            data=json.dumps(self.valid_login),
            content_type='application/json'
        )
        cookies = response.cookies
        self.assertEqual(response.status_code, 200, 'unable to login with valid credentials')

        response2 = self.client.patch(
            reverse('django_sso_app_user:detail', args=[self.profile.sso_id]),
            data=json.dumps(self.valid_password_update),
            content_type='application/json'
        )
        cookies2 = response2.cookies

        self.profile.refresh_from_db()
        second_rev = self.profile.sso_rev

        self.assertEqual(second_rev, first_rev + 1, 'rev not incremented')

        self.assertTrue(len(cookies2.keys()) > 0, 'no jwt cookie set')

        devices = self.profile.devices.all()

        self.assertEqual(devices.count(), 1, 'other devices not deleted')

        self.assertEqual(devices.first().fingerprint, self.valid_login['fingerprint'], 'device not updated')

        jwt_cookie = cookies.get('jwt').value
        jwt_cookie2 = cookies2.get('jwt').value

        # print('\nRISPOSTA, user rev', self.profile.sso_rev, '\n\nTOKEN', jwt_cookie)

        unverified_payload = jwt.decode(jwt_cookie, None, False)
        unverified_payload2 = jwt.decode(jwt_cookie2, None, False)

        self.assertEqual(unverified_payload2.get('sso_rev'), unverified_payload.get('sso_rev') + 1,
                         'rev not incremented in cookie')

        response3 = Client().post(
            reverse('rest_login'),
            data=json.dumps(self.valid_login_after_password_change),
            content_type='application/json'
        )

        cookies3 = response3.cookies
        #print('\n\n\n RISPOSTS!', response3.data, cookies3)

        self.assertEqual(response3.status_code, 200, 'unable to login with new password')
        jwt_cookie3 = cookies3.get('jwt').value
        unverified_payload3 = jwt.decode(jwt_cookie3, None, False)

        print('\n\n\n Unv pay', unverified_payload3)

        self.assertEqual(unverified_payload2.get('sso_rev'), unverified_payload3.get('sso_rev'), 'rev changed after login')

    def test_user_password_update_refreshes_profile_even_if_called_with_authorization_headers(self):
        """
        User password update
        """

        first_rev = self.profile.sso_rev
        response = self.client.post(
            reverse('rest_login'),
            data=json.dumps(self.valid_login),
            content_type='application/json'
        )
        print('RESPONSE1', response)

        cookies = response.cookies

        self.assertEqual(response.status_code, 200, 'unable to login with valid credentials')

        received_jwt = cookies.get('jwt').value

        self.assertEqual(response.data['token'], received_jwt, 'jwt differs between cookie and response')

        response2 = Client().patch(
            '/api/v1/auth/users/{0}/'.format(self.profile.sso_id),
            data=json.dumps(self.valid_password_update),
            content_type='application/json',
            HTTP_AUTHORIZATION='Bearer {}'.format(received_jwt)
        )

        print('RESPONSE2', self.valid_password_update, response2.data)

        self.assertEqual(response2.status_code, 200, 'cannot patch with jwt inside headers')
        cookies2 = response2.cookies

        self.profile.refresh_from_db()
        second_rev = self.profile.sso_rev

        self.assertEqual(second_rev, first_rev + 1, 'rev not incremented')

        self.assertTrue(len(cookies2.keys()) > 0, 'no jwt cookie set')

        devices = self.profile.devices.all()

        self.assertEqual(devices.count(), 1, 'other devices not deleted')

        self.assertEqual(devices.first().fingerprint, self.valid_login['fingerprint'], 'device not updated')

        jwt_cookie = cookies.get('jwt').value
        jwt_cookie2 = cookies2.get('jwt').value

        # print('\nRISPOSTA, user rev', self.profile.sso_rev, '\n\nTOKEN', jwt_cookie)

        unverified_payload = jwt.decode(jwt_cookie, None, False)
        unverified_payload2 = jwt.decode(jwt_cookie2, None, False)

        self.assertEqual(unverified_payload2.get('sso_rev'), unverified_payload.get('sso_rev') + 1,
                         'rev not incremented in cookie')

        print('LOGGING IN')
        client3 = Client()
        response3 = client3.post(
            reverse('rest_login'),
            data=json.dumps(self.valid_login_after_password_change),
            content_type='application/json'
        )

        cookies3 = response3.cookies

        self.assertEqual(response3.status_code, 200, 'unable to login with new password')

        jwt_cookie3 = cookies3.get('jwt').value
        unverified_payload3 = jwt.decode(jwt_cookie3, None, False)

        self.assertEqual(unverified_payload2.get('sso_rev'), unverified_payload3.get('sso_rev'), 'rev changed after login')

    def test_user_email_update_by_staff_disables_user_login_user_must_confirm_email(self):
        """
        User update by staff refreshes disables login and deletes all user devices
        """
        first_rev = self.profile.sso_rev

        response2 = self.client.patch(
            '/api/v1/auth/users/{0}/'.format(self.profile.sso_id),
            data=json.dumps(self.valid_email_update),
            **self.staff_user_valid_token_headers
        )
        cookies2 = response2.cookies

        self.assertTrue('jwt' not in cookies2.keys(), 'jwt cookie set')

        self.profile.refresh_from_db()
        second_rev = self.profile.sso_rev

        self.assertEqual(second_rev, first_rev + 1, 'rev not incremented')

        devices = self.profile.devices.all()

        self.assertEqual(devices.count(), 0, 'user devices not deleted')

        response3 = Client().post(
            reverse('rest_login'),
            data=json.dumps(self.valid_login),
            content_type='application/json'
        )
        cookies3 = response3.cookies
        print('RESP!!!!', response3.data)

        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST,
                         'user can login without confirmating email change')

        self.assertEqual(response3.data, [_('We have sent an e-mail to you for verification. Follow the link provided to finalize the signup process. Please contact us if you do not receive it within a few minutes.')])

    def test_user_email_update_by_staff_with_skip_email_confirmation_activates_new_email(self):
        """
        User update by staff refreshes disables login and deletes all user devices
        """
        first_rev = self.profile.sso_rev

        print('\n sending patch from user', self.staff_user, 'to user', self.user, 'with new email',
              self.valid_email_update)
        response2 = self.client.patch(
            '/api/v1/auth/users/{0}/?skip_confirmation=true'.format(self.profile.sso_id),
            data=json.dumps(self.valid_email_update),
            content_type='application/json',
            HTTP_AUTHORIZATION='Token {}'.format(self.staff_user_token.key)
        )
        cookies2 = response2.cookies
        print('Patch response', response2, response2.__dict__)

        self.assertTrue('jwt' not in cookies2.keys(), 'jwt cookie set')

        self.profile.refresh_from_db()
        second_rev = self.profile.sso_rev

        self.assertEqual(second_rev, first_rev + 1, 'rev not incremented')

        devices = self.profile.devices.all()

        self.assertEqual(devices.count(), 0, 'user devices not deleted')

        print('\n Trying to login from user', self.user, 'with credentials', self.valid_login)
        response3 = self.client.post(
            reverse('rest_login'),
            data=json.dumps(self.valid_login),
            content_type='application/json'
        )
        cookies3 = response3.cookies

        print('\n Login from user', self.user, 'returns', response3.data)

        self.assertEqual(response3.status_code, 200, 'user can NOT login without confirmating email change')
