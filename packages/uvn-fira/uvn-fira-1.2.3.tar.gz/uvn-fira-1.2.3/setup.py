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
    'version': '1.2.3',
    'description': 'The backend and API code for the Unscripted mini-game.',
    'long_description': "# Fira\n\nFira is the package that contains the backend code and API code for Unscripted's minigame. Fira is named after Fira Sans, one of the game's characters.\n\n\n[![MPL](https://img.shields.io/github/license/alicerunsonfedora/fira)](LICENSE.txt)\n![Python](https://img.shields.io/badge/python-2.7+-blue.svg)\n\n## Requirements\n\n- Python 2.7\n- Poetry package manager\n- Ren'Py\n\n## Installing\n\nTo install Fira to a Python environment, run `pip install uvn-fira`. For environments in Ren'Py, run `pip install uvn-fira --target game/python-packages`.\n\n## Building from Source\n\nClone the Fira repository and then run `poetry install` to create a Python virtual environment and install the development dependencies to.\n\nTo build the final package, run `poetry build`.\n\nTo publish the package to PyPI, run `poetry publish`.\n\n> Note: For any scripts that rely on these functions, make sure you have your Python environment link to the Ren'Py module.\n\n## License\n\nThe Fira package is licensed under the Mozilla Public License v2.0.",
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
