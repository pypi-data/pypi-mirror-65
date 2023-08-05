import logging

from django import forms
from django.forms import CharField, DateField, FloatField, HiddenInput

from allauth.account.forms import (LoginForm as allauth_LoginForm,
                                   SignupForm as allauth_SignupForm)
from allauth.account.models import EmailAddress
from allauth.account.adapter import get_adapter
from allauth.account import app_settings as allauth_app_settings
from allauth.utils import get_user_model

from .apps.services.models import Service

from .utils import is_test_user
from . import app_settings

logger = logging.getLogger('django_sso_app.core')


SIGNUP_FORM_FIELDS = app_settings.USER_FIELDS + (
    'email2',  # ignored when not present
    'password1',
    'password2'  # ignored when not present
)


class LoginForm(allauth_LoginForm):
    fingerprint = CharField(label='fingerprint', max_length=255, required=False, widget=HiddenInput(),
                            initial='undefined')


class BaseSignupForm(allauth_SignupForm):
    fingerprint = CharField(label='fingerprint', max_length=255, required=False, widget=HiddenInput(),
                            initial='undefined')
    referrer = CharField(label='referrer', max_length=255, required=False, widget=HiddenInput(),
                        initial=app_settings.APP_URL)

    field_order = SIGNUP_FORM_FIELDS

    # pai
    def __init__(self, *args, **kwargs):
        super(BaseSignupForm, self).__init__(*args, **kwargs)

        if 'username' not in app_settings.USER_FIELDS:
            self.fields.pop('username')
        if 'email' not in app_settings.USER_FIELDS:
            self.fields.pop('email')

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super(BaseSignupForm, self)
        return kwargs

    def save(self, request):
        # test_mode check
        new_user = super(BaseSignupForm, self).save(request)
        test_mode = request.GET.get('test_mode', None)
        adapter = get_adapter(request)

        username = self.cleaned_data["username"]
        email = self.cleaned_data["email"]
        fingerprint = self.cleaned_data["fingerprint"]
        referrer = self.cleaned_data["referrer"]

        try:

            if test_mode is None and username == app_settings.TEST_USER_USERNAME:
                user_model = get_user_model()
                username_field = allauth_app_settings.USER_MODEL_USERNAME_FIELD

                self.add_error(allauth_app_settings.USER_MODEL_USERNAME_FIELD, adapter.error_messages['username_taken'])

                raise forms.ValidationError(
                    adapter.error_messages['username_taken'],
                    params={
                        'model_name': user_model.__name__,
                        'field_label': username_field,
                    }
                )

            if test_mode is None and email == app_settings.TEST_USER_EMAIL:
                user_model = get_user_model()

                self.add_error('email', adapter.error_messages['email_taken'])

                raise forms.ValidationError(
                    adapter.error_messages['email_taken'],
                    params={
                        'model_name': user_model.__name__,
                        'field_label': 'email',
                    }
                )

            if test_mode is not None and is_test_user(new_user):
                logger.info('User "{}" is TEST_USER, confirming email "{}"'.format(app_settings.TEST_USER_USERNAME,
                                                                                   app_settings.TEST_USER_EMAIL))

                adapter.confirm_email(request, EmailAddress.objects.get(email=new_user.email))

            # service subscription by "referrer" field
            if new_user is not None:
                if referrer not in [app_settings.APP_URL, '', None]:
                    logger.info('Subscripting new user to service with url "{}"'.format(referrer))

                    service = Service.objects.filter(service_url=referrer).first()
                    if service is not None:
                        adapter.subscribe_profile_to_service(new_user.sso_app_profile, service)

        # delete creating user model if any exception occurred
        except Exception as e:
            logger.exception('Error subscribing new user "{}"'.format(e))

            if new_user is not None:
                new_user.delete()

            raise

        return new_user


# custom signup form
if app_settings.BACKEND_SIGNUP_MUST_FILL_PROFILE:
    class SignupForm(BaseSignupForm):
        first_name = CharField(required='first_name' in app_settings.REQUIRED_PROFILE_FIELDS)
        last_name = CharField(required='last_name' in app_settings.REQUIRED_PROFILE_FIELDS)
        description = CharField(required='description' in app_settings.REQUIRED_PROFILE_FIELDS)
        picture = CharField(required='picture' in app_settings.REQUIRED_PROFILE_FIELDS)
        birthdate = DateField(required='birthdate' in app_settings.REQUIRED_PROFILE_FIELDS)
        latitude = FloatField(required='latitude' in app_settings.REQUIRED_PROFILE_FIELDS)
        longitude = FloatField(required='longitude' in app_settings.REQUIRED_PROFILE_FIELDS)
        country = CharField(required='country' in app_settings.REQUIRED_PROFILE_FIELDS)
        address = CharField(required='address' in app_settings.REQUIRED_PROFILE_FIELDS)
        # business_address = CharField(required='business_address' in app_settings.REQUIRED_PROFILE_FIELDS)
        language = CharField(required='language' in app_settings.REQUIRED_PROFILE_FIELDS)

else:
    class SignupForm(BaseSignupForm):
        pass
