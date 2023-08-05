# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['caduceussocket']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['caduceus = caduceus:session.run']}

setup_kwargs = {
    'name': 'caduceussocket',
    'version': '0.1.0',
    'description': 'A python socket manager.',
    'long_description': 'Caduceus\n',
    'author': 'Callum Burns-Curd',
    'author_email': 'callum@fish.cat',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/C-Bookie/Caduceus',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
