import logging
import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from django_countries.fields import CountryField

from ..groups.models import Group
from ... import app_settings
from ...models import CreatedAtModel, UpdatableModel, DeactivableModel, PublicableModel

User = get_user_model()

logger = logging.getLogger('django_sso_app.core.apps.profiles')


class AbstractProfileModel(CreatedAtModel, UpdatableModel, DeactivableModel, PublicableModel):
    """
    Profile abstract model
    """

    class Meta:
        abstract = True

    def natural_key(self):
        return self.sso_id

    sso_id = models.CharField(_('sso id'), max_length=36, unique=True, db_index=True, default=uuid.uuid4)  # unique on not null , editable=False
    sso_rev = models.PositiveIntegerField(_('sso revision'), default=1)

    username = models.CharField(_('username'), max_length=150, null=True, blank=True)  # django
    email = models.EmailField(_('email address'), null=True, blank=True)  # django
    ssn = models.CharField(_('social security number'), max_length=255, null=True, blank=True)
    phone = models.CharField(_('phone'), max_length=255, null=True, blank=True)

    first_name = models.CharField(_('first name'), max_length=255, null=True,
                                  blank=True)
    last_name = models.CharField(_('last name'), max_length=255, null=True,
                                 blank=True)

    # role = models.SmallIntegerField(null=True, blank=True)

    description = models.TextField(_('description'), null=True, blank=True)
    picture = models.TextField(_('picture'), null=True, blank=True)
    birthdate = models.DateField(_('birthdate'), null=True, blank=True)

    latitude = models.FloatField(_('latitude'), null=True, blank=True)
    longitude = models.FloatField(_('longitude'), null=True, blank=True)

    # country = models.CharField(_('country'), max_length=46, null=True,
    #                            blank=True)
    country = CountryField(_('country'), max_length=46, null=True, blank=True)

    address = models.TextField(_('address'), null=True, blank=True)
    language = models.CharField(_('language'), max_length=3, null=True, blank=True)

    unsubscribed_at = models.DateTimeField(_('unsubscription date'), null=True, blank=True)

    @property
    def is_unsubscribed(self):
        return self.unsubscribed_at is not None

    @is_unsubscribed.setter
    def is_unsubscribed(self, value):
        self.unsubscribed_at = timezone.now()

    def get_absolute_url(self):
        return reverse("django_sso_app_profile:detail", args=[self.sso_id])

    @property
    def username(self):
        if self.user is not None:
            return self.user.username
        return self.username

    @property
    def email(self):
        if self.user is not None:
            return self.user.email
        return self.email

    def __str__(self):
        return '{}:{}:{}'.format(self.email, self.sso_id, self.username)

    @property
    def is_incomplete(self):
        if app_settings.LOGIN_MUST_FILL_PROFILE:
            for field in app_settings.REQUIRED_PROFILE_FIELDS:
                if getattr(self, field, None) in [None, '']:
                    return True

        return False


class Profile(AbstractProfileModel):
    class Meta:
        app_label = 'django_sso_app'
        verbose_name = _('Profile')

    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                null=True, blank=True,
                                verbose_name=_("user"),
                                related_name="sso_app_profile")
    apigw_consumer_id = models.CharField(_('API gateway consumer id'), max_length=36, null=True, blank=True)

    groups = models.ManyToManyField(Group, blank=True, related_name='sso_app_profiles', verbose_name=_('groups'),
                                    related_query_name='sso_app_profile')

    def save(self, *args, **kwargs):
        logger.debug('Saving profile')
        return super(Profile, self).save(*args, **kwargs)

    def update_rev(self, commit=False):
        if getattr(self, '__rev_updated', False):
            logger.debug('Rev already updated')
        else:
            logger.info(
                'Updating rev for User {}, from {} to {}, commit? {}'.format(self,
                                                                             self.sso_rev,
                                                                             self.sso_rev + 1,
                                                                             commit))

            self.sso_rev = models.F('sso_rev') + 1
            setattr(self, '__rev_updated', True)

        if commit:
            self.save()
            self.refresh_from_db()

    def add_to_group(self, group_name, creating=False):
        logger.info('Adding "{}" to group "{}"'.format(self, group_name))

        g, _created = Group.objects.get_or_create(name=group_name)
        if _created:
            logger.info('New group "{}" created'.format(g))

        if creating:
            setattr(self.user, '__django_sso_app__creating', True)

        self.groups.add(g)


class DjangoSsoAppUserStatus(object):
    def __init__(self, is_active, is_unsubscribed, is_to_subscribe):
        self.is_active = is_active
        self.is_unsubscribed = is_unsubscribed
        self.is_to_subscribe = is_to_subscribe

    def __repr__(self):
        return ("{}(is_active={}, is_unsubscribed={}, is_to_subscribe={})"
                .format(self.__class__.__name__, self.is_active,
                        self.is_unsubscribed, self.is_to_subscribe))

    @staticmethod
    def get_user_status(is_unsubscribed, subscriptions, email_verified=True):
        _is_active = app_settings.DEACTIVATE_USER_ON_UNSUBSCRIPTION

        if is_unsubscribed:  # is unsubscribed from sso
            return DjangoSsoAppUserStatus(is_active=_is_active,
                                          is_unsubscribed=True,
                                          is_to_subscribe=False)
        else:  # is still subscribed to sso
            for subscription in subscriptions:
                if subscription["service_url"] == app_settings.APP_URL:  #
                    # subscription found
                    if subscription["is_unsubscribed"]:  # user is unsubscribed from service
                        return DjangoSsoAppUserStatus(is_active=(_is_active
                                                                 and email_verified),
                                                      is_unsubscribed=True,
                                                      is_to_subscribe=False)
                    return DjangoSsoAppUserStatus(is_active=email_verified,
                                                  is_unsubscribed=False,
                                                  is_to_subscribe=False)

            # is NOT subscribed
            return DjangoSsoAppUserStatus(
                is_active=email_verified, is_unsubscribed=False,
                is_to_subscribe=app_settings.SERVICE_SUBSCRIPTION_IS_MANDATORY)
