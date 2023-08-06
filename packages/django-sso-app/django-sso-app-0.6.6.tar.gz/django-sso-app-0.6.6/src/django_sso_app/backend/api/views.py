from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from ...core.permissions import is_staff
from ..views import local_space_available, CURRENT_DIR, logger


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
