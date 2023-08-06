#!/usr/bin/env python3

from setuptools import setup

setup(
    name             = 'hgwebplus',
    version          = '0.1.0',
    author           = 'Gary Kramlich',
    author_email     = 'grim@reaperworld.com',
    url              = 'https://keep.imfreedom.org/grim/hgwebplus',
    description      = 'Mercurial plugin to add additional functionality to hgweb',
    package_dir      = {'hgext3rd': 'src'},
    packages         = ['hgext3rd'],
    install_requires = [
        'cmarkgfm',
    ],
    license          = 'GPLv2',
    classifiers      = [
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Topic :: Software Development :: Version Control',
    ],
)
