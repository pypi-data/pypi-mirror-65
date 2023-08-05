#!/usr/bin/env python3

import re
from setuptools import setup


with open('./tinder_cli/__init__.py', 'r') as f:
    version = re.search(r'(?<=__version__ = .)([\d\.]*)', f.read()).group(1)

with open('./README.md', 'r') as f:
    readme = f.read()


if __name__ == '__main__':
    setup(
        name='tinder-cli',
        version=version,
        author='Zsolt Mester',
        author_email='',
        description='Tinder for terminal junkies',
        long_description=readme,
        license='MIT',
        url='https://github.com/meister245/tinder-cli',
        project_urls={
            "Code": "https://github.com/meister245/tinder-cli",
            "Issue tracker": "https://github.com/meister245/tinder-cli/issues",
        },
        packages=[
            'tinder_cli'
        ],
        install_requires=[
            'requests',
            'pyyaml'
        ],
        python_requires='>=3.6',
        include_package_data=True,
        scripts=[
            'scripts/tinder-cli',
            'scripts/tinder-cli.py'
        ]
    )