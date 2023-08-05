from setuptools import setup, find_packages
from qoaladep import version

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='qoaladep',
    version=version,
    description='qoala.id data science team library for deployment model',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='qoala deployment team',
    packages=["qoaladep", "qoaladep.gcp", "qoaladep.aws", "qoaladep.utils", "qoaladep.aws.textract", "qoaladep.gcp.bigquery", "qoaladep.gcp.datastore", "qoaladep.gcp.", "qoaladep.gcp.ml_engine", "qoaladep.gcp.ocr", "qoaladep.gcp.pubsub", "qoaladep.gcp.storage"],
)
