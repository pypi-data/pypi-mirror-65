import logging

from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import pre_save, post_save

from allauth.account.adapter import get_adapter

from ....utils import set_session_key
from ....tokens.utils import jwt_encode
from ....permissions import is_staff
from ..utils import get_request_device
from ....functions import get_random_string
from ...profiles.models import Profile
from ..models import Device
from .... import app_settings

logger = logging.getLogger('django_sso_app.core.apps.devices.signals')
adapter = get_adapter()


# profile

@receiver(post_save, sender=Profile)
def post_profile_saved(sender, instance, created, **kwargs):
    if kwargs['raw']:
        # https://github.com/django/django/commit/18a2fb19074ce6789639b62710c279a711dabf97
        return

    if not created:  # if instance.pk:
        profile = instance

        logger.debug('Profile "{}" post_save signal'.format(profile))

        rev_updated = getattr(profile, '__rev_updated', False)

        if rev_updated:
            logger.info('Rev updated, removing all user devices for Profile "{}"'.format(profile))

            adapter.remove_all_user_profile_devices(profile.user)


# device

@receiver(pre_save, sender=Device)
def pre_device_save(sender, instance, **kwargs):
    if not app_settings.APIGATEWAY_ENABLED:
        user = instance.profile.user
        device = instance

        if not user.is_superuser:
            logger.debug('Skip creating api gateway JWT for Device "{}"'.format(device))

            device.apigw_jwt_id = None
            device.apigw_jwt_key = None
            device.apigw_jwt_secret = get_random_string(32)


@receiver(user_logged_in)
def post_user_login(**kwargs):
    user = kwargs['user']

    if not user.is_superuser:
        request = kwargs['request']

        logger.debug('Devices, "{}" LOGGED IN!!!'.format(user))

        device = get_request_device(request)
        token = jwt_encode(device.get_jwt_payload(), device.apigw_jwt_secret)

        set_session_key(request, '__django_sso_app__jwt_token', token)
