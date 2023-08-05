import logging
import os

from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import reverse

from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from allauth.account.models import EmailAddress
from allauth.account.views import INTERNAL_RESET_URL_KEY, INTERNAL_RESET_SESSION_KEY
from allauth.account.forms import UserTokenForm
from allauth.utils import get_request_param
from allauth.account.adapter import get_adapter

from ..apps.users.serializers import SuccessfullLoginResponseSerializer, SuccessfullLogoutResponseSerializer
from ..apps.passepartout.utils import get_passepartout_login_redirect_url
from ..permissions import is_authenticated
from ..utils import set_session_key, get_session_key, get_random_fingerprint
from .. import views as django_sso_app_views
from .. import app_settings
from .serializers import LoginSerializer, SignupSerializer, PasswordResetSerializer, PasswordResetFromKeySerializer

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters('password', 'password1', 'password2'))

logger = logging.getLogger('django_sso_app.core.api')

CURRENT_DIR = os.getcwd()
SUCCESS_STATUS_CODES = (status.HTTP_200_OK, status.HTTP_201_CREATED, status.HTTP_302_FOUND)
EMAIL_NOT_VERIFIED_MESSAGE = get_adapter().error_messages['email_not_verified']


class DjangoSsoAppApiViewMixin(APIView):
    # Form wrapper mixin

    http_method_names = ['get', 'post', 'head', 'options']
    _initial = {}
    response_errors = ['Server error.']
    response_error_status = status.HTTP_500_INTERNAL_SERVER_ERROR
    response_redirects_to_email_confirmation = False

    def get_initial(self):
        """Return the initial data to use for forms on this view."""
        return self._initial.copy()

    def get_request_fingerprint(self, request):
        return request.data.get('fingerprint', get_random_fingerprint(request))

    def get_error_response(self):
        return Response(self.response_errors, status=self.response_error_status)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(DjangoSsoAppApiViewMixin, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super(DjangoSsoAppApiViewMixin, self).form_valid(form)
        status_code = response.status_code

        if status_code not in SUCCESS_STATUS_CODES:
            raise Exception('Wrong status code "{}"'.format(status_code))

        location = response.get('location', None)
        if location == reverse('account_email_verification_sent'):
            self.response_redirects_to_email_confirmation = True

        return response

    def form_invalid(self, form):
        form_errors = dict(form.errors.items())

        self.response_error_status = status.HTTP_400_BAD_REQUEST
        self.response_errors = form_errors

        return Response(self.response_errors, status=self.response_error_status)


# allauth views

class LoginView(DjangoSsoAppApiViewMixin, django_sso_app_views.LoginView):
    """
    Login
    """
    permission_classes = (AllowAny, )
    serializer_class = LoginSerializer
    http_method_names = ['post', 'head', 'options']
    email_not_verified_errors = [EMAIL_NOT_VERIFIED_MESSAGE]

    def get_form_kwargs(self, **kwargs):
        kwargs = super(LoginView, self).get_form_kwargs(**kwargs)

        kwargs['data'] ={
            'login': self.request.data.get('login', None),
            'password': self.request.data.get('password', None),
            'fingerprint': self.request.data.get('fingerprint', get_random_fingerprint(self.request)),
        }

        return kwargs

    def get_success_response(self):
        request = self.request
        data = {
            'user': request.user,
            'token': get_session_key(request, '__django_sso_app__jwt_token'),
            'redirect_url': get_passepartout_login_redirect_url(request),
        }
        serializer = SuccessfullLoginResponseSerializer(instance=data,
                                                        context={'request': self.request})

        response = Response(serializer.data, status=status.HTTP_200_OK)

        return response

    def post(self, request, *args, **kwargs):
        logger.info('API logging in')

        if is_authenticated(request.user):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            set_session_key(request, '__django_sso_app__device__fingerprint', self.get_request_fingerprint(request))

            _response = super(LoginView, self).post(request, *args, **kwargs)
            _status_code = _response.status_code

            # check user must confirm email
            if self.response_redirects_to_email_confirmation:
                self.response_error_status = status.HTTP_400_BAD_REQUEST
                self.response_errors = self.email_not_verified_errors

                raise Exception('Email not verified')

        except:
            logger.exception('API Error logging in')
            return self.get_error_response()

        else:
            if is_authenticated(request.user):
                response = self.get_success_response()
            else:
                logger.info('user "{}" is not logged in'.format(request.user))

                # check user has unsubscribed
                user_unsubscribed_at = get_session_key(request, '__django_sso_app__user_is_unsubscribed', None)
                if user_unsubscribed_at is not None:
                    self.response_error_status = status.HTTP_400_BAD_REQUEST
                    self.response_errors = ['Unsubscribed at "{}"'.format(user_unsubscribed_at)]

                # check user must confirm email
                if _response.get('location', None) == reverse('account_email_verification_sent'):
                    self.response_error_status = status.HTTP_400_BAD_REQUEST
                    self.response_errors = self.email_not_verified_errors

                return self.get_error_response()

            return self.get_response_with_cookie(request, response)


class LogoutView(DjangoSsoAppApiViewMixin, django_sso_app_views.LogoutView):
    """
    Logout
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.Serializer
    http_method_names = ['post', 'head', 'options']

    def get_success_response(self):
        request = self.request
        redirect_url = get_request_param(request, 'next')
        data = {
            'redirect_url': redirect_url 
        }
        serializer = SuccessfullLogoutResponseSerializer(instance=data,
                                                         context={'request': self.request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        logger.info('API Logging out')

        if request.user and request.user.is_anonymous:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            _response = super(LogoutView, self).post(request, *args, **kwargs)
            _status_code = _response.status_code

            if _status_code not in SUCCESS_STATUS_CODES:
                logger.info('LogoutView status_code error ({})'.format(_status_code))

        except:
            logger.exception('API Error logging out')
            return self.get_error_response()

        else:
            return self.get_response_with_invalidated_cookie(self.get_success_response())


class SignupView(DjangoSsoAppApiViewMixin, django_sso_app_views.SignupView):
    """
    Signup
    """
    permission_classes = (AllowAny, )
    serializer_class = SignupSerializer
    http_method_names = ['head', 'post', 'options']
    signup_form_fields = app_settings.REQUIRED_USER_FIELDS + ('password1', 'password2', 'fingerprint', 'referrer')

    def get_form_kwargs(self, **kwargs):
        kwargs = super(SignupView, self).get_form_kwargs(**kwargs)

        data = {}
        for field in self.signup_form_fields:
            data[field] = self.request.data.get(field, None)

        if app_settings.BACKEND_SIGNUP_MUST_FILL_PROFILE:
            for f in app_settings.PROFILE_FIELDS:
                data[f] = self.request.data.get(f, None)

        kwargs['data'] = data

        return kwargs

    def post(self, request, *args, **kwargs):
        logger.info('API Signing up')

        if is_authenticated(request.user):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            response = super(SignupView, self).post(request, *args, **kwargs)

        except:
            logger.exception('API Error signin up')
            return self.get_error_response()

        else:
            return response


class EmailView(DjangoSsoAppApiViewMixin, django_sso_app_views.EmailView):
    """
    Manage user email addresses
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.Serializer
    http_method_names = ['get', 'head', 'options']

    def get(self, request, *args, **kwargs):
        logger.info('API Getting email')

        try:
            _response = super(EmailView, self).get(request, *args, **kwargs)

        except:
            logger.exception('API Error getting email')
            return self.get_error_response()

        else:
            email_addresses = EmailAddress.objects.filter(user=request.user).count()

            return Response(email_addresses, status=status.HTTP_200_OK)


class PasswordResetView(DjangoSsoAppApiViewMixin, django_sso_app_views.PasswordResetView):
    """
    Reset user password
    """
    permission_classes = (AllowAny, )
    serializer_class = PasswordResetSerializer
    http_method_names = ['head', 'post', 'options']

    def get_form_kwargs(self, **kwargs):
        kwargs = super(PasswordResetView, self).get_form_kwargs(**kwargs)

        kwargs['data'] = {
            'email': self.request.data.get('email', None)
        }

        return kwargs

    def post(self, request, *args, **kwargs):
        logger.info('API Asking for password reset')
        try:
            _response = super(PasswordResetView, self).post(request, *args, **kwargs)

        except:
            logger.exception('API Error while asking password reset')
            return self.get_error_response()

        else:
            return _response


class PasswordResetFromKeyView(DjangoSsoAppApiViewMixin, django_sso_app_views.PasswordResetFromKeyView):
    """
    Confirm user password reset
    """
    permission_classes = (AllowAny, )
    serializer_class = PasswordResetFromKeySerializer
    http_method_names = ['head', 'post', 'options']

    __django_sso_app__is_api_view = True

    def get_form_kwargs(self, **kwargs):
        self.key = self.kwargs['key']
        uidb36 = self.kwargs['uidb36']

        token_form = UserTokenForm(
            data={'uidb36': uidb36, 'key': self.key})

        if token_form.is_valid():
            self.reset_user = token_form.reset_user

        else:
            logger.error('key is not valid!')
            raise KeyError('key is not valid')

        kwargs = super(PasswordResetFromKeyView, self).get_form_kwargs(**kwargs)

        kwargs['data'] = {
            'password1': self.request.data.get('password1', None),
            'password2': self.request.data.get('password2', None)
        }

        return kwargs

    def post(self, request, uidb36, key, **kwargs):
        logger.info('Resetting password form key')
        try:
            set_session_key(request, INTERNAL_RESET_SESSION_KEY, key)

            response = super(PasswordResetFromKeyView, self).post(request, uidb36, INTERNAL_RESET_URL_KEY, **kwargs)

        except:
            logger.exception('Error while resetting password form key')
            return self.get_error_response()

        else:
            return response
