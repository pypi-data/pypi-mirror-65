#!/usr/bin/env python

import os
import subprocess

from setuptools import setup, find_packages


def run_setup():
    requirements = []

    python_requirement = ">=3.5"

    extras_requirements = {
        "cli": [],
        "flask": [
            "Flask>=1.1.1",
        ],
        "grpc": [
            "grpcio>=1.17.1",
            "googleapis-common-protos>=1.5.5",
        ],
        "gunicorn": [
            "gunicorn>=20.0.4",
        ],
        "logging": [],
        "sqlalchemy": [
            "SQLAlchemy>=1.3.15",
        ]
    }

    with open('README.md', 'r') as f:
        long_description = f.read()

    setup(
        name='tool-belt',
        version=git_version(),

        license='MIT License',

        author='Mahdi Mohaveri',
        author_email='mmohaveri@gmail.com',

        package_dir={'': 'src'},
        packages=find_packages('src'),
        package_data={
            'toolbelt': ['py.typed'],
        },
        include_package_data=True,

        description='A set of utility modules that helps you create web services faster.',
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/mmohaveri/python-tool-belt",

        python_requires=python_requirement,
        install_requires=requirements,
        extras_require=extras_requirements,

        zip_safe=True,
        keywords=[
            "web-service",
            "toolkit",
            "toolbelt",
            "logging",
            "grpc",
            "flask",
            "gunicorn",
            "cli",
        ],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Operating System :: Unix',
            'Operating System :: POSIX',
            'Operating System :: Microsoft :: Windows',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3 :: Only',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: Implementation :: PyPy',
            'Topic :: Software Development',
            'Topic :: Utilities',
            'Typing :: Typed'
        ],
    )


def git_version():
    git_commit_cmd = ['git', 'rev-parse', '--short', 'HEAD']
    git_version_cmd = ['git', 'describe', '--abbrev=1', '--tags']

    return _run_cmd(git_version_cmd) or _run_cmd(git_commit_cmd) or "Unknown"


def _run_cmd(cmd):
    cwd = os.path.abspath(os.path.dirname(__file__))

    env = {key: os.environ.get(key) for key in [
        'SYSTEMROOT', 'PATH', 'HOME'] if os.environ.get(key) is not None}
    env['LANGUAGE'] = 'C'
    env['LANG'] = 'C'
    env['LC_ALL'] = 'C'

    child = subprocess.Popen(cmd, stdout=subprocess.PIPE, env=env, cwd=cwd)
    output, err = child.communicate()

    if err is not None or child.returncode != 0:
        return None

    return output.strip().decode('ascii')


if __name__ == "__main__":
    run_setup()
