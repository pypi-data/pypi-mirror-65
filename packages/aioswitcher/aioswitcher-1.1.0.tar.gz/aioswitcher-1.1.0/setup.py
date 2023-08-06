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
    'version': '1.1.0',
    'description': 'Switcher Boiler Unofficial Bridge and API.',
    'long_description': '# Switcher Boiler Unofficial Bridge and API</br>[![gh-release]][2] [![pypi-license]][11] [![pypi-downloads]][11]\n\n[![gh-build-status]][7] [![read-the-docs]][8] [![codecov]][3] [![dependabot-status]][1]\n\nPyPi module named [aioswitcher][11] for integrating with the [Switcher Water Heater](https://www.switcher.co.il/).</br>\nPlease check out the [documentation][8].\n\n> *Important Note:*</br>\n> This project adheres [semver](https://semver.org/) since version `0.1.0`,  prior\n> to this, it adhered [calver](https://calver.org/).</br>\n> As a result of this midst project change, [PyPi][11] automatically marks the wrong version,\n> `2019.10.25`, as the latest.</br>\n> If you use `2019.10.25` or earlier [calver](https://calver.org/) adhering versions, please note</br>\n> **it will soon be deleted from [PyPi][11] - Please use the latest [semver](https://semver.org/) adhering version**.\n\n<!-- Real Links -->\n[1]: https://dependabot.com\n[2]: https://github.com/TomerFi/aioswitcher/releases\n[3]: https://codecov.io/gh/TomerFi/aioswitcher\n[7]: https://github.com/TomerFi/aioswitcher/actions?query=workflow%3ABuild\n[8]: https://aioswitcher.tomfi.info/\n[11]: https://pypi.org/project/aioswitcher/\n<!-- Badges Links -->\n[codecov]: https://codecov.io/gh/TomerFi/aioswitcher/graph/badge.svg\n[dependabot-status]: https://api.dependabot.com/badges/status?host=github&repo=TomerFi/aioswitcher\n[gh-build-status]: https://github.com/TomerFi/aioswitcher/workflows/Build/badge.svg\n[gh-release]: https://img.shields.io/github/v/release/TomerFi/aioswitcher?logo=github\n[pypi-downloads]: https://img.shields.io/pypi/dm/aioswitcher.svg?logo=pypi\n[pypi-license]: https://img.shields.io/pypi/l/aioswitcher.svg?logo=pypi\n[read-the-docs]: https://readthedocs.org/projects/aioswitcher/badge/?version=stable\n',
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
