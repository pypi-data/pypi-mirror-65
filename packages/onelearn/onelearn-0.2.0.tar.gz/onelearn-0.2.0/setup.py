# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['onelearn', 'onelearn.datasets', 'onelearn.playground']

package_data = \
{'': ['*'], 'onelearn.datasets': ['data/*']}

install_requires = \
['bokeh>=1.3.4,<2.0.0',
 'colorcet>=2.0.2,<3.0.0',
 'matplotlib>=3.1,<4.0',
 'numba>=0.48,<0.49',
 'numpy>=1.17.4,<2.0.0',
 'scikit-learn>=0.22,<0.23',
 'scipy>=1.3.2,<2.0.0',
 'seaborn>=0.9,<0.10',
 'streamlit>=0.49.0,<0.50.0',
 'tqdm>=4.36,<5.0']

setup_kwargs = {
    'name': 'onelearn',
    'version': '0.2.0',
    'description': 'onelearn is a small python package for online learning',
    'long_description': '\n[![Build Status](https://travis-ci.com/onelearn/onelearn.svg?branch=master)](https://travis-ci.com/onelearn/onelearn)\n[![Documentation Status](https://readthedocs.org/projects/onelearn/badge/?version=latest)](https://onelearn.readthedocs.io/en/latest/?badge=latest)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/onelearn)\n![PyPI - Wheel](https://img.shields.io/pypi/wheel/onelearn)\n[![GitHub stars](https://img.shields.io/github/stars/onelearn/onelearn)](https://github.com/onelearn/onelearn/stargazers)\n[![GitHub issues](https://img.shields.io/github/issues/onelearn/onelearn)](https://github.com/onelearn/onelearn/issues)\n[![GitHub license](https://img.shields.io/github/license/onelearn/onelearn)](https://github.com/onelearn/onelearn/blob/master/LICENSE)\n[![Coverage Status](https://coveralls.io/repos/github/onelearn/onelearn/badge.svg?branch=master)](https://coveralls.io/github/onelearn/onelearn?branch=master)\n\n# onelearn: Online learning in Python\n\n[Documentation](https://onelearn.readthedocs.io) | [Reproduce experiments](https://onelearn.readthedocs.io/en/latest/experiments.html) |\n\nonelearn stands for ONE-shot LEARNning. It is a small python package for **online learning** \nwith Python. It provides :\n\n- **online** (or **one-shot**) learning algorithms: each sample is processed **once**, only a \n  single pass is performed on the data\n- including **multi-class classification** and regression algorithms\n- For now, only *ensemble* methods, namely **Random Forests**\n\n## Installation\n\nThe easiest way to install onelearn is using pip\n\n    pip install onelearn\n\n\nBut you can also use the latest development from github directly with\n\n    pip install git+https://github.com/onelearn/onelearn.git\n\n## References\n\n    @article{mourtada2019amf,\n      title={AMF: Aggregated Mondrian Forests for Online Learning},\n      author={Mourtada, Jaouad and Ga{\\"\\i}ffas, St{\\\'e}phane and Scornet, Erwan},\n      journal={arXiv preprint arXiv:1906.10529},\n      year={2019}\n    }\n ',
    'author': 'Stéphane Gaïffas',
    'author_email': 'stephane.gaiffas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://onelearn.readthedocs.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
