#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

REQUIREMENTS = ['Click>=7.0', ]

SETUP_REQUIREMENTS = []

TEST_REQUIREMENTS = []

setup(
    author="Bram Daams",
    author_email='b.daams@science.ru.nl',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A dynamic Ansible inventory based on running linuxcontainers",
    entry_points={
        'console_scripts': [
            'lxcible=lxcible.cli:main',
        ],
    },
    install_requires=REQUIREMENTS,
    license="GNU General Public License v3",
    long_description=README + '\n\n' + HISTORY,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords='lxcible',
    name='lxcible',
    packages=find_packages(include=['lxcible', 'lxcible.*']),
    setup_requires=SETUP_REQUIREMENTS,
    test_suite='tests',
    tests_require=TEST_REQUIREMENTS,
    url='https://gitlab.science.ru.nl/bram/lxcible',
    version='0.1.0',
    zip_safe=False,
)
