#!/usr/bin/python
# coding: utf8

import os

from setuptools import setup, find_packages
here = os.path.abspath(os.path.dirname(__file__))

config = {
    'description': 'Flask Azure Active Directory Auth',
    'author': 'Matthias Wutte',
    'url': '',
    'download_url': 'https://github.com/wuttem',
    'author_email': 'matthias.wutte@gmail.com',
    'version': '0.8',
    'install_requires': [
        "flask",
        "werkzeug",
        "flask-login",
        "requests"
    ],
    'tests_require': ["pytest", "mock"],
    'packages': find_packages(),
    'scripts': [],
    'name': 'flask-ad-auth'
}

setup(**config)