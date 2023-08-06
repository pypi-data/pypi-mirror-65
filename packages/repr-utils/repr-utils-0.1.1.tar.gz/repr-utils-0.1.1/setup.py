# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['repr_utils', 'repr_utils.templates']

package_data = \
{'': ['*']}

install_requires = \
['isort>=4.3.21,<5.0.0', 'jinja2>=2.11.1,<3.0.0', 'tabulate>=0.8.7,<0.9.0']

setup_kwargs = {
    'name': 'repr-utils',
    'version': '0.1.1',
    'description': '    Contains common ellements that when displayed will adhere to the correct format (e.g markdown, latex, html, text) in tools like jupyter notebooks',
    'long_description': 'REPR-UTIL\n---------\nA toolkit to quickly display elements in tools like `jupyter`_ by building upon `ipython rich display`_.\n\nContributions are appreciated.\n\n.. _`ipython rich display`: https://ipython.readthedocs.io/\n.. _`jupyter`: https://jupyter.org/\n',
    'author': 'luttik',
    'author_email': 'dtluttik@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Luttik/repr_utils',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
