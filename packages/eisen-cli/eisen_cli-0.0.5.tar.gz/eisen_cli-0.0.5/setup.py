from setuptools import setup, find_packages


VERSION = '0.0.5'

with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

setup(
    name='eisen_cli',
    version=VERSION,
    description='Eisen Command Line Interface (CLI)',
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'eisen = eisen_cli.main:cli'
        ],
    },
)