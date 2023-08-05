# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['sort_images_exif']
install_requires = \
['exif']

setup_kwargs = {
    'name': 'sort-images-exif',
    'version': '0.1',
    'description': 'Sort images',
    'long_description': 'Sort images with python according to exif and time in path name\n\n\nJust a small script. Documentation: see --help\n',
    'author': 'Alexander K.',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/devkral/sort-images-exif',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
