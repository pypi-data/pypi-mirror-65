from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='pywarface',
    version='1.0',
    description='A Python library for interacting with the my.com Warface API',
    license="GPLv3",
    long_description=long_description,
    author='Evan Pratten',
    author_email='ewpratten@retrylife.ca',
    url="https://retrylife.ca/",
    packages=['pywarface'],
    install_requires=['requests']
)