#!/usr/bin/env python
import sys
import os

from django.conf import settings

if os.environ.get('DB_BACKEND') == 'mysql':
    DATABASES = {
        'default': {
            'NAME': 'test_db',
            'ENGINE': 'django.db.backends.mysql',
            'USER': 'travis',
        }
    }
elif os.environ.get('DB_BACKEND') == 'postgres':
    DATABASES = {
        'default': {
            'NAME': 'test_db',
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'USER': 'postgres',
        }
    }
else:
    DATABASES={
        'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory;'}
    }

settings.configure(
    DATABASES=DATABASES,
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
        'epochdatetimefield',
        'epochdatetimefield.tests',
    ],
)


def runtests(*test_args):
    import django.test.utils

    runner_class = django.test.utils.get_runner(settings)
    test_runner = runner_class(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(['epochdatetimefield'])
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
