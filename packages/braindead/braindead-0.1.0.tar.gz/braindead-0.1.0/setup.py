# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['braindead']

package_data = \
{'': ['*'],
 'braindead': ['default_template/*', 'default_template/static/styles/*']}

install_requires = \
['jinja2>=2.11.1,<3.0.0',
 'markdown>=3.2.1,<4.0.0',
 'pygments>=2.6.1,<3.0.0',
 'toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['braindead = braindead.rendering:render_blog']}

setup_kwargs = {
    'name': 'braindead',
    'version': '0.1.0',
    'description': 'Braindead is a braindead simple static site generator for your personal blog',
    'long_description': None,
    'author': 'Olaf Górski',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://grski.pl/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
