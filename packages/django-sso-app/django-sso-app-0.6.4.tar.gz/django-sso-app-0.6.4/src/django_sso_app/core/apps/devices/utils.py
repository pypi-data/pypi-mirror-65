import logging

from allauth.account.adapter import get_adapter

from ...tokens.utils import jwt_decode
from ...utils import get_session_key, set_session_key
from ...tokens.utils import get_request_jwt
from ...exceptions import RequestHasValidJwtWithNoDeviceAssociated

logger = logging.getLogger('django_sso_app.core.apps.devices')


def get_request_device(request):
    device = getattr(request, 'device', None)

    if device is None:
        logger.debug('no previous device')
        fingerprint = get_session_key(request, '__django_sso_app__device__fingerprint')

        if fingerprint is None:
            logger.debug('received empty fingerprint')

            raw_token = get_request_jwt(request)

            if raw_token is None:
                fingerprint = 'undefined'
            else:
                try:
                    device, verified_payload = jwt_decode(raw_token, verify=True)

                except RequestHasValidJwtWithNoDeviceAssociated:
                    logger.warning('no device associated to request token "{}"'.format(raw_token))
                    raise
                else:
                    fingerprint = verified_payload['fp']

        if device is None:
            user = request.user
            profile = user.sso_app_profile

            logger.info(
                'Request has no device, getting profile "{}" device with fingerprint "{}"'.format(profile,
                                                                                                  fingerprint))

            device = profile.devices.filter(fingerprint=fingerprint).first()

            if device is None:
                logger.debug('profile has no device with fingerprint "{}"'.format(fingerprint))
                adapter = get_adapter(request)
                device = adapter.add_user_profile_device(user, fingerprint)
            else:
                logger.debug('fingerprint "{}" had device'.format(fingerprint))

        else:
            logger.debug('request has device "{}"'.format(device))

    else:
        logger.info(
            'request already has device "{}"'.format(device))

    assert device is not None

    setattr(request, 'device', device)
    set_session_key(request, '__django_sso_app__device__fingerprint', device.fingerprint)

    return device
