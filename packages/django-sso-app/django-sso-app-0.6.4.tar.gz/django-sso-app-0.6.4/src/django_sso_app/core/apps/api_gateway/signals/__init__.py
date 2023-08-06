from .... import app_settings


if app_settings.APIGATEWAY_ENABLED:
    if app_settings.BACKEND_ENABLED:
        from .backend import *
    else:
        from .app import *
