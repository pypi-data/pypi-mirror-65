from setuptools import setup, find_packages
from os.path import join, dirname
import random_protasevich_api

setup(
    name='api_random_protasevich',
    version=random_protasevich_api.__version__,
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
)
