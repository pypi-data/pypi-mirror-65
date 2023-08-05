import pathlib

from setuptools import setup

setup(
    name='fxq-gcp-commons',
    version='1.3.3',
    packages=[
        'fxq.gcp'
    ],
    url='https://bitbucket.org/fxqlabs/fxq-gcp-commons/',
    license='MIT',
    author='Jonathan Turnock',
    author_email='jonathan.turnock@outlook.com',
    description='',
    long_description=(pathlib.Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    install_requires=['grpcio', 'Flask', 'google-cloud-datastore', 'google-cloud-pubsub']
)
