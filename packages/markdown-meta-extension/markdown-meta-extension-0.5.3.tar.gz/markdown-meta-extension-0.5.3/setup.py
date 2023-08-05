"""Setup for installing the package.

This module also provides configuration options and meta data for the package.

Author:
    Martin Schorfmann
Since:
    2019-12-11
Version:
    2020-03-10
"""

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# Package meta data
NAME = "markdown-meta-extension"
DESCRIPTION = (
    "Markdown Meta Extension for using "
    "Python functions and classes from within documents."
)
URL = "https://gitlab.com/markdown-meta-extension/markdown-meta-extension"
EMAIL = "schorfma@uni-bremen.de"
AUTHOR = "Martin Schorfmann"
REQUIRES_PYTHON = ">=3.7.0"
VERSION = "0.5.3"

LICENSE = "MIT"
LICENSE_FILE = "./LICENSE.md"

# Requires packages for execution
REQUIRED = [
    "Click",
    "jinja2",
    "Markdown",
    "MarkupSafe",
    "pathvalidate",
    "PyYAML"
]

TESTS_REQUIRED = [
    "beautifulsoup4",
    "lxml",
    "Markdown",
    "parse"
]

# Optional packages
EXTRAS = {
    "pelican": [
        "pelican"
    ]
}

ENTRY_POINTS = {
    "markdown.extensions": [
        "markdown_meta_extension = markdown_meta_extension.__init__"
    ],
    "console_scripts": [
        "markdown-meta-extension = markdown_meta_extension:markdown_meta_extension_parser",
        "markdown-meta-extension-glob = markdown_meta_extension:markdown_meta_extension_glob_parser"
    ]
}

# https://github.com/navdeep-G/setup.py
here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if "README.md" is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, "README.md"), encoding="utf-8") as file:
        long_description = "\n" + file.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package"s __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, "__version__.py")) as file:
        exec(file.read(), about)
else:
    about["__version__"] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system("{0} setup.py sdist bdist_wheel --universal".format(sys.executable))

        self.status("Uploading the package to PyPI via Twine…")
        os.system("twine upload dist/*")

        self.status("Pushing git tags…")
        os.system("git tag v{0}".format(about["__version__"]))
        os.system("git push --tags")

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(
        exclude=[
            "tests",
            "*.tests",
            "*.tests.*",
            "tests.*"
        ]
    ),
    # If your package is a single module, use this instead of "packages":
    # py_modules=["mypackage"],

    entry_points=ENTRY_POINTS,
    install_requires=REQUIRED,
    tests_require=TESTS_REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license=LICENSE,
    license_file=LICENSE_FILE,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Text Processing :: Markup",
        "License :: OSI Approved :: MIT License"
    ],
    # $ setup.py publish support.
    cmdclass={
        "upload": UploadCommand,
    },
)
