#!/usr/bin/env python

# To generate DEB package from Python Package:
# sudo pip3 install stdeb
# python3 setup.py --verbose --command-packages=stdeb.command bdist_deb
#
#
# To generate RPM package from Python Package:
# sudo apt-get install rpm
# python3 setup.py bdist_rpm --verbose --fix-python --binary-only
#
#
# To generate EXE MS Windows from Python Package (from MS Windows only):
# python3 setup.py bdist_wininst --verbose
#
#
# To generate PKGBUILD ArchLinux from Python Package (from PyPI only):
# sudo pip3 install git+https://github.com/bluepeppers/pip2arch.git
# pip2arch.py PackageNameHere
#
#
# To Upload to PyPI by executing:
# python3 setup.py register
# python3 setup.py bdist_egg sdist --formats=zip upload --sign


import os
import pprint
from pathlib import Path
from shutil import copytree, which
from setuptools import setup, find_packages, Command
from tempfile import TemporaryDirectory
from zipapp import create_archive

import logging

logger = logging.getLogger(__name__)

setup_requirements = ["pytest-runner", "setuptools_scm"]

from web_minify import version_filename, __version__ as web_minify_version


def read_file(fname, strip=True):
    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    data = ""
    if os.path.exists(fn):
        with open(fn) as f:
            data = f.read()
            data = data.strip() if strip else data
            # logger.info(f"Got data '{data}' from '{fn}'")
    else:
        logger.error(f"Could not find file {fn}")
        logger.warning(f"NOTE: Current working directory is {os.getcwd()}")
    return data


def remove_comment(line, sep="#"):
    i = line.find(sep)
    if i >= 0:
        line = line[:i]
    return line.strip()


def read_requirements_file(fname: str):
    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    print(f"Reading requirements from {fn}")
    lines = []
    if os.path.exists(fn):
        with open(fn) as f:
            for r in f.readlines():
                r = r.strip()
                if len(r) < 1:
                    continue
                r = remove_comment(r)
                if len(r) < 1:
                    continue
                lines.append(r)
    else:
        logger.error(f"Could not find requirements file {fn}")
        logger.warning(f"NOTE: Current working directory is {os.getcwd()}")
    return lines


##############################################################################
# Dont touch below


class ZipApp(Command):
    description, user_options = "Creates a ZipApp.", []

    def initialize_options(self):
        pass  # Dont needed, but required.

    def finalize_options(self):
        pass  # Dont needed, but required.

    def run(self):
        with TemporaryDirectory() as tmpdir:
            copytree(".", Path(tmpdir) / "web-minify")
            (Path(tmpdir) / "__main__.py").write_text("import runpy\nrunpy.run_module('web-minify')")
            create_archive(tmpdir, "web-minify.pyz", which("python3"))


##############################################################################

package = {
    "name": "web-minify",
    "version": web_minify_version,
    "author": "Lennart Rolland",
    "author_email": "lennart@firtkissdesigns.com",
    "maintainer": "Lennart Rolland",
    "maintainer_email": "lennart@firtkissdesigns.com",
    "description": ("CSS HTML JS SVG PNG JPEG Minifier"),
    "license": "GPL-3 LGPL-3 MIT",
    "platforms": ["Linux"],
    "keywords": "python3, CSS, HTML, JS, SVG, PNG, JPEG, Compressor, CSS3, HTML5, Web, Javascript, Minifier, Minify, Uglify, Obfuscator",
    "url": "https://gitlab.com/firstkiss/web-minifier",
    "download_url": "https://gitlab.com/firstkiss/web-minify",
    "project_urls": {"Docs": "https://gitlab.com/firstkiss/web-minify/README.md", "Bugs": "https://gitlab.com/firstkiss/web-minify/-/issues", "C.I.": "https://gitlab.com/firstkiss/web-minify/pipelines"},
    "packages": find_packages(),
    "zip_safe": True,
    "long_description": read_file("README.md"),
    "long_description_content_type": "text/markdown",
    "setup_requires": setup_requirements,
    "zip_safe": True,
    "install_requires": read_requirements_file("requirements/requirements.in"),  # Allow flexible deps for install
    "tests_require": read_requirements_file("requirements/test_requirements.txt"),  # Use rigid deps for testing
    "test_suite": "../tests",
    "python_requires": ">=3.7.4",
    "data_files": [("web-minify", [version_filename])],
    "include_package_data": True,
    # scripts=['css-html-js-minify.py'],  # uncomment if want install as script
    "entry_points": {"console_scripts": ["css-html-js-minify = css_html_js_minify.minify:main"]},
    "cmdclass": {"zipapp": ZipApp},
    # From https://pypi.org/pypi?%3Aaction=list_classifiers
    "classifiers": ["Development Status :: 3 - Alpha", "Intended Audience :: Developers", "Intended Audience :: Other Audience", "Topic :: Utilities", "Natural Language :: English", "Operating System :: POSIX :: Linux", "Programming Language :: Python :: 3.7", "Topic :: Other/Nonlisted Topic"],
}


pprint.pprint(package)
setup(**package)
