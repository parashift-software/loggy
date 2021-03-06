#!/usr/bin/env python

from setuptools import find_packages
from setuptools import setup

PROJECT = 'loggy'

# Change docs/sphinx/conf.py too!
VERSION = '0.1'

try:
    long_description = open('README.md', 'rt').read()
except IOError:
    long_description = ''

setup(
    name=PROJECT,
    version=VERSION,

    description='AWS LogGroup-Kinesis Subscription Manager',
    long_description=long_description,

    author='Grayson Kuhns',
    author_email='grayson@parashift.xyz',

    url='https://github.com/parashift-software/loggy',
    download_url='https://github.com/parashift-software/loggy',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Intended Audience :: Developers',
        'Environment :: Console',
    ],

    platforms=['Any'],

    scripts=[],

    provides=[],
    install_requires=['cliff'],

    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'loggy = src.main:main',
        ],
        'parashift.loggy': [
            'setup = src.setup:Setup',
            'environments = src.environments.list_cmd:EnvironmentsList',
            'environments_add = src.environments.add_cmd:EnvironmentsAdd',
            'environments_list = src.environments.list_cmd:EnvironmentsList',
            'environments_delete = src.environments.delete_cmd:EnvironmentsDelete',
            'audit = src.audit_cmd:Audit',
            'blacklist = src.blacklist.list_cmd:BlacklistLogGroupList',
            'blacklist_list = src.blacklist.list_cmd:BlacklistLogGroupList',
            'blacklist_clear = src.blacklist.clear_cmd:BlacklistLogGroupClear',
        ],
    },

    zip_safe=False,
)
