from django.contrib.auth import get_user_model

from django_sso_app.backend.tests.factories import UserTestCase
from django_sso_app.core.apps.emails.models import EmailAddress

User = get_user_model()


class TestEmailAddress(UserTestCase):

    def test_user_email_deletes_other_user_emails_when_primary_and_verified(self):
        self.assertEqual(self.user.emailaddress_set.count(), 1)

        new_email = EmailAddress.objects.create(user=self.user, email='email2@example.com')

        self.assertEqual(self.user.emailaddress_set.count(), 2)

        new_email.primary = True
        new_email.verified = True
        new_email.save()

        self.assertEqual(self.user.emailaddress_set.count(), 1, 'other user email not confirmed')
