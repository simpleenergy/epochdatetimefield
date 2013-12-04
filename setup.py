#!/usr/bin/env python
from setuptools import setup, find_packages
import subprocess
import os

__doc__ = """
App for Django to allow using datetime objects over integer fields.
"""


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

STAGE = 'final'

version = (0, 1, 1, STAGE)


def get_version():
    number = '.'.join(map(str, version[:3]))
    stage = version[3]
    if stage == 'final':
        return number
    elif stage == 'alpha':
        process = subprocess.Popen('git rev-parse HEAD'.split(), stdout=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return number + '-' + stdout.strip()[:8]

setup(
    name='epochdatetimefield',
    version=get_version(),
    description=__doc__,
    long_description=read('README.rst'),
    url="https://epochdatetimefield.readthedocs.org/en/latest/",
    author="SimpleEnergy",
    author_email='nick@simpleenergy.com',
    packages=[package for package in find_packages() if package.startswith('epochdatetimefield')],
    install_requires=[
        'Django>=1.4',
    ],
    zip_safe=False,
    include_package_data=True,
)
