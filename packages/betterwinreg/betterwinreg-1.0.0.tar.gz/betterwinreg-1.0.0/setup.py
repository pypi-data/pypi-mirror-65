from pathlib import Path
from setuptools import setup, find_packages

HERE = Path(__file__).parent
README = (HERE / 'README.md').open().read()
VERSION = '1.0.0'

setup(
    name='betterwinreg',
    version=VERSION,
    packages=find_packages(exclude=('tests/',)),

    python_requires='>=3.7',

    description='A sane way of working with the Windows registry',
    long_description=README,
    long_description_content_type='text/markdown',
    keywords='winreg windows registry oop',

    url='https://github.com/thefumbduck/betterwinreg',
    project_urls={
        'Bug tracker': 'https://github.com/thefumbduck/betterwinreg/issues',
        'Documentation': 'https://github.com/thefumbduck/betterwinreg',
        'Source code': 'https://github.com/thefumbduck/betterwinreg',
    },

    author='thefumbduck',
    author_email='51268203+thefumbduck@users.noreply.github.com',
    license='GNU GPL v3',
)
