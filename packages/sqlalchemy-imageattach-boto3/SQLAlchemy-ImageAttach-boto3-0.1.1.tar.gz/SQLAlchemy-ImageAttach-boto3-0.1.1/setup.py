# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['sqlalchemy_imageattach_boto3']
install_requires = \
['SQLAlchemy-ImageAttach>=1.1.0,<1.2.0', 'boto3>=1.11,<2.0']

setup_kwargs = {
    'name': 'sqlalchemy-imageattach-boto3',
    'version': '0.1.1',
    'description': 'SQLAlchemy-ImageAttach AWS S3 Store with boto3',
    'long_description': '# SQLAlchemy-ImageAttach-boto3\n\n[![PyPI version badge](https://badgen.net/pypi/v/sqlalchemy-imageattach-boto3)](https://pypi.org/project/sqlalchemy-imageattach-boto3/)\n[![PyPI license badge](https://badgen.net/pypi/license/sqlalchemy-imageattach-boto3)](LICENSE)\n\nSQLAlchemy-ImageAttach AWS S3 Store with boto3\n\nSince the `S3Store` of [SQLAlchemy-ImageAttach](https://github.com/dahlia/sqlalchemy-imageattach)\nuses HTTP API and AWS Signature Version 4 to get/put images to S3, AWS access\nkey and secret key is required. But if an application does not have access key\n(i.e. given access by AWS IAM Role), the application cannot use `S3Store`. So\nSQLAlchemy-ImageAttach-boto3 offers `Boto3S3Store`, reimplemented `S3Store` with\n[boto3](https://github.com/boto/boto3), so that the application can use various\ncredential sources that boto3 offers.\n\n\n## Installation\n\nAvailable on [PyPI](https://pypi.org/project/sqlalchemy-imageattach-boto3/):\n\n```sh\n$ pip install SQLAlchemy-ImageAttach-boto3\n```\n',
    'author': 'Spoqa Creators',
    'author_email': 'dev@spoqa.com',
    'maintainer': 'rusty',
    'maintainer_email': 'rusty@spoqa.com',
    'url': 'https://github.com/spoqa/sqlalchemy-imageattach-boto3',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
}


setup(**setup_kwargs)
