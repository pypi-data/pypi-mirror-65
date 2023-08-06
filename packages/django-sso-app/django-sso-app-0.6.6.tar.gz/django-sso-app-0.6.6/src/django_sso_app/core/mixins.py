from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView

from . import app_settings

User = get_user_model()


class TryAuthenticateMixin(object):

    def try_authenticate(self, username, email, password):
        credentials = username or email or None
        user = None

        if username is None and email is not None:
            credentials = 'email'
        if username is not None and email is None:
            credentials = 'username'

        if credentials is not None:
            user = authenticate(username=credentials, password=password)

        if user is not None:
            return user

        raise User.DoesNotExist('Check credentials.')


class WebpackBuiltTemplateViewMixin(TemplateView):
    """
    Uses built template view when DJANGO_SSO_APP_BACKEND_HAS_CUSTOM_FRONTEND_APP
    """

    def get_template_names(self):
        if app_settings.BACKEND_HAS_CUSTOM_FRONTEND_APP:
            return ['frontend/built.html']
        else:
            return [getattr(self, 'template_name')]

    def get_context_data(self, *args, **kwargs):
        context = super(WebpackBuiltTemplateViewMixin, self).get_context_data(*args, **kwargs)
        return context
