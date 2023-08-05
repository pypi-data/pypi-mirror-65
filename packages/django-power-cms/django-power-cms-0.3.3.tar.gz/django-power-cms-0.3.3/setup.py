# -*- coding: utf-8 -*-
import os
from io import open
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

with open(os.path.join(here, "requirements.txt"), "r", encoding="utf-8") as fobj:
    requires = [x for x in fobj.readlines() if x]
requires = [x.strip() for x in requires if x.strip()]

setup(
    name="django-power-cms",
    version="0.3.3",
    description="A power content management system based on django admin framework.",
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
    keywords=["django admin extentions", "django power cms"],
    install_requires=requires,
    packages=find_packages(".", exclude=["django_power_cms_example", "django_power_cms_example.migrations", "django_power_cms_demo"]),
    py_modules=["django_power_cms"],
    zip_safe=False,
    include_package_data=True,
)