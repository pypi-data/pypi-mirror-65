from setuptools import setup, find_namespace_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))
with open("README.md", 'r') as fh:
    long = fh.read()
setup(
    name='mathraining-scrapper',
    author='Charlotte Thomas',
    packages=find_namespace_packages(include=['mathraining.*']),
    version='0.0.2',
    description='The Mathraining Website Scrapper',
    url='https://github.com/Mathraining-Discord-Bot/MT-Scrapper',
    author_email='charlotte@sfiars.eu',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    python_requires='>=3.5',
    long_description=long,
    long_description_content_type="text/markdown",
    install_requires=['faster_than_requests', 'beautifulsoup4']
)
