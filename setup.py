"""
Install mix-tools
"""

import os
from setuptools import setup, find_packages


def main():
    """Install mix-tools"""
    setup(
        name='mix_tools',
        packages=find_packages(exclude=['tests', 'tests.*']),
        version='0.1')


if __name__ == '__main__':
    main()
