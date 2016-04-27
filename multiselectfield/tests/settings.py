INSTALLED_APPS = [
    'multiselectfield',
]

SECRET_KEY = '1'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.db',
    }
}