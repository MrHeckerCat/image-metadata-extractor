# setup.py
from setuptools import find_packages, setup

requires = [
    "google-cloud-storage",
    "exiftool",
]

setup(
    name="image-metadata-extractor",
    version="0.1.0",
    packages=find_packages(),
    install_requires=requires,
)
