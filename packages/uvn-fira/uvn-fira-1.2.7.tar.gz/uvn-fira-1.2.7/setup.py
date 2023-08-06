# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['uvn_fira', 'uvn_fira.api', 'uvn_fira.core']

package_data = \
{'': ['*']}

install_requires = \
['toml>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'uvn-fira',
    'version': '1.2.7',
    'description': 'The backend and API code for the Unscripted mini-game.',
    'long_description': '# Fira\n\n**Fira** is the main backend and API code for the minigame in [Unscripted](https://unscripted.marquiskurt.net), a visual novel about software development. Fira provides many facets of the minigame, including a public API that players can use to code solutions to the minigame puzzles, a configuration and data generator from level files, and a virtual machine that runs low-level code that the minigame processes. Fira is named after Fira Sans, one of the game\'s characters.\n\n\n[![MPL](https://img.shields.io/github/license/alicerunsonfedora/fira)](LICENSE.txt)\n![Python](https://img.shields.io/badge/python-2.7+-blue.svg)\n[![PyPI version](https://badge.fury.io/py/uvn-fira.svg)](https://pypi.org/project/uvn-fira)\n\n## Requirements\n\n- Python 2.7+\n- Poetry package manager\n\n## Getting started\n\nFira comes pre-packaged in Unscripted but can be installed outside of the game to work better with IDEs and other Python tools such as Poetry.\n\n### Dependencies\n\nFira is both a Python 2 and Python 3 package and relies on the TOML Python package. These dependencies will be installed with the package, either from source or from PyPI.\n\n### Quick Start: Install on PyPI\n\nFira is available on PyPI and can be installed as such:\n\n```\npip install uvn-fira\n```\n\n### Install from source\n\nTo install Fira from the source code, first clone the repository from GitHub via `git clone`. You\'ll also need to install [Poetry](https://python-poetry.org). In the root of the source, run the following commands:\n\n```\npoetry install\npoetry build\n```\n\nThe resulting wheel files will be available in the `dist` directory.\n\n## Usage\n\nFor players installing this package to solve minigame puzzles, using the Fira package to access the API is relatively straightforward:\n\n```py\nfrom uvn_fira.api import get_level_information, CSPlayer, CSWorld\n\ngp, gw = get_level_information(0,\n                               fn_path=renpy.config.savedir + "/minigame",\n                               exists=renpy.loadable,\n                               load=renpy.exports.file) # type: (CSPlayer, CSWorld)\n```\n\nDocumentation on the API is located inside of Unscripted by going to **Help &rsaquo; Minigame** or **Settings &rsaquo; Minigame**.\n\nThe documentation for the entire package is located at [https://fira.marquiskurt.net](https://fira.marquiskurt.net), which is useful for developers that wish to make custom toolkits that connect to the minigame\'s virtual machine or for modders that wish to make custom minigame levels.\n\n## Reporting bugs\n\nBugs and feature requests for Fira can be submitted on YouTrack. [Submit a report &rsaquo;](https://youtrack.marquiskurt.net/youtrack/newIssue?project=FIRA)\n\n## License\n\nThe Fira package is licensed under the Mozilla Public License v2.0.',
    'author': 'Marquis Kurt',
    'author_email': 'software@marquiskurt.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alicerunsonfedora/fira',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*',
}


setup(**setup_kwargs)
