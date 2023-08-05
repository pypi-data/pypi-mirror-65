import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

from ..groups.models import Group
from ..profiles.models import Profile
from ...models import CreatedAtModel, UpdatableModel, PublicableModel, DeactivableModel

logger = logging.getLogger('django_sso_app.core.apps.services')


class Service(CreatedAtModel, UpdatableModel, PublicableModel, DeactivableModel):
    class Meta:
        app_label = 'django_sso_app'
        verbose_name = _('Service')

    name = models.CharField(_('name'), max_length=32, unique=True, null=True)
    service_url = models.CharField(_('service url'), max_length=255, unique=True)
    picture = models.TextField(_('picture'), null=True, blank=True)

    cookie_domain = models.CharField(_('cookie domain'), max_length=255, null=True, blank=True)  # unused but useful
    redirect_wait = models.PositiveIntegerField(_('redirect wait'), default=2000)

    subscription_required = models.BooleanField(_('subscription required'), default=False)
    is_public = models.BooleanField(_('is public'), default=True)

    groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True,
                                    related_name='sso_app_services', related_query_name='sso_app_service')

    def get_tos(self, language):
        logger.debug('Service {0}, gettings tos for language {1}'.format(self, language))
        return self.terms_of_service.filter(language=language).first()

    def __str__(self):
        return '{}:{}'.format(self.name, self.service_url)

    def get_absolute_url(self):
        return reverse("django_sso_app_service:detail", args=[self.pk])


class TOS(CreatedAtModel, UpdatableModel, DeactivableModel):
    class Meta:
        app_label = 'django_sso_app'
        verbose_name = _('TOS')

    language = models.CharField(_('language'), max_length=35)
    text = models.TextField(_('text'), default='')

    service = models.ForeignKey(Service, related_name="terms_of_service", on_delete=models.CASCADE,
                                verbose_name=_('service'))

    def __str__(self):
        return '{}:{}'.format(self.id, self.language)


class Subscription(CreatedAtModel, UpdatableModel, DeactivableModel, PublicableModel):
    class Meta:
        app_label = 'django_sso_app'
        verbose_name = _('Subscription')

    profile = models.ForeignKey(
        Profile,
        to_field='sso_id',
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name=_('profile')
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name=_('service')
    )
    unsubscribed_at = models.DateTimeField(_('unsubscribed at'), null=True, blank=True)

    @property
    def is_unsubscribed(self):
        return self.unsubscribed_at is not None

    @property
    def is_subscribed(self):
        return self.unsubscribed_at is None

    @property
    def user(self):
        return self.profile.user

    def __str__(self):
        return '{}@{}'.format(self.profile, self.service.service_url)

    def get_absolute_url(self):
        return reverse("django_sso_app_service:subscription-detail", args=[self.pk])
