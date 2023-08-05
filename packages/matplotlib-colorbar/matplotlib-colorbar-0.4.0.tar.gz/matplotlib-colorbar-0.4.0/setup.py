#!/usr/bin/env python

# Standard library modules.
import os

# Third party modules.
from setuptools import setup, find_packages

# Local modules.
import versioneer

# Globals and constants variables.
BASEDIR = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the relevant file
with open(os.path.join(BASEDIR, "README.rst"), "r") as f:
    long_description = f.read()

setup(
    name="matplotlib-colorbar",
    version=versioneer.get_version(),
    description="Artist for matplotlib to display a color bar",
    long_description=long_description,
    author="Philippe Pinard",
    author_email="philippe.pinard@gmail.com",
    maintainer="Philippe Pinard",
    maintainer_email="philippe.pinard@gmail.com",
    url="https://github.com/ppinard/matplotlib-colorbar",
    license="BSD",
    keywords="matplotlib color bar image",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    packages=find_packages(),
    package_data={},
    install_requires=["matplotlib"],
    zip_safe=True,
    cmdclass=versioneer.get_cmdclass(),
)
