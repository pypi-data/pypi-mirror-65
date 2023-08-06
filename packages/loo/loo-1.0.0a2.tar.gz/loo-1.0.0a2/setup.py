from setuptools import find_packages, setup
from loo import __version__

with open("README.md", 'r') as file:
    long_description = file.read()

setup(
   name='loo',
   version=__version__,
   description='LooMan Cli',
   long_description=long_description,
   license="MIT",
   author='Fredrik Larsson',
   author_email='larsson.fredrik31@gmail.com',
   url='https://github.com/LooMan/looman-cli',
   packages = find_packages(exclude=['docs', 'tests*']),
   install_requires=['click'], #external packages as dependencies
   entry_points = {
        'console_scripts': [
            'loo=loo.cli:main',
        ],
    },
)