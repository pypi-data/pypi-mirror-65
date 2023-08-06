# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mce']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3,<20.0',
 'bdd2dfa>=0.4.0,<0.5.0',
 'bidict>=0.18.3,<0.19.0',
 'dfa[draw]>=2.0.0,<3.0.0',
 'funcy>=1.13,<2.0',
 'multiprocess>=0.70.9,<0.71.0',
 'py-aiger-bdd>=0.3.1,<0.4.0',
 'py-aiger-bv>=2.0.0,<3.0.0',
 'py-aiger-coins[sat,bdd]>=1.4.0,<2.0.0',
 'py-aiger-sat>=1.1.0,<2.0.0',
 'scipy>=1.4.1,<2.0.0']

setup_kwargs = {
    'name': 'mce-spec-inference',
    'version': '0.1.0',
    'description': 'Maximum Causal Entropy Specification Inference.',
    'long_description': '',
    'author': 'Marcell Vazquez-Chanlatte',
    'author_email': 'mvc@linux.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mvcisback/mce-spec-inference',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
