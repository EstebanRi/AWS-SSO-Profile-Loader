#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name='AWS Profile Loader',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
"boto3"
    ],
    entry_points={
        'console_scripts': [
            'awsupdatecredentials=scripts.update_credentials_new:main',
            'awssetprofile=scripts.set_default_profile:main'
        ]
    }
)