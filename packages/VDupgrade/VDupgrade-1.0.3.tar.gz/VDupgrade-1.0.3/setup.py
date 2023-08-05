import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

setup(
    author='Joyphy',
    name='VDupgrade',
    version='1.0.3',
    description='None',
    long_description=README,
    long_description_content_type='text/markdown',
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
    ],
    packages=['VDupgrade'],
    zip_safe=False,
)