# setup.py

import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README =(HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name = "praneet-reader",
    version = "1.1.0",
    description = "Real the latest Real Python tutorials",
    long_description = README,
    long_description_content_type = "text/markdown",
    url = "https://github.com/Praneet460",
    author = "Praneet Nigam",
    author_email = "nigampraneet460@gmail.com",
    license = "MIT",
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7"
    ],
    packages=["reader"],
    include_package_data = True,
    install_requires=["feedparser", "html2text"],
    entry_points = {
        "console_scripts": [
            "realpython = reader.__main__:main"
        ]
    }
)
