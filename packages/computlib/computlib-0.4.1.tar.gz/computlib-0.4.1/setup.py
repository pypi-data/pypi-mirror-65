# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['computlib']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'computlib',
    'version': '0.4.1',
    'description': 'Simple mathematical library',
    'long_description': '# Computlib\n\nA simple compute library\n\n[![PyPI](https://img.shields.io/pypi/v/computlib)](https://pypi.org/project/computlib/)\n[![PyPI - License](https://img.shields.io/pypi/l/computlib)](https://pypi.org/project/computlib/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/computlib)](https://pypi.org/project/computlib/)\n[![pipeline status](https://gitlab.com/mlysakowski/computlib/badges/master/pipeline.svg)](https://gitlab.com/mlysakowski/computlib/-/commits/master)\n[![coverage report](https://gitlab.com/mlysakowski/computlib/badges/master/coverage.svg)](https://gitlab.com/mlysakowski/computlib/-/commits/master)\n[![python:3.7](https://gitlab.com/mlysakowski/computlib/-/jobs/artifacts/master/raw/test_python3.7.svg?job=python3.7)](https://gitlab.com/mlysakowski/computlib/-/commits/master)\n[![python:3.8](https://gitlab.com/mlysakowski/computlib/-/jobs/artifacts/master/raw/test_python3.8.svg?job=python3.8)](https://gitlab.com/mlysakowski/computlib/-/commits/master)\n[![bandit](https://gitlab.com/mlysakowski/computlib/-/jobs/artifacts/master/raw/test_bandit.svg?job=check-bandit)](https://gitlab.com/mlysakowski/computlib/-/commits/master)\n[![black](https://gitlab.com/mlysakowski/computlib/-/jobs/artifacts/master/raw/test_black.svg?job=check-black)](https://gitlab.com/mlysakowski/computlib/-/commits/master)\n[![safety](https://gitlab.com/mlysakowski/computlib/-/jobs/artifacts/master/raw/test_safety.svg?job=check-safety)](https://gitlab.com/mlysakowski/computlib/-/commits/master)\n[![flake8](https://gitlab.com/mlysakowski/computlib/-/jobs/artifacts/master/raw/test_flake8.svg?job=check-flake8)](https://gitlab.com/mlysakowski/computlib/-/commits/master)\n[![documentation](https://gitlab.com/mlysakowski/computlib/-/jobs/artifacts/master/raw/documentation.svg?job=pages)](https://gitlab.com/mlysakowski/computlib/-/commits/master)\n\n\n## Documentations\n\nSee [Documentation page](https://mlysakowski.gitlab.io/computlib/)\n',
    'author': 'Mathieu LYSAKOWSKI',
    'author_email': 'mathieu@phec.net',
    'maintainer': 'Mathieu LYSAKOWSKI',
    'maintainer_email': 'mathieu@phec.net',
    'url': 'https://gitlab.com/mlysakowski/computlib',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
