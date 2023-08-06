# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pecho']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.3,<0.5.0']

setup_kwargs = {
    'name': 'pecho',
    'version': '0.4.0',
    'description': 'Easy way to write things like status bars',
    'long_description': "# pecho\n[![PyPI](https://img.shields.io/pypi/v/pecho)](https://pypi.org/project/pecho/)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pecho)\n![PyPI - Wheel](https://img.shields.io/pypi/wheel/pecho)\n\nPecho makes it easy to write things like status bars.\n\n## Usage\n```python\nfrom pecho import echo\n\necho('1%')  # 1%\necho('2%')  # Replaces with 2%\necho('3%', newline=True)  # Replaces with 3% and appends a newline\necho('4%')  # 3%\\n4%\n```\n",
    'author': 'Nihaal Sangha',
    'author_email': '18350092+OrangutanGaming@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/OrangutanGaming/pecho',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
