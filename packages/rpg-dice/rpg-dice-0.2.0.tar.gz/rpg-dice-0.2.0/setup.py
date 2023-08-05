import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rpg-dice",
    version="0.2.0",
    author="Paweł Fertyk",
    author_email="pfertyk@pfertyk.me",
    description="A simple dice roller",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pfertyk/rpg-dice",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Operating System :: OS Independent",
    ],
)
