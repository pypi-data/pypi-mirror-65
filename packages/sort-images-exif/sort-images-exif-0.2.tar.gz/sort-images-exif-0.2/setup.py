# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['sort_images_exif']
install_requires = \
['exif']

entry_points = \
{'console_scripts': ['sort_images_exif = sort_images_exif:main']}

setup_kwargs = {
    'name': 'sort-images-exif',
    'version': '0.2',
    'description': 'Sort images',
    'long_description': '\n# What can it do\n\nSort images with python according to datetime in exif and in pathname.\nIt automatically removes 100% duplicates and fixes missing exif dates.\n\nAdditionally features are:\n* pruning of non-images\n* configurable patterns for renaming\n* collision detection of images and configurable handling\n\n# how to install\n\nInstall with\n```` sh\npip install sort-images-exif\n\n````\n\n# Usage\n\n```` sh\nsort_images_exif <dir>\n\n````\n\nFor more documtentation see:\n --help\n',
    'author': 'Alexander K.',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/devkral/sort-images-exif',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
