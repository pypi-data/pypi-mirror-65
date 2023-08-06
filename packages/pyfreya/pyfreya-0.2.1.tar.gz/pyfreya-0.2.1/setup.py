#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()
    example_start = readme.find('PyFreya Example')  # remove example part from README
    readme = readme[:example_start]

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = []

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Morten Andreasen",
    author_email='yggdrasil.the.binder@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Cohort Analysis Tool",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pyfreya',
    name='pyfreya',
    packages=find_packages(include=['pyfreya', 'pyfreya.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://gitlab.com/Yggdrasil27/pyfreya',
    version='0.2.1',
    zip_safe=False,
    PROJECT_URLS={
        "Bug Tracker": "https://gitlab.com/Yggdrasil27/pyfreya/-/issues",
        "Documentation": "https://pyfreya.readthedocs.io/en/latest/",
    },
)
