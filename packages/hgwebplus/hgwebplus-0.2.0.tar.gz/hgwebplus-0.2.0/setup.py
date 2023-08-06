from setuptools import setup


setup(
    name='hgwebplus',
    version='0.2.0',
    author='Gary Kramlich',
    author_email='grim@reaperworld.com',
    url='https://keep.imfreedom.org/grim/hgwebplus',
    description='Mercurial plugin to add additional functionality to hgweb',
    package_dir={'hgext3rd': 'src'},
    packages=['hgext3rd'],
    install_requires=[
        'cmarkgfm',
        # skip mercurial because it might be installed on the system
        # 'mercurial',
    ],
    license='GPLv2',
    classifiers=[
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Topic :: Software Development :: Version Control',
    ],
)
