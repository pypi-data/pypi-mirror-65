import logging
# import inspect
# import warnings

from django.db import transaction
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import activate as activate_translation
from django.core.cache import cache
from django.contrib.auth import (authenticate,
                                 get_backends,
                                 login as django_login)
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import SuspiciousOperation

from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.models import EmailAddress
from allauth.account import app_settings as allauth_app_settings

from .mixins import TryAuthenticateMixin
from .utils import set_session_key, check_user_can_login
from .apps.devices.models import Device
from .apps.devices.utils import get_request_device
from .apps.services.models import Subscription
from .apps.profiles.utils import get_or_create_user_profile, update_profile
from .apps.profiles.models import Profile
from .apps.passepartout.utils import get_passepartout_login_redirect_url
from .tokens.utils import get_request_jwt_fingerprint, get_request_jwt, renew_response_jwt
from .permissions import is_authenticated, is_staff
from . import app_settings

logger = logging.getLogger('django_sso_app.core')


class AccountAdapter(DefaultAccountAdapter, TryAuthenticateMixin):
    def __init__(self, request=None):
        super(AccountAdapter, self).__init__(request)

        self.error_messages = DefaultAccountAdapter.error_messages
        self.error_messages['email_not_verified'] = _('We have sent an e-mail to you for verification. Follow the link provided to finalize the signup process. Please contact us if you do not receive it within a few minutes.')

    def is_open_for_signup(self, request):
        """
        Checks whether or not the site is open for signups.

        Next to simply returning True/False you can also intervene the
        regular flow by raising an ImmediateHttpResponse
        """
        return True

    def is_ajax(self, request):
        is_ajax = request.path.startswith('/api') or \
                  super(AccountAdapter, self).is_ajax(request) or \
                  request.META.get('CONTENT_TYPE', None) == 'application/json'

        return is_ajax

    def get_login_redirect_url(self, request):
        """
        Returns the default URL to redirect to after logging in.  Note
        that URLs passed explicitly (e.g. by passing along a `next`
        GET parameter) take precedence over the value returned here.
        """

        if request.path.startswith(reverse('account_signup')) or request.path.startswith(reverse('rest_signup')):
            logger.info('do not get redirect_url from signup')
            redirect_url = None
        else:
            redirect_url = get_passepartout_login_redirect_url(request)

            if redirect_url is None:
                redirect_url = super(AccountAdapter, self).get_login_redirect_url(request)

        return redirect_url

    def login(self, request, user):
        # HACK: This is not nice. The proper Django way is to use an
        # authentication backend
        logger.debug('adapter login')

        check_user_can_login(user)

        if not hasattr(user, 'backend'):
            from .backends import DjangoSsoAppLoginAuthenticationBackend
            backends = get_backends()
            backend = None
            for b in backends:
                if isinstance(b, DjangoSsoAppLoginAuthenticationBackend):
                    # prefer our own backend
                    backend = b
                    break
                elif not backend and hasattr(b, 'get_user'):
                    # Pick the first vald one
                    backend = b
            backend_path = '.'.join([backend.__module__,
                                     backend.__class__.__name__])
            user.backend = backend_path

        if request.path.startswith(reverse('account_signup')) or request.path.startswith(reverse('rest_signup')):
            logger.debug('do not login from signup')

        else:
            logger.debug('django loggin in')

            # disabling rev update
            setattr(user, '__django_sso_app__user_loggin_in', True)

            # django
            django_login(request, user)

            if is_authenticated(user):
                if not user.is_superuser:
                    # setting up request user
                    setattr(request, 'user', user)

    def logout(self, request):
        logger.debug('adapter logout, user logged out, setting flags')
        # print(inspect.stack()[1].function)
        try:
            _device = get_request_device(request)

        except Exception as e:
            logger.debug('no device on request because of "{}"'.format(e))

        logging_out_user = request.user

        # allauth logout
        super(AccountAdapter, self).logout(request)

        if not is_authenticated(request.user):
            deleted_devices = self.remove_all_user_profile_devices(logging_out_user)
            logger.info('({}) devices deleted for user "{}"'.format(deleted_devices, logging_out_user))

    def confirm_email(self, request, email_address):
        """
        Marks the email address as confirmed on the db
        """
        email_address.verified = True

        # email_address.set_as_primary(conditional=True)
        email_address.set_as_primary(conditional=False) # allauth originally won't swap email addresses

        email_address.save()

    def set_password(self, user, password):
        user.set_password(password)
        user.save()

    def authenticate(self, request, **credentials):
        logger.debug('adapter authenticate')
        #exceptions print(inspect.stack()[1].function)

        """Only authenticates, does not actually login. See `login`"""
        from .backends import DjangoSsoAppLoginAuthenticationBackend

        self.pre_authenticate(request, **credentials)

        DjangoSsoAppLoginAuthenticationBackend.unstash_authenticated_user()
        user = authenticate(request, **credentials)
        alt_user = DjangoSsoAppLoginAuthenticationBackend.unstash_authenticated_user()
        user = user or alt_user

        if user and allauth_app_settings.LOGIN_ATTEMPTS_LIMIT:
            cache_key = self._get_login_attempts_cache_key(
                request, **credentials)
            cache.delete(cache_key)
        else:
            self.authentication_failed(request, **credentials)

        if is_authenticated(user):
            logger.info('adapter authenticated "{}"'.format(user))
            _profile = get_or_create_user_profile(user, Profile)

            # check unsubscription
            user_unsubscribed_at = user.sso_app_profile.unsubscribed_at
            if user_unsubscribed_at is not None:
                set_session_key(request, '__django_sso_app__user_is_unsubscribed', str(user_unsubscribed_at))

        return user

    def update_user_profile(self, user, cleaned_data, commit=True):
        logger.debug('adapter update user profile')
        profile = update_profile(user.sso_app_profile, cleaned_data, commit)

        return profile

    @transaction.atomic
    def save_user(self, request, user, form, commit=True):
        """
        Saves a new User instance using information provided in the
        signup form.
        """
        # !atomic
        cleaned_data = form.cleaned_data
        email = cleaned_data.get('email', None)
        username = cleaned_data.get('username', None)
        logger.debug('Saving new user {0} with email {1}.'.format(
                     username, email))

        new_user = super(AccountAdapter, self).save_user(request, user, form, commit)

        self.update_user_profile(new_user, cleaned_data, commit)

        return new_user

    def render_mail(self, template_prefix, email, context):
        user = context.get('user')
        logger.info('render mail for "{}"'.format(user))
        user_language = user.sso_app_profile.language

        activate_translation(user_language)
        context.update({
            'EMAILS_DOMAIN': settings.EMAILS_DOMAIN,
            'EMAILS_SITE_NAME': settings.EMAILS_SITE_NAME
        })

        return super(AccountAdapter, self).render_mail(template_prefix, email, context)

    def get_email_confirmation_url(self, request, emailconfirmation):
        """Constructs the email confirmation (activation) url.
        Note that if you have architected your system such that email
        confirmations are sent outside of the request context request
        can be None here.
        """
        _url = reverse(
            "account_confirm_email",
            args=[emailconfirmation.key])

        email_confirmation_url = '{}://{}{}'.format(app_settings.HTTP_PROTOCOL,
                                                    settings.EMAILS_DOMAIN,
                                                    _url)

        return email_confirmation_url

    # pai

    def unconfirm_all_user_emails(self, user):
        logger.info('Unconfirming all emails for user "{}"'.format(user))

        return EmailAddress.objects.filter(user=user,
                                           verified=True).update(verified=False)

    def add_user_profile_device(self, user, fingerprint, user_agent=None):
        profile = user.sso_app_profile
        logger.info(
            'Adding User Device for profile "{}" with fingerprint "{}"'.format(profile,
                                                                               fingerprint))

        device = Device.objects.create(profile=profile, fingerprint=fingerprint)
        logger.debug('device "{}" created with key "{}" and fingerprint "{}"'.format(device,
                                                                                     device.apigw_jwt_key,
                                                                                     device.fingerprint))

        return device

    def remove_user_profile_device(self, device):
        logger.info('Removing Device {0}'.format(device.id))

        device.delete()

        return 1

    def remove_all_user_profile_devices(self, user):
        logger.info('Removing All Profile Devices for "{}"'.format(user))

        removed = 0
        for device in user.sso_app_profile.devices.all():
            removed += self.remove_user_profile_device(device)

        return removed

    def subscribe_profile_to_service(self, profile, service, update_rev=False, commit=True):
        logger.info('Subscribinig "{}" to service "{}"'.format(profile, service))

        subscription, _subscription_created = \
            Subscription.objects.get_or_create(
                profile=profile, service=service)

        if _subscription_created:
            logger.info('Created service subscrption for "{}"'.format(profile))

            setattr(profile.user, '__django_sso_app__subscription_updated', True)

            if update_rev:
                profile.update_rev(commit)
        else:
            logger.info('Profile "{}" can not subscribe "{}"'.format(profile, service))

        return _subscription_created

    def disable_profile_subscription(self, profile, subscription, update_rev=False, commit=True):
        service = subscription.service
        logger.info('Unubscribinig "{}" form service "{}"'.format(profile, service))

        try:
            subscription.unsubscribed_at = timezone.now()
            subscription.save()

            if update_rev and commit:
                profile.save()

        except:
            logger.exception('Profile "{}" can not unsubscribe from "{}"'.format(profile, service))
            return False

        else:
            return True

    def get_request_profile_device(self, request):
        received_jwt = get_request_jwt_fingerprint(request)

        return Device.objects.filter(fingerprint=received_jwt).first()

    def delete_request_profile_device(self, request):
        profile = request.user.sso_app_profile
        logger.info('Deleting request profile device for "{}"'.format(profile))

        removing_device = self.get_request_profile_device(request)

        if removing_device is not None:
            logger.info('Removing logged out user profile device "{}" for "{}"'.format(removing_device, profile))
            self.remove_user_profile_device(removing_device)
        else:
            logger.warning('Can not find request device for profile "{}"'.format(profile))

    def try_completely_unsubscribe(self, username, email, password):
        if self.request is None:
            raise KeyError('no request object')

        user = self.try_authenticate(username, email, password)
        requesting_user = self.request.user

        if not requesting_user.is_superuser and not user.is_superuser:
            profile = user.sso_app_profile
            logger.info('Completely unsubscribing Profile "{}"'.format(profile))

            profile.unsubscribed_at = timezone.now()
            profile.is_active = False
            user.is_active = False

            user.save()  # Profile update managed by user signal

            self.logout(self.request)
        else:
            _msg = 'User "{}" tried to completely unsubscribe "{}"'.format(requesting_user, user)
            logger.warning(_msg)

            raise SuspiciousOperation(_msg)

    def try_update_response_jwt(self, user, response):
        if self.request is None:
            raise KeyError('no request object')

        requesting_user = self.request.user

        if not requesting_user.is_superuser and not user.is_superuser:
            received_jwt = get_request_jwt(self.request)

            if received_jwt is not None:
                is_same_user = requesting_user == user

                if is_same_user:
                    logger.info('From browser as same user "{}"'.format(user))
                    renew_response_jwt(received_jwt, user, self.request, response)

                elif not is_same_user and is_staff(requesting_user):
                    # returns user jwt to staff user
                    logger.info('From browser as staff user "{}"'.format(requesting_user))
                    renew_response_jwt(received_jwt, user, self.request, response)

                else:
                    _msg = 'User "{}" tried to updated profile for "{}"'.format(requesting_user, user)
                    logger.warning(_msg)

                    raise SuspiciousOperation(_msg)

        else:
            _msg = 'User "{}" tried to updated profile for "{}"'.format(requesting_user, user)
            logger.warning(_msg)

            raise SuspiciousOperation(_msg)
