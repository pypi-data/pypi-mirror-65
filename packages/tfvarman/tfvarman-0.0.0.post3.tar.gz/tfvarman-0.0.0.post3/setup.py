"""
Setup script for tfvarman
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.
version = "0.0.0-3" #NOTE: please blame pypy for the weird version numbers...

setup(
    name='tfvarman',
    version=version,
    description="variable management cli tool for terraform cloud",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/dsikes/tfvarman',
    author='Dan Sikes',
    author_email='dansikes7@gmail.com',
    keywords='terraform, automation, tfvars, terraform variables',
    packages=[
        'tfvarman',
        'tfvarman.utils'
    ],
    install_requires=[
        'click',
        'cerberus',
        'tabulate',
        'pyaml',
        'requests'
    ],
    entry_points = {
        'console_scripts': ['tfvarman=tfvarman.cli:main'],
    },
    
    project_urls={
        'Source': 'https://github.com/dsikes/tfvarman',
    },
)