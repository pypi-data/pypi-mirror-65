# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cloudendure',
 'cloudendure.cloudendure_api',
 'cloudendure.cloudendure_api.api',
 'cloudendure.cloudendure_api.models',
 'cloudendure.cloudendure_api.test',
 'cloudendure.tests']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.12.30,<2.0.0',
 'certifi>=2019.11.28,<2020.0.0',
 'cookiecutter>=1.7.0,<2.0.0',
 'fire>=0.3.0,<0.4.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'requests>=2.23.0,<3.0.0',
 'setuptools>=45.2.0,<46.0.0',
 'six>=1.14.0,<2.0.0',
 'urllib3>=1.25.8,<2.0.0']

entry_points = \
{'console_scripts': ['ce = cloudendure.cloudendure:main',
                     'cloudendure = cloudendure.cloudendure:main']}

setup_kwargs = {
    'name': 'cloudendure',
    'version': '0.2.5',
    'description': 'Python wrapper and CLI for CloudEndure',
    'long_description': '# cloudendure-python\n\nPython wrapper and CLI for [CloudEndure](https://www.cloudendure.com/)\n\n[![PyPI](https://img.shields.io/pypi/v/cloudendure) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cloudendure)](https://pypi.org/project/cloudendure/) [![PyPi Publish](https://github.com/2ndWatch/cloudendure-python/workflows/PyPi%20Publish/badge.svg)](https://2ndwatch.github.io/cloudendure-python/) [![Documenation](https://github.com/2ndWatch/cloudendure-python/workflows/Github%20Pages/badge.svg)](https://2ndwatch.github.io/cloudendure-python/)\n\n## Requirements\n\n[Python 3.7+](https://www.python.org/downloads/)\n\n## Installation & Usage\n\n### Basic Installation / pip\n\n```sh\npip install cloudendure\ncloudendure version\n```\n\n### Local Development with Poetry\n\n```sh\nbrew install poetry # if not installed\npoetry install\n```\n\n### Local Development with Docker\n\n```sh\ndocker run --rm -it cloudendurepy/cloudendure bash\n```\n\n### Usage\n\nThen import the package:\n\n```python\nimport cloudendure\n```\n\n## Getting Started\nCloudEndure Pipeline Flow\n![CloudEndure Pipeline Flow](images/ce_migration_pipeline.png)\n\nCloudEndure Data Flow\n![CloudEndure Data Flow](images/ce_dataflow.png)\n\nPipeline Flow (as seen in AWS Console)\n![Pipeline_Flow](images/stepfunctions_graph.svg)\n\n### Logging in via CLI using environment variables\n\nPlease note: `cloudendure` and `ce` can be used interchangeably\n\n```sh\nexport CLOUDENDURE_USERNAME=<your_ce_user>\nexport CLOUDENDURE_PASSWORD=<your_ce_password>\nexport CLOUDENDURE_DESTINATION_ACCOUNT=<destination_aws_account_id>\n\ncloudendure api login\n```\n\nor\n\n```sh\nexport CLOUDENDURE_USER_API_TOKEN=<your_ce_user_api_token>\nexport CLOUDENDURE_DESTINATION_ACCOUNT=<destination_aws_account_id>\n\nce api login\n```\n\n### Logging in via CLI inline\n\nPlease note: `cloudendure` and `ce` can be used interchangeably\n\n```sh\ncloudendure api login --user=<your_ce_user> --password=<your_ce_password>\n```\n\nor\n\n```sh\nce api login --token=<your_ce_user_api_token>\n```\n\nLogging in for the first time will generate the `~/.cloudendure.yml` file.\n\n## Coming Soon\n\nThis project is currently a work in progress and will actively change. This client has not yet been finalized and is entirely subject to change.\n\n## Changelog\n\nCheck out the [CHANGELOG](CHANGELOG.md)\n',
    'author': 'Mark Beacom',
    'author_email': 'mark@markbeacom.com',
    'maintainer': 'Evan Lucchesi',
    'maintainer_email': 'evan@2ndwatch.com',
    'url': 'https://2ndwatch.github.io/cloudendure-python/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
