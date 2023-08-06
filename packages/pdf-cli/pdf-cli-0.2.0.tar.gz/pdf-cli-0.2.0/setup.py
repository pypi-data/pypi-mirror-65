# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pdf_cli', 'pdf_cli.commands']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0', 'pyPdf4>=1.27.0,<2.0.0']

entry_points = \
{'console_scripts': ['pdfcli = pdf_cli.main:main']}

setup_kwargs = {
    'name': 'pdf-cli',
    'version': '0.2.0',
    'description': 'command line pdf tools',
    'long_description': '# pdfcli\n\npdfcli is a command line utility to work with pdf.\n\nIt is able to split,join,reorder,extract pdf.\n\n    $ pdfcli --help\n    Usage: pdfcli [OPTIONS] COMMAND [ARGS]...\n    \n    Options:\n      --help  Show this message and exit.\n    \n    Commands:\n      decrypt    decrypt pdf\n      encrypt    encrypt pdf\n      extract    extract one or multiple pages and build a new document.\n      info       dump pdf informations.\n      join       join multiple pdf together in a single file\n      rotate     rotate selected pages Rotate selected pages and outputs in new...\n      split      split pdf into single page file\n      watermark  use first page of pdf and add it as watermark to other\n                 document...\n### Examples\n\nExtract pages 1, and from 5 to 9 one file for page\n\n    pdfcli split source.pdf -p 1,5-9\n    \nCreate a new pdf using pages 1, and from 5 to 9 \n\n    pdfcli extract source.pdf  -p 1,5-9 -o new.pdf\n\n',
    'author': 'Stefano Apostolico',
    'author_email': 's.apostolico@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/saxix/pdfcli.git',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>3.6',
}


setup(**setup_kwargs)
