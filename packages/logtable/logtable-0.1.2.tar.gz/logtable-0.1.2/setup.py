from __future__ import print_function

import distutils.spawn
import re
import shlex
import subprocess
import sys

from setuptools import find_packages
from setuptools import setup


def get_version():
    filename = "logtable/__init__.py"
    with open(filename) as f:
        match = re.search(
            r"""^__version__ = ['"]([^'"]*)['"]""", f.read(), re.M
        )
    if not match:
        raise RuntimeError("{} doesn't contain __version__".format(filename))
    version = match.groups()[0]
    return version


def get_long_description():
    with open("README.md") as f:
        long_description = f.read()
    try:
        import github2pypi

        return github2pypi.replace_url(
            slug="wkentaro/logtable", content=long_description
        )
    except Exception:
        return long_description


def main():
    version = get_version()

    if sys.argv[1] == "release":
        if not distutils.spawn.find_executable("twine"):
            print(
                "Please install twine:\n\n\tpip install twine\n",
                file=sys.stderr,
            )
            sys.exit(1)

        commands = [
            "git submodule update --init github2pypi",
            "git tag v{:s}".format(version),
            "git push origin master --tag",
            "python setup.py sdist",
            "twine upload dist/logtable-{:s}.tar.gz".format(version),
        ]
        for cmd in commands:
            subprocess.check_call(shlex.split(cmd))
        sys.exit(0)

    setup(
        name="logtable",
        version=version,
        packages=find_packages(),
        install_requires=["pandas", "pyyaml", "tabulate"],
        author="Kentaro Wada",
        author_email="www.kentaro.wada@gmail.com",
        description="Monitor and Compare Logs on Terminal.",
        long_description=get_long_description(),
        long_description_content_type="text/markdown",
        url="http://github.com/wkentaro/logtable",
        license="MIT",
        classifiers=[
            "Development Status :: 4 - Beta",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3 :: Only",
            "Topic :: Scientific/Engineering :: Information Analysis",
            "Topic :: Scientific/Engineering :: Visualization",
        ],
        entry_points={"console_scripts": ["logtable=logtable.cli:main"]},
    )


if __name__ == "__main__":
    main()
