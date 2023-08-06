import logging

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in

from ....permissions import is_staff
from ..utils import get_or_create_user_profile
from ..models import Profile

logger = logging.getLogger('django_sso_app.core.apps.profiles.signals')

User = get_user_model()


@receiver(pre_save, sender=Profile)
def profile_pre_updated(sender, instance, **kwargs):
    """
    Profile model has been updated, updating rev
    """
    if kwargs['raw']:
        # https://github.com/django/django/commit/18a2fb19074ce6789639b62710c279a711dabf97
        return

    if not instance._state.adding:
        user = instance.user

        if not user.is_superuser:
            if getattr(user, '__django_sso_app__apigateway_update', False):
                logger.debug('Profile has been updted by api gateway, skipping rev update')
            elif getattr(user, '__django_sso_app__creating', False):
                logger.debug('Created, skipping rev update')
            else:
                logger.debug('Profile model has been updated, updating rev')
                instance.update_rev(False)


@receiver(post_save, sender=Profile)
def profile_updated(sender, instance, created, **kwargs):
    """
    Profile model has been updated, updating rev
    """
    profile = instance

    if kwargs['raw']:
        # https://github.com/django/django/commit/18a2fb19074ce6789639b62710c279a711dabf97
        setattr(profile.user, '__django_sso_app__loaddata', True)
        return

    if not created:  # if instance.pk:
        logger.debug('Profile model has been updated, refreshing instance')
        profile.refresh_from_db()

# user

@receiver(post_save, sender=User)
def create_update_user_profile(sender, instance, created, **kwargs):
    if kwargs['raw']:
        # https://github.com/django/django/commit/18a2fb19074ce6789639b62710c279a711dabf97
        # setting property flag
        setattr(instance, '__django_sso_app__loaddata', True)
        return

    user = instance

    if not user.is_superuser:

        if created:
            logger.debug('user created, creating profile')

            profile = get_or_create_user_profile(user, Profile, commit=True)

            logger.debug('new profile created "{}"'.format(profile))

            # refreshing user instance
            user.sso_app_profile = profile

        else:
            profile = get_or_create_user_profile(user, Profile, commit=False)
            update_rev = True

            # replaced by '__user_loggin_in'
            # if user.previous_serialized_as_string == user.serialized_as_string:
            if getattr(user, '__django_sso_app__creating', False):
                update_rev = False
            if getattr(user, '__django_sso_app__user_loggin_in', False):
                update_rev = False
            if user.password_has_been_hardened:
                update_rev = False
            if getattr(user, '__django_sso_app__email_updated', False):
                update_rev = True
            if getattr(user, '__django_sso_app__password_updated', False):
                update_rev = True

            if update_rev:
                logger.info('Update rev by User signal while user fields have been updated')
                profile.update_rev(True)  # updating rev


@receiver(user_logged_in)
def post_user_login(**kwargs):
    """
    Post login profile creation safety
    :param kwargs:
    :return:
    """
    user = kwargs['user']

    if not user.is_superuser:
        _profile = get_or_create_user_profile(user, Profile)
        # setattr(user, 'sso_app_profile', _profile)

        logger.debug('Profile, "{}" LOGGED IN!!!'.format(_profile))
