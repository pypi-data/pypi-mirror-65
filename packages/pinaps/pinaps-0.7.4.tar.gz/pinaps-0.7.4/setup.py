from distutils.core import setup

from setuptools import setup, find_packages

setup(
    name="pinaps",
    version="0.7.4",
    packages=find_packages(),
    install_requires=[
          'driverSC16IS750',
          'NeuroParser',
    ],
    license='MIT',
    author="harri.renney.blino",
    author_email="harri.renney@blino.co.uk",
    description="[BETA]Supporting python package for use with the Blino PiNaps Raspberry pi hat.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/blino-dev/pinaps/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
