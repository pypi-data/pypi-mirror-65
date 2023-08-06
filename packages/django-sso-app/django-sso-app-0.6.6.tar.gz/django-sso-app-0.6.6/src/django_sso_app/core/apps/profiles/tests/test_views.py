import json

import jwt
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from rest_framework import status

from django_sso_app.backend.tests.factories import UserTestCase

from .... import app_settings

User = get_user_model()


class TestProfileRetrieve(UserTestCase):

    def test_user_can_retrieve_profile_with_subscriptions(self):
        """
          Registration via rest_auth view
        """
        print('FIRST', json.dumps(self.valid_login))

        response = self.client.post(
            reverse('rest_login'),
            data=json.dumps(self.valid_login),
            content_type='application/json'
        )
        cookies = response.cookies

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response2 = self.client.get(
            reverse('django_sso_app_profile:detail', args=(self.profile.sso_id,)),
            content_type='application/json'
        )

        self.assertEqual(response2.status_code, status.HTTP_200_OK)

        print('RISPSTA2', response2.data)

        self.assertEqual(response2.data.get('subscriptions'),
                         [{'service_url': el.service.service_url, 'is_unsubscribed': el.is_unsubscribed} for el in
                          self.profile.subscriptions.all()])


class TestProfileUpdate(UserTestCase):

    def test_profile_update_refreshes_and_returns_current_device_jwt_and_deletes_other_devices(self):
        """
        Profile update refreshes caller jwt and deletes all but caller devices
        """
        first_rev = self.profile.sso_rev
        response = self.client.post(
            reverse('rest_login'),
            data=json.dumps(self.valid_login),
            content_type='application/json'
        )
        cookies = response.cookies

        response2 = self.client.patch(
            reverse('django_sso_app_profile:detail', args=[self.profile.sso_id]),
            data=json.dumps(self.valid_profile_update),
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

        profile_object = self.valid_profile_update
        for f in app_settings.PROFILE_FIELDS:
            model_val = getattr(self.user.sso_app_profile, f, None)
            object_val = profile_object.get(f, None)

            if f == 'birthdate':
                model_val = str(model_val)
            elif f == 'country':
                object_val = object_val.upper()
                model_val = str(model_val).upper()

            self.assertEqual(model_val, object_val)


class TestCompleteUnsubscription(UserTestCase):

    def test_user_can_completely_unsubscribe_deleting_devices_and_disables_login(self):
        """
        Profile update refreshes caller jwt and deletes all but caller devices
        """
        first_rev = self.profile.sso_rev
        response = self.client.post(
            reverse('rest_login'),
            data=json.dumps(self.valid_login),
            content_type='application/json'
        )
        cookies = response.cookies

        url2 = reverse('django_sso_app_profile:complete_unsubscription', args=[self.profile.sso_id])

        response2 = self.client.post(
            url2,
            data=json.dumps(self.valid_unsubscription),
            content_type='application/json'
        )
        cookies2 = response2.cookies

        self.assertEqual(response2.status_code, status.HTTP_200_OK)

        self.profile.refresh_from_db()
        second_rev = self.profile.sso_rev
        self.assertEqual(second_rev, first_rev + 1, 'rev not incremented')

        self.assertTrue(len(cookies2.keys()) > 0, 'no jwt cookie set')

        devices = self.profile.devices.all()

        self.assertEqual(devices.count(), 0, 'devices not deleted')

        self.assertEqual(response2.data, 'Successfully completely unsubscribed.')

        response3 = Client().post(
            reverse('rest_login'),
            data=json.dumps(self.valid_login),
            content_type='application/json'
        )
        print('RESP3!!!', response3.cookies.items(), self.valid_login, response3.data, response3.status_code)

        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)
