import os
from setuptools import setup, find_packages
from pathlib import Path
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

def strip_comments(l):
    return l.split('#', 1)[0].strip()


def _pip_requirement(req):
    if req.startswith('-r '):
        _, path = req.split()
        return reqs(*path.split('/'))
    return [req]


def _reqs(*f):
    path = (Path.cwd() ).joinpath(*f)
    with path.open() as fh:
        reqs = [strip_comments(l) for l in fh.readlines()]
        return [_pip_requirement(r) for r in reqs if r]


def reqs(*f):
    return [req for subreq in _reqs(*f) for req in subreq]

setup(
    name='django-admin-log-control',
    version='1.1.4',
    packages=find_packages(),
    description='Control your admin-panel changes',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Nurbergen',
    author_email='nhinatolla@gmail.com',
    url='https://github.com/nkhinatolla/django-admin-logs-control/',
    license='MIT',
    install_requires=reqs('requirements.txt'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
