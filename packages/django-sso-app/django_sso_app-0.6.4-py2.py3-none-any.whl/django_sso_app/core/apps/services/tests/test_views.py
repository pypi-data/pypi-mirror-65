import json

import jwt
from django.urls import reverse
from rest_framework import status

from ...users.tests.test_views import UserTestCase


class TestSubscriptions(UserTestCase):

    def test_user_can_list_subscriptions(self):
        """
        """
        response = self.client.post(
            reverse('rest_login'),
            data=json.dumps(self.valid_login),
            content_type='application/json'
        )
        cookies = response.cookies

        response2 = self.client.get(
            reverse('django_sso_app_service:subscription-list'),
            content_type='application/json'
        )
        print('RESP!!!', response2.json())
        print('dfasdfdsf', self.profile.subscriptions.all())

        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response2.data['results']), 1)
        self.assertEqual(response2.data['results'][0].get('service').get('service_url'), self.service.service_url)


    def test_user_can_retrieve_subscription(self):
        response = self.client.post(
            reverse('rest_login'),
            data = json.dumps(self.valid_login),
            content_type='application/json'
        )
        cookies = response.cookies

        response2 = self.client.get(
            reverse('django_sso_app_service:subscription-detail', args=(self.user_subscription.id,)),
            content_type='application/json'
        )

        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data.get('is_unsubscribed'), False)



class TestServices(UserTestCase):

    def test_user_can_list_services(self):
        """
        """
        response = self.client.post(
            reverse('rest_login'),
            data = json.dumps(self.valid_login),
            content_type='application/json'
        )
        cookies = response.cookies

        response2 = self.client.get(
            reverse('django_sso_app_service:list'),
            content_type='application/json'
        )

        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response2.data['results']), 2)

    def test_user_can_retrieve_service(self):
        """
        """
        response = self.client.post(
            reverse('rest_login'),
            data = json.dumps(self.valid_login),
            content_type='application/json'
        )
        cookies = response.cookies

        response2 = self.client.get(
            reverse('django_sso_app_service:detail', args=(self.service.id, )),
            content_type='application/json'
        )

        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data.get('service_url'), self.service.service_url)

    def test_user_can_not_subscribe_profile_to_service_twice(self):
        """
        """
        response = self.client.post(
            reverse('rest_login'),
            data = json.dumps(self.valid_login),
            content_type='application/json'
        )
        cookies = response.cookies

        response2 = self.client.post(
            reverse('django_sso_app_service:subscription', args=(self.service.id, )),
            content_type='application/json'
        )

        self.assertEqual(response2.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response2.data, 'Already subscribed.')

    def test_user_can_subscribe_to_service_with_rev_incremented_and_devices_deleted(self):
        """
        """
        first_rev = self.profile.sso_rev
        response = self.client.post(
            reverse('rest_login'),
            data=json.dumps(self.valid_login),
            content_type='application/json'
        )
        cookies = response.cookies
        first_devices = self.profile.devices.all()
        first_devices = [x.id for x in first_devices]

        response2 = self.client.post(
            reverse('django_sso_app_service:subscription', args=(self.service2.id, )),
            content_type='application/json'
        )

        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

        self.profile.refresh_from_db()

        self.assertEqual(response2.data, 'Successfully subscribed.')

        self.profile.refresh_from_db()
        second_rev = self.profile.sso_rev

        self.assertEqual(second_rev, first_rev+1, 'rev not incremented')

        response3 = self.client.get(
            reverse('django_sso_app_service:list'),
            content_type='application/json'
        )

        self.assertEqual(response3.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response3.data['results']), 2)

        cookies2 = response2.cookies
        jwt_cookie2 = cookies2.get('jwt').value
        unverified_payload2 = jwt.decode(jwt_cookie2, None, False)

        print('\n\n\n Unv pay', unverified_payload2)

        self.assertEqual(unverified_payload2.get('sso_rev'), second_rev, 'cookie rev NOT changed after login')

        second_devices = self.profile.devices.all()
        second_devices = [x.id for x in second_devices]

        print('\n\n DEVICES', first_devices, second_devices)
        self.assertEqual(len(second_devices), 1)

    def test_user_can_unsubscribe_profile_from_service_with_rev_incremented(self):
        first_rev = self.profile.sso_rev

        response = self.client.post(
            reverse('rest_login'),
            data = json.dumps(self.valid_login),
            content_type='application/json'
        )
        cookies = response.cookies

        response2 = self.client.post(
            reverse('django_sso_app_service:unsubscription', args=(self.service.id, )),
            data=json.dumps(self.valid_unsubscription),
            content_type='application/json'
        )
        cookies2 = response2.cookies

        print('\n\nRISPOSTA', response2.json())

        self.assertEqual(response2.status_code, status.HTTP_200_OK)

        self.assertEqual(response2.data, 'Successfully unsubscribed.')

        self.profile.refresh_from_db()
        second_rev = self.profile.sso_rev

        self.assertEqual(second_rev, first_rev+1, 'rev not incremented on service unsubscription')

        jwt_cookie = cookies2.get('jwt')
        self.assertNotEqual(jwt_cookie, None, 'no new jwt received')

        unverified_payload = jwt.decode(jwt_cookie.value, None, False)

        print('\n\n\n Unv pay', unverified_payload)

        self.assertEqual(unverified_payload.get('sso_rev'), second_rev, 'rev NOT updated in JWT')

    def test_staff_user_can_subscribe_profile_to_service_with_profile_rev_incremented(self):
        first_rev = self.profile.sso_rev

        response = self.client.post(
            reverse('rest_login'),
            data=json.dumps(self.valid_staff_login),
            content_type='application/json'
        )
        cookies = response.cookies

        response2 = self.client.post(
            reverse('django_sso_app_service:subscription', args=(self.service2.id, )),
            data=json.dumps({'sso_id': str(self.profile.sso_id)}),
            content_type='application/json'
        )
        cookies2 = response2.cookies

        print('\n\nRISPOSTA', response2.json())

        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response2.data, 'Successfully subscribed.')

        self.profile.refresh_from_db()
        second_rev = self.profile.sso_rev

        self.assertEqual(second_rev, first_rev+1, 'rev not incremented on service subscription')

