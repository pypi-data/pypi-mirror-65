#!/usr/bin/env python

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'pybuilder',
        version = '0.12.0',
        description = 'PyBuilder',
        long_description = 'PyBuilder\n=========\n\n[PyBuilder](https://pybuilder.io)\n\n\n[![Gitter](https://img.shields.io/gitter/room/pybuilder/pybuilder)](https://gitter.im/pybuilder/pybuilder)\n[![Build Status](https://img.shields.io/travis/pybuilder/pybuilder/master)](https://travis-ci.org/pybuilder/pybuilder)\n[![Coverage Status](https://img.shields.io/coveralls/github/pybuilder/pybuilder/master)](https://coveralls.io/r/pybuilder/pybuilder?branch=master)\n\n[![PyBuilder Version](https://img.shields.io/pypi/v/pybuilder)](https://pypi.org/project/pybuilder/)\n[![PyBuilder Python Versions](https://img.shields.io/pypi/pyversions/pybuilder)](https://pypi.org/project/pybuilder/)\n[![PyBuilder Downloads Per Day](https://img.shields.io/pypi/dd/pybuilder)](https://pypi.org/project/pybuilder/)\n[![PyBuilder Downloads Per Week](https://img.shields.io/pypi/dw/pybuilder)](https://pypi.org/project/pybuilder/)\n[![PyBuilder Downloads Per Month](https://img.shields.io/pypi/dm/pybuilder)](https://pypi.org/project/pybuilder/)\n\nPyBuilder is a software build tool written in 100% pure Python, mainly\ntargeting Python applications.\n\nPyBuilder is based on the concept of dependency based programming, but it also\ncomes with a powerful plugin mechanism, allowing the construction of build life\ncycles similar to those known from other famous (Java) build tools.\n\nPyBuilder is running on the following versions of Python: 2.7, 3.5, 3.6, 3.7, 3.8, and PyPy 2.7, 3.5 and 3.6.\n\nSee the [Travis Build](https://travis-ci.org/pybuilder/pybuilder) for version specific output.\n\n## Installing\n\nPyBuilder is available using pip:\n\n    $ pip install pybuilder\n\nFor development builds use:\n\n    $ pip install --pre pybuilder\n\nSee the [PyPI](https://pypi.org/project/pybuilder/) for more information.\n\n## Getting started\n\nPyBuilder emphasizes simplicity. If you want to build a pure Python project and\nuse the recommended directory layout, all you have to do is create a file\nbuild.py with the following content:\n\n```python\nfrom pybuilder.core import use_plugin\n\nuse_plugin("python.core")\nuse_plugin("python.unittest")\nuse_plugin("python.coverage")\nuse_plugin("python.distutils")\n\ndefault_task = "publish"\n```\n\nSee the [PyBuilder homepage](https://pybuilder.io) for more details and\na list of plugins.\n\n## Release Notes\n\nThe release notes can be found [here](https://pybuilder.io/release-notes/).\nThere will also be a git tag with each release. Please note that we do not currently promote tags to GitHub "releases".\n\n## Development\nSee [Developing PyBuilder](https://pybuilder.io/documentation/developing-pybuilder.html)\n',
        long_description_content_type = 'text/markdown',
        author = 'Alexander Metzner, Maximilien Riehl, Michael Gruber, Udo Juettner, Marcel Wolf, Arcadiy Ivanov, Valentin Haenel',
        author_email = 'alexander.metzner@gmail.com, max@riehl.io, aelgru@gmail.com, udo.juettner@gmail.com, marcel.wolf@me.com, arcadiy@ivanov.biz, valentin@haenel.co',
        license = 'Apache License',
        url = 'https://pybuilder.io',
        scripts = ['scripts/pyb'],
        packages = [
            'pybuilder',
            'pybuilder._vendor',
            'pybuilder._vendor.colorama',
            'pybuilder._vendor.pkg_resources',
            'pybuilder._vendor.pkg_resources._vendor',
            'pybuilder._vendor.pkg_resources._vendor.packaging',
            'pybuilder._vendor.pkg_resources.extern',
            'pybuilder._vendor.tailer',
            'pybuilder._vendor.tblib',
            'pybuilder._vendor.virtualenv_support',
            'pybuilder.extern',
            'pybuilder.pluginhelper',
            'pybuilder.plugins',
            'pybuilder.plugins.python',
            'pybuilder.plugins.python.remote_tools',
            'pybuilder.remote'
        ],
        namespace_packages = [],
        py_modules = [],
        classifiers = [
            'Programming Language :: Python',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python :: Implementation :: PyPy',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: POSIX :: Linux',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: OS Independent',
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Apache Software License',
            'Topic :: Software Development :: Build Tools',
            'Topic :: Software Development :: Quality Assurance',
            'Topic :: Software Development :: Testing'
        ],
        entry_points = {
            'console_scripts': ['pyb = pybuilder.cli:main']
        },
        data_files = [],
        package_data = {
            '': ['*.whl'],
            'pybuilder': ['LICENSE'],
            'pybuilder._vendor': ['LICENSES']
        },
        install_requires = [],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        keywords = '',
        python_requires = '!=3.0,!=3.1,!=3.2,!=3.3,!=3.4,>=2.7',
        obsoletes = [],
    )
