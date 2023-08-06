from setuptools import setup, find_packages

from chatwatch.settings import version_string

setup(
    name="chatwatch.py",
    version=version_string,
    packages=["chatwatch"],
    url="https://github.com/TAG-Epic/chatwatch.py",
    license="GNU GPLv3",
    author="Epic",
    author_email="admin@itzepic.net",
    description="ChatWatch library",
)
