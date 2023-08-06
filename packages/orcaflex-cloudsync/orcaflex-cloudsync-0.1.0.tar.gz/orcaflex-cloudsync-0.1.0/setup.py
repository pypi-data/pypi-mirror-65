# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ofxcloudsync', 'ofxcs']

package_data = \
{'': ['*']}

install_requires = \
['OrcFxAPI==11.0.2',
 'PyYAML==5.3.1',
 'appdirs>=1.4.3,<2.0.0',
 'awscli==1.18.31',
 'boto3==1.12.30',
 'click==7.1.1',
 'pytest-mock>=3.0.0,<4.0.0',
 'pytest==5.4.1']

entry_points = \
{'console_scripts': ['ofxcs = ofxcs:ofxcs']}

setup_kwargs = {
    'name': 'orcaflex-cloudsync',
    'version': '0.1.0',
    'description': 'Tool to sync OrcaFlex simulations to the cloud and local drives',
    'long_description': None,
    'author': 'AgileDat',
    'author_email': 'ofxcs@agiledat.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
