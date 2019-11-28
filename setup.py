# Author: Alejandro M. BERNARDIS
# Email: alejandro.bernardis@gmail.com
# Created: 2019/11/22 14:13
# ~

from os import path
from io import open
from setuptools import setup, find_packages
from aysa.common import __version__ as common

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'readme.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name=common.__title__,
    version=common.__version__,
    description=common.__summary__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=common.__uri__,
    author=common.__author__,
    author_email=common.__email__,
    keywords='docker common services development deployment utils',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires='>=3.6.*, <4',

    package_data={
        '': ['LICENSE', 'README.md']
    },

    install_requires=[
        'requests==2.22.0',
        'docopt==0.6.2',
        'dotted==0.1.8',
    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],

    project_urls={
        'Bug Reports': common.__issues__,
        'Source': common.__uri__,
    },

)
