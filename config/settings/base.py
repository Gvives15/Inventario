from pathlib import Path
import os
import sys
import dj_database_url

def _env(*names):
    for n in names:
        v = os.getenv(n)
        if v:
            return v
    return None

BASE_DIR = Path(__file__).resolve().parent.parent.parent

sys.path.append(str(BASE_DIR / 'core' / 'src'))
sys.path.append(str(BASE_DIR / 'core' / 'src' / 'api'))

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY') or 'dev-unsafe-default'
DEBUG = os.getenv('DEBUG', 'True') == 'True'

_default_hosts = ['localhost', '127.0.0.1']
ALLOWED_HOSTS = [h.strip() for h in (os.getenv('DJANGO_ALLOWED_HOSTS') or ','.join(_default_hosts)).split(',') if h.strip()]
CSRF_TRUSTED_ORIGINS = [f"https://{h.lstrip('.')}" for h in ALLOWED_HOSTS if not h.startswith('.')]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'inventory',
    'panel',
    'contact.apps.ContactConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'panel' / 'src' / 'web' / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

_pg_host = _env('PGHOST', 'almacenamiento_PGHOST')
_pg_user = _env('PGUSER', 'almacenamiento_PGUSER')
_pg_password = _env('PGPASSWORD', 'almacenamiento_PGPASSWORD')
_pg_db = _env('PGDATABASE', 'almacenamiento_PGDATABASE')
_pg_port = _env('PGPORT', 'almacenamiento_PGPORT') or '5432'
_pg_sslmode = _env('PGSSLMODE', 'almacenamiento_PGSSLMODE')
_aws_region = _env('AWS_REGION', 'almacenamiento_AWS_REGION')

if not _pg_password and _pg_host and _pg_user and _aws_region:
    try:
        import boto3
        rds = boto3.client('rds', region_name=_aws_region)
        _pg_password = rds.generate_db_auth_token(DBHostname=_pg_host, Port=int(_pg_port), DBUsername=_pg_user)
    except Exception:
        _pg_password = None
_pg_url = None
if _pg_host and _pg_user and _pg_db and _pg_password:
    _pg_url = f"postgres://{_pg_user}:{_pg_password}@{_pg_host}:{_pg_port}/{_pg_db}"
    if _pg_sslmode:
        _pg_url += f"?sslmode={_pg_sslmode}"

_DB_URL = _env('DATABASE_URL', 'POSTGRES_URL', 'POSTGRES_PRISMA_URL') or _pg_url

DATABASES = {
    'default': (
        dj_database_url.parse(_DB_URL, conn_max_age=600)
        if _DB_URL
        else dj_database_url.config(default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'), conn_max_age=0)
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
