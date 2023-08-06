import os
from typing import Optional

import setuptools


def get_version() -> Optional[str]:
    version_file_path = './version'
    if os.path.isfile('./version'):
        with open(version_file_path, 'r') as version_file:
            return version_file.read()


setuptools.setup(
    name=f'json-datetime-noamfisher',
    version=get_version(),
    description='allows you to dump / load jsons that contain date / datetime / time objects',
    author=os.environ.get('GITLAB_USER_NAME'),
    author_email=os.environ.get('GITLAB_USER_EMAIL'),
    extras_require={
        'test': ['pytest']
    },
    packages=setuptools.find_packages()
)
