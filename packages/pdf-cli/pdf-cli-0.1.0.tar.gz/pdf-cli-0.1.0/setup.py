# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pdf_cli', 'pdf_cli.commands']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0', 'pyPdf4>=1.27.0,<2.0.0', 'pytest-coverage>=0.0,<0.1']

entry_points = \
{'console_scripts': ['pdfcli = pdf_cli.main:main']}

setup_kwargs = {
    'name': 'pdf-cli',
    'version': '0.1.0',
    'description': 'command line pdf tools',
    'long_description': '# pdfcli\n\npdfcli is a command line utility to work with pdf.\n\nIt is able to split,join,reorder,extract pdf.\n\n    $ pdfcli --help\n    Usage: pdfcli [OPTIONS] COMMAND [ARGS]...\n    \n    Options:\n      --help  Show this message and exit.\n    \n    Commands:\n      extract  extract one or multiple pages and build a new document.\n      join     join multiple pdf together in a single file\n      split    split pdf into single page file\n',
    'author': 'Stefano Apostolico',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>3.6',
}


setup(**setup_kwargs)
