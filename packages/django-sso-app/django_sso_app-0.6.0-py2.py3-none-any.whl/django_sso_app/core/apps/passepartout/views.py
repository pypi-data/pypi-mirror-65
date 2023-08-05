import logging
from urllib.parse import urlencode, urljoin

# import pyximport
# pyximport.install()

from django.http import Http404
from django.shortcuts import redirect, reverse
# from django.views.decorators.csrf import csrf_exempt

# from rest_framework.response import Response
# from rest_framework import status

from allauth.account.adapter import get_adapter

from ..services.models import Service
from ...utils import invalidate_cookie, set_cookie, set_session_key, get_session_key
from ...permissions import is_authenticated
from ...functions import get_url_host
from ... import app_settings
from .models import Passepartout
from .functions import get_referrer

logger = logging.getLogger('django_sso_app.core.apps.passepartout')


# @csrf_exempt
def passepartout_login_view(request, token):
    """
    Receives unguessable token by path parameter and destination url by get parameter.
    1) checks user subscription to destination service (obtained by next param as Service url)
    2) checks its position in DJANGO_SSO_APP_URLS ordered dictionary
    3) redirects to next APP_URL if there are subsquent sso domains or directly to service url (if redirecting to APP_URL request will include a jwt token COOKIES)
    """
    try:
        nextUrl = request.GET.get('next', None)
        logger.debug('ENTERING passepartout with next {}'.format(nextUrl))

        if nextUrl is None:
            raise Http404("No next url")

        try:
            passepartout = Passepartout.objects.get(deleted=False, token=token)

        except Passepartout.DoesNotExist:
            logger.error("Passepartout not found, invalidating cookie")

            response = redirect(reverse('account_login'))
            invalidate_cookie(response, app_settings.JWT_COOKIE_NAME)

            return response

        referrer = request.META.get('HTTP_REFERER', None)
        if referrer is None:
            referrer = get_referrer(app_settings.APP_DOMAIN,
                                    app_settings.BACKEND_DOMAINS_DICT,
                                    app_settings.BACKEND_DOMAINS,
                                    app_settings.BACKEND_FULL_URLS_CHAIN)

        comes_from = get_url_host(referrer)
        sso_urls_chain = app_settings.BACKEND_URLS_CHAIN
        sso_urls_chain_dict = app_settings.BACKEND_URLS_CHAIN_DICT
        logger.debug('Passepartout chain dict: {0}, this is: {1}. Comes from {2} with nextUrl: {3}'.format(sso_urls_chain,
                                                                                                           app_settings.COOKIE_DOMAIN,
                                                                                                           comes_from,
                                                                                                           nextUrl))

        previous_sso_instance_index = sso_urls_chain_dict[comes_from]
        last_sso_instance_index = len(sso_urls_chain) - 1
        next_sso_instance_index = last_sso_instance_index + 1

        is_last_bump = previous_sso_instance_index == last_sso_instance_index
        goes_to = None
        redirect_args = None

        next_url_base_path = get_url_host(nextUrl)
        if next_url_base_path is None:
            if is_last_bump:
                next_url_base_path = sso_urls_chain[last_sso_instance_index]
            else:
                next_url_base_path = get_url_host(referrer)

            oldNextUrl = nextUrl
            nextUrl = urljoin(next_url_base_path, nextUrl)

            logger.debug('next url "{}" has no base_path, setting "{}"'.format(oldNextUrl, nextUrl))

        if next_url_base_path not in app_settings.BACKEND_FULL_URLS_CHAIN:
            try:
                _service = Service.objects.get(service_url=next_url_base_path)
            except Service.DoesNotExist:
                raise Http404("Service not found")

        set_session_key(request, '__django_sso_app__device__fingerprint', passepartout.device.fingerprint)

        if is_last_bump:
            logger.info('Is last login bump')
            passepartout.deleted = True
            passepartout.save()
            goes_to = nextUrl
        else:
            redirect_args = {
                'next': nextUrl
            }
            goes_to = sso_urls_chain[next_sso_instance_index]

        # if subscribed is None:
        #    subscrition_created = user.subscribe_to_service(service)
        #    logger.info('Did passepartout subscribed user, {0} to {2}? {3}'.format(user, nextUrl, subscription_created))
        #    redirect_args['subscribed'] = 'true'

        formatted_redirect_args = ''
        if not is_last_bump:
            formatted_redirect_args = '?' + urlencode(redirect_args)

        redirect_to = goes_to + formatted_redirect_args
        logger.info('Passepartout login redirecting to {0}'.format(redirect_to))

        response = redirect(redirect_to)

        user = passepartout.device.profile.user

        adapter = get_adapter(request)

        try:
            adapter.login(request, user)

        except Exception as e:
            logger.exception('adapter login error {}, invalidating cookie'.format(e))
            invalidate_cookie(response, app_settings.JWT_COOKIE_NAME)  # invalidate cookie

        else:
            if is_authenticated(user):
                token = get_session_key(request, '__django_sso_app__jwt_token', None)
                if token is None:
                    logger.error('no token in session')
                    raise Exception('no token in session')
                else:
                    set_cookie(response, app_settings.JWT_COOKIE_NAME, token, None)
            else:
                logger.warning('user "{}" can not authenticate'.format(user))

    except Exception as e:
        logger.error('Passepartout login ERROR: {}'.format(e), exc_info=True)
        raise

    return response
