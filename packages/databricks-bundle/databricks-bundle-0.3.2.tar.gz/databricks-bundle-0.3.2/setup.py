# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['databricksbundle']

package_data = \
{'': ['*'],
 'databricksbundle': ['_config/*',
                      'dbutils/*',
                      'jdbc/*',
                      'notebook/*',
                      'pipeline/*',
                      'spark/*']}

install_requires = \
['injecta>=0.7.0,<0.8.0',
 'ipython>=7.0.0,<8.0.0',
 'pandas>=0.24.2,<0.25.0',
 'pyarrow>=0.16.0,<0.17.0',
 'pyfony-bundles>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'databricks-bundle',
    'version': '0.3.2',
    'description': 'Databricks bundle for the Pyfony framework',
    'long_description': 'Databricks bundle for the Pyfony framework\n',
    'author': 'Jiri Koutny',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DataSentics/databricks-bundle',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<3.8.0',
}


setup(**setup_kwargs)
