# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['screenplay_pdf_to_json',
 'screenplay_pdf_to_json.parse_pdf',
 'screenplay_pdf_to_json.utils']

package_data = \
{'': ['*']}

install_requires = \
['pdfminer.six>=20200124,<20200125']

setup_kwargs = {
    'name': 'screenplay-pdf-to-json',
    'version': '0.2.8',
    'description': '',
    'long_description': None,
    'author': 'VVNoodle',
    'author_email': 'brickkace@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
