# -*- coding: utf-8 -*-
import os
from io import open
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

with open(os.path.join(here, "requirements.txt"), "r", encoding="utf-8") as fobj:
    requires = fobj.readlines()
requires = [x.strip() for x in requires if x.strip()]

setup(
    name="python-abspath",
    version="0.1.0",
    description="python-abspath provides a command line tool that prints the absolute paths of all given files. File names can be piped via STDIN or given as arguments. Work for both Windows and Linux.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="zencore",
    author_email="dobetter@zencore.cn",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords=["command line utils", "python-abspath"],
    install_requires=requires,
    packages=find_packages("."),
    py_modules=["abspath"],
    zip_safe=False,
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "abspath = abspath:print_abspath",
        ]
    },
)