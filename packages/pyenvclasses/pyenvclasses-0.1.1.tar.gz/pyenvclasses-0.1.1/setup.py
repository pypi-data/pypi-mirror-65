# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['envclasses']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyenvclasses',
    'version': '0.1.1',
    'description': 'Wrapper for python dataclasses to read from the environment',
    'long_description': None,
    'author': 'Ian Baldwin',
    'author_email': 'ian@iantbaldw.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
