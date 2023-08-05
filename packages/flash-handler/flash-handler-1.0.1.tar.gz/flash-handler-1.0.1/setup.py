import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent


with open(HERE / 'README.md', 'rb') as f:
    README = f.read().decode('utf-8')


with open(HERE / 'requirements.txt', 'rb') as f:
    REQUIRED = f.read().decode('utf-8').splitlines()


# This call to setup() does all the work
setup(
    name="flash-handler",
    version="1.0.1",
    description="A simple Excel file handler",
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    packages=["flash_handler"],
    include_package_data=True,
    install_requires=REQUIRED,
)
