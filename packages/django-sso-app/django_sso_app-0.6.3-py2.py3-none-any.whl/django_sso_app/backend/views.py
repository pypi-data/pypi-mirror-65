import logging

import os
import platform

from urllib.parse import urlsplit
from django.utils import translation
from django.shortcuts import redirect
# from django.views.generic import TemplateView

from rest_framework.views import Response, status, APIView
from rest_framework.permissions import AllowAny

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from ..core.permissions import is_staff

logger = logging.getLogger('django_sso_app.backend')

CURRENT_DIR = os.getcwd()

if platform.system() == 'Windows':
    def local_space_available(dir):
        """Return space available on local filesystem."""
        import ctypes
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(dir), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value
else:
    def local_space_available(dir):
        destination_stats = os.statvfs(dir)
        return destination_stats.f_bsize * destination_stats.f_bavail


def set_language_from_url(request, user_language):
    prev_lang = request.session.get(translation.LANGUAGE_SESSION_KEY, request.LANGUAGE_CODE)

    translation.activate(user_language)
    request.session[translation.LANGUAGE_SESSION_KEY] = user_language

    url = request.META.get('HTTP_REFERER', '/')
    parsed = urlsplit(url)

    _url = parsed.path
    if len(_url) > 1:
        _url = '/{}/'.format(user_language) + _url.lstrip('\/{}\/'.format(prev_lang))

    return redirect(_url)


class StatsView(APIView):
    """
    Return instance stats
    """

    permission_classes = (AllowAny,)

    def get(self, request):
        try:
            #stats = os.statvfs(CURRENT_DIR)
            free_space_mb = int(local_space_available(CURRENT_DIR) / (1024 * 1024))
            # free_space_mb = int(
            #     (stats.f_bavail * stats.f_frsize) / (1024 * 1024))

            logger.info(
                'Free space (MB): {}.'.format(free_space_mb))

            if free_space_mb > 200:
                health_status = 'green'
            else:
                if free_space_mb < 100:
                    health_status = 'yellow'
                else:
                    health_status = 'red'

            data = {
                'status': health_status,
                'meta': str(request.META.items())
            }

            if is_staff(request.user):
                data['free_space_mb'] = free_space_mb

            return Response(data, status.HTTP_200_OK)

        except Exception as e:
            err_msg = str(e)
            logger.exception('Error getting health {}'.format(err_msg))
            return Response(err_msg, status.HTTP_500_INTERNAL_SERVER_ERROR)


schema_view = get_schema_view(
   openapi.Info(
      title="Django SSO App",
      default_version='v1',
   ),
   public=True,
   permission_classes=(AllowAny,),
)
