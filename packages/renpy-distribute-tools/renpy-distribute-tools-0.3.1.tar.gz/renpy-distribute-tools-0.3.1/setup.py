# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['renpy_distribute_tools']

package_data = \
{'': ['*']}

install_requires = \
['pylint>=2.4.4,<3.0.0']

setup_kwargs = {
    'name': 'renpy-distribute-tools',
    'version': '0.3.1',
    'description': "Utilities that make Ren'Py distribution less of a pain in the arse",
    'long_description': "# Ren'Py Distribution Tools\n\nA set of tools to make Ren'Py distribution less of a pain in the arse.\n\n[![MPL](https://img.shields.io/github/license/alicerunsonfedora/renpy-distribute-tools)](LICENSE.txt) \n![Python](https://img.shields.io/badge/python-3.7+-blue.svg) \n\n## Installing `renpy-distribute-tools`\n\nTo install via PyPI:\n\n```\npip install renpy-distribute-tools\n```\n\nOr, if you're using a Poetry project, just add the dependency:\n\n```\npoetry add renpy-distribute-tools\n```\n\n## Building from source\n\nRen'Py Distribute Tools is a Poetry project and can be built using Poetry's `build` command.\n\n1. Clone the repository.\n2. In the root of the project, run `poetry install`.\n3. Finally, run `poetry build`.\n\n## What's included\n\nThe Ren'Py Distribution Tools set comes with utilities that make it easy to do the following:\n\n- Modifying a visual novel's `Info.plist`.\n- Code-signing the visual novel binaries in the Mac app with entitlements.\n- Creating a ZIP copy of the Mac app and sending it to Apple's notarization servers.\n- Stapling the notarization ticket to a macOS app.\n\n## Usage\n\nSee the [documentation](https://alicerunsonfedora.github.io/renpy-distribute-tools) for more info.",
    'author': 'Marquis Kurt',
    'author_email': 'software@marquiskurt.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alicerunsonfeodra/renpy-distribute-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
