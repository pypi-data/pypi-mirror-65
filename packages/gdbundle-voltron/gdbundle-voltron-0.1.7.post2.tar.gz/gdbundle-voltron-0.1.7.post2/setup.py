# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gdbundle_voltron']

package_data = \
{'': ['*']}

install_requires = \
['voltron==0.1.7']

setup_kwargs = {
    'name': 'gdbundle-voltron',
    'version': '0.1.7.post2',
    'description': 'gdbundle plugin for snare/voltron',
    'long_description': '# gdbundle-voltron\n\nThis is a [gdbundle](https://github.com/memfault/gdbundle) plugin for [snare/voltron](https://github.com/snare/voltron)\n\n## Compatibility\n\nThis works for GDB, but it appears that the LLDB version of Voltron (as of [bcf25d957657414d025ff488889cdef8d4fcae06](https://github.com/snare/voltron/commit/bcf25d957657414d025ff488889cdef8d4fcae06)) does not work due not pinning versions in it\'s `setup.py` and does not work on Python 3.7. \n\n```\nImportError: cannot import name \'DispatcherMiddleware\' from \'werkzeug.wsgi\'\n```\n\n## Installation\n\nAfter setting up [gdbundle](https://github.com/memfault/gdbundle), install the package from PyPi. \n\n```\n$ pip install gdbundle-voltron\n```\n\nIf you\'ve decided to manually manage your packages using the `gdbundle(include=[])` argument,\nadd it to the list of plugins.\n\n```\n# .gdbinit\n\n[...]\nimport gdbundle\nplugins = ["voltron"]\ngdbundle.init(include=plugins)\n```\n\n## Building\n\n```\n$ poetry build\n$ poetry publish\n```\n',
    'author': 'Tyler Hoffman',
    'author_email': 'tyler@memfault.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.7.*, !=3.8.*',
}


setup(**setup_kwargs)
