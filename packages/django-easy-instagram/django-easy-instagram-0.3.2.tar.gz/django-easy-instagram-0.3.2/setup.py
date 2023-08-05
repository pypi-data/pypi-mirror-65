"""
Created on 24/gen/2014

@author: Marco Pompili
"""

import os
from setuptools import setup, find_packages

setup(
    name='django-easy-instagram',
    version='0.3.2',
    description='Instagram client for Django.',
    long_description_content_type='text/markdown',
    long_description=open('README.md', encoding='utf-8').read(),
    author='Tom Anthony, Marco Pompili',
    author_email='django@tomanthony.co.uk',
    license='BSD-3 License',
    url='https://github.com/TomAnthony/django-easy-instagram/',
    packages=find_packages(),
    platforms='any',
    include_package_data=True,
    install_requires=[
        'django>=1.6',
        'html5lib',
        'requests',
        'sorl-thumbnail',
        'Pillow',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Framework :: Django',
        'Framework :: Django :: 1.6',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.2',
    ],
)
