# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['recap_argument_graph']

package_data = \
{'': ['*']}

install_requires = \
['graphviz>=0.13.2,<0.14.0',
 'lxml>=4.4.2,<5.0.0',
 'networkx>=2.4,<3.0',
 'pendulum>=2.0,<3.0']

setup_kwargs = {
    'name': 'recap-argument-graph',
    'version': '0.1.26',
    'description': '',
    'long_description': None,
    'author': 'Mirko Lenz',
    'author_email': 'info@mirko-lenz.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
