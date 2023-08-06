# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['min_renovasjon']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'min-renovasjon',
    'version': '0.1.2',
    'description': 'A Python3 API for Min Renovasjon',
    'long_description': '### IN\xa0DEVELOPMENT\n\n# Min Renovasjon Python API\nPython 3 API for [Min Renovasjon][https://www.norkart.no/product/min-renovasjon/].\n\n# Example\n```python\nfrom min_renovasjon import MinRenovasjon\n\nsearch_string = "Jonas Lies gate 22, 200 Lillestrøm"\nren = MinRenovasjon(search_string)\n```\nNorwegian street names often contains the word veg/vei (it means road in English).\nThis package handles this automatically, so a lookup for \n`Hageveien` or `Hagevegen` should give the same result.\n\n```python\n# Fractions\nren.fractions()\n\n# Next waste collections\nren.waste_collections()\n```\n\n###\n\n[https://www.norkart.no/product/min-renovasjon/]: https://www.norkart.no/product/min-renovasjon/',
    'author': 'Knut Flage Henriksen',
    'author_email': 'post@flaksen.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/knutfh/min_renovasjon_py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
