
# -*- coding: utf-8 -*-

# DO NOT EDIT THIS FILE!
# This file has been autogenerated by dephell <3
# https://github.com/dephell/dephell

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


import os.path

readme = ''
here = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(here, 'README.rst')
if os.path.exists(readme_path):
    with open(readme_path, 'rb') as stream:
        readme = stream.read().decode('utf8')


setup(
    long_description=readme,
    name='micropy-cli',
    version='3.1.1',
    description='Micropython Project Management Tool with VSCode support, Linting, Intellisense, Dependency Management, and more!',
    python_requires='==3.*,>=3.6.0',
    project_urls={"documentation": "https://micropy-cli.readthedocs.io", "homepage": "https://github.com/BradenM/micropy-cli", "repository": "https://github.com/BradenM/micropy-cli"},
    author='Braden Mars',
    author_email='bradenmars@bradenmars.me',
    license='MIT',
    keywords='micropython stubs linting vscode intellisense',
    classifiers=['Topic :: Software Development :: Code Generators', 'Topic :: Software Development :: Embedded Systems', 'Topic :: Software Development :: Build Tools', 'Programming Language :: Python :: Implementation :: MicroPython', 'Programming Language :: Python :: Implementation :: CPython', 'Development Status :: 5 - Production/Stable', 'Intended Audience :: Developers', 'License :: OSI Approved :: MIT License'],
    entry_points={"console_scripts": ["micropy = micropy.cli:cli"]},
    packages=['micropy', 'micropy.config', 'micropy.data', 'micropy.packages', 'micropy.project', 'micropy.project.modules', 'micropy.stubs', 'micropy.utils'],
    package_dir={"": "."},
    package_data={"micropy": ["lib/stubber/*.conf", "lib/stubber/*.md", "lib/stubber/.vscode/*.json", "lib/stubber/patches/*.patch", "lib/stubber/runOnPc/*.cfg", "lib/stubber/runOnPc/*.cmd"], "micropy.data": ["*.json", "schemas/*.json"], "micropy.project": ["template/*.conf", "template/.vscode/*.json"]},
    install_requires=['boltons==19.*,>=19.3.0', 'cachier==1.*,>=1.2.0', 'click==7.*,>=7.0.0', 'colorama!=0.4.2,>=0.4.1; sys_platform == "win32"', 'dpath==1.*,>=1.4.0', 'jinja2==2.*,>=2.10.0', 'jsonschema==3.2.0', 'packaging==19.*,>=19.2.0', 'questionary==1.*,>=1.4.0', 'requests==2.*,>=2.22.0', 'requirements-parser==0.*,>=0.2.0', 'rshell==0.*,>=0.0.26', 'tqdm==4.*,>=4.39.0'],
    extras_require={"dev": ["autoflake==1.*,>=1.3.0", "autopep8==1.*,>=1.4.0", "bump2version==0.*,>=0.5.11", "codacy-coverage==1.*,>=1.3.0", "coveralls==1.*,>=1.8.0", "doc8==0.*,>=0.8.0", "docformatter==1.*,>=1.3.0", "flake8==3.*,>=3.7.0", "isort==4.*,>=4.3.0", "mypy==0.*,>=0.750.0", "pylint==2.*,>=2.4.0", "pyminifier==2.*,>=2.1.0", "pytest==5.*,>=5.3.0", "pytest-cov==2.*,>=2.8.0", "pytest-datadir==1.*,>=1.3.0", "pytest-forked==1.*,>=1.1.0", "pytest-mock==1.*,>=1.12.0", "pytest-runner==5.*,>=5.2.0", "pytest-testmon==1.*,>=1.0.0", "pytest-watch==4.*,>=4.2.0", "pytest-xdist==1.*,>=1.30.0", "recommonmark==0.*,>=0.6.0", "requests-mock==1.*,>=1.7.0", "rope==0.*,>=0.14.0", "sphinx==2.*,>=2.2.0", "sphinx-click==2.*,>=2.3.0", "tox==3.*,>=3.14.0", "tox-gh-actions==0.*,>=0.3.0"]},
)
