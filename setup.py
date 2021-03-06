#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='TruePeopleSearch',
    author='thehappydinoa',
    version='1.0.3',
    author_email='thehappydinoa@gmail.com',
    description='Uses True People Search to gather info',
    license='GPLv3',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    zip_safe=False,
    package_data={
        '': ['*.gif', '*.png', '*.conf', '*.mtz', '*.machine']  # list of resources
    },
    install_requires=[
        'canari>=3.3.9,<4',
        'beautifulsoup4>=4.6.3',
        'requests>=2.19.1',
        'fake-useragent>=0.1.11'
    ]
)
