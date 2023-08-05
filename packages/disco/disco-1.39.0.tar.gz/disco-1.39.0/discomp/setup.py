#  Copyright (c) 2019 Samsung, Inc. and its affiliates.
#
#  This source code is licensed under the RESTRICTED license found in the
#  LICENSE file in the root directory of this source tree.

import setuptools
import sys


if sys.version_info < (3, 6):
    raise RuntimeError("This package requires Python 3.6+")

setuptools.setup(
    name='discomp',
    version='0.0.1',
    author='Disco',
    author_email='contact@dis.co',
    description='Run Python jobs in parallel on the cloud using DISCO',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Iqoqo/python-sdk',
    packages=setuptools.find_packages(),
    install_requires=open('requirements.txt', 'r').read().split('\n'),
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
    ],
    package_data={
        '': ['*.txt', '*.rst', '*.gql'],
        'disco.gql.docker.commands': ['*']
    }
)
