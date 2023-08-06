# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['envclasses']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyenvclasses',
    'version': '0.1.0',
    'description': 'Wrapper for python dataclasses to read from the environment',
    'long_description': "![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)\n[![PyPI version](https://badge.fury.io/py/pyenvclasses.svg)](https://badge.fury.io/py/pyenvclasses)\n![Tests](https://github.com/sandal-tan/pyenvclasses/workflows/.github/workflows/test.yaml/badge.svg)\n\n# Envclasses\n\nEnvclasses are a thin wrapper around dataclasses which allows for the values to be defined via environment variables\nrather than explicitly in code. Values are typed and are able to be defaulted. \n\n## Motivation\n\nI got tired of writing code that was configured through environment variables, referencing the environment variable \nwhen I needed to instantiate something. This made it difficult to keep up with how I could configure that software that\nI was writing as I would have to comb through the code and make sure that the documentation was up to date. \n\nEnvclasses are an attempt to reduce the sprawl of configuration through environment variables and centralize\nconfiguration into a single, document-able class. They are both inspired by, and built on top of dataclasses, which is\nwhy their structure is so similar.\n\n## Usage\n\nDefining an environment class is simple:\n\n```python\n\nfrom envclasses import EnvClassMeta\n\nclass ApplicationConfig(metaclass=EnvClassMeta):\n\n    db_url: str\n    db_username: str\n    db_password: str\n    port: int = 5050\n    mode: str = 'development'\n\n\nconfig = ApplicationConfig()\n```\n\nThe provided metaclass will turn the `ApplicationConfig` into a dataclass with fields defined from `os.environ`.\nThe metaclass will prioritize upper-case versions of fields before lower-case, that is to say `DB_URL` would be\nprioritized over `db_url`. Mixed-case variants are not considered.\n\nIf values are not defined, the metaclass will wait until all fields have been tested to report which are missing. In the\nevent that we should ignore missing fields, the environment variable `env_ignore_missing` should be defined as `true` or\n`yes`.\n",
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
