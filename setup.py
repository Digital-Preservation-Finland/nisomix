"""
Install nisomix
"""

from setuptools import setup, find_packages


def main():
    """Install nisomix"""
    setup(
        name='nisomix',
        packages=find_packages(exclude=['tests', 'tests.*']),
        version='0.1',
        install_requires=['lxml', 'xml-helpers'],
        dependency_links=[
            'git+https://gitlab.csc.fi/dpres/xml-helpers.git'
            '@develop#egg=xml-helpers-0.0'
        ]
    )


if __name__ == '__main__':
    main()
