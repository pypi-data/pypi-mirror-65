# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aioswitcher', 'aioswitcher.api', 'aioswitcher.bridge']

package_data = \
{'': ['*']}

extras_require = \
{'checkers': ['bandit==1.6.2',
              'black==19.10b0',
              'doc8==0.8.0',
              'flake8==3.7.9',
              'flake8-docstrings==1.5.0',
              'isort==4.3.21',
              'mypy==0.770',
              'pygments==2.6.1',
              'yamllint==1.21.0'],
 'tests': ['asynctest==0.13.0',
           'codecov==2.0.22',
           'pytest==5.4.1',
           'pytest-aiohttp==0.3.0',
           'pytest-asyncio==0.10.0',
           'pytest-cov==2.8.1']}

setup_kwargs = {
    'name': 'aioswitcher',
    'version': '1.1.2',
    'description': 'Switcher Water Heater Unofficial Bridge and API.',
    'long_description': "# Switcher Water Heater Unofficial Bridge and API</br>[![pypi-version]][11] [![pypi-downloads]][11] [![license-badge]][4]\n\n[![gh-build-status]][7] [![read-the-docs]][8] [![codecov]][3] [![dependabot-status]][1]\n\nPyPi module named [aioswitcher][11] for integrating with the [Switcher Water Heater](https://www.switcher.co.il/).</br>\nPlease check out the [documentation][8].\n\n## Install\n\n```shell\npip install aioswitcher\n```\n\n## Usage Example\n\nPlease check out the [documentation][8] for the full usage section.\n\n```python\nasync with SwitcherV2Api(\n        your_loop, ip_address, phone_id,\n        device_id, device_password) as swapi:\n    # get the device state\n    state_response = await swapi.get_state()\n\n    # control the device: on / off / on + 30 minutes timer\n    turn_on_response = await swapi.control_device(consts.COMMAND_ON)\n    turn_off_response = await swapi.control_device(consts.COMMAND_OFF)\n    turn_on_30_min_response = await swapi.control_device(consts.COMMAND_ON, '30')\n```\n\n## Contributing\n\nThe contributing guidelines are [here](.github/CONTRIBUTING.md)\n\n## Code of Conduct\n\nThe code of conduct is [here](.github/CODE_OF_CONDUCT.md)\n\n<!-- Real Links -->\n[1]: https://dependabot.com\n[2]: https://github.com/TomerFi/aioswitcher/releases\n[3]: https://codecov.io/gh/TomerFi/aioswitcher\n[4]: https://github.com/TomerFi/aioswitcher\n[7]: https://github.com/TomerFi/aioswitcher/actions?query=workflow%3ABuild\n[8]: https://aioswitcher.tomfi.info/\n[11]: https://pypi.org/project/aioswitcher\n<!-- Badges Links -->\n[codecov]: https://codecov.io/gh/TomerFi/aioswitcher/graph/badge.svg\n[dependabot-status]: https://api.dependabot.com/badges/status?host=github&repo=TomerFi/aioswitcher\n[gh-build-status]: https://github.com/TomerFi/aioswitcher/workflows/Build/badge.svg\n[license-badge]: https://img.shields.io/github/license/tomerfi/aioswitcher\n[pypi-downloads]: https://img.shields.io/pypi/dm/aioswitcher.svg?logo=pypi&color=1082C2\n[pypi-version]: https://img.shields.io/pypi/v/aioswitcher?logo=pypi\n[read-the-docs]: https://readthedocs.org/projects/aioswitcher/badge/?version=stable\n",
    'author': 'Tomer Figenblat',
    'author_email': 'tomer.figenblat@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/aioswitcher/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
