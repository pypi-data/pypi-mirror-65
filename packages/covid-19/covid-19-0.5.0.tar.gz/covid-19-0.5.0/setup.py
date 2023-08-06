# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['covid_19']

package_data = \
{'': ['*']}

install_requires = \
['hug>=2.6.1,<3.0.0', 'pandas>=1.0.3,<2.0.0', 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['covid = covid_19.api:__hug__.cli']}

setup_kwargs = {
    'name': 'covid-19',
    'version': '0.5.0',
    'description': 'An API around the https://github.com/CSSEGISandData/COVID-19 dataset',
    'long_description': '# COVID-19 API\n\n**[coronavirus-api.net][coronavirus-api]**\n\n![](https://github.com/knowsuchagency/covid-19/workflows/black/badge.svg)\n![](https://github.com/knowsuchagency/covid-19/workflows/unit%20tests/badge.svg)\n\nThis API is a wrapper around Johns Hopkins\' https://github.com/CSSEGISandData/COVID-19 dataset.\n\nPlease abide by their terms of use with respect to how you use their data via this API.\n\n## Installation\n\nThis package is hosted on [pypi](https://pypi.org/project/covid-19/)\n\nThe recommended method of installation is through [pipx].\n```bash\npipx install covid-19\n```\nHowever, covid-19 can also be pip-installed as normal.\n```bash\npip install covid-19\n```\n\n## Website\n\nThe [coronavirus api website](https://coronavirus-api.net/get_all?min_date=2020-02-01&state=California&limit=100) allows several methods of slicing and dicing the data.\n\nFor example, the `get_all` endpoint (which returns all data) can be filtered for rows which only contain\ndata for California and Colorado as of March 22nd in this way:\n\n`https://coronavirus-api.net/get_all?min_date=2020-03-22&states=["California", "Colorada"]`\n\nThe [main page][coronavirus-api] will list the available endpoints and their available parameters.\n\n## CLI Usage\n\nThis package installs a command-line tool, `covid`\n\nIt lets you programmatically access John Hopkins\' dataset via terminal commands\nor via a rest api that can itself be instantiated locally from the cli\n\n```bash\ncovid --help\n\nThis API is a wrapper around Johns Hopkins\' https://github.com/CSSEGISandData/COVID-19 dataset.\n\nPlease abide by their terms of use with respect to how you use their data via this API.\n\n\nAvailable Commands:\n\n - get_all: Fetch all data from John Hopkins.\n - countries: Return all countries and regions in the dataset.\n - states: Return all states and provinces in the dataset.\n - for_date: Return all data for a specific date.\n - serve: Serve REST API locally.\n\n```\n\ni.e.\n\n```bash\ncovid for_date 2020-03-21\n[\n    {\n        "Province/State": "Hubei",\n        "Country/Region": "China",\n        "Last Update": "2020-03-22T09:43:06",\n        "Confirmed": 67800.0,\n        "Deaths": 3144.0,\n        "Recovered": 59433.0,\n        "Latitude": 30.9756,\n        "Longitude": 112.2707\n...\n```\n\n## Docker\n\nThis package can also be run as a [docker image][docker image].\n\n```bash\ndocker run knowsuchagency/covid-19 --help\n```\n\n[pipx]: https://github.com/pipxproject/pipx\n[coronavirus-api]: https://coronavirus-api.net\n[docker image]: https://hub.docker.com/repository/docker/knowsuchagency/covid-19\n',
    'author': 'Stephan Fitzpatrick',
    'author_email': 'knowsuchagency@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://coronavirus-api.net',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
