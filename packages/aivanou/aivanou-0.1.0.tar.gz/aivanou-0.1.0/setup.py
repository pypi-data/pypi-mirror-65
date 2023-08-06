#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

import os
import re
import sys

from setuptools import find_packages, setup
from setuptools.command.install import install


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')
        tag_from_version = f"v{get_version()}"

        if tag != tag_from_version:
            info = "Git tag: {0} does not match the version: {1}".format(
                tag, get_version()
            )
            sys.exit(info)


def get_version():
    # get version string from version.py
    # TODO: ideally the version.py should be generated when setup is run
    version_file = os.path.join(os.path.dirname(__file__), "version.py")
    version_regex = r"__version__ = ['\"]([^'\"]*)['\"]"
    with open(version_file, "r") as f:
        version = re.search(version_regex, f.read(), re.M).group(1)
        return version


if __name__ == "__main__":
    if sys.version_info < (3, 6):
        sys.exit("python >= 3.6 required")

    with open("README.md", encoding="utf8") as f:
        readme = f.read()

    with open("requirements.txt") as f:
        reqs = f.read()

    version = get_version()
    print("-- Building version: " + version)

    setup(
        # Metadata
        name="aivanou",
        version=version,
        author="Aivanou",
        author_email="csivanou@gmail.com",
        description="Test project",
        long_description=readme,
        long_description_content_type="text/markdown",
        url="https://github.com/tierex/algorithms",
        license="BSD-3",
        keywords=["test"],
        python_requires=">=3.6",
        install_requires=reqs.strip().split("\n"),
        include_package_data=True,
        packages=find_packages(exclude=("test", "test.*")),
        test_suite="test.suites.unittests",
        # PyPI package information.
        classifiers=[
        ],
        cmdclass={
            'verify': VerifyVersionCommand,
        }
    )
