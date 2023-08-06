import logging

from django.urls import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.hashers import get_hasher, identify_hasher

from ... import app_settings

logger = logging.getLogger('django_sso_app.core.apps.users')


class DjangoSsoAppUserModelMixin(object):
    # username = models.CharField(_('username'), max_length=150, unique=True)  # django
    email = models.EmailField(_('email address'), blank=True)  # django

    """
    @property
    def previous_serialized_as_string(self):
        return getattr(self, '__serialized_as_string')

    @property
    def serialized_as_string(self):
        serialized = ''
        for f in app_settings.USER_FIELDS + ('password', 'is_active'):
            serialized += '__' + str(getattr(self, f, None))

        logger.debug('serialized_as_string {}'.format(serialized))
        return serialized
    """

    @property
    def email_has_been_updated(self):
        return getattr(self, '__django_sso_app__old_email', None) != self.email

    @property
    def password_has_been_hardened(self):
        has_password = getattr(self, '__django_sso_app__old_password', self.password) not in [None, '']

        if has_password:
            old_hashed_password = getattr(self, '__django_sso_app__old_password')
            old_hasher = identify_hasher(old_hashed_password)
            new_hashed_password = self.password
            new_hasher = identify_hasher(new_hashed_password)

            try:
                hasher = get_hasher('default')
                return hasher.must_update(old_hashed_password)

            except AssertionError:
                logger.exception('Error checking password hardened')
                return old_hasher != new_hasher
        else:
            return False

    def __init__(self, *args, **kwargs):
        super(DjangoSsoAppUserModelMixin, self).__init__(*args, **kwargs)
        setattr(self, '__django_sso_app__old_password', self.password)
        setattr(self, '__django_sso_app__old_email', self.email)
        # setattr(self, '__serialized_as_string', self.serialized_as_string)  # replaced by '..__user_loggin_in'

    def get_absolute_url(self):
        profile = self.get_sso_app_profile()
        if profile is not None:
            return reverse("django_sso_app_user:detail", kwargs={"sso_id": profile.sso_id})

    def get_sso_app_profile(self):
        return getattr(self, 'sso_app_profile', None)

    @property
    def sso_id(self):
        profile = self.get_sso_app_profile()
        if profile is not None:
            return profile.sso_id

        return None

    @property
    def sso_rev(self):
        profile = self.get_sso_app_profile()
        if profile is not None:
            return profile.sso_rev

        return 0

    @property
    def sso_app_profile__sso_id(self):
        return self.sso_id

    @property
    def is_unsubscribed(self):
        profile = self.get_sso_app_profile()
        if profile is not None:
            return profile.is_unsubscribed

        return not self.is_active
