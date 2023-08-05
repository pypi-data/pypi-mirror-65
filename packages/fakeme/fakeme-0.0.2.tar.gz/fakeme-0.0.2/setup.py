# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fakeme', 'fakeme.cli']

package_data = \
{'': ['*'], 'fakeme': ['data/*']}

install_requires = \
['mimesis>=4.0,<5.0', 'pandas>=1.0,<2.0', 'ply>=3.11,<4.0']

entry_points = \
{'console_scripts': ['fakeme = fakeme.cli:cli']}

setup_kwargs = {
    'name': 'fakeme',
    'version': '0.0.2',
    'description': 'Relative Data Generator: generate tables with data, that depend each other',
    'long_description': 'Fakeme \n=======\n\nData Generator for Chained and Relative Data\n\n|badge1| |badge2| |badge3|\n\n.. |badge1| image:: https://img.shields.io/pypi/pyversions/fakeme \n.. |badge2| image:: https://img.shields.io/pypi/v/fakeme\n.. |badge3| image:: https://travis-ci.com/xnuinside/fakeme.svg?branch=master\n\nDocumentation in process: https://fakeme.readthedocs.io/en/latest/ \n\nUse under the hood at current time:\n\n     - Mimesis (like one of the generators for fields values)\n     - Pandas (like main instrument to combain data in tables (frames) \n     - Standart Python Library\n\n\nSupport Python 3.7\n\nWhat it does not do?\n=========================\n\nThis is not random value generated library - for this exist pretty cool lib Mimesis and another. \n\n\nWhat it does?\n=========================\n\n**Fakeme** oriented on generation data that depend on values in another tables/datasets.\nData, that knitted together as real. \n\n**Fakeme** can help you if you want to generate several tables, that must contains in columns values, \nthat you will use like key for join.\n\nFor example, *user_data* table has field *user_id* and *users* table contains list of users with column id. \nYou want join it on user_id = id.\n\n**Fakeme** will generate for you 2 tables with same values in those 2 columns. \n\nIt does not matter to have columns with same name you can define dependencies between tables with alias names. \n \n \nWhat you can to do\n=========================\n\n1. Define that fields in your datasets must contain similar values\n\n2. You can set up how much values must intersect, for example, you want to emulate data for email validation pipeline - \nyou have one dataset with *incoming* messages  and you need to find all emails that was not added previously in your *contacts* table.\n\nSo you will have incoming messages table, that contains, for example only 70% of emails that exist in contacts table. \n\n3. You can use multiply columns as a key (dependency) in another column, for example, \n*player_final_report* must contains for each player same values as in other tables, for example, you have *player* table\nwith players details and *in_game_player_activity* with all player activities for some test reasons it\'s critical\nto you generate *player_final_report* with 1-to-1 data from other 2 tables.\n \n4. Union tables. You can generate tables that contains all rows from another tables. \n\n5. You can define your own generator for fields on Python.\n\n6. You can define your own output format\n\n\nExamples\n=========================\n\n   You can find usage examples in \'fakeme/examples/\' folder.\n\n    Example from fakeme/examples/generate_data_related_to_existed_files:\n\n.. code-block:: python\n\n    from fakeme import Fakeme\n\n    # to use some existed data you should provide with_data argument -\n    # and put inside list with the paths to the file with data\n\n    # data file must be in same format as .json or csv output of fakeme.\n    # so it must be [{"column_name": value, "column_name2": value2 ..},\n    #   {"column_name" : value, "column_name2": value2 ..}..]\n    # Please check example in countries.json\n\n    cities_schema = [{"name": "name"},\n                     {"name": "country_id"},\n                     {"name": "id"}]\n\n    # all fields are strings - so I don\'t define type, because String will be used as default type for the column\n\n    tables_list = [(\'cities\', cities_schema)]\n\n    Fakeme(\n        tables=tables_list,\n        with_data=[\'countries.json\'],\n        rls={\'cities\': {  # this mean: for table \'cities\'\n            \'country_id\': {  # and column \'country_id\' in table \'cities\'\n                \'table\': \'countries.json\',   # please take data from data  in countries.json\n                \'alias\': \'id\',  # with alias name \'id\'\n                \'matches\': 1  # and I want all values in country_id must be from countries.id column, all.\n            }\n        }},\n        settings={\'row_numbers\': 1300}  # we want to have several cities for each country,\n                                        # so we need to have more rows,\n    ).run()\n\n    # run and you will see a list of cities, that generated with same ids as in countries.json\n\n\nDocs: https://fakeme.readthedocs.io/en/latest/',
    'author': 'xnuinside',
    'author_email': 'xnuinside@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/xnuinside/fakeme',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
