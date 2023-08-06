from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import ProfileApiViewSet, ProfileCompleteUnsubscriptionApiView, ProfileDetailApiView


_base_urlpatterns = [
    url(r'^$', ProfileApiViewSet.as_view({'get': 'list'}), name='list'),

    url(r'^(?P<sso_id>[-_\w]+)/$', ProfileApiViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'}),
        name="detail"),
]

_urlpatterns = _base_urlpatterns + [
    # sso_id regexp can be either uuid or slug
    url(r'^(?P<sso_id>[-_\w]+)/completely-unsubscribe/$',
        ProfileCompleteUnsubscriptionApiView.as_view({'post': 'completely_unsubscribe'}),
        name='complete_unsubscription'),
]

extra_urlpatterns = (format_suffix_patterns([
                         url(r'^profile/$', ProfileDetailApiView.as_view(), name="profile_detail")]),
                     'django_sso_app_profile_extra')

base_urlpatterns = (format_suffix_patterns(_base_urlpatterns), 'django_sso_app_profile')
urlpatterns = (format_suffix_patterns(_urlpatterns), 'django_sso_app_profile')

