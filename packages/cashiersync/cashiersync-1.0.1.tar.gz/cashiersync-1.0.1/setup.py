"""Setup"""
from setuptools import setup, find_packages
from distutils.core import setup
from codecs import open
from os import path

# Get the long description from the README file
#here = path.abspath(path.dirname(__file__))
# with open(path.join(here, 'README.md'), encoding='utf-8') as f:
#     long_description = f.read()

setup(
    name="cashiersync",
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    version='1.0.1',
    description="Server-side synchronization component for Cashier",
    author="Alen Siljak",
    author_email="cashier@alensiljak.eu.org",
    url="https://gitlab.com/alensiljak/cashier-sync",
    # download_url = "http://pypi.org/download/python3-chardet-1.0.1.tgz",
    keywords=["cashier", "finance", "portfolio", "ledger"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    #long_description=long_description,
    #long_description_content_type="text/markdown",
    install_requires=[
        'flask', 'flask_cors',
        'pyyaml', 'pyxdg'
    ],
    # entry_points={
    #     'console_scripts': [
    #         'cashiersync=cashiersync.app:run_server',
    #     ],
    # },
    include_package_data=True
)