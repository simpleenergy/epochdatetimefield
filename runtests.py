#!/usr/bin/env python
import sys

from django.conf import settings


settings.configure(
    DATABASES={
        'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': ':memory;'}
    },
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
