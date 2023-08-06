# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['special_k',
 'special_k.check_gpg_keys',
 'special_k.model_metadata',
 'special_k.serializers',
 'special_k.tests',
 'special_k.tests.fake_keys']

package_data = \
{'': ['*']}

install_requires = \
['click>=6.3,<7.0',
 'dill>=0.2,<0.4',
 'funcy>=1.10,<2.0',
 'gpg==1.10.0',
 'h5py>=2.7.1,<3.0.0',
 'joblib>=0.11,<=0.15',
 'msgpack>=0.5.6,<0.6.0',
 'numpy>=1.10.0,<2.0.0',
 'pandas>=0.25.3,<0.26.0',
 'voluptuous>=0.11.5,<0.12.0']

extras_require = \
{'torch': ['torch>=1.4,<2.0']}

setup_kwargs = {
    'name': 'special-k',
    'version': '0.1.1',
    'description': 'Safe serialization of ML models.',
    'long_description': None,
    'author': 'Mikey Shulman',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
