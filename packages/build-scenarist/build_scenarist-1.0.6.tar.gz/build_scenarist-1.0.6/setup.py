# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import io
import os
import re

def read(*names, **kwargs):
      with io.open(os.path.join(os.path.dirname(__file__), *names), encoding=kwargs.get("encoding", "utf8")) as fp:
            return fp.read()

def find_version(*file_paths):
      version_file = read(*file_paths)
      version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
      if version_match:
            return version_match.group(1)
      raise RuntimeError("Unable to find version string.")

setup(name="build_scenarist",
      keywords=["CI", "ci", "crossplatform", "build", "tool", "dev", "shell"],
      version=find_version("build_scenarist", "__init__.py"),
      description="Make-like utility to execute platform-dependent scripts (scenarios) written in Python 2.7. Format of scenario-name consist information about platform it written. Scenarios consist of targets",
      url="http://github.com/sogimu/scenarist",
      author="Aleksandr Lizin",
      author_email="sogimu@nxt.ru",
      packages=find_packages(),
      scripts=["scenarist.py"],
      package_data={"build_scenarist": ["src/*"]},
      zip_safe=True,
      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: Freely Distributable",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development",
        "Topic :: Software Development :: Build Tools",
        "Topic :: System",
        "Topic :: System :: Operating System",
        "Topic :: System :: Shells",
        "Operating System :: OS Independent",
      ],
      )
