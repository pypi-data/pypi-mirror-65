from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

name = "simpleiniparser"
version = "0.2.0"
description = "Simple tooling to seamlessly parse ini file"
long_description = """
It may feel boring to rewrite a parser fore every project you start.

Filling your ini file with pythonic values will make you save time.
"""
try:
    with open(path.join(here, "README.md"), encoding="utf-8") as f:
        long_description = "%s\n%s" % (long_description, f.read())
except TypeError:  # Python2
    with open(path.join(here, "README.md")) as f:
        long_description = "%s\n%s" % (long_description, f.read())


long_description_content_type = "text/markdown"
url = "https://github.com/cgte/simpleiniparser"
packages = [
    "simpleiniparser",
]
package_data = {}
install_requires = []
test_requires = []
extras_require = {"dev": ["pytest", "pytest-cov", "tox", "wheel"]}
author = "Colin Goutte"
author_email = "colin.goutte@free.fr"
# package_dir = {"": "simpleiniparser"}
license = "Apache 2"
classifiers = [
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Intended Audience :: Developers",
    "Natural Language :: English",
]
keywords = "ini utilities"
setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    long_description_content_type=long_description_content_type,
    url=url,
    packages=packages,
    package_data=package_data,
    install_requires=install_requires,
    extras_require=extras_require,
    author=author,
    author_email=author_email,
    license=license,
    classifiers=classifiers,
    keywords=keywords,
    # package_dir=package_dir,
)
