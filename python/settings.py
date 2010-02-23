from ragendja.settings_pre import *
from settings_private import SECRET_KEY, DISQUS_WEBSITE_SHORTNAME, \
    DISQUS_API_KEY, GOOGLE_ANALYTICS_ID, DEFAULT_FROM_EMAIL, JAVA_DOMAIN

SERVER_EMAIL = DEFAULT_FROM_EMAIL

MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/media/admin/'

USE_I18N = False
LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', 'English'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
)

MIDDLEWARE_CLASSES = (
    'google.appengine.ext.appstats.recording.AppStatsDjangoMiddleware',
    'ragendja.middleware.ErrorMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # Django authentication
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # Google authentication
    #'ragendja.auth.middleware.GoogleAuthenticationMiddleware',
    # Hybrid Django/Google authentication
    #'ragendja.auth.middleware.HybridAuthenticationMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'ragendja.sites.dynamicsite.DynamicSiteIDMiddleware',
    'cc.vidr.util.OverrideSiteIDMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
)

# Google authentication
#AUTH_USER_MODULE = 'ragendja.auth.google_models'
#AUTH_ADMIN_MODULE = 'ragendja.auth.google_admin'
# Hybrid Django/Google authentication
#AUTH_USER_MODULE = 'ragendja.auth.hybrid_models'

LOGIN_URL = '/account/login/'
LOGOUT_URL = '/account/logout/'
LOGIN_REDIRECT_URL = '/'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.webdesign',
    'django.contrib.flatpages',
    'django.contrib.redirects',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    
    # third-party
    'appenginepatcher',
    'tabs',
    'disqus',
    'recurse',
    'console',
    
    # template tags
    'helloworld',
    'quotes',
    'codehilite',
    
    # views
    'projects',
    'backup',
    'blog',
    'pages',
)

from ragendja.settings_post import *
