#!/usr/bin/python
from datetime import date
from setuptools import setup
import os
from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt')
reqs = [str(ir.req) for ir in install_reqs]

try:
    # This borks sdist.
    os.remove('.SELF')
except:
    pass

setup(
    name="search_horizon",
    version="0.1",
    author="Dmitri Zimine, Kirill Izotov",
    author_email="dz@stackstorm.com",
    license="Apache v2.0",
    description="Horizon plugin for Search service",
    packages=['search', 'search.search'],
    package_data={"search": ["search/templates/search/*.html"]},
    zip_safe=False,
    install_requires=reqs
)