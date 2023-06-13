import os
from setuptools import setup, find_packages
import filesify


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ""


setup(
    name="filesify",
    version=filesify.__version__,
    description=read("DESCRIPTION"),
    long_description=read("README.rst"),
    keywords="filesify django files container upload configuration volatile storage",
    packages=find_packages(),
    author="",
    author_email="",
    url="https://github.com/lazybird/django-filesify/",
    include_package_data=True,
    test_suite="filesify.tests.runtests.runtests",
)
