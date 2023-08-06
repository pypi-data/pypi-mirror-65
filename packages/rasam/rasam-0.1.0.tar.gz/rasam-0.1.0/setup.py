# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rasam', 'rasam.components']

package_data = \
{'': ['*']}

install_requires = \
['rasa>=1.9.5,<2.0.0', 'urlextract>=0.14.0,<0.15.0']

setup_kwargs = {
    'name': 'rasam',
    'version': '0.1.0',
    'description': 'Rasa Improvements',
    'long_description': '# rasam\nRasa Improvements\n\n## Usage\n\n### Installation\n\n```shell script\npip install rasam\n```\n\n### Rasa `config.yml`\n\n```yaml\npipeline:\n  - name: rasam.RegexEntityExtractor\n  - name: rasam.URLEntityExtractor\n```\n\n## Author\n[Ronie Martinez](ronmarti18@gmail.com)\n',
    'author': 'Ronie Martinez',
    'author_email': 'ronmarti18@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.8',
}


setup(**setup_kwargs)
