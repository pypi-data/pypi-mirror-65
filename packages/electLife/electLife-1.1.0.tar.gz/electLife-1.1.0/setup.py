#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='electLife',
    version='1.1.0',
    description=(
        'Electric life calculation module'
    ),
    long_description=open('README.cd').read(),
    author='SZ',
    author_email='z1398655303@163.com',
    maintainer='shawnzhao',
    maintainer_email='z1398655303@163.com',
    license='MIT License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/z13986553031/predicted-life',
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)