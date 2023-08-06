import logging

# import pyximport
# pyximport.install()

from django.contrib.auth import get_user_model

from ...utils import is_test_user
from ... import app_settings

User = get_user_model()

logger = logging.getLogger('django_sso_app.core.apps.profiles')


def update_profile(profile, update_object, commit=True):
    logger.info('Updating profile fields for "{}"'.format(profile))

    for f in app_settings.PROFILE_FIELDS + ('sso_rev', ):
        if hasattr(profile, f):
            new_val = update_object.get(f, None)
            if new_val is not None:
                setattr(profile, f, new_val)
                logger.debug('profile field updated "{}":"{}"'.format(f, new_val if f != 'password' else '*'))

    if commit:
        profile.save()

    return profile


def get_or_create_user_profile(user, ProfileModel, initials=None, commit=True):
    logger.debug('get or create user profile')

    try:
        profile = user.sso_app_profile

    except ProfileModel.DoesNotExist:
        logger.info('User "{}" has no profile, creating one'.format(user))

        # set creating flag to disable rev update
        # setattr(user, '__django_sso_app__creating', True)

        sso_id = getattr(user, '__django_sso_app__profile__sso_id', None)
        if sso_id is not None:
            sso_rev = getattr(user, '__django_sso_app__profile__sso_rev', 0)
            profile = ProfileModel(user=user, sso_id=sso_id, sso_rev=sso_rev)

        else:
            profile = ProfileModel(user=user)

        if is_test_user(user):
            logger.info('User "{}" is TEST_USER, setting sso_id="{}"'.format(user, app_settings.TEST_USER_USERNAME))

            profile.sso_id = app_settings.TEST_USER_USERNAME

        if initials is not None:
            profile = update_profile(profile, initials, commit=False)

        if commit:
            profile.save()

    # force user sso_app_profile object field
    setattr(user, 'sso_app_profile', profile)

    return profile
