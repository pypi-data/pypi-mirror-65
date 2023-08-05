import setuptools

with open("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "vnumdata",
    version = "0.0.1",
    author = "Vignesh K",
    author_email = "abc@xyz.com",
    description = "A simple package for calculating a single number and create in my Udemy course",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "",
    keywords = 'package numbers calculations',
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
        ]
    )
