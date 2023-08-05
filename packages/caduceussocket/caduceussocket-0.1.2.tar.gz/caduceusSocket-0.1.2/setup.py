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
    'version': '0.1.2',
    'description': 'A python socket manager.',
    'long_description': '\n# A python socket manager.\n\nExtend Session for server classes.\nExtend Connection for client clasess.\nTo expose functions to RPC calling, add their name to the white_list_functions list.\nTo call a function, you can send JSON with the function name and arguments contained:\n\n\t{\n\t\t"type": "function_name",\n\t\t"args": [\n\t\t\t"argument 1",\n\t\t\t"argument 2"\n\t\t]\n\t}\n\nYou can register a new connection by sending the clients name and the name of the session they should be moved to:\n\n\t{\n\t\t"type": "register",\n\t\t"args": [\n\t\t\t"client_name",\n\t\t\t"session_name"\n\t\t]\n\t}\n\nTo send a message to other clients, you can call the broadcast message using the message and client name:\n\t\n\t{\n\t\t"type": "broadcast",\n\t\t"args": [\n\t\t\t"message",\n\t\t\t"client_name"\n\t\t]\n\t}\n',
    'author': 'Callum Burns-Curd',
    'author_email': 'callum@fish.cat',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/C-Bookie/Caduceus',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
