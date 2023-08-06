import logging

from urllib.parse import urlencode

# import pyximport
# pyximport.install()

from django.shortcuts import reverse

from ...utils import get_session_key, set_session_key
from ...permissions import is_staff
from ... import app_settings
from ..devices.utils import get_request_device

from .models import Passepartout
from .functions import get_next_bump

logger = logging.getLogger('django_sso_app.core.apps.passepartout')


def get_passepartout_login_redirect_url(request):
    if request.user.is_superuser:
        return None

    if app_settings.PASSEPARTOUT_PROCESS_ENABLED:
        redirect_url = get_session_key(request, '__django_sso_app__passepartout__redirect_url')

        if redirect_url is None:
            logger.info(
                'Passepartout login enabled, BACKEND_URLS_CHAIN: {0}'.format(
                    app_settings.BACKEND_URLS_CHAIN))

            _nextUrl = nextUrl = request.GET.get('next', None)
            if nextUrl is None:
                nextUrl = app_settings.APP_URL

            device = get_request_device(request)

            assert device is not None

            logger.info(
                'Login started passepartout logic'
                'for user {0}, with device {1}, nextUrl is {2}'.format(
                    request.user, device, nextUrl))

            token = get_session_key(request, '__django_sso_app__jwt_token')

            passepartout = Passepartout.objects.create_passepartout(device=device, jwt=token)
            logger.info('Created passepartout object {0}'.format(passepartout))

            args = {
                'next': nextUrl
            }

            next_sso_service = get_next_bump(app_settings.APP_URL, app_settings.BACKEND_FULL_URLS_CHAIN)
            if next_sso_service is not None:
                redirect_url = next_sso_service + reverse('django_sso_app_passepartout:login',
                                                          args=[passepartout.token]) + '?' + urlencode(args)

                set_session_key(request, '__django_sso_app__passepartout__redirect_url', redirect_url)

            else:
                redirect_url = None
        else:
            logger.info('Only one SSO instance, no passepartout process')

        return redirect_url
