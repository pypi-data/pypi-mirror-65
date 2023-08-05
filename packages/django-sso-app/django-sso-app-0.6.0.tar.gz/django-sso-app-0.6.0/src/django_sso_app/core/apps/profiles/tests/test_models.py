# profile filed update updates rev

from django.contrib.auth import get_user_model

from django_sso_app.backend.tests.factories import UserTestCase

User = get_user_model()


class ProfileTestCase(UserTestCase):

    def test_profile_field_update_updates_rev(self):
        """
        User update updates user revision
        """

        profile_rev = self.profile.sso_rev

        self.profile.country = 'IT'
        self.profile.save()

        self.profile.refresh_from_db()

        self.assertEqual(self.profile.sso_rev, profile_rev + 1)
