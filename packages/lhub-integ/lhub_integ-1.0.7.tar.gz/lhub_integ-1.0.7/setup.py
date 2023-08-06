# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lhub_integ', 'lhub_integ.common']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2',
 'PySocks==1.7.1',
 'PyYAML==5.3.1',
 'beautifulsoup4==4.8.2',
 'click>=7.0,<7.1',
 'dataclasses-json',
 'docstring-parser>=0.1,<0.2',
 'netaddr==0.7.19',
 'python-dateutil==2.8.1',
 'python-magic==0.4.15',
 'urllib3==1.25.8',
 'wheel>=0.32.3,<0.33.0']

entry_points = \
{'console_scripts': ['bundle-requirements = '
                     'lhub_integ.bundle_requirements:main']}

setup_kwargs = {
    'name': 'lhub-integ',
    'version': '1.0.7',
    'description': 'The Logichub Integration SDK',
    'long_description': "# lhub_integ\nPython package to shim basic scripts to work with integration machinery.\nThis package requires Python 3.6:\n```\n# Optional: install Python 3.6 with pyenvv\nbrew install pyenv\npyenv install 3.6.6\npyenv init # Follow the instructions\npyenv local 3.6.6\npython --version\n```\n\n```\npip install lhub_integ\n```\n\n## Usage (as an integration writer)\nTo write a Python script that is convertible into an integration:\n\n1. Create a directory that will contain your integration\n2. Install lhub_integ as a local package:\n```pip install lhub_integ```\n\nPython scripts must provide an entrypoint function with some number of arguments. These arguments will correspond to columns\nin the input data. The function should return a Python dictionary that can be serialized to JSON\n\n```python\ndef process(url, num_bytes: int):\n  return {'output': url + 'hello'}\n```\n\n### Specifying Dependencies\nYou must create a `requirements.txt` file specifying your dependencies. To create a dependency bundle run:\n```\n$ bundle-requirements\n```\nThis script is provided when you install lhub_integ.\n\n### Publishing\nYou will need the PyPi username and password that are in 1Password (search for PyPi)\n\n1. Bump the version in pyproject.toml\n\n2. `poetry publish --build`\n",
    'author': 'Russell Cohen',
    'author_email': 'russell@logichub.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://logichub.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
