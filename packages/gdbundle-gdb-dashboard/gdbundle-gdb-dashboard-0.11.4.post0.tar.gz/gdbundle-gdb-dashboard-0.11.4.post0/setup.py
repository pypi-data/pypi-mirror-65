# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gdbundle_gdb_dashboard']

package_data = \
{'': ['*'],
 'gdbundle_gdb_dashboard': ['scripts/.gitignore',
                            'scripts/.gitignore',
                            'scripts/.keep',
                            'scripts/.keep']}

setup_kwargs = {
    'name': 'gdbundle-gdb-dashboard',
    'version': '0.11.4.post0',
    'description': 'gdbundle plugin for cyrus-and/gdb-dashboard',
    'long_description': '# gdbundle-gdb-dashboard\n\nThis is a [gdbundle](https://github.com/memfault/gdbundle) plugin for [cyrus-and/gdb-dashboard](https://github.com/cyrus-and/gdb-dashboard)\n\n## Compatibility\n\n- GDB\n\n## Installation\n\nAfter setting up [gdbundle](https://github.com/memfault/gdbundle), install the package from PyPi. \n\n```\n$ pip install gdbundle-gdb-dashboard\n```\n\nIf you\'ve decided to manually manage your packages using the `gdbundle(include=[])` argument,\nadd it to the list of plugins.\n\n```\n# .gdbinit\n\n[...]\nimport gdbundle\nplugins = ["gdb-dashboard"]\ngdbundle.init(include=plugins)\n```\n\n## Building\n\nTo build this package, it requires calling `make` first as we need to download the `.gdbinit` file from the actual repository since it isn\'t packaged as a Python package.\n\n```\n$ make\n$ poetry build\n$ poetry publish\n```\n',
    'author': 'Tyler Hoffman',
    'author_email': 'tyler@memfault.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
