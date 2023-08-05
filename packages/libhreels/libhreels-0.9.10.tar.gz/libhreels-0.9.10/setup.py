# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libhreels']

package_data = \
{'': ['*']}

install_requires = \
['PyQt5==5.13',
 'argparse>=1.4.0,<2.0.0',
 'matplotlib>=3.2.1,<4.0.0',
 'requests>=2.23.0,<3.0.0',
 'scipy>=1.4.1,<2.0.0']

entry_points = \
{'console_scripts': ['calc = libhreels.calcHREELS:myMain',
                     'dielectrics = libhreels.dielectrics:myMain',
                     'run = libhreels.HREELS:myMain',
                     'view = libhreels.ViewHREELS:myMain',
                     'viewAuger = libhreels.ViewAuger:myMain']}

setup_kwargs = {
    'name': 'libhreels',
    'version': '0.9.10',
    'description': 'Handling, simulating, and plotting HREELS and Auger spectroscopy data',
    'long_description': None,
    'author': 'Wolf Widdra',
    'author_email': 'wolf.widdra@physik.uni-halle.de',
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
