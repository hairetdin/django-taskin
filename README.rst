======
Taskin
======

Taskin is a Django app for task management. Create many projects and tasks.


Required
--------

Python 3.x

* pip install djangorestframework
* pip install djangorestframework-jwt


Quick start
-----------

1. Clone this Taskin application

  git clone https://github.com/hairetdin/django-taskin.git

  cd django-taskin

2. Install

  pip install dist/django-taskin-0.1.tar.gz

3. Add 'taskin' and 'rest_framework' to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'rest_framework',
        'taskin',
    ]

4. Add REST_FRAMEWORK and JWT_AUTH settings::

    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.AllowAny',
        ],
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
            'rest_framework.authentication.SessionAuthentication',
        ),
        'PAGE_SIZE': 10,
    }

    import datetime
    JWT_AUTH = {
        'JWT_RESPONSE_PAYLOAD_HANDLER': 'taskin.views.jwt_response_payload_handler',
        'JWT_AUTH_HEADER_PREFIX': 'Bearer',
        # default JWT_EXPIRATION_DELTA - 5 minutes
        # JWT_EXPIRATION_DELTA = datetime.timedelta(seconds=300)
        'JWT_EXPIRATION_DELTA': datetime.timedelta(hours=12),
    }

5. Add email settings for send notification to user about task::

    EMAIL_HOST = ''
    EMAIL_PORT = ''
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    DEFAULT_FROM_EMAIL = ''

Mail is sent using the SMTP host and port specified in the EMAIL_HOST and EMAIL_PORT settings.
The EMAIL_HOST_USER and EMAIL_HOST_PASSWORD settings,
if set, are used to authenticate to the SMTP server,
and the EMAIL_USE_TLS and EMAIL_USE_SSL settings control whether a secure connection is used.
See https://docs.djangoproject.com/en/dev/ref/settings for more detail.

User get notify to email If you add

    TASKIN_DEFAULT_FROM_EMAIL = 'your.email@your-domain.com'

in settings.
User email address take from user.email field.

6. Include the taskin URLconf in your project urls.py like this::

    url(r'^taskin/', include('taskin.urls')),

7. Run `python manage.py migrate` to create the taskin models.

8. Run server

  python manage.py runserver

9. Visit http://127.0.0.1:8000/taskin/ to create new project and task.


Uninstall
---------

  pip uninstall django-taskin

Internationalization
--------------------

There are available two language: english and russian. English - default.

Add settings to settings.py to apply Russian translation

    LANGUAGE_CODE = 'ru-ru'
    #LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    LOCALE_PATHS = [
        #os.path.join(BASE_DIR, 'locale'),
        os.path.join(BASE_DIR, "taskin/locale"),
    ]
