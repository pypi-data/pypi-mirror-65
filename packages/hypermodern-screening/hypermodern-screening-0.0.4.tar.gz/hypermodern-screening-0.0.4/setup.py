# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hypermodern_screening']

package_data = \
{'': ['*']}

install_requires = \
['chaospy>=3.2.7,<4.0.0']

setup_kwargs = {
    'name': 'hypermodern-screening',
    'version': '0.0.4',
    'description': 'The hypermodern screening project',
    'long_description': '.. image:: https://badge.fury.io/py/hypermodern-screening.svg\n  :target: https://pypi.org/project/hypermodern-screening\n\n.. image:: https://github.com/tostenzel/hypermodern-screening/workflows/Continuous%20Integration/badge.svg?branch=master\n  :target: https://github.com/tostenzel/hypermodern-screening/actions\n\n.. image:: https://codecov.io/gh/tostenzel/hypermodern-screening/branch/master/graph/badge.svg\n  :target: https://codecov.io/gh/tostenzel/hypermodern-screening\n\n.. image:: https://readthedocs.org/projects/hypermodern-screening/badge/?version=latest\n   :target: https://hypermodern-screening.readthedocs.io/en/latest/?badge=latest\n\n\n|\n\nThe ``hypermodern-screening`` package provides tools for efficient global sensitivity analyses based on elementary effects. Its unique feature is the option to compute these effects for models with correlated input parameters. The underlying conceptual approach is developed by Stenzel (2020). The fundamental idea comes from Ge and Menendez (2017). It is the combination of inverse transform sampling with an intelligent juggling of parameter positions in the input vector to create different dependency hierarchies. The package does also include a variety of sampling methods.\n\nThe name ``hypermodern-screening`` is inspired by the brilliant series of `blog <https://cjolowicz.github.io/posts/>`_ articles about cutting-edge tools for python development by Claudio Jolowicz in 2020. He calls his guide "Hypermodern Python"`*`. Its corner stones are ``poetry`` for packaging and dependency management and ``nox`` for automated testing. Another recommendation is rigorous typing. The repository framework widely follows the blog series.\n\nRead the documentation `here <https://hypermodern-screening.readthedocs.io>`_ and install ``hypermodern-screening`` from PyPI with\n\n.. code-block:: bash\n\n    $ pip install hypermodern_screening\n\n\n.. image:: docs/.static/albert_robida_1883.jpg\n   :width: 40pt\n\n`**`\n\nReferences\n~~~~~~~~~~\n\n    Stenzel, T. (2020): `Uncertainty Quantification for an Eckstein-Keane-Wolpin model with\n    correlated input parameters <https://github.com/tostenzel/thesis-projects-tostenzel/blob/master/latex/main.pdf>`_.\n    *Master\'s thesis, University of Bonn*.\n\n    Ge, Q. and Menendez, M. (2017). `Extending Morris method for qualitative global sensitivity\n    analysis of models with dependent inputs <https://doi.org/10.1016/j.ress.2017.01.010>`_. *Reliability Engineering & System Safety 100(162)*,\n    28-39.\n\n|\n\n-----\n\n`*`: Claudio, in turn, was inspired by the chess book "Die hypermoderne Schachpartie" (1925) by Savielly Tartakower.\n\n`**`: The image is a detail from the photogravure *Paris by night* by Albert Robida, 1883 (via `Old Book Illustrations <https://www.oldbookillustrations.com/illustrations/paris-night>`_).\n',
    'author': 'tostenzel',
    'author_email': 'tobias.stenzel@mailbox.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tostenzel/hypermodern-screening',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
