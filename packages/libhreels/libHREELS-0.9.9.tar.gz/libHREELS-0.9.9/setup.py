# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libhreels']

package_data = \
{'': ['*'], 'libhreels': ['.vscode/*']}

install_requires = \
['PyQt5==5.13',
 'argparse>=1.4.0,<2.0.0',
 'matplotlib>=3.2.1,<4.0.0',
 'requests>=2.23.0,<3.0.0',
 'scipy>=1.4.1,<2.0.0']

entry_points = \
{'console_scripts': ['calc = libHREELS.calcHREELS:myMain',
                     'dielectrics = libHREELS.dielectrics:myMain',
                     'run = libHREELS.HREELS:myMain',
                     'view = libHREELS.ViewHREELS:myMain',
                     'viewAuger = libHREELS.ViewAuger:myMain']}

setup_kwargs = {
    'name': 'libhreels',
    'version': '0.9.9',
    'description': 'Handling, simulating, and plotting HREELS and Auger spectroscopy data',
    'long_description': None,
    'author': 'e3fm8',
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
