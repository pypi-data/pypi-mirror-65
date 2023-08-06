# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['csvy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'csvy',
    'version': '0.1.5',
    'description': 'Convenience wrappers for the standard library csv module.',
    'long_description': 'csvy\n----\n\nBasic context wrappers for stardard library csv.read and csv.write methods.\n\n##### Writer Example\nB\n\nThe writer returns a straight up csv.writer object:\n\n    import csvy\n\n    with csvy.writer(\'csvpath.csv\') as csvfile:\n        csvfile.writerow([1, 2, 3, 4])\n\n\n##### Reader Example\n\nThe reader returns a proxy object that behaves a bit differently. You must\ncall the `iter` method that yield an enumerator:\n\n    import csvy\n\n    with csvy.reader(\'csvpath.csv\') as csvfile:\n        for index, row in csvfile.iter():\n            print(f"{index}: {row}")\n\n\nIf a header row is detected, the row object will be a `namedtuple` based\non the values of the header line:\n\n    """\n    src.csv:\n\n    A,B,C,column D\n    1,2,3,4\n    5,6,7,8\n\n    """\n    import csvy\n\n    with csvy.reader(\'src.csv\') as csvfile:\n        for index, row in csvfile.iter():\n            print(row.a)\n            print(row.column_d)\n\n\n',
    'author': 'Mark Gemmill',
    'author_email': 'gitlab@markgemmill.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/mgemmill-pypi/csvy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
