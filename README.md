# Aesculapius_kg

Aesculapius is a medical service that offers search and placement of information about your clinics and professional
specialists.

### Its features include the following:

* Convenient search for clinics and professional specialists
* Detailed information about each specialist and clinic
* The fastest way to choose a doctor and sign up for a consultation

## Setup

The first thing to do is to clone the repository:

```shell
$ git clone https://github.com/0muraliev/Aesculapius_kg.git
$ cd Aesculapius_kg
```

Create a virtual environment to install dependencies in and activate it:

```shell
$ virtualenv venv
$ source venv/bin/activate
```

Then install the dependencies:

```shell
(venv)$ pip install -r requirements.txt
```

Before applying migrations, create a secret_settings.py file in the Platform folder:

```python
SECRET_KEY = '<SECRET_KEY>'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '<CLIENT_ID>',
            'secret': '<SECRET>',
        },
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'}
    },
    'vk': {
        'APP': {
            'client_id': '<CLIENT_ID>',
            'secret': '<SECRET>',
        },
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'}
    }
}

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = '<EMAIL>'
EMAIL_HOST_PASSWORD = '<PASSWORD>'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_SUBJECT_PREFIX = '[Aesculapius.kg] '

LOCATION_FIELD = {
    'provider.google.api': '//maps.google.com/maps/api/js?sensor=false',
    'provider.google.api_key': '<API_KEY>',
    'provider.google.map.type': 'ROADMAP',
}
```

We apply migrations and start the server:

```shell
(venv)$ python manage.py migrate
  ...
(venv)$ python manage.py runserver
```
