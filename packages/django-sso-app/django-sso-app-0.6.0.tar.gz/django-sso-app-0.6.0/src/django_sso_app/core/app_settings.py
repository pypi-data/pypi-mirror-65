from .settings.common import *


class AppSettings(object):

    def __init__(self, prefix):
        self.prefix = prefix
        self.env = env  # got from .settings.common
        # check shape string
        if self.SHAPE not in AVAILABLE_SHAPES:
            raise Exception('Wrong DJANGO_SSO_APP_SHAPE ({})'.format(self.SHAPE))

    def _env(self, key, dflt, type=str):
        if type == bool:
            return self.env.bool(key, default=dflt)
        elif type == tuple:
            return self.env.tuple(key, default=dflt)
        if type == int:
            return self.env.int(key, default=dflt)
        elif type == list:
            return self.env.list(key, default=dflt)
        else:
            return self.env(key, default=dflt)

    def _django_setting(self, name, dflt, type=str):
        from django.conf import settings
        getter = getattr(settings,
                         'DJANGO_SETTING_GETTER',
                         lambda name, dflt: getattr(settings, name, self._env(name, dflt, type)))
        return getter(name, dflt)

    def _setting(self, name, dflt, type=str):
        from django.conf import settings
        getter = getattr(settings,
                         'DJANGO_SSO_APP_SETTING_GETTER',
                         lambda name, dflt: getattr(settings, name, self._env(name, dflt, type)))
        return getter(self.prefix + name, dflt)

    @property
    def SHAPE(self):
        return self._setting('SHAPE', DJANGO_SSO_APP_SHAPE)

    @property
    def BACKEND_ENABLED(self):
        return self.SHAPE in BACKEND_SHAPES

    @property
    def APP_ENABLED(self):
        return not self.BACKEND_ENABLED

    @property
    def APIGATEWAY_ENABLED(self):
        return self.SHAPE.find('apigateway') > -1

    @property
    def APIGATEWAY_HOST(self):
        return self._setting('APIGATEWAY_HOST', 'http://kong:8001')

    @property
    def BACKEND_STANDALONE(self):
        return self.SHAPE.find('standalone') > -1

    @property
    def REPLICATE_PROFILE(self):
        return self.SHAPE.find('persistence') > -1

    @property
    def BACKEND_CUSTOM_FRONTEND_APP(self):
        return self._setting('BACKEND_CUSTOM_FRONTEND_APP', None)

    @property
    def BACKEND_HAS_CUSTOM_FRONTEND_APP(self):
        return self.BACKEND_CUSTOM_FRONTEND_APP is not None

    @property
    def BACKEND_FRONTEND_APP_RESTONLY(self):
        return self._setting('BACKEND_FRONTEND_APP_RESTONLY', self.BACKEND_HAS_CUSTOM_FRONTEND_APP)

    @property
    def COOKIE_DOMAIN(self):
        return self._django_setting('COOKIE_DOMAIN', COOKIE_DOMAIN)  # defaults to .settings value

    @property
    def COOKIE_AGE(self):
        days_expire = 365
        return self._django_setting('COOKIE_AGE', days_expire * 24 * 60 * 60, int)

    @property
    def COOKIE_HTTPONLY(self):
        return self._django_setting('COOKIE_HTTPONLY', True, bool)

    @property
    def APIGATEWAY_CONSUMER_GROUP(self):
        return self._setting('APIGATEWAY_CONSUMER_GROUP', self.COOKIE_DOMAIN)

    @property
    def APIGATEWAY_CONSUMER_USERNAME_HEADER(self):
        return self._setting('APIGATEWAY_CONSUMER_USERNAME_HEADER', 'HTTP_X_CONSUMER_USERNAME')

    @property
    def APIGATEWAY_ANONYMOUS_CONSUMER_USERNAME(self):
        return self._setting('APIGATEWAY_ANONYMOUS_CONSUMER_USERNAME', 'anonymous')

    @property
    def APIGATEWAY_ANONYMOUS_CONSUMER_USERNAMES(self):
        return self._setting('APIGATEWAY_ANONYMOUS_CONSUMER_USERNAMES', [self.APIGATEWAY_ANONYMOUS_CONSUMER_USERNAME])

    @property
    def APIGATEWAY_CONSUMER_GROUPS_HEADER(self):
        return self._setting('APIGATEWAY_CONSUMER_GROUPS_HEADER', 'HTTP_X_CONSUMER_GROUPS')

    @property
    def BACKEND_SIGNUP_MUST_FILL_PROFILE(self):
        return self._setting('BACKEND_SIGNUP_MUST_FILL_PROFILE', False, bool)

    @property
    def USER_FIELDS(self):
        return self._setting('USER_FIELDS', ('username', 'email'), tuple)

    @property
    def REQUIRED_USER_FIELDS(self):
        return self._setting('REQUIRED_USER_FIELDS', self.USER_FIELDS)

    @property
    def PROFILE_FIELDS(self):
        return self._setting('PROFILE_FIELDS', ('first_name', 'last_name',
                                                'ssn', 'phone',
                                                'description',
                                                'picture',
                                                'birthdate',
                                                'latitude', 'longitude',
                                                'country',
                                                'address',
                                                'language'), tuple)

    @property
    def REQUIRED_PROFILE_FIELDS(self):
        return self._setting('REQUIRED_PROFILE_FIELDS', (), tuple)

    @property
    def HTTP_PROTOCOL(self):
        return self._django_setting('HTTP_PROTOCOL', ACCOUNT_DEFAULT_HTTP_PROTOCOL)  # defaults to .settings value

    @property
    def APP_DOMAIN(self):
        return self._django_setting('APP_DOMAIN', APP_DOMAIN)  # defaults to .settings value

    @property
    def APP_URL(self):
        return self._django_setting('APP_URL', self.HTTP_PROTOCOL + '://' + self.APP_DOMAIN)

    @property
    def SERVICE_URL(self):
        return self._setting('SERVICE_URL', self.APP_URL)

    @property
    def SERVICE_SUBSCRIPTION_REQUIRED(self):
        return self._setting('SERVICE_SUBSCRIPTION_REQUIRED', self.REPLICATE_PROFILE, bool)

    @property
    def LOGIN_URL(self):
        return self._setting('LOGIN_URL', '/login/')

    @property
    def LOGIN_MUST_FILL_PROFILE(self):
        return self._setting('LOGIN_MUST_FILL_PROFILE', False, bool)

    @property
    def MANAGE_USER_GROUPS(self):
        return self._setting('MANAGE_USER_GROUPS', True, bool)

    @property
    def AUTH_HEADER_TYPES(self):
        return self._setting('AUTH_HEADER_TYPES', ('Bearer',))

    @property
    def JWT_COOKIE_NAME(self):
        return self._setting('JWT_COOKIE_NAME', 'jwt')

    @property
    def JWT_ALGORITHM(self):
        _JWT_ALLOWED_ALGORITHMS = (
            'HS256',
            'HS384',
            'HS512',
            'RS256',
            'RS384',
            'RS512',
        )

        return self._setting('JWT_ALGORITHM', _JWT_ALLOWED_ALGORITHMS[0])

    @property
    def TOKENS_JWT_SECRET(self):
        return self._setting('TOKENS_JWT_SECRET', 'secret')

    @property
    def USER_ID_CLAIM(self):
        return self._setting('USER_ID_CLAIM', 'sso_id')

    @property
    def BACKEND_STAFF_TOKEN(self):
        return self._setting('BACKEND_STAFF_TOKEN', None)

    @property
    def DJANGO_SSO_APP_USER_ID_FIELD(self):
        return self._setting('DJANGO_SSO_APP_USER_ID_FIELD', 'sso_app_profile__sso_id')

    @property
    def BACKEND_HIDE_PASSWORD_FROM_USER_SERIALIZER(self):
        return self._setting('BACKEND_HIDE_PASSWORD_FROM_USER_SERIALIZER', self.BACKEND_ENABLED, bool)

    @property
    def BACKEND_DOMAINS(self):
        return self._setting('BACKEND_DOMAINS', [self.APP_DOMAIN], list)

    @property
    def BACKEND_DOMAIN(self):
        return self._setting('BACKEND_DOMAIN', self.BACKEND_DOMAINS[0],)

    @property
    def BACKEND_DOMAINS_DICT(self):
        _BACKEND_DOMAINS_DICT = {}
        i = 0
        for el in self.BACKEND_DOMAINS:
            _BACKEND_DOMAINS_DICT[el] = i
            i += 1
        return _BACKEND_DOMAINS_DICT

    @property
    def BACKEND_FULL_URLS_CHAIN(self):
        return ['{}://{}'.format(self.HTTP_PROTOCOL, el) for el in self.BACKEND_DOMAINS]

    @property
    def BACKEND_URLS_CHAIN(self):
        return ['{}://{}'.format(self.HTTP_PROTOCOL, el) for el in self.BACKEND_DOMAINS if el != self.APP_DOMAIN]

    @property
    def BACKEND_URLS_CHAIN_DICT(self):
        i = 0
        _BACKEND_URLS_CHAIN_DICT = {}
        for el in self.BACKEND_URLS_CHAIN:
            _BACKEND_URLS_CHAIN_DICT[el] = i
            i += 1
        return _BACKEND_URLS_CHAIN_DICT

    @property
    def PASSEPARTOUT_PROCESS_ENABLED(self):
        return len(self.BACKEND_URLS_CHAIN) > 0

    @property
    def BACKEND_URL(self):
        return self._setting('BACKEND_URL', self.HTTP_PROTOCOL + '://' + self.BACKEND_DOMAIN)

    @property
    def REMOTE_USERS_URL(self):
        return self.BACKEND_URL + '/api/v1/auth/users/'

    @property
    def REMOTE_USER_URL(self):
        return self.REMOTE_USERS_URL + '{sso_id}/'

    @property
    def REMOTE_PROFILES_URL(self):
        return self.BACKEND_URL + '/api/v1/auth/profiles/'

    @property
    def REMOTE_PROFILE_URL(self):
        return self.REMOTE_PROFILES_URL + '{sso_id}/'

    @property
    def REMOTE_LOGIN_URL(self):
        return self.BACKEND_URL + '/login/'

    @property
    def REMOTE_LOGOUT_URL(self):
        return self.BACKEND_URL + '/logout/'

    @property
    def REMOTE_SIGNUP_URL(self):
        return self.BACKEND_URL + '/signin/'

    @property
    def REMOTE_EMAIL_URL(self):
        return self.BACKEND_URL + '/email/'

    @property
    def REMOTE_PROFILE_VIEW_URL(self):
        return self.BACKEND_URL + '/profile/'

    @property
    def REMOTE_PROFILE_UPDATE_URL(self):
        return self.BACKEND_URL + '/profile/update/'

    @property
    def I18N_PATH_ENABLED(self):
        return self._django_setting('I18N_PATH_ENABLED', I18N_PATH_ENABLED, bool)

    @property
    def SOCIALACCOUNTS(self):
        return self._django_setting('SOCIALACCOUNTS', ['google'], list)

    @property
    def SOCIALACCOUNTS_ENABLED(self):
        return self._django_setting('SOCIALACCOUNTS_ENABLED', len(self.SOCIALACCOUNTS) > 0, bool)

    @property
    def STAFF_USER_GROUPS(self):
        return self._django_setting('STAFF_USER_GROUPS', ['staff'], list)

    @property
    def TEST_USER_USERNAME(self):
        return self._django_setting('TEST_USER_USERNAME', 'user')

    @property
    def TEST_USER_EMAIL(self):
        return self._django_setting('TEST_USER_EMAIL', 'user@example.com')


# Ugly? Pennersr says Guido recommends this himself ...
# http://mail.python.org/pipermail/python-ideas/2012-May/014969.html
import sys  # noqa

app_settings = AppSettings('DJANGO_SSO_APP_')
app_settings.__name__ = __name__
sys.modules[__name__] = app_settings
