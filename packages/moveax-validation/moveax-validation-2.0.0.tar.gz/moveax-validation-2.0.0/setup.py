# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['validation',
 'validation.constants',
 'validation.exceptions',
 'validation.parser',
 'validation.rules',
 'validation.types',
 'validation.utils',
 'validation.validator']

package_data = \
{'': ['*']}

install_requires = \
['phonenumbers>=8.10,<9.0', 'python-dateutil>=2.7.3,<3.0.0']

setup_kwargs = {
    'name': 'moveax-validation',
    'version': '2.0.0',
    'description': 'Python implementation of our validation library',
    'long_description': "# Validation library\n[![Build Status](https://travis-ci.com/moveaxlab/validation-py.svg?branch=master)](https://travis-ci.com/moveaxlab/validation-py)\n[![Coverage Status](https://coveralls.io/repos/github/moveaxlab/validation-py/badge.svg?branch=master)](https://coveralls.io/github/moveaxlab/validation-py?branch=master)\n![GitHub](https://img.shields.io/github/license/moveaxlab/validation-py.svg)\n![PyPI](https://img.shields.io/pypi/v/moveax-validation.svg?style=popout)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/moveax-validation.svg)\n\n## Installation\n- Install from [Pypi](https://pypi.org/project/moveax-validation/):\n\n    ```console\n    $ pip install moveax-validation\n            --- or ---\n    $ poetry add moveax-validation\n    ```\n\n## Usage\n- Simple example:\n\n    ```python\n    >>> from validation import ValidatorFactory\n\n    >>> data = ['foo', 'bar']\n    >>> schema = {\n        'elements': {\n            'rules': ['minlen:3']\n            'type': 'string'\n        },\n        'rules': ['maxlen:3'],\n        'type': 'array'\n    }\n    >>> validator = ValidatorFactory.make(schema)\n    >>> validator.validate(data)\n    ```\n\n## Testing\n- Run the test suite with:\n\n    ```console\n    $ poetry run coverage run unit.py\n    ```\n",
    'author': 'Mattias E. Mignone',
    'author_email': 'mattias.mignone@moveax.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/moveaxlab/validation-py/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
