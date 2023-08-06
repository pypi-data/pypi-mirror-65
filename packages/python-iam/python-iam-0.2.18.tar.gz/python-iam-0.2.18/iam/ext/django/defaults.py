"""Specifies configuration defaults for the :mod:`iam.ext.django` Django
application.
"""
import os

from django.urls import reverse_lazy
from unimatrix.lib.environ import parselist


__all__ = [
    'AUTH_USER_MODEL',
    'AUTHENTICATION_BACKENDS',
    'IAM_ACCOUNT_PRINCIPALS',
    'IAM_REALM',
    'IAM_REALM_SETTINGS',
    'IAM_DEBUG_PATH',
    'IAM_TERMS_OF_SERVICE',
    'IAM_PRIVACY_POLICY',
    'IAM_ENABLE_DEBUG_PAGE',
    'IAM_ENABLE_FACEBOOK',
    'IAM_ENABLE_GOOGLE',
    'IAM_ENABLE_LINKEDIN',
    'IAM_ENABLE_MAGIC_LINK',
    'IAM_ENABLE_PASSWORD_RESET',
    'IAM_ENABLE_TWITTER',
    'IAM_IMAGE_LOGO',
    'IAM_IMAGE_SPLASH',
    'IAM_REDIRECT_AUTHENTICATED_USER',
    'IAM_REQUIRE_USERNAME',
    'IAM_STAFF_REALM',
    'IAM_SUPERUSER_REALM',
    'IAM_TERMS_AUTHORITATIVE_LANGUAGE',
    'IAM_URL_NAMESPACE',
    'LOGIN_URL',
    'LOGIN_REDIRECT_URL',
    'LOGOUT_REDIRECT_URL',
    'SOCIAL_AUTH_FACEBOOK_KEY',
    'SOCIAL_AUTH_FACEBOOK_SECRET',
    'SOCIAL_AUTH_GOOGLE_OAUTH2_KEY',
    'SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET',
    'SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY',
    'SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET',
    'SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE',
    'SOCIAL_AUTH_LINKEDIN_OAUTH2_FIELD_SELECTORS',
    'SOCIAL_AUTH_LINKEDIN_OAUTH2_EXTRA_DATA',
    'SOCIAL_AUTH_PIPELINE',
    'SOCIAL_AUTH_TWITTER_KEY',
    'SOCIAL_AUTH_TWITTER_SECRET',
    'SOCIAL_AUTH_URL_NAMESPACE',
]

AUTH_USER_MODEL = 'iam.Subject'

AUTHENTICATION_BACKENDS = [
    'iam.ext.django.lib.backends.LocalSubjectBackend',
    'iam.ext.django.lib.backends.PhonenumberBackend'
]


#: Account principal types that may be used to register a new account.
#: Valid values are 'username', 'email' and 'phonenumber'. May be provided
#: through the environment variable 'IAM_ACCOUNT_PRINCIPALS' as a
#: colon-separated list, using :mod:`iam.ext.django.defaults`. The ``email``
#: account principal is always enabled.
IAM_ACCOUNT_PRINCIPALS = parselist(os.environ, 'IAM_ACCOUNT_PRINCIPALS', cls=list)
if 'email' not in IAM_ACCOUNT_PRINCIPALS:
    IAM_ACCOUNT_PRINCIPALS.append('email')

IAM_DEBUG_PATH = os.getenv('IAM_DEBUG_PATH') or '/debug'

IAM_REALM = 'default'

#: Settings per realm.
IAM_REALM_SETTINGS = {}

#: Specifies the :term:`Realm` in which :term:`Super Users` are created.
IAM_SUPERUSER_REALM = os.getenv('IAM_SUPERUSER_REALM') or 'master'

#: Specifies the :term:`Realm` in which :term:`Staff Users` are created.
IAM_STAFF_REALM = os.getenv('IAM_STAFF_REALM') or 'backoffice'

IAM_ENABLE_DEBUG_PAGE = os.getenv('IAM_ENABLE_DEBUG_PAGE') == '1'

IAM_ENABLE_GOOGLE = os.getenv('IAM_ENABLE_GOOGLE') == '1'

IAM_ENABLE_FACEBOOK = os.getenv('IAM_ENABLE_FACEBOOK') == '1'

IAM_ENABLE_LINKEDIN = os.getenv('IAM_ENABLE_LINKEDIN') == '1'

IAM_ENABLE_MAGIC_LINK = os.getenv('IAM_ENABLE_MAGIC_LINK') == '1'

IAM_ENABLE_PASSWORD_RESET = os.getenv('IAM_ENABLE_PASSWORD_RESET') == '1'

IAM_ENABLE_TWITTER = os.getenv('IAM_ENABLE_TWITTER') == '1'

IAM_IMAGE_LOGO = os.getenv('IAM_IMAGE_LOGO')\
    or 'iam/logo.svg'

IAM_IMAGE_SPLASH = os.getenv('IAM_IMAGE_SPLASH')\
    or 'iam/splash.jpg'

#: Slug of the :class:`~iam.ext.django.models.PlatformAgremeent` that
#: maintains the :term:`Privacy Policy`.
IAM_PRIVACY_POLICY = 'privacy'


#: Redirect authenticated users when they visit the login page. Default is
#: ``True``.
IAM_REDIRECT_AUTHENTICATED_USER = os.getenv('IAM_REDIRECT_AUTHENTICATED_USER') == '1'
if os.getenv('IAM_REDIRECT_AUTHENTICATED_USER') is None:
    IAM_REDIRECT_AUTHENTICATED_USER = True


IAM_REQUIRE_USERNAME = os.getenv('IAM_REQUIRE_USERNAME') == '1'

#: Slug of the :class:`~iam.ext.django.models.PlatformAgremeent` that
#: maintains the :term:`Terms of Service`.
IAM_TERMS_OF_SERVICE = 'terms'


#: Specifies the authoritative language of platform terms.
IAM_TERMS_AUTHORITATIVE_LANGUAGE = 'en'

IAM_URL_NAMESPACE = 'iam'

LOGIN_URL = reverse_lazy(f'{IAM_URL_NAMESPACE}:login')

LOGIN_REDIRECT_URL = '/'

LOGOUT_REDIRECT_URL = reverse_lazy(f'{IAM_URL_NAMESPACE}:login')

SOCIAL_AUTH_FACEBOOK_KEY = os.getenv('IAM_FACEBOOK_KEY')

SOCIAL_AUTH_FACEBOOK_SECRET = os.getenv('IAM_FACEBOOK_SECRET')

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('GOOGLE_OAUTH2_KEY')

SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('GOOGLE_OAUTH2_SECRET')

SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = os.getenv('IAM_LINKEDIN_KEY')

SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = os.getenv('IAM_LINKEDIN_SECRET')

SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE = ['r_basicprofile', 'r_emailaddress']

SOCIAL_AUTH_LINKEDIN_OAUTH2_FIELD_SELECTORS = [
    'email-address',
    'formatted-name',
    'public-profile-url',
    'picture-url'
]

SOCIAL_AUTH_PIPELINE = (
    'iam.ext.django.lib.auth.on_redirected',
    'iam.ext.django.lib.auth.on_authenticated',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details'
)

SOCIAL_AUTH_LINKEDIN_OAUTH2_EXTRA_DATA = [
    ('id', 'id'),
    ('formattedName', 'name'),
    ('emailAddress', 'email_address'),
    ('pictureUrl', 'picture_url'),
    ('publicProfileUrl', 'profile_url'),
]

SOCIAL_AUTH_TWITTER_KEY = os.getenv('IAM_TWITTER_KEY')

SOCIAL_AUTH_TWITTER_SECRET = os.getenv('IAM_TWITTER_SECRET')

SOCIAL_AUTH_URL_NAMESPACE = 'social'

if IAM_ENABLE_FACEBOOK:
    AUTHENTICATION_BACKENDS.insert(0,
        'social_core.backends.facebook.FacebookOAuth2')

if IAM_ENABLE_GOOGLE:
    AUTHENTICATION_BACKENDS.insert(0,
        'iam.lib.backends.google.GoogleOAuth2')

if IAM_ENABLE_LINKEDIN:
    AUTHENTICATION_BACKENDS.insert(0,
        'social_core.backends.linkedin.LinkedinOAuth2')

if IAM_ENABLE_TWITTER:
    AUTHENTICATION_BACKENDS.insert(0,
        'social_core.backends.twitter.TwitterOAuth')
