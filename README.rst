======
Taskin
======

Taskin is a Django app for task management. Create many projects and tasks.


Required
--------

* pip install djangorestframework
* pip install djangorestframework-jwt


Quick start
-----------

1. Download this Taskin application

  wget https://github.com/hairetdin/django-taskin/archive/master.zip

  unzip master.zip

  cd django-taskin-master

2. Install

  python setup.py install

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
            'rest_framework.authentication.SessionAuthentication',
            'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
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

5. Include the taskin URLconf in your project urls.py like this::

    url(r'^taskin/', include('taskin.urls')),

6. Run `python manage.py migrate` to create the taskin models.

7. Visit http://127.0.0.1:8000/taskin/ to create new project and task.
