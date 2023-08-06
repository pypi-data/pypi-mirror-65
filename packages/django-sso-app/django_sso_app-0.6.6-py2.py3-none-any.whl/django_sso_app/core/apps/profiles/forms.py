import logging

from django import forms
from django.utils.translation import ugettext_lazy as _

from django_countries.fields import CountryField

from ... import app_settings
from .models import Profile

logger = logging.getLogger('django_sso_app.core.apps.profiles')


class ProfileForm(forms.Form):
    # role = forms.ChoiceField(
    #     label=_('Role'),
    #     choices=app_settings.PROFILE_ROLE_CHOICES,
    #     initial=0)

    ssn = forms.CharField(
        label=_('Social Security Number'),
        widget=forms.TextInput(
            attrs={'type': 'text',
                   'placeholder': _('Social Security Number')}))

    phone = forms.CharField(
        label=_('Phone'),
        widget=forms.TextInput(
            attrs={'type': 'text',
                   'placeholder': _('Phone')}))

    first_name = forms.CharField(
        label=_('First name'),
        widget=forms.TextInput(
            attrs={'type': 'text',
                   'placeholder': _('First name')}))

    last_name = forms.CharField(
        label=_('Last name'),
        widget=forms.TextInput(
            attrs={'type': 'text',
                   'placeholder': _('Last name')}))

    description = forms.CharField(
        label=_('Description'),
        widget=forms.Textarea(
            attrs={'placeholder': _('Description')}))

    picture = forms.ImageField(
        label=_('Picture'),
    )

    birthdate = forms.DateField(
        label=_('Birthdate'),
        widget=forms.TextInput(
            attrs={'type': 'date',
                   'placeholder': _('Birthdate')}))

    latitude = forms.FloatField(label=_('Latitude'))

    longitude = forms.FloatField(label=_('Longitude'))

    """
    country = forms.CharField(
        label=_('Country'),
        widget=forms.TextInput(
            attrs={'type': 'text',
                   'placeholder': _('Country')}))
    """
    country = CountryField().formfield(label=_('Country'))

    address = forms.CharField(
        label=_('Address'),
        widget=forms.Textarea(
            attrs={'placeholder': _('Address')}))

    language = forms.CharField(
        label=_('Language'),
        widget=forms.TextInput(
            attrs={'type': 'text',
                   'placeholder': _('Language')}))

    def set_required_fields(self):
        for field in app_settings.PROFILE_FIELDS:
            if field in self.fields.keys():
                self.fields[field].required = field in app_settings.REQUIRED_PROFILE_FIELDS

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        self.set_required_fields()


class UserProfileForm(forms.ModelForm, ProfileForm):
    class Meta:
        model = Profile
        fields = app_settings.PROFILE_FIELDS
