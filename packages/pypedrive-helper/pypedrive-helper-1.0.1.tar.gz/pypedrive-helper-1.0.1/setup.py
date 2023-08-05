import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="pypedrive-helper",
    version="1.0.1",
    description="The Python Pipedrive API Helper",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/kristan-dev/pipedrive_helper",
    author="Kristan Eres",
    author_email="spectre.aloha@outlook.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["requests"],
    python_requires='>=3.6',
)