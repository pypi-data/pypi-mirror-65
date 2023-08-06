# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='djangorestsearch',
    version='0.8.5',
    url='https://github.com/wemap/django-rest-search',
    license='BSD',
    description='ElasticSearch integration for Django.',
    long_description=open('README.rst', 'r').read(),
    author='Jeremy Lainé',
    author_email='jeremy@getwemap.com',
    packages=['rest_search'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        "Programming Language :: Python :: 3 :: Only",
    ],
    install_requires=[
        'aws-requests-auth>=0.3.0',
        'elasticsearch>=6.0.0,<7.0.0',
    ],
    python_requires='>=3',
)
