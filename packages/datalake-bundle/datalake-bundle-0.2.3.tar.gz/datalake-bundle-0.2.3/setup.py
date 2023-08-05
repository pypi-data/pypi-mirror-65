# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['datalakebundle']

package_data = \
{'': ['*'],
 'datalakebundle': ['_config/.gitignore',
                    '_config/.gitignore',
                    '_config/.gitignore',
                    '_config/config.yaml',
                    '_config/config.yaml',
                    '_config/config.yaml',
                    '_config/config_test.yaml',
                    '_config/config_test.yaml',
                    '_config/config_test.yaml',
                    'hdfs/*',
                    'table/*',
                    'test/*']}

install_requires = \
['console-bundle>=0.2.0,<0.3.0',
 'databricks-bundle>=0.2.4,<0.4.0',
 'pyfony-bundles>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'datalake-bundle',
    'version': '0.2.3',
    'description': 'DataLake bundle for the Pyfony Framework',
    'long_description': 'DataLake bundle for the Pyfony Framework\n',
    'author': 'Jiri Koutny',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DataSentics/datalake-bundle',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<3.8.0',
}


setup(**setup_kwargs)
