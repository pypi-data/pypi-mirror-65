from distutils.core import setup

from setuptools import setup, find_packages

setup(
    name="SC16IS750",
    version="0.1.8",
    packages=find_packages(),
    license='TODO',
    author="harri.renney.blino",
    author_email="harri.renney@blino.co.uk",
    description="Python driver for interfacing with the SC16IS750",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Harri-Renney/SC16IS750",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
