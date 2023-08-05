"""Packaging settings."""


from codecs import open
from os.path import abspath, dirname, join
from subprocess import call

from setuptools import Command, find_packages, setup

from jira_cli import __version__


this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.rst'), encoding='utf-8') as file:
    long_description = file.read()


class RunTests(Command):
    """Run all tests."""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        errno = call(['py.test', '--cov=skele', '--cov-report=term-missing'])
        raise SystemExit(errno)


setup(
    name = 'jira-simple-cli',
    version = __version__,
    description = 'A Command Line Interface for Jira',
    long_description = long_description,
    url = 'https://gitlab.com/mundo03/jira-cli',
    author = 'Edmundo Sanchez',
    author_email = 'zomundo@gmail.com',
    license = 'GNU v3.0',
    classifiers = [
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: Public Domain',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
    ],
    keywords = 'cli',
    packages = find_packages(exclude=['docs', 'tests*']),
    install_requires = ['jira'],
    setup_requires=['wheel','twine'],
    extras_require = {
        'test': ['pytest'],
    },
    entry_points = {
        'console_scripts': [
            'jira=jira_cli.cli:main',
        ],
    },
    cmdclass = {'test': RunTests},
)
