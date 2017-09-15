"""
Install nisomix
"""

import os
from setuptools import setup, find_packages


def main():
    """Install nisomix"""
    setup(
        name='nisomix',
        packages=find_packages(exclude=['tests', 'tests.*']),
        version='0.1')


if __name__ == '__main__':
    main()
