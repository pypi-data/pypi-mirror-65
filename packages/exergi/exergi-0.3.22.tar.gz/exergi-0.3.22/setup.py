import pathlib
from setuptools import find_packages,setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="exergi",
    version="0.3.22",
    description="SE Libary for various tasks",
    long_description=README,
    long_description_content_type="text/markdown",
    author="KasperJanehag",
    author_email="kasper.janehag@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=["pandas","boto3"],
)