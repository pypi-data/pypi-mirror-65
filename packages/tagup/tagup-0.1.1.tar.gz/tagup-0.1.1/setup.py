# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tagup']

package_data = \
{'': ['*']}

install_requires = \
['lark-parser>=0.8.5,<0.9.0']

setup_kwargs = {
    'name': 'tagup',
    'version': '0.1.1',
    'description': 'Reference implementation of the Tagup Language',
    'long_description': '# tagup\n\n**tagup** is a Python module which provides a reference implementation of the [Tagup Language](https://fairburn.dev/tagup/).\n\nThis module currently implements [version 1.0.0](https://fairburn.dev/tagup/1.0.0/) of the Tagup Language.\n\n## Changelog\n\n**v0.1.1**\n\n- Added non-standard option to trim whitespace from arguments before tag evaluation.\n- Fixed bug where whitespace was considered when specifying a name/position for argument substitution.\n\n**v0.1.0**\n\n- Initial release.\n',
    'author': 'Garrett Fairburn',
    'author_email': 'garrett@fairburn.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://fairburn.dev/tagup/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3,<4',
}


setup(**setup_kwargs)
