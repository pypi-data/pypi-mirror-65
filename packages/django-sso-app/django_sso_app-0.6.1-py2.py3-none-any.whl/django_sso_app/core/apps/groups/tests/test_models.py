# user groups update updates user rev

from django.test import TestCase
from django.contrib.auth import get_user_model

from allauth.account.models import EmailAddress

from ...groups.models import Group
from ...profiles.models import Profile

User = get_user_model()


class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="pippo", email="pippo@disney.com")
        self.user_email = EmailAddress.objects.create(user=self.user,
                                                      email=self.user.email,
                                                      primary=True,
                                                      verified=True)
        self.group = Group.objects.create(name='new_group')
        print('Created group', self.group)


    def test_add_profile_to_group_updates_rev(self):
        user = self.user
        profile = self.user.sso_app_profile

        profile_rev = profile.sso_rev

        profile.groups.add(self.group)

        print('profile groups', profile.groups.all())

        profile.refresh_from_db()

        self.assertEqual(profile.sso_rev, profile_rev + 1)
