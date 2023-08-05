# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sphinx_scylla_theme', 'sphinx_scylla_theme.extensions']

package_data = \
{'': ['*'],
 'sphinx_scylla_theme': ['static/*',
                         'static/css/*',
                         'static/css/doc/*',
                         'static/css/doc/ext/*',
                         'static/fonts/*',
                         'static/img/*',
                         'static/js/*',
                         'static/js/foundation/*',
                         'static/js/vendor/*']}

install_requires = \
['sphinx==1.8.0']

setup_kwargs = {
    'name': 'sphinx-scylla-theme',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Nick Volynkin',
    'author_email': 'nick.volynkin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
