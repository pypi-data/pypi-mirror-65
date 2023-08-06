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
    'version': '0.1.1',
    'description': 'Amend Docker images by running a command in a separate layer.',
    'long_description': '# docker-amend\n\n**Install**: `pipx install docker-amend` (plain `pip` works too)\n\n**Usage**: ```docker-amend [OPTIONS] IMAGE COMMAND...```\n\n**Example**:\n\n```\n$ docker build -t my-image .\n...\n$ docker-amend my-image poetry add requests\n$ docker run my-image poetry show\nrequests         2.23.0     Python HTTP for Humans.\n$ grep requests pyproject.toml\nrequests = ^2.23.0\n```\n\n**Options**:\n\n* `-t, --tag NAME[:VERSION]`: Use a different name/tag for the resulting image\n* `-v, --volume SOURCE:TARGET`: Bind mount a volume (assumes --no-pwd-volume)\n* `--no-cwd-volume`: Do not mount cwd as a volume\n* `--install-completion`: Install completion for the current shell.\n* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n* `--help`: Show this message and exit.\n',
    'author': 'Alexander Pushkov',
    'author_email': 'alexander@notpushk.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/notpushkin/docker-amend',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
