import os
import datetime
import binascii
from random import seed, randint
import base64

from django.core.management.utils import get_random_secret_key

from .exceptions import ProfileIncompleteException, DectivatedUserException, UnsubscribedUserException
from .permissions import is_staff, is_authenticated
from . import app_settings

# initializing seed
SEED = int(base64.b16encode(bytes(get_random_secret_key(), 'utf-8')), 16)
seed(SEED)


def set_cookie(response, key, value, days_expire=None):
    """
    Sets response auth cookie

    :param response:
    :param key:
    :param value:
    :param days_expire:
    :return:
    """
    if days_expire is None:
        max_age = app_settings.COOKIE_AGE  # django default
    else:
        max_age = days_expire * 24 * 60 * 60

    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
                                         "%a, %d-%b-%Y %H:%M:%S GMT")

    response.set_cookie(key, value, max_age=None, expires=expires, path='/',
                        domain=app_settings.COOKIE_DOMAIN,
                        secure=None,
                        httponly=app_settings.COOKIE_HTTPONLY)


def invalidate_cookie(response, key):
    """
    Sets response auth cookie to 'Null'

    :param response:
    :param key:
    :return:
    """
    response.set_cookie(key, None, max_age=None, expires='Thu, 01 Jan 1970 00:00:01 GMT', path='/',
                        domain=app_settings.COOKIE_DOMAIN, secure=None, httponly=False)


def set_session_key(request, key, value):
    """
    Sets django sessions request key
    :param request:
    :param key:
    :param value:
    :return:
    """
    # set session key
    request.session[key] = value


def get_session_key(request, key, default=None):
    """
    Gets django sessions request key
    :param request:
    :param key:
    :param default:
    :return:
    """
    # get session key
    return request.session.get(key, default)

""" noqa
# Must use functions above because of django restframework
# swapping the original request object instance with a new one..

def set_session_key(request, key, value):
    # set request key
    setattr(request, key, value)

def get_session_key(request, key, default=None):
    # get request key
    return getattr(request, key, default)
"""


def check_user_can_login(user):
    """
    Check user login ability
    :param user:
    :return:
    """

    if is_authenticated(user) and not user.is_superuser:
        if not user.is_active:
            raise DectivatedUserException()
        else:
            if user.sso_app_profile.is_unsubscribed:
                raise UnsubscribedUserException()
            else:
                if app_settings.BACKEND_ENABLED and app_settings.BACKEND_SIGNUP_MUST_FILL_PROFILE:
                    if user.sso_app_profile.is_incomplete:
                        raise ProfileIncompleteException('Must fill in profile.')


def is_test_user(user):
    """
    Chack if user is TEST_USER
    :param user:
    :return:
    """

    return user.username == app_settings.TEST_USER_USERNAME or user.email == app_settings.TEST_USER_EMAIL


def get_random_token(length=4):
    """
    Returns random token
    :param request:
    :return:
    """
    start = randint(0, 4095 - length)
    end = start + length

    return binascii.hexlify(os.urandom(2048)).decode("utf-8")[start:end]


def get_random_fingerprint(request):
    """
    Returns random fingerprint
    :param request:
    :return:
    """
    return 'random_{}_{}'.format(id(request), get_random_token(8))
