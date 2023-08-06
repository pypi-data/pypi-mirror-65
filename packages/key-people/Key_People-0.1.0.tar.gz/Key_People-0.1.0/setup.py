# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['key_people']

package_data = \
{'': ['*'], 'key_people': ['DB/*']}

setup_kwargs = {
    'name': 'key-people',
    'version': '0.1.0',
    'description': 'This is used to pull any of the key people from a company based off of the ticker. Currently NASDAQ and NYSE supported',
    'long_description': 'This package is used to pull key people from a company based on the ticker.\n\n\nfrom Key_People import get_Key_People, Key_People, get_c_Name\nlist_of_key_people = get_Key_People("AAPL")\ncompany_Name = get_c_Name("AAPL")\n\n#if you are doing multiple entries and want to make it quicker\ndb = Key_People()\n\nentry = db.entry("AAPL")\n\nentry.company_Name\nentry.key_People\nentry.ticker\n',
    'author': 'Henry Becket Trotter',
    'author_email': 'beckettrotter@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/BecketTrotter/Key_People',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.7,<3.0',
}


setup(**setup_kwargs)
