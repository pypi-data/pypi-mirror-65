import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="python-sonic-client",
    version="0.0.5",
    description="Python client for Sonic Search DB",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/cyprx/pysonic",
    author="cyprx",
    author_email="cyprx@outlook.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["pysonic"],
    include_package_data=False,
)
