# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['coldtype',
 'coldtype.color',
 'coldtype.pens',
 'coldtype.renderer',
 'coldtype.text']

package_data = \
{'': ['*']}

install_requires = \
['booleanOperations>=0.9.0,<0.10.0',
 'fontPens>=0.2.4,<0.3.0',
 'fontTools>=4.7.0,<5.0.0',
 'freetype-py>=2.1.0,<3.0.0',
 'noise>=1.2.2,<2.0.0',
 'skia-pathops>=0.4.0,<0.5.0',
 'uharfbuzz>=0.9.1,<0.10.0',
 'unicodedata2>=13.0.0,<14.0.0',
 'watchdog>=0.10.2,<0.11.0',
 'websockets>=8.1,<9.0']

setup_kwargs = {
    'name': 'coldtype',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Rob Stenson',
    'author_email': 'rob@goodhertz.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.8',
}


setup(**setup_kwargs)
