from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.test import TestCase, Client

from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress

from rest_framework.authtoken.models import Token

from django_sso_app.core.apps.services.models import Service, Subscription

User = get_user_model()


class UserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.adapter = get_adapter()

        email = self.email = "pippo@disney.com"
        username = self.username = "pippo"
        password = self.password = "paperina"
        updated_password = "pippapippa"

        username2 = "cenerentola"
        email2 = "cenerentola@disney.com"
        password2 = "tanticassi"

        self.admin_user = User.objects.create_user(username='admin', email='admin@example.com', password='admin')

        self.service = Service.objects.create(service_url='http://example.com', name='example.com')
        self.service2 = Service.objects.create(service_url='http://disney.org', name='disney.org',
                                               subscription_required=True)

        self.user = User.objects.create_user(username=username, email=email, password=password)
        self.user_email = EmailAddress.objects.create(user=self.user,
                                                      email=email,
                                                      primary=True,
                                                      verified=True)
        self.profile = self.user.sso_app_profile

        self.user_subscription = Subscription.objects.create(profile=self.profile,
                                                             service=self.service)




        self.user2 = User.objects.create_user(username=username2, email=email2, password=password2)

        self.user2_email = EmailAddress.objects.create(user=self.user2,
                                                       email=email2,
                                                       primary=True,
                                                       verified=True)
        self.profile2 = self.user2.sso_app_profile


        staff_email = staff_user_email = 'staff@example.com'

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

        self.valid_new_external_user = {
            'email': 'cane@gmail.com',
            'username': 'cane',
            'password': 'pippopluto',
            'profile': {
                'first_name': 'Pluto',
                'last_name': 'Cagnaccio',
                'ssn': '123456',
                'phone': '+39144144144',
                'description': 'Bau bau..',
                'picture': None,
                'birthdate': '1940-01-01',
                'latitide': 11.12,
                'longitude': 30.1,
                'country': 'it',
                'address': 'Viale dei cani 11, 11040, Tripoli',
                'language': 'it',
                'subscriptions': [
                    {
                        'service': {
                            'name': self.service2.name
                        }
                    }
                ]
            }
        }

        self.valid_profile_update = self.valid_new_external_user['profile']

        self.valid_new_profile = {
            'email': 'paperino@gmail.com',
            'username': 'paperino',
            'password1': 'supercacca',
            'password2': 'supercacca',
            'referrer': 'http://example.com'
        }

        self.invalid_new_profile = {
            'password': 'nonnapapera',
            'referrer': 'http://example.com'
        }

        self.valid_new_profile_hashed_pw = {
            'email': 'paperino@gmail.com',
            'username': 'paperino',
            'password': make_password('nonnapapera'),
            'referrer': 'http://example.com'
        }

        self.valid_new_profile_login = {
            'login': 'paperino',
            'password': 'nonnapapera',
            'fingerprint': '123456'
        }

        self.staff_user_valid_login = {
            'login': self.staff_user.username,
            'password': self.staff_user_password,
            'fingerprint': '123456'
        }

        self.valid_login = {
            'login': username,
            'password': password,
            'fingerprint': '123456'
        }

        self.valid_staff_login = {
            'login': self.staff_user_username,
            'password': self.staff_user_password,
            'fingerprint': '123456'
        }

        self.valid_admin_login = {
            'login': 'admin',
            'password': 'admin'
        }

        self.valid_unsubscription = {
            'password': password
        }

        self.valid_email_login = {
            'login': email,
            'password': 'paperina',
            'fingerprint': '123456'
        }
        self.valid_username_login = {
            'login': 'pippo',
            'password': 'paperina',
            'fingerprint': '123456'
        }
        self.invalid_login = {
            'login': 'topolino@disney.com',
            'password': ''
        }

        self.valid_login_after_password_change = {
            'login': username,
            'password': updated_password,
            'fingerprint': '123456'
        }

        self.valid_password_update = {
            'password': updated_password
        }

        self.valid_email_update = {
            'email': 'pippo2@gmail.com'
        }

        self.device0 = self.adapter.add_user_profile_device(self.user, '000000')
        self.device1 = self.adapter.add_user_profile_device(self.user, '111111')
        self.device2 = self.adapter.add_user_profile_device(self.user, '222222')
        self.device2.apigw_jwt_secret='secret'
        self.device2.save()

        self.migrated_user_username = 'supercacca'
        self.migrated_user_email = 'supercacca@supercacca.com'
        self.migrated_user_password = 'supercacca'
        self.migrated_user_hashed_password = 'pbkdf2_sha256$15000$KCmb0T1BofB7$fV4zlS1mFUC8HYhrgnAtEfvFzB1pgnyDloidsDLYVag='

        self.valid_migrated_user_login = {
            'login': self.migrated_user_username,
            'password': self.migrated_user_password,
            'fingerprint': '123'
        }

