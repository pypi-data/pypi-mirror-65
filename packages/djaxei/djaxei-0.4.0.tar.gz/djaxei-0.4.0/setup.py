# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['djaxei', 'djaxei.migrations']

package_data = \
{'': ['*'], 'djaxei': ['templates/djaxei/*']}

install_requires = \
['django>=1.11,<4', 'openpyxl<3']

setup_kwargs = {
    'name': 'djaxei',
    'version': '0.4.0',
    'description': 'A django admin extension for importing exporting records from/to xls/ods',
    'long_description': '# A django admin extension for importing exporting records from/to xls/ods\n\nA Python library project using:\n* pytest\n* flake8\n* tox\n* bumpversion\n* isort\n\n* Free software: MIT license\n* Documentation: __TBD__\n\n\nFeatures\n--------\n\n* TODO\n\nCredits\n-------\n\n',
    'author': 'Giovanni Bronzini',
    'author_email': 'g.bronzini@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/GigiusB/djaxei.git',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
