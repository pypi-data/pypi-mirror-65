from setuptools import setup
import os

setup(
    name='team4159-hoard',
    packages=['hoard'],
    version='0.0.1',
    install_requires=[open(os.path.join(os.path.abspath(
        os.path.dirname(__file__)), 'requirements.txt')).read().split('\n')[:-1]]
)
