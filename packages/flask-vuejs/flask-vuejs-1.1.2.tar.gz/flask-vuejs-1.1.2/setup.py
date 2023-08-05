# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_vuejs']

package_data = \
{'': ['*'],
 'flask_vuejs': ['frontend/*',
                 'frontend/components/*',
                 'init/*',
                 'templates/vue/*']}

install_requires = \
['flask>=1.1.1,<2.0.0']

setup_kwargs = {
    'name': 'flask-vuejs',
    'version': '1.1.2',
    'description': 'Connect Flask With VueJS Framework',
    'long_description': '![GitHub repo size](https://img.shields.io/github/repo-size/pacotei/flask-vuejs)![GitHub top language](https://img.shields.io/github/languages/top/pacotei/flask-vuejs)![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flask-vuejs)\n![PyPI - License](https://img.shields.io/pypi/l/flask-vuejs)\n\nDocumentation: https://flaskvue.pacotei.xyz/',
    'author': 'Marcus Pereira',
    'author_email': 'oi@pacotei.xyz',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://flaskvue.pacotei.xyz/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
