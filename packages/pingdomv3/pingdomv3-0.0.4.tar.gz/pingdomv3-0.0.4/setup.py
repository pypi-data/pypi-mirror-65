from __future__ import print_function
import os
from os.path import dirname, abspath, join
import pingdomv3
import codecs
from setuptools import setup


HERE = dirname(abspath(__file__))

author = "Cheney Yan"
author_email = "cheney.yant@gmail.com"
keywords = ["pingdom", "v3", "API", "python3"]


def read(*parts):
    with codecs.open(join(HERE, *parts), "rb", "utf-8") as f:
        return f.read()

setup(
    name="pingdomv3",
    version=pingdomv3.__version__,
    description="Pingdom V3 API for python3",
    long_description=read("README.md"),
    long_description_content_type='text/markdown',
    python_requires='>=3',
    author=author,
    author_email=author_email,
    maintainer=author,
    maintainer_email=author_email,
    keywords=keywords,
    url="https://github.com/cheney-yan/pingdom-py-api-v3",
    license="MIT",
    py_modules=["pingdomv3"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
