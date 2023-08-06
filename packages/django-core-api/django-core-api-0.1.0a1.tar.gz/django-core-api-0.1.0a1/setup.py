#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup


def read(f):
    return open(f, 'r', encoding='utf-8').read()


def _extract_dependencies(filename):
    pkgs, deps = [], []
    with open(filename) as f:
        for line in f.readlines():
            if '://' in line:
                deps.append(line)
            else:
                pkgs.append(line)
    return pkgs, deps


def parse_requirements():
    install_packages, install_deps = _extract_dependencies('./requirements.txt')
    dev_packages, dev_deps = _extract_dependencies('./requirements-dev.txt')

    return (
        install_packages,
        dev_packages,
        install_deps + dev_deps,
    )


install, dev_install, dependencies = parse_requirements()

setup(
    name='django-core-api',
    version='0.1.0a1',
    license='BSD',
    description='Django Core RESTFul API',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='Joao Daher',
    author_email='joao@daher.dev',
    packages=find_packages(exclude=['test_*']),
    include_package_data=True,
    install_requires=install,
    tests_require=dev_install,
    dependency_links=dependencies,
    python_requires=">=3.7",
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
