# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shinobi_client',
 'shinobi_client.orms',
 'shinobi_client.tests',
 'shinobi_client.tests.orms']

package_data = \
{'': ['*']}

install_requires = \
['logzero>=1.5.0,<2.0.0', 'requests>=2.23,<3.0', 'toml>=0.9,<0.10']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8'],
 'cli': ['fire>=0.3.0,<0.4.0'],
 'shinobi-controller': ['gitpython>=3,<4',
                        'docker-compose>=1.25,<2.0',
                        'get-port>=0.0.5,<0.0.6']}

setup_kwargs = {
    'name': 'shinobi-client',
    'version': '1.0.0',
    'description': 'A Python client for controlling Shinobi (an open-source video management solution)',
    'long_description': '[![Build Status](https://travis-ci.com/colin-nolan/python-shinobi-client.svg?branch=master)](https://travis-ci.com/colin-nolan/python-shinobi-client)\n[![Code Coverage](https://codecov.io/gh/colin-nolan/python-shinobi-client/branch/master/graph/badge.svg)](https://codecov.io/gh/colin-nolan/python-shinobi-client)\n\n# Shinobi Python Client\n_A Python client for controlling [Shinobi](https://gitlab.com/Shinobi-Systems/Shinobi) (an open-source video management \nsolution)._\n\n\n## About\nThis package contains an (very incomplete) set of tools for interacting with Shinobi using Python.\n\nThis library tries to use the (rather unique) [documented API](https://shinobi.video/docs/api) but it also uses \nundocumented endpoints (which may not be stable).\n\n\n## Installation\nInstall from [PyPi](https://pypi.org/project/shinobi-client/):\n```bash\npip install shinobi-client\n```\n\nInstall with ability to start a Shinobi installation:\n```bash\npip install shinobi-client[shinobi-controller]\n```\n\nInstall with CLI:\n```bash\npip install shinobi-client[cli]\n```\n\n## Usage\n### Python\nStart with creating the client for a particular Shinobi installation:\n```python\nfrom shinobi_client import ShinobiClient\n\nshinobi_client = ShinobiClient(host, port, super_user_token)\n```\n\n#### User\n```python\nuser = shinobi_client.user.get(email)\n\nusers = shinobi_client.user.get_all()\n\nuser = shinobi_client.user.create(email, password)\n\nmodified = shinobi_client.user.modify(email, password=new_password)\n\ndeleted = shinobi_client.user.delete(email)\n```\n\n#### API Key\n```python\napi_key = shinobi_client.api_key.get(email, password)\n```\n\n#### Shinobi Controller\nStarts/Stops a temporary [containerised installation of Shinboi](https://github.com/colin-nolan/docker-shinobi). Written\nfor the purpose of testing but it is also installable as an extra. Requires Docker.\n```python\nfrom shinobi_client import start_shinobi\n\nwith start_shinobi() as shinobi_client:\n    print(shinobi_client.url)\n    # Do things with a temporary Shinobi installation\n```\nor\n```python\nfrom shinobi_client import ShinobiController\n\ncontroller = ShinobiController()\nshinobi_client = controller.start()\nprint(shinobi_client.url)\n# Do things with a temporary Shinobi installation\ncontroller.stop()\n```\n\n### CLI\nA basic auto-generated CLI is available if the package is installed with the `cli` extra: \n```bash\nPYTHONPATH=. python shinobi_client/user.py \\\n        --host=HOST --port=PORT --super_user_token=SUPER_USER_TOKEN \\\n    get user@example.com\n```\ne.g.\n```bash\n$ PYTHONPATH=. python shinobi_client/cli.py \\\n        --host=\'0.0.0.0\' --port=50694 --super_user_token=\'26dd3352-73c4-4bbd-8b09-17f2aacbd7b9\' \\\n    create \'user@example.com\' \'password123\'\n```\n\n\n## Development\nInstall with dev-dependencies:\n```bash\npoetry install --no-root --extras "shinobi-controller, cli"\n```\n\nRun tests with:\n```bash\npython -m unittest discover -v -s shinobi/tests\n```\n\n\n## Legal\n[AGPL v3.0](LICENSE.txt). Copyright 2020 Colin Nolan.\n\nI am not affiliated to the development of Shinobi project in any way. This work is in no way related to the company that\nI work for.\n',
    'author': 'Colin Nolan',
    'author_email': 'cn580@alumni.york.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/colin-nolan/python-shinobi-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
