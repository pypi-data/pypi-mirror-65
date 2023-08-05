# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neural_semigroups']

package_data = \
{'': ['*']}

install_requires = \
['numpy==1.18.1',
 'pandas==1.0.2',
 'pytorch-ignite==0.3.0',
 'tensorboard==2.1.1',
 'torch==1.4.0',
 'tqdm==4.43.0']

setup_kwargs = {
    'name': 'neural-semigroups',
    'version': '0.2.3',
    'description': 'Neural networks powered research of semigroups',
    'long_description': "# Neural Semigroups\n\nHere we try to model Cayley tables of semigroups using neural networks.\n\nMore documentation can be found \n[here](https://neural-semigroups.readthedocs.io).\n\n## Motivation\n\nThis work was inspired by [a sudoku\nsolver](https://github.com/Kyubyong/sudoku). A solved Sudoku puzzle\nis nothing more than a Cayley table of a quasigroup from 9 items with\nsome well-known additional properties. So, one can imagine a puzzle\nmade from a Cayley table of any other magma, e. g. a semigroup, by\nhiding part of its cells.\n\nThere are two major differences between sudoku and puzzles based on\nsemigroups:\n\n1) it's easy to take a glance on a table to understand whether it is\na sudoku or not. That's why it was possible to encode numbers in a\ntable cells as colour intensities. Sudoku is a picture, and a\nsemigroup is not. It's difficult to check a Cayley table's\nassociativity with a naked eye;\n\n2) sudoku puzzles are solved by humans for fun and thus catalogued.\nWhen solving a sudoku one knows for sure that there is a unique\nsolution. On the contrary, nobody guesses values in a partially\nfilled Cayley table of a semigroup as a form of amuzement. As a\nresult, one can create a puzzle from a full Cayley table of a\nsemigroup but there may be many distinct solutions.\n",
    'author': 'Boris Shminke',
    'author_email': 'boris@shminke.ml',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/inpefess/neural-semigroups',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
