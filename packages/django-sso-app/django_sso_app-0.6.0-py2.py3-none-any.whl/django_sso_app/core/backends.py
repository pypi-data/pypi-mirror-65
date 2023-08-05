import logging

from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ObjectDoesNotExist
# from django.utils.encoding import smart_str
from django.utils.http import urlencode
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model

from allauth.account.auth_backends import AuthenticationBackend as allauth_AuthenticationBackend

from .apps.users.utils import fetch_remote_user, create_local_user_from_remote_backend, \
                              update_local_user_from_remote_backend, create_local_user_from_jwt, \
                              create_local_user_from_apigateway_headers

from .permissions import is_authenticated
from .apps.profiles.models import Profile
from .apps.groups.utils import update_profile_groups
from .exceptions import ServiceSubscriptionRequiredException
from .apps.api_gateway.functions import get_apigateway_sso_id, get_apigateway_profile_groups_from_header
from .apps.profiles.utils import get_or_create_user_profile

from . import app_settings
# from .utils import set_session_key, get_session_key

logger = logging.getLogger('django_sso_app.core')
User = get_user_model()


class DjangoSsoAppLoginAuthenticationBackend(allauth_AuthenticationBackend):
    def authenticate(self, request, **credentials):
        user = super(DjangoSsoAppLoginAuthenticationBackend, self).authenticate(request, **credentials)

        if is_authenticated(user):
            logger.debug('"{}" is authenticated'.format(user))

            return user


class DjangoSsoAppBaseAuthenticationBackend(ModelBackend):
    """
    See django.contrib.auth.backends.RemoteUserBackend.

    The jwt contains an expected payload such as the following

        {
          "sso_id": "<uuid>",
          "sso_rev": 0,
          "id": 1,
          "fp": "b28493a6a29a5a38973a8a3e3abe7f34",
          "iss": "nxhnkMPKcpRWaTKwNOvGcLcs5MHJINOg"
        }
    """

    def authenticate(self, request, **kwargs):
        """
        Returns user instance or None

        :param request:
        :param kwargs: django chooses the right authentication backend by parsing "authenticate" method signature
        :return:
        """
        raise NotImplementedError('authenticate')

    def try_update_user(self, sso_id, user, user_profile, encoded_jwt, decoded_jwt, **kwargs):
        raise NotImplementedError('try_update_user')

    def try_update_profile_groups(self, request, user):
        raise NotImplementedError('try_update_profile_groups')

    def redirect_to_service_subscription(self, user):
        _qs = urlencode({'next': app_settings.SERVICE_URL})
        _url = '{}{}?{}'.format(app_settings.BACKEND_URL, app_settings.LOGIN_URL, _qs)
        logger.info('User {} must agree to the Terms of Service,'
                    ' redirecting to {} ...'
                    .format(user, _url))
        response = HttpResponseRedirect(redirect_to=_url)

        raise ServiceSubscriptionRequiredException(response)

    def try_update_profile_subscriptions(self, user):
        # Redirect user to Term Of Service.
        # is_to_subscribe = getattr(user, '__django_sso_app__is_to_subscribe', False)
        if user and app_settings.SERVICE_SUBSCRIPTION_REQUIRED:
            logger.debug('update subscriptions check for "{}":"{}"'.format(app_settings.SERVICE_URL,
                                                                           app_settings.SERVICE_SUBSCRIPTION_REQUIRED))

            if app_settings.BACKEND_ENABLED:
                user_service_subscription = user.sso_app_profile.subscriptions.filter(
                    service__service_url=app_settings.SERVICE_URL).first()

                if ((user_service_subscription is None) or (user_service_subscription.is_unsubscribed)):
                    self.redirect_to_service_subscription(user)

            else:
                if app_settings.REPLICATE_PROFILE:
                    remote_user = getattr(user, '__django_sso_app__remote_user', None)
                    if remote_user is not None:
                        remote_profile_subscriptions = remote_user['profile']['subscriptions']
                        logger.debug('remote_profile_subscriptions "{}"'.format(remote_profile_subscriptions))

                        active_subscriptions = []
                        for s in remote_profile_subscriptions:
                            if not s['is_unsubscribed']:
                                active_subscriptions.append(s['service_url'])

                        if app_settings.SERVICE_URL not in active_subscriptions:
                            self.redirect_to_service_subscription(user)


class DjangoSsoAppApiGatewayAuthenticationBackend(DjangoSsoAppBaseAuthenticationBackend):
    """
    Authenticates by request CONSUMER_USERNAME header
    """

    backend_path = 'django_sso_app.core.backends.DjangoSsoAppApiGatewayAuthenticationBackend'

    def authenticate(self, request, consumer_username, encoded_jwt, decoded_jwt):
        logger.info('backend authenticating by apigateway consumer {}'.format(consumer_username))

        if consumer_username is None:
            logger.debug('consuner_usename not set, skipping authentication')
            return

        if app_settings.BACKEND_ENABLED:
            logger.debug('backend enabled')
            try:
                sso_id = get_apigateway_sso_id(consumer_username)
                profile = Profile.objects.get(sso_id=sso_id)
                user = profile.user

            except ObjectDoesNotExist:
                logger.debug('user with apigateway consumer username "{}" do not exists'.format(consumer_username))
                return
            else:
                logger.debug('user with apigateway consumer username "{}" EXISTS'.format(consumer_username))
                # allauth logic
                setattr(user, 'backend', self.backend_path)

        else:
            logger.debug('app enabled')
            try:
                sso_id = get_apigateway_sso_id(consumer_username)
                profile = Profile.objects.get(sso_id=sso_id)
                user = profile.user

            except ObjectDoesNotExist:
                logger.info('No profile with id "{}"'.format(sso_id))
                try:
                    user = self.try_replicate_user(request, sso_id, encoded_jwt)

                except Exception as e:
                    logger.warning('cannot replicate user because of "{}"'.format(e))
                    return

            else:
                if app_settings.REPLICATE_PROFILE:
                    if decoded_jwt is None:
                        logger.warning('decoded_jwt not set')
                        return

                    user = self.try_update_user(sso_id, user, profile, encoded_jwt, decoded_jwt, consumer_username)

                else:
                    # just updates user groups
                    logger.debug('Do not update profile')

            # updating relations
            if app_settings.MANAGE_USER_GROUPS:
                self.try_update_profile_groups(request, user)

            self.try_update_profile_subscriptions(user)

        return user

    def try_replicate_user(self, request, sso_id, encoded_jwt):
        logger.debug('try_replicate_user')

        if app_settings.REPLICATE_PROFILE:
            logger.info('Replicate user with sso_id "{}" from remote backend'.format(sso_id))
            # create local profile from SSO
            backend_user = fetch_remote_user(sso_id=sso_id, encoded_jwt=encoded_jwt)

            user = create_local_user_from_remote_backend(backend_user)

        else:
            # create local profile from headers
            logger.info('Do not replicate user, creating from headers')
            try:
                user = create_local_user_from_apigateway_headers(request)

            except Exception as e:
                logger.warning('cannot create user from headers because of "{}"'.format(e))
                return

        return user

    def try_update_user(self, sso_id, user, user_profile, encoded_jwt, decoded_jwt, consumer_username):
        logger.debug('try_update_user')

        rev_changed = user_profile.sso_rev < decoded_jwt['sso_rev']
        first_access = not user.is_active and not user_profile.is_unsubscribed

        if rev_changed or first_access:
            if rev_changed:
                logger.info('Rev changed from "{}" to "{}" for apigateway consumer "{}", updating ...'
                            .format(user_profile.sso_rev, decoded_jwt['sso_rev'],
                                    consumer_username))
            if first_access:
                logger.info('"{} apigateway consumer first access, updating ...'.format(consumer_username))

            # update local profile from SSO
            setattr(user, '__django_sso_app__apigateway_update', True)

            remote_user = fetch_remote_user(sso_id=sso_id, encoded_jwt=encoded_jwt)     
            user = update_local_user_from_remote_backend(remote_user=remote_user,
                                                         profile=user_profile)

            logger.info('{} updated with latest data from SSO'.format(user))

        else:
            logger.info('Nothing changed for apigateway consumer "{}"'.format(consumer_username))

        return user

    def try_update_profile_groups(self, request, user):
        logger.info('try_update_profile_groups for "{}"'.format(user))

        consumer_groups = request.META.get(
            app_settings.APIGATEWAY_CONSUMER_GROUPS_HEADER, None)
        profile_groups = get_apigateway_profile_groups_from_header(consumer_groups)

        update_profile_groups(user.sso_app_profile, profile_groups)


class DjangoSsoAppJwtAuthenticationBackend(DjangoSsoAppBaseAuthenticationBackend):
    """
    Authenticates by request jwt
    """

    backend_path = 'django_sso_app.core.backends.DjangoSsoAppApiGatewayAuthenticationBackend'

    def authenticate(self, request, encoded_jwt, decoded_jwt):
        logger.info('backend authenticating by request jwt')

        if encoded_jwt is None or decoded_jwt is None:
            logger.debug('request jwt not set, skipping authentication')
            return

        if app_settings.BACKEND_ENABLED:
            logger.debug('backend enabled')

            try:
                sso_id = decoded_jwt['sso_id']
                profile = Profile.objects.get(sso_id=sso_id)
                user = profile.user

            except ObjectDoesNotExist:
                logger.debug('user with sso_id "{}" does not exists'.format(sso_id))
                return

            else:
                # allauth logic
                setattr(user, 'backend', self.backend_path)
        else:
            logger.debug('app enabled')

            try:
                sso_id = decoded_jwt['sso_id']
                user_profile = Profile.objects.get(sso_id=sso_id)
                user = user_profile.user

                if app_settings.REPLICATE_PROFILE:
                    if decoded_jwt is None:
                        logger.warning('decoded_jwt not set')
                        return

                    logger.debug('try_update_user "{}" for apigateway consumer "{}"'.format(sso_id, sso_id))

                    user = self.try_update_user(sso_id, user, user_profile, encoded_jwt, decoded_jwt, sso_id)

                else:
                    # just updates user groups
                    logger.debug('Do not replicate profile')

            except ObjectDoesNotExist:
                try:
                    user = self.try_replicate_user(sso_id, encoded_jwt, decoded_jwt)

                except Exception as e:
                    logger.warning('cannot replicate user because of "{}"'.format(e))
                    return

            # update relations
            if app_settings.MANAGE_USER_GROUPS:
                self.try_update_profile_groups(request, user)

            self.try_update_profile_subscriptions(user)

        return user

    def try_replicate_user(self, sso_id, encoded_jwt, decoded_jwt):
        logger.debug('try_replicate_user')

        assert(encoded_jwt is not None and decoded_jwt is not None)

        if app_settings.REPLICATE_PROFILE:
            # create local profile from SSO
            logger.info('Replicate user with sso_id "{}" from remote backend'.format(sso_id))

            backend_user = fetch_remote_user(sso_id=sso_id,
                                             encoded_jwt=encoded_jwt)

            user = create_local_user_from_remote_backend(backend_user)

        else:
            # create local profile from jwt
            logger.info('Replicating user with sso_id "{}" from JWT'.format(sso_id))

            user = create_local_user_from_jwt(decoded_jwt)

            backend_user = decoded_jwt

        # setattr(user, 'sso_app_profile', get_or_create_user_profile(user, Profile, backend_user))

        return user

    def try_update_user(self, sso_id, user, user_profile, encoded_jwt, decoded_jwt):
        logger.debug('try_update_user')

        rev_changed = user_profile.sso_rev < decoded_jwt['sso_rev']
        first_access = not user.is_active and not user_profile.is_unsubscribed

        if rev_changed or first_access:
            if rev_changed:
                logger.info('Rev changed from "{}" to "{}" for "{}", updating ...'
                            .format(user_profile.sso_rev, decoded_jwt['sso_rev'],
                                    sso_id))
            if first_access:
                logger.info('"{}" first access, creating ...'.format(sso_id))

            ## update local profile from SSO

            logger.info('"{}" updated with latest data from SSO'.format(sso_id))

        else:
            logger.info('Nothing changed for "{}"'.format(sso_id))

        return user

    def try_update_profile_groups(self, request, user):
        # Update user groups
        if app_settings.REPLICATE_PROFILE:
            logger.info('try_update_profile_groups for "{}"'.format(user))

            remote_user_object = getattr(user, '__django_sso_app__remote_user')
            remote_user_object_groups = remote_user_object.get('groups', [])
            update_profile_groups(user.sso_app_profile, remote_user_object_groups)
