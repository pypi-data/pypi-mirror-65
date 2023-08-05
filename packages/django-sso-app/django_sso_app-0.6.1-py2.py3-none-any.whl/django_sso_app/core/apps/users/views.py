import logging


from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.forms import ValidationError
from django.http import Http404
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import cache_page
from django.db.models import Q
from django.core.exceptions import SuspiciousOperation

from allauth.account.adapter import get_adapter

from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from allauth.account.models import EmailAddress

from .serializers import (CheckUserExistenceSerializer,
                          UserSerializer, NewUserSerializer,
                          UserRevisionSerializer)
from ...permissions import StaffPermission
from ...permissions import is_staff
from ...utils import is_test_user, invalidate_cookie, get_session_key
from ... import app_settings

User = get_user_model()

logger = logging.getLogger('django_sso_app.core.apps.users')


class CheckUserExistenceApiView(APIView):
    """
    Retrieve a "condensed" user instance {"id": ".."} by either "username" or "email" as query params.
    """
    permission_classes = (permissions.AllowAny, )

    def get_object(self, login=None, username=None, email=None):
        try:
            if login is not None:
                user = User.objects.filter(Q(username=login) | Q(email=login)).first()
                if user is not None:
                    return user

                email_address = EmailAddress.objects.filter(email=login, verified=True).first()
                if email_address is not None:
                    return email_address.user

            elif username is None and email is not None:
                email_address = EmailAddress.objects.filter(email=email, verified=True).first()
                if email_address is not None:
                    return email_address.user

            elif username is not None and email is None:
                return User.objects.get(username=username)

            raise User.DoesNotExist('Either login username or email must be set.')

        except (User.DoesNotExist, EmailAddress.DoesNotExist):
            return None

    def get(self, *args, **kwargs):
        login = self.request.query_params.get('login', self.request.GET.get('login', None))
        username = self.request.query_params.get('username', None)
        email = self.request.query_params.get('email', None)

        found = False
        if login is not None or username is not None or email is not None:
            item = self.get_object(login, username, email)
            found = item is not None

        if not found:
            raise Http404

        serializer = CheckUserExistenceSerializer(item)

        return Response(serializer.data)


class UserApiViewSet(mixins.ListModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    """
    User api viewset
    """

    lookup_field = 'sso_app_profile__sso_id'
    # serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NewUserSerializer
        else:
            return UserSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.filter(is_staff=False)

        if not is_staff(user):
            profile = user.get_sso_app_profile()
            queryset = queryset.filter(sso_app_profile__sso_id=profile.sso_id, is_active=True)

        return queryset

    def get_object(self, *args, **kwargs):
        sso_id = self.kwargs.get('sso_id')

        try:
            user = User.objects.get(sso_app_profile__sso_id=sso_id)
            self.check_object_permissions(self.request, user)
            return user
        except User.DoesNotExist:
            raise Http404

    def list(self, request, *args, **kwargs):
        """
        List users
        """
        logger.info('List users')

        return super(UserApiViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Create user
        """
        logger.info('Creating user')

        return super(UserApiViewSet, self).create(request, *args, **kwargs)

    def partial_update(self, request, sso_id, *args, **kwargs):
        logger.info('Updating user')

        try:
            response = super(UserApiViewSet, self).partial_update(request, sso_id, *args, **kwargs)

        except (IntegrityError, ValidationError) as e:
            logger.exception('partial_update')

            logger.info('User {0} tried to update email with already registered one'.format(request.user))

            return Response(_('Email already registered.'), status=status.HTTP_409_CONFLICT)

        response_status_code = response.status_code
        logger.info('Partial_update status code is {}, {}'.format(response_status_code, request.data))

        if response_status_code == 200:
            adapter = get_adapter(request)
            user = self.get_object()
            requesting_user = request.user

            if get_session_key(request, '__django_sso_app__user_email_updated', False):
                is_same_user = requesting_user == user

                if is_same_user:
                    # loggin out after email update
                    adapter.logout(request)
                else:
                    if not is_staff(requesting_user):
                        _msg = 'User "{}" tried to updated email for "{}"'.format(requesting_user, user)
                        logger.warning(_msg)

                        raise SuspiciousOperation(_msg)
            else:
                adapter.try_update_response_jwt(user, response)

        return response

    def delete_test_user(self, request, sso_id, *args, **kwargs):
        logger.info('Deleting user')
        requesting_user = self.request.user
        logger.info('User "{}" wants to delete user with sso_id "{}"'.format(requesting_user, sso_id))

        try:
            user = self.get_object()
            user_is_test_user = False

            if is_test_user(user):
                user_is_test_user = True
                logger.info('deleting user "{}"'.format(user))
                user.delete()

        except Exception as e:
            response = Response(_('Error deleting user "{}": {}').format(sso_id, e),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            response = Response(None, status=status.HTTP_200_OK)

            if user_is_test_user:
                invalidate_cookie(response, app_settings.JWT_COOKIE_NAME)

        return response


class UserRevisionsApiView(generics.ListAPIView):
    """
    User revisions entrypoint
    """

    queryset = User.objects.filter(is_superuser=False)
    serializer_class = UserRevisionSerializer
    permission_classes = (StaffPermission,)

    @method_decorator(cache_page(120))
    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class UserDetailApiView(generics.RetrieveAPIView):
    """
    User detail entrypoint
    """
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()

    def get_object(self, *args, **kwargs):
        user = getattr(self.request, 'user', None)
        return user
