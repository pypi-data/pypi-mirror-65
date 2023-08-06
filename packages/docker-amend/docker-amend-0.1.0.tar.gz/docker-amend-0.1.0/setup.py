# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['docker_amend']
install_requires = \
['docker>=4.2.0,<5.0.0', 'typer>=0.1.1,<0.2.0']

entry_points = \
{'console_scripts': ['docker-amend = docker_amend:_run']}

setup_kwargs = {
    'name': 'docker-amend',
    'version': '0.1.0',
    'description': 'Amend Docker images by running a command in a separate layer.',
    'long_description': None,
    'author': 'Alexander Pushkov',
    'author_email': 'alexander@notpushk.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
