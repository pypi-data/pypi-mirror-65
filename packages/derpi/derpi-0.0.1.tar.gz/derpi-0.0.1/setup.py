# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from os import path
from itertools import product
from functools import reduce
__author__ = 'luckydonald, pingmader'
long_description = """Python API wrapper for the new API of derpibooru.org"""

here = path.abspath(path.dirname(__file__))

setup(
    name='derpi', version="0.0.1",
    description=long_description,
    long_description=long_description,
    # The project's main homepage.
    url='https://github.com/derpipy/derpipy',
    # Author details
    author=__author__,
    author_email='derpi.github+code@luckydonald.de, pingmader@gmail.com',
    # Choose your license
    license='MIT',
    platforms=["any"],
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 1 - Planning',  # 2 - Pre-Alpha, 3 - Alpha, 4 - Beta, 5 - Production/Stable
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Multimedia',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Environment :: MacOS X',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX :: Linux',
        'Operating System :: iOS',
        'Operating System :: MacOS',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Android',
        'Operating System :: Microsoft :: Windows',
        'Topic :: Internet',
        'Topic :: Multimedia',
        'Topic :: Multimedia :: Video',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Software Development :: Libraries',
        'Typing :: Typed',
    ],
    # What does your project relate to?
    keywords=(
        'derpibooru derpibooru.org python api wrapper my_little_pony mlp '
        'friendship_is_magic FiM fim earthpony unicorn pegasus' + reduce(
            lambda a, x: a+' '+x, map(lambda x: x[0]+x[1], product(['pon', 'p0n'], ['', 'y', 'e', 'ies', 'es', 's']))
        )
    ),
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),
    # find_packages(exclude=['contrib', 'docs', 'tests*']),
    # List run-time dependencies here. These will be installed by pip when your
    # project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[],
    # List additional groups of dependencies here (e.g. development dependencies).
    # You can install these using the following syntax, for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'sync': ['requests'],
        'async': ['httpx'],
    },
    # If there are data files included in your packages that need to be
    # installed, specify them here. If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    # package_data={
    # 'sample': ['package_data.dat'],
    # },
    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages.
    # see http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
)
