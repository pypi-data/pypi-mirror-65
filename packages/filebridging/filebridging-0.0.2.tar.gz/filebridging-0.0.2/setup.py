"""Setup."""

import codecs
import os
import re
import setuptools
import sys

if sys.version_info < (3, 8):
    raise RuntimeError("Python3.8+ is needed to use this library")

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """Read file in `part.part.part.part.ext`.

    Start from `here` and follow the path given by `*parts`
    """
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_information(info, *file_path_parts):
    """Read information in file."""
    version_file = read(*file_path_parts)
    version_match = re.search(
        r"^__{info}__ = ['\"]([^'\"]*)['\"]".format(
            info=info
        ),
        version_file,
        re.M
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setuptools.setup(
    name='filebridging',
    version=find_information("version", "filebridging", "__init__.py"),
    author=find_information("author", "filebridging", "__init__.py"),
    author_email=find_information("email", "filebridging", "__init__.py"),
    description=(
        "Share files via a bridge server using TCP over SSL and end-to-end "
        "encryption."
    ),
    license=find_information("license", "filebridging", "__init__.py"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gogs.davte.it/davte/filebridging",
    packages=setuptools.find_packages(),
    platforms=['any'],
    install_requires=[],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Framework :: AsyncIO",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Communications :: File Sharing",
    ],
    keywords=(
        'file share '
        'tcp ssl tls end-to-end encryption '
        'python asyncio async'
    ),
    include_package_data=True,
)
