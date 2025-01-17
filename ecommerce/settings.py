import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY', '')

if os.environ.get('ENV') == 'development':
    DEBUG = True
else:
    DEBUG = False

ALLOWED_HOSTS = [
    'localhost',
    '8000-pharting-supplemint-evq9f9h4spd.ws.codeinstitute-ide.net',
    'supplemint-ff2fe0e93175.herokuapp.com', ]

CSRF_TRUSTED_ORIGINS = [
    'https://8000-pharting-supplemint-evq9f9h4spd.ws.codeinstitute-ide.net',
    'https://supplemint-ff2fe0e93175.herokuapp.com']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'home',
    'products',
    'bag',
    'checkout',
    'profiles',
    'storages',
    'contact',
    'blog',
    'referrals',
    'reviews',
    'ckeditor',
    'ckeditor_uploader',
    'core',
    'django.contrib.sitemaps',
    'compressor',
]

MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
    'csp.middleware.CSPMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'templates', 'allauth'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'bag.contexts.bag_contents',
            ],
        },
    },
]

SITE_ID = 1

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = False
ACCOUNT_USERNAME_MIN_LENGTH = 4
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_ON_GET = True
LOGOUT_REDIRECT_URL = '/'

MESSAGES_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

WSGI_APPLICATION = 'ecommerce.wsgi.application'

if 'DATABASE_URL' in os.environ:
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'UserAttributeSimilarityValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'MinimumLengthValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'CommonPasswordValidator'
        ),
    },
    {
        'NAME': (
            'django.contrib.auth.password_validation.'
            'NumericPasswordValidator'
        ),
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

ACCOUNT_FORMS = {
    'signup': 'referrals.forms.CustomSignupForm',
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = 'static/'

# Django Compressor Settings
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    BASE_DIR / "static",
]


def add_cache_headers(headers, path, url):
    if path.endswith(('.css', '.js', '.png', '.jpg', '.jpeg', '.webp', '.svg',
                     '.woff', '.woff2')):
        headers['Cache-Control'] = 'public, max-age=31536000, immutable'


# Cache control for static files
WHITENOISE_MAX_AGE = 31536000  # 1 year
WHITENOISE_ALLOW_ALL_ORIGINS = True
WHITENOISE_ADD_HEADERS_FUNCTION = add_cache_headers

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

if 'USE_AWS' in os.environ:
    # Cache control
    AWS_S3_OBJECT_PARAMETERS = {
        'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
        'CacheControl': 'max-age=94608000',
        'ContentEncoding': 'br',  # Enable brotli compression
    }
    # Bucket Config
    AWS_STORAGE_BUCKET_NAME = 'supplemint'
    AWS_S3_REGION_NAME = 'eu-north-1'
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

    # Static and media files
    STATICFILES_STORAGE = 'custom_storages.StaticStorage'
    STATICFILES_LOCATION = 'static'
    DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'
    MEDIAFILES_LOCATION = 'media'

    # Override static and media URLs in production
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATICFILES_LOCATION}/'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Stripe
FREE_DELIVERY_THRESHOLD = 50
STANDARD_DELIVERY_PERCENTAGE = 10
STRIPE_CURRENCY = 'usd'
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', '')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
STRIPE_WH_SECRET = os.getenv('STRIPE_WH_SECRET', '')

# Email
if os.environ.get('ENV') == 'development':
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_TLS = True
    EMAIL_PORT = 587
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASS')
    DEFAULT_FROM_EMAIL = os.getenv('EMAIL_HOST_USER')

# CKEditor Settings
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Full',
        'height': 300,
        'width': '100%',
        'removePlugins': 'stylesheetparser,notification',
        'extraPlugins': 'image2,uploadimage',
        'removeButtons': '',
        'versionCheck': False,
        'toolbar_Full': [
            ['Format', 'Bold', 'Italic', 'Underline', 'Strike',
                'SpellChecker'],
            ['NumberedList', 'BulletedList', 'Indent', 'Outdent',
                'JustifyLeft', 'JustifyCenter', 'JustifyRight',
                'JustifyBlock'],
            ['Image', 'Table', 'Link', 'Unlink', 'Anchor', 'SectionLink',
                'Subscript', 'Superscript'],
            ['Undo', 'Redo'],
            ['Source'],
            ['Maximize']
        ],
    },
}

# Content Security Policy
CSP_DEFAULT_SRC = ("'none'",)
CSP_IMG_SRC = (
    "'self'",
    'data:',
    'https://supplemint-ff2fe0e93175.herokuapp.com/',
    'https://supplemint.s3.eu-north-1.amazonaws.com',
    'https://*.s3.eu-north-1.amazonaws.com',
    'https://supplemint.s3.amazonaws.com'
)
CSP_STYLE_SRC = (
    "'self'",
    "'unsafe-inline'",
    'https://fonts.googleapis.com',
    'https://supplemint-ff2fe0e93175.herokuapp.com/',
    'https://supplemint.s3.amazonaws.com',
    'https://supplemint.s3.eu-north-1.amazonaws.com',
    'https://*.s3.amazonaws.com',
    'https://*.s3.eu-north-1.amazonaws.com'
)
CSP_STYLE_SRC_ELEM = (
    "'self'",
    "'unsafe-inline'",
    'https://fonts.googleapis.com',
    'https://supplemint-ff2fe0e93175.herokuapp.com/',
    'https://supplemint.s3.amazonaws.com',
    'https://supplemint.s3.eu-north-1.amazonaws.com',
    'https://*.s3.amazonaws.com',
    'https://*.s3.eu-north-1.amazonaws.com'
)
CSP_SCRIPT_SRC = (
    "'self'",
    "'unsafe-inline'",
    'https://supplemint-ff2fe0e93175.herokuapp.com/',
    'https://supplemint.s3.eu-north-1.amazonaws.com',
    'https://*.s3.eu-north-1.amazonaws.com',
    'https://supplemint.s3.amazonaws.com',
    'https://js.stripe.com/v3/',
    'https://kit.fontawesome.com',
    'https://code.jquery.com'
)
CSP_SCRIPT_SRC_ELEM = (
    "'self'",
    "'unsafe-inline'",
    'https://supplemint-ff2fe0e93175.herokuapp.com/',
    'https://supplemint.s3.amazonaws.com',
    'https://supplemint.s3.eu-north-1.amazonaws.com',
    'https://*.s3.eu-north-1.amazonaws.com',
    'https://js.stripe.com/v3/',
    'https://kit.fontawesome.com',
    'https://code.jquery.com'
)
CSP_FONT_SRC = (
    "'self'",
    'https://fonts.gstatic.com/',
    'https://ka-f.fontawesome.com/'
)
CSP_CONNECT_SRC = (
    "'self'",
    'https://api.stripe.com/',
    'https://ka-f.fontawesome.com/'
)
CSP_FRAME_SRC = (
    "'self'",
    'https://js.stripe.com'
)
CSP_FRAME_ANCESTORS = (
    "'self'",
    'https://js.stripe.com'
)
