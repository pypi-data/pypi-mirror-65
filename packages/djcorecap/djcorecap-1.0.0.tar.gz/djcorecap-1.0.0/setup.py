# -*- coding: utf-8 -*-

'''
djcorecap/setup
---------------

setuptools setup file for the djcorecap package
'''


import os
from setuptools import find_packages, setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'bokeh>=1.1.0',
    'django>=1.8',
    'django-crispy-forms>=1.7.2',
]

setup_requirements = []

test_requirements = []


setup(
    author='Chris Pappalardo',
    author_email='cpappala@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.0',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    description='Useful functions, tags, and Bootstrap-friendly templates for Django.',
    install_requires=requirements,
    license="MIT license",
    long_description='%s\n\n%s' % (readme, history),
    include_package_data=True,
    keywords='djcorecap',
    name='djcorecap',
    packages=find_packages(),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/ChrisPappalardo/djcorecap',
    version='1.0.0',
    zip_safe=False,
)
