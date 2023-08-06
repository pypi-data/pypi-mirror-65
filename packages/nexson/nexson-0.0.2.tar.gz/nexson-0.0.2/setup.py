#!/usr/bin/env python
import sys
import os

# setup.py largely based on
#   http://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/
# Also see Jeet Sukumaran's DendroPy

###############################################################################
# setuptools/distutils/etc. import and configuration
try:
    # noinspection PyUnresolvedReferences
    import ez_setup

    try:
        ez_setup_path = " ('" + os.path.abspath(ez_setup.__file__) + "')"
    except OSError:
        ez_setup_path = ""
    sys.stderr.write("using ez_setup%s\n" % ez_setup_path)
    ez_setup.use_setuptools()
    # noinspection PyUnresolvedReferences
    import setuptools

    try:
        setuptools_path = " ('" + os.path.abspath(setuptools.__file__) + "')"
    except OSError:
        setuptools_path = ""
    sys.stderr.write("using setuptools%s\n" % setuptools_path)
    # noinspection PyUnresolvedReferences
    from setuptools import setup, find_packages
except ImportError as e:
    sys.stderr.write("using distutils\n")
    from distutils.core import setup

    sys.stderr.write("using canned package list\n")
    PACKAGES = ['nexson',
                'nexson.syntax',
                'nexson.validation',
                ]
    EXTRA_KWARGS = {}
else:
    sys.stderr.write("searching for packages\n")
    PACKAGES = find_packages()
    EXTRA_KWARGS = dict(
        include_package_data=True,
        test_suite="nexson.test"
    )

EXTRA_KWARGS["zip_safe"] = True
ENTRY_POINTS = {}
EXTRA_KWARGS['scripts'] = []

###############################################################################
# setuptools/distuils command extensions
try:
    from setuptools import Command
except ImportError:
    sys.stderr.write("setuptools.Command could not be imported: setuptools extensions not available\n")
else:
    sys.stderr.write("setuptools command extensions are available\n")
    command_hook = "distutils.commands"
    ENTRY_POINTS[command_hook] = []

setup(
    name='nexson',
    version='0.0.2',  # sync with __version__ in nexson/__init__.py
    description='Library for dealing with phylogenetic trees in the NexSON format',
    long_description=(open('README.rst').read()),
    url='https://github.com/OpenTreeOfLife/nexson',
    license='BSD',
    author='Emily Jane B. McTavish and Mark T. Holder',
    py_modules=['nexson'],
    install_requires=['setuptools', # sync with requirements.txt
                      'wheel',
                      'peyutil>=0.0.1' 
                      ],
    packages=PACKAGES,
    entry_points=ENTRY_POINTS,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
    **EXTRA_KWARGS
)
