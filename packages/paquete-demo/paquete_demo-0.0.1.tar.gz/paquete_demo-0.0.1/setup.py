import os.path
from setuptools import setup, find_packages

# The directory containing this file
HERE = os.path.abspath(os.path.dirname(__file__))

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fid:
    README = fid.read()

setup(
    name='paquete_demo',
    version='0.0.1',
    description='Paquete demo.',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://bitbucket.org/ageabigdata/paquete_demo',
    author='Usuario demo',
    author_email="bigdata@agea.com.ar",
    license="MIT",
    install_requires=[
        'pandas'
    ],
    packages=find_packages(),
)

