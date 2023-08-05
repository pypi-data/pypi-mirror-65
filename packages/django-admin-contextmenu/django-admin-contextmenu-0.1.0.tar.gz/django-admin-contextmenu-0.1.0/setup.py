#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import io
from os.path import join, dirname
from setuptools import setup


def get_version(package):
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search('__version__ = [\'"]([^\'"]+)[\'"]', init_py).group(1)


# use io.open until python2.7 support is dropped
with io.open("README.md", encoding="utf8") as f:
    readme = f.read()

with io.open("CHANGELOG.md", encoding="utf8") as f:
    changelog = f.read()


setup(
    name='django-admin-contextmenu',
    version=get_version('contextmenu'),
    url='https://github.com/nshayanfar/django-admin-contextmenu',
    license='MIT',
    description='django-admin-contextmenu app, adds a contextmenu column to django admin\'s changelist page.',
    long_description=readme + changelog,
    long_description_content_type="text/markdown",
    author='Nima Shayanfar',
    author_email='nshayanfar@gmail.com',
    packages=['contextmenu'],
    package_data={
        '': ['**/**/*.html']
    },
    python_requires='>=3.5',
    zip_safe=False,
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Utilities',
    ],
)
