#!/usr/bin/env python

from distutils.core import setup

from setuptools import find_packages

setup(
    name='odoo_backup_cli',
    version='1.0.2',
    description='Odoo backup tool',
    author='Omar Diaz',
    author_email='zcool2005@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
      'Click',
      'requests',
      'minio',
    ],
    zip_safe=False,
    entry_points='''
        [console_scripts]
        odoo_backup=odoo_backup:tool
    ''',
)
