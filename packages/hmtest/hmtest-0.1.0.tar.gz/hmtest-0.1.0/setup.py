# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hmtest']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0',
 'desert>=2020.1.6,<2021.0.0',
 'marshmallow>=3.5.1,<4.0.0',
 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['hmtest = hmtest.console:main']}

setup_kwargs = {
    'name': 'hmtest',
    'version': '0.1.0',
    'description': 'The hypermodern Python project',
    'long_description': '[![Tests](https://github.com/pekkaro/hmtest/workflows/Tests/badge.svg)](https://github.com/pekkaro/hmtest/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/pekkaro/hmtest/branch/master/graph/badge.svg)](https://codecov.io/gh/pekkaro/hmtest)\n\n# hmtest\nThis repository follows this tutorial https://cjolowicz.github.io/posts/hypermodern-python-01-setup/\n',
    'author': 'Pekka Röyttä',
    'author_email': 'roytta@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pekkaRo/hmtest',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
