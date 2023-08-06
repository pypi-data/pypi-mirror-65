# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gdbundle_example']

package_data = \
{'': ['*'], 'gdbundle_example': ['scripts/*']}

setup_kwargs = {
    'name': 'gdbundle-example',
    'version': '0.0.1',
    'description': 'Example gdbundle plugin',
    'long_description': '# gdbundle-example\n\nThis is a [gdbundle](https://github.com/memfault/gdbundle) plugin example. It is not meant to be useful, but to serve as a reference for gdbundle plugin creators and curious individuals.\n\n## Compatibility\n\n- GDB\n- LLDB\n\n## Installation\n\nAfter setting up [gdbundle](https://github.com/memfault/gdbundle), install the package from PyPi. \n\n```\n$ pip install gdbundle-example\n```\n\nIf you\'ve decided to manually manage your packages using the `gdbundle(include=[])` argument,\nadd it to the list of plugins.\n\n```\n# .gdbinit\n\n[...]\nimport gdbundle\nplugins = ["example"]\ngdbundle.init(include=plugins)\n```\n\n## Building\n\n```\n$ poetry build\n$ poetry publish\n```\n',
    'author': 'Tyler Hoffman',
    'author_email': 'tyler@memfault.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
