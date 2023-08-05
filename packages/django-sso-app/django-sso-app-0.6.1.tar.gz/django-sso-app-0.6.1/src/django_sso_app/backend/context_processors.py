from django.conf import settings
# from meta.views import Meta

def emails_domain_settings(request):
    return {
        "EMAILS_DOMAIN": settings.EMAILS_DOMAIN,
        "EMAILS_SITE_NAME": settings.EMAILS_SITE_NAME,

        "DJANGO_ALLAUTH_ENABLED": getattr(settings, 'DJANGO_ALLAUTH_ENABLED', None)
    }

def google_api_settings(request):
    return {
        "GOOGLE_API_KEY": settings.GOOGLE_API_KEY,
        "GOOGLE_MAPS_API_VERSION": settings.GOOGLE_MAPS_API_VERSION,
    }

def google_analytics_settings(request):
    return {
        "GOOGLE_ANALYTICS_TRACKING_ID": settings.GOOGLE_ANALYTICS_TRACKING_ID,
    }

def raven_js_dsn_settings(request):
    return {
        "RAVEN_JS_DSN": settings.RAVEN_JS_DSN,
    }

def disable_js(request):
    is_active = request.GET.get('nojs', None)

    return {
        "DISABLE_JS": is_active is not None,
    }

def get_repository_rev(request):
    return {
        "REPOSITORY_REV": settings.REPOSITORY_REV
    }

"""
def django_meta(request):
    return {
        'meta': Meta(
           description=settings.META_DEFAULT_DESCRIPTION,
        )
    }
"""

def get_meta_info(request):
    return {
        "META_DESCRIPTION": getattr(settings, 'META_DESCRIPTION', '')
    }
