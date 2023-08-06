# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['srtm']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'python-srtm',
    'version': '0.1.0',
    'description': '',
    'long_description': '# NASA SRTM altitude data parsing in Python\n\nProvides an API onto SRTM `.hgt` or `.hgt.zip` files.\n\nRequires Python 3.8, **may** work with Python 3.6 & 3.7.\n\n## Installation\n\n```\npip install python-srtm\n\nexport SRTM1_DIR=/path/to/srtm1/\nexport SRTM3_DIR=/path/to/srtm3/\n```\n\n## Use\n\nYou can access either SRTM1 or SRTM3 data. SRTM 1, for example:\n\n```python\n# SRTM1\npython\n\n>>> from srtm import Srtm1HeightMapCollection\n>>> srtm1_data = Srtm1HeightMapCollection()\n>>> srtm1_data.get_altitude(latitude=40.123, longitude=-7.456)\n615\n>>> Srtm1HeightMapCollection().get_elevation_profile(40.123, -7.456, 40.129, -7.460)\n[615, 620, 618, 620, 616, 603, 593, 582, 575, 579, 580, 589, 589, 581, 565, 553, 545, 541, 534, 533, 529, 520, 514]\n```\n\nOr SRTM3:\n\n```python\n# SRTM3\npython\n\n>>> from srtm import Srtm3HeightMapCollection\n>>> srtm3_data = Srtm3HeightMapCollection()\n>>> srtm3_data.get_altitude(latitude=40.123, longitude=-7.456)\n608\n>>> Srtm3HeightMapCollection().get_elevation_profile(40.123, -7.456, 40.129, -7.460)\n[626, 616, 585, 593, 577, 548, 528, 514]\n```\n\n## Release process\n\n```\n# Run the tests\npytest\n\n# Update the setup.py\ndephell convert\nblack setup.py\n\n# Ensure poetry.lock is up to date\npoetry lock\n\nexport VERSION="VERSION HERE"\n\n# Version bump\npoetry version $VERSION\n\n\n# Commit\ngit add .\ngit commit -m "Releasing version $VERSION"\n\n# Tagging and branching\ngit tag "v$VERSION"\ngit branch "v$VERSION"\ngit push origin \\\n    refs/tags/"v$VERSION" \\\n    refs/heads/"v$VERSION" \\\n    master\n\npoetry publish --build\n```\n',
    'author': 'Adam Charnock',
    'author_email': 'adam@adamcharnock.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/adamcharnock/python-srtm',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
