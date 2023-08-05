# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tsrc',
 'tsrc.cli',
 'tsrc.test',
 'tsrc.test.cli',
 'tsrc.test.helpers',
 'tsrc.workspace']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3.0,<20.0.0',
 'cli-ui>=0.10.0,<0.11.0',
 'colored_traceback>=0.3.0,<0.4.0',
 'path>=13.1.0,<14.0.0',
 'requests>=2.22.0,<3.0.0',
 'ruamel.yaml>=0.16.7,<0.17.0',
 'schema>=0.7.1,<0.8.0',
 'tabulate>=0.8.6,<0.9.0',
 'unidecode>=1.1.1,<2.0.0']

entry_points = \
{'console_scripts': ['tsrc = tsrc.cli.main:main']}

setup_kwargs = {
    'name': 'tsrc',
    'version': '2.0.0',
    'description': 'Manage groups of git repositories',
    'long_description': '.. image::  https://raw.githubusercontent.com/TankerHQ/sdk-js/master/src/public/tanker.png\n   :target: #readme\n\n|\n\n.. image:: https://img.shields.io/github/license/TankerHQ/tsrc.svg\n   :target: https://github.com/TankerHQ/tsrc/blob/master/LICENSE\n\n.. image:: https://github.com/TankerHQ/tsrc/workflows/tests/badge.svg\n   :target: https://github.com/TankerHQ/tsrc/actions\n\n.. image:: https://github.com/TankerHQ/tsrc/workflows/linters/badge.svg\n   :target: https://github.com/TankerHQ/tsrc/actions\n\n.. image:: https://img.shields.io/codecov/c/github/TankerHQ/tsrc.svg?label=Coverage\n   :target: https://codecov.io/gh/TankerHQ/tsrc\n\n.. image:: https://img.shields.io/pypi/v/tsrc.svg\n   :target: https://pypi.org/project/tsrc/\n\n\ntsrc: manage groups of git repositories\n========================================\n\n`Overview`_ · `Installation`_ · `Usage example`_ · `Documentation`_ · `Release notes`_ · `Contributing`_ · `License`_\n\nOverview\n---------\n\ntsrc is a command-line tool that helps you manage groups of several git repositories.\n\nIt can be `seen in action on asciinema.org <https://asciinema.org/a/131625>`_.\n\n\nInstallation\n-------------\n\n`tsrc` is `available on pypi <https://pypi.org/project/tsrc>`_ an can be installed via ``pip``. It requires **Python 3.5** or later.\n\n\nUsage Example\n-------------\n\n\n* Create a *manifest* repository. (``git@example.org/manifest``)\n\n* Push a file named ``manifest.yml`` looking like:\n\n.. code-block:: yaml\n\n    repos:\n      - src: foo\n        url: git@example.com/foo.git\n\n      - src: bar\n        url: git@example.com/bar.git\n\n\n* Create a new workspace with all the repositories listed in the manifest:\n\n.. code-block:: console\n\n    $ tsrc init git@git.local/manifest.git\n\n    :: Configuring workspace in /path/to/work\n    ...\n    => Cloning missing repos\n    * (1/2) foo\n    ...\n    * (2/2) bar\n    ...\n    : Configuring remotes\n    Done ✓\n\n\n* Synchronize all the repositories in the workspace:\n\n.. code-block:: console\n\n    $ tsrc sync\n    => Updating manifest\n    ...\n    :: Configuring remotes\n    :: Synchronizing workspace\n    * (1/2) foo\n    => Fetching origin\n    => Updating branch\n    Already up to date\n    * (2/2) bar\n    => Updating branch\n    Updating 29ac0e1..b635a43\n    Fast-forward\n     bar.txt | 1 +\n     1 file changed, 1 insertion(+)\n     create mode 100644 bar.txt\n    Done ✓\n\n\nDocumentation\n--------------\n\nFor more details and examples, please refer to `tsrc documentation <https://TankerHQ.github.io/tsrc/>`_.\n\nRelease notes\n-------------\n\nDetailed changes for each release are documented in the `changelog <https://tankerhq.github.io/tsrc/changelog/>`_.\n\nContributing\n------------\n\nWe welcome feedback, `bug reports <https://github.com/TankerHQ/tsrc/issues>`_, and bug fixes in the form of `pull requests <https://github.com/TankerHQ/tsrc/pulls>`_.\n\nDetailed instructions can be found `in the documentation <https://tankerhq.github.io/tsrc/contrib/>`_.\n\nLicense\n-------\n\ntsrc is licensed under a `BSD 3-Clause license <https://github.com/TankerHQ/tsrc/blob/master/LICENSE>`_.\n',
    'author': 'Dimitri Merejkowsky',
    'author_email': 'd.merej@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/TankerHQ/tsrc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
