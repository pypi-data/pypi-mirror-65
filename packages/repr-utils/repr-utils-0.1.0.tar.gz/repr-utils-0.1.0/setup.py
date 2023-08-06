# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['repr_utils', 'repr_utils.templates']

package_data = \
{'': ['*']}

install_requires = \
['jinja2>=2.11.1,<3.0.0', 'tabulate>=0.8.7,<0.9.0']

setup_kwargs = {
    'name': 'repr-utils',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'luttik',
    'author_email': 'dtluttik@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
