# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shinobi_client', 'shinobi_client.tests']

package_data = \
{'': ['*']}

install_requires = \
['logzero>=1.5.0,<2.0.0', 'requests>=2.23,<3.0', 'toml>=0.9,<0.10']

extras_require = \
{'shinobi-controller': ['gitpython>=3,<4',
                        'docker-compose>=1.25,<2.0',
                        'get-port>=0.0.5,<0.0.6']}

setup_kwargs = {
    'name': 'shinobi-client',
    'version': '0.1.1',
    'description': 'https://github.com/colin-nolan/python-shinobi-client',
    'long_description': '[![Build Status](https://travis-ci.com/colin-nolan/python-shinobi.svg?branch=master)](https://travis-ci.com/colin-nolan/python-shinobi)\n[![Code Coverage](https://codecov.io/gh/colin-nolan/python-shinobi/branch/master/graph/badge.svg)](https://codecov.io/gh/colin-nolan/python-shinobi)\n\n# Shinobi Python Client\n_A Python client for controlling [Shinobi](https://gitlab.com/Shinobi-Systems/Shinobi), an open-source video management \nsolution._\n\n\n## About\nThis package contains an (very incomplete) set of tools for interacting with Shinobi using Python.\n\nThis library tries to use the (rather unique) [documented API](https://shinobi.video/docs/api) but it also uses \nundocumented endpoints (which may not be stable).\n\n\n## Installation\nInstall from [PyPi](https://pypi.org/project/shinobi-client/):\n```\npip install shinobi-client\n```\n\nInstall with ability to start a Shinobi installation:\n```\npip install shinobi-client[shinobi-controller]\n```\n\n\n## Usage\n### User ORM\n```python\nfrom shinobi_client import ShinobiUserOrm\n\nuser_orm = ShinobiUserOrm(host, port, super_user_token)\n\nuser = user_orm.get(email)\n\nusers = user_orm.get_all()\n\nuser = user_orm.create(email, password)\n\nmodified = user_orm.modify(email, password=new_password)\n\ndeleted = user_orm.delete(email)\n```\n\n### Shinobi Controller\nStarts/Stops a temporary [containerised installation of Shinboi](https://github.com/colin-nolan/docker-shinobi). Written\nfor the purpose of testing but it is installable as an extra.\n```python\nfrom shinobi_client import start_shinobi\n\nwith start_shinobi() as shinobi:\n    print(shinobi.url)\n    # Do things with a temporary Shinobi installation\n```\nor\n```python\nfrom shinobi_client import ShinobiController\n\ncontroller = ShinobiController()\nshinobi = controller.start()\nprint(shinobi.url)\n# Do things with a temporary Shinobi installation\ncontroller.stop()\n```\n\n\n## Development\nInstall with dev-dependencies:\n```\npoetry install --no-root --extras "shinobi-controller"\n```\n\nRun tests with:\n```\npython -m unittest discover -v -s shinobi/tests\n```\n\n\n## Legal\n[AGPL v3.0](LICENSE.txt). Copyright 2020 Colin Nolan.\n\nI am not affiliated to the development of Shinobi project in any way. This work is in no way related to the company that\nI work for.\n',
    'author': 'Colin Nolan',
    'author_email': 'cn580@alumni.york.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/colin-nolan/python-shinobi-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
