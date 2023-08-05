import json
import logging

import requests

from django.db import transaction
from django.utils.encoding import smart_str
from django.contrib.auth import get_user_model

from allauth.account.models import EmailAddress

from ... import app_settings
from ..api_gateway.kong.functions import get_apigateway_sso_id
from ..profiles.utils import update_profile, get_or_create_user_profile
from ..profiles.models import Profile

logger = logging.getLogger('django_sso_app.core.apps.users')
User = get_user_model()


def fetch_remote_user(sso_id, encoded_jwt=None):
    """
    Fetches user model from remote django-sso-app backend
    :param sso_id:
    :param encoded_jwt:
    :return:
    """
    logger.info("Getting SSO profile for ID {} ...".format(sso_id))

    if encoded_jwt is None:
        headers = {
            "Authorization": "Token {}".format(app_settings.BACKEND_STAFF_TOKEN)
        }
    else:
        headers = {
            "Authorization": "Bearer {}".format(encoded_jwt)
        }

    url = app_settings.REMOTE_USER_URL.format(sso_id=sso_id) + '?with_password=true'

    response = requests.get(url=url, headers=headers, timeout=10, verify=False)
    response.raise_for_status()
    sso_user = response.json()

    logger.info("Retrieved SSO profile for ID {}".format(sso_id))

    return sso_user


def update_user(user, update_object, commit=True):
    logger.info('Updating user fields for "{}"'.format(user))

    for f in app_settings.USER_FIELDS + ('password', 'is_active', 'date_joined'):
        if hasattr(user, f):
            new_val = update_object.get(f, None)
            if new_val is not None:
                setattr(user, f, new_val)
                logger.debug('profile field updated "{}":"{}"'.format(f, new_val if f != 'password' else '*'))

    if commit:
        user.save()

    return user


def check_remote_user_existence_by_username(username):
    logger.info('Checking with SSO Backend if user {} already exists ...'
                .format(smart_str(username)))

    url = app_settings.BACKEND_USERS_CHECK_URL
    params = {
        'username': username
    }
    response = requests.get(url=url, params=params, timeout=10, verify=False)
    response.raise_for_status()

    if response.status_code == requests.codes.NOT_FOUND:
        logger.info('User {} does NOT exist'.format(smart_str(username)))

        return None

    sso_id = json.loads(response.text).get('sso_id', None)

    logger.info('User {} already exists with SSO ID {}'
                .format(smart_str(username), sso_id))

    return sso_id


def check_remote_user_existence_by_email(email):
    logger.info('Checking with SSO if a user with email {} already exists ...'
                .format(smart_str(email)))

    url = app_settings.REMOTE_USERS_CHECK_URL
    params = {
        'email': email
    }
    response = requests.get(url=url, params=params, timeout=10, verify=False)
    response.raise_for_status()

    if response.status_code == requests.codes.NOT_FOUND:
        logger.info('A user with email {} does NOT exist'
                    .format(smart_str(email)))

        return None

    sso_id = json.loads(response.text).get('sso_id', None)

    logger.info('A user with email {} already exists with SSO ID {}'
                .format(smart_str(email), sso_id))

    return sso_id


def get_remote_user_by_sso_id(sso_id):
    logger.info('Getting remote user with sso_id "{}"'.format(sso_id))

    url = app_settings.REMOTE_USER_URL.format(sso_id=sso_id) + '?with_password=true'
    params = {
        'sso_id': sso_id
    }
    response = requests.get(url=url, params=params, timeout=10, verify=False)
    response.raise_for_status()

    if response.status_code == requests.codes.NOT_FOUND:
        logger.info('A user with sso_id "{}" does NOT exist'.format(smart_str(sso_id)))
        return

    response_data = json.loads(response.text)
    sso_id = response_data.get('sso_id', None)

    if sso_id is None:
        logger.warning('No user with sso_id "{}" found'.format(sso_id))
        return

    logger.info('A user with sso_id "{}" exists'.format(smart_str(sso_id)))
    return response_data


def create_local_user_from_object(user_object, verified=False):
    logger.info('Creating local user from object "{}". Verified: {}'.format(user_object, verified))

    username = user_object.get('username')
    email = user_object.get('email')
    sso_id = user_object.get('sso_id', None)
    sso_rev = user_object.get('sso_rev', 0)

    if sso_id is not None:
        sso_id = smart_str(sso_id)

        if User.objects.filter(sso_app_profile__sso_id=sso_id).count() > 0:
            raise Exception('Profile with sso_id "{}" already present'.format(sso_id))

        logger.info('Creating local user with sso_id "{}" and sso_rev "{}" ...'.format(sso_id, sso_rev))

    if User.objects.filter(username=username).count() > 0:
        raise Exception('User with username "{}" already present'.format(username))

    if User.objects.filter(email=email).count() > 0:
        raise Exception('User with email "{}" already present'.format(email))

    new_user = User()

    setattr(new_user, '__django_sso_app__creating', True)
    setattr(new_user, '__django_sso_app__profile__sso_id', sso_id)
    setattr(new_user, '__django_sso_app__profile__sso_rev', sso_rev)

    # saving model there (commit) implies profile creation with pre-defined attrs sso_id, sso_rev
    new_user = update_user(new_user, user_object, commit=True)

    email = user_object.get('email', None)

    if email is not None:
        if EmailAddress.objects.filter(email__iexact=email).count() > 0:
            raise Exception('EmailAddress already present')

        created_email = EmailAddress.objects.create(user=new_user,
                                                    email=email,
                                                    verified=verified,
                                                    primary=True)
        logger.info(
            'A new EmailAddress for {0} has been created with id {1}'
            ''.format(
                email, created_email.id))

        if verified:
            logger.info(
                '{0} must NOT confirm email {1}'.format(new_user, email))
        else:
            logger.info(
                '{0} must confirm email {1}'.format(new_user, email))

    logger.info('local user created "{}"'.format(new_user))

    return new_user


@transaction.atomic
def create_local_user_from_remote_backend(remote_user, can_subscribe=False):
    # Creates new user only by profile object
    remote_user_profile_object = remote_user.get('profile')

    new_user = create_local_user_from_object(remote_user_profile_object,
                                             verified=getattr(remote_user, 'email_verified', False))

    setattr(new_user, '__django_sso_app__remote_user', remote_user)  # noqa (subscription required)

    setattr(new_user, 'sso_app_profile', get_or_create_user_profile(new_user, Profile, remote_user_profile_object))

    return new_user


@transaction.atomic
def create_local_user_from_apigateway_headers(request):
    consumer_username = request.META.get(app_settings.APIGATEWAY_CONSUMER_USERNAME_HEADER)
    logger.info('Creating local user from apigateway consumer username "{}"'.format(smart_str(consumer_username)))

    sso_id = get_apigateway_sso_id(consumer_username)
    sso_rev = 0
    username = consumer_username
    temporary_email = '{}@{}'.format(sso_id, app_settings.APP_DOMAIN)

    profile_object = {
        'sso_id': sso_id,
        'sso_rev': sso_rev,
        'username': username,
        'email': temporary_email
    }

    new_user = create_local_user_from_object(profile_object)

    #setattr(new_user, 'sso_app_profile', get_or_create_user_profile(new_user, Profile, profile_object))

    return new_user


@transaction.atomic
def create_local_user_from_jwt(decoded_jwt):
    logger.info('Creating local user from jwt')

    sso_id = decoded_jwt.get('sso_id')
    sso_rev = decoded_jwt.get('sso_rev')
    username = decoded_jwt.get('username', sso_id)
    temporary_email = '{}@{}'.format(sso_id, app_settings.APP_DOMAIN)

    profile_object = {
        'sso_id': sso_id,
        'sso_rev': sso_rev,
        'username': username,
        'email': temporary_email
    }

    new_user = create_local_user_from_object(profile_object)

    #setattr(new_user, 'sso_app_profile', get_or_create_user_profile(new_user, Profile, profile_object))

    return new_user


@transaction.atomic
def update_local_user_from_remote_backend(remote_user, profile, commit=True):
    assert profile is not None

    sso_id = profile.sso_id
    remote_object_profile = remote_user['profile']

    logger.info('Updating local profile with sso_id "{}" ...'.format(sso_id))
    user = update_user(profile.user, remote_user, commit)

    setattr(user, '__django_sso_app__remote_user', remote_user)

    setattr(user, 'sso_app_profile', update_profile(profile, remote_object_profile, commit))

    return user
