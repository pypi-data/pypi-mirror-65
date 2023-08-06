# pylint: disable=missing-docstring
import sys
import os
from os import path

from setuptools import setup
from setuptools import find_packages
from setuptools.command.test import test as TestCommand


def get_readme_contents():
    # Setup with the description in the README file
    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
        long_description = f.read()
        return long_description

    return None


class PyTest(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ["--boxed"]

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        if isinstance(self.pytest_args, str):
            self.pytest_args = self.pytest_args.split(" ")
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


here = os.path.abspath(os.path.dirname(__file__))
os.chdir(here)


tests_require = [
    "astroid",
    "wrapt < 1.12.0",
    "pytest >= 4.0.0",
    "pytest-runner",
    "pytest-pylint",
    "pytest-xdist",
    "pytest-cov",
    "pytest-mock",
    "requests-mock",
    "pylint",
    "requests_toolbelt",
    "Sphinx",
    "keras",
    "tensorflow >= 2.1.0",
    "coremltools",
    "numpy",
]


setup(
    name="fritz",
    version="2.2.3",
    description="Fritz Machine Learning Library.",
    long_description=get_readme_contents(),
    long_description_content_type="text/markdown",
    url="https://github.com/fritzlabs/fritz-python",
    project_urls={
        "Documentation": "https://docs.fritz.ai/cli/index.html",
        "Source Code": "https://github.com/fritzlabs/fritz-python",
        "Bug Tracker": "https://github.com/fritzlabs/fritz-python/issues",
    },
    keywords="machine learning, training, app development",
    author="Fritz Engineering",
    author_email="engineering@fritz.ai",
    license="MIT",
    zip_safe=False,
    packages=find_packages(),
    install_requires=[
        "requests",
        "click",
        "click-plugins",
        "termcolor",
        "pbxproj",
    ],
    extras_require={"train": ["keras", "tensorflow"]},
    tests_require=tests_require,
    cmdclass={"test": PyTest},
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points={"console_scripts": ["fritz = cli:main"]},
)
