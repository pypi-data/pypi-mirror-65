# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymana']

package_data = \
{'': ['*']}

install_requires = \
['click-aliases>=1.0.1,<2.0.0',
 'click>=7.0,<8.0',
 'dask-image>=0.2.0,<0.3.0',
 'dask[array]>=2.11.0,<3.0.0',
 'napari>=0.2.12,<0.3.0',
 'numpy>=1.18.1,<2.0.0',
 'opencv-python-headless==4.2.0.34',
 'openslide-python>=1.1.1,<2.0.0',
 'scikit-image>=0.16.2,<0.17.0',
 'sympy>=1.5.1,<2.0.0']

entry_points = \
{'console_scripts': ['pymana = pymana.cli:cli']}

setup_kwargs = {
    'name': 'pymana',
    'version': '0.1.5',
    'description': '',
    'long_description': 'pymana\n==============\n\n:code:`pymana.separation.separated` does not work!\n',
    'author': 'Sumanth Ratna',
    'author_email': 'sumanthratna@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sumanthratna/pymana',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
