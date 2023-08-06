# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsonpath']

package_data = \
{'': ['*']}

install_requires = \
['lark-parser>=0.8.5,<0.9.0', 'typing_extensions>=3.7,<4.0']

extras_require = \
{'docs': ['sphinx>=2.3.1,<3.0.0', 'livereload>=2.6.1,<3.0.0'],
 'lint': ['black>=19.3b0,<20.0',
          'flake8>=3.7.8,<4.0.0',
          'isort>=4.3.21,<5.0.0',
          'mypy>=0.750,<0.751',
          'pytest>=5.2.0,<6.0.0',
          'flake8-bugbear>=19.8,<20.0',
          'blacken-docs>=1.5.0,<2.0.0',
          'doc8>=0.8.0,<0.9.0',
          'pygments>=2.5.2,<3.0.0',
          'livereload>=2.6.1,<3.0.0',
          'pexpect>=4.8.0,<5.0.0'],
 'test': ['pytest>=5.2.0,<6.0.0',
          'pytest-cov>=2.7.1,<3.0.0',
          'pexpect>=4.8.0,<5.0.0']}

entry_points = \
{'console_scripts': ['jp = jsonpath.cli:main']}

setup_kwargs = {
    'name': 'jsonpath-extractor',
    'version': '0.4.0',
    'description': 'A selector expression for extracting data from JSON.',
    'long_description': '========\nJSONPATH\n========\n\n|license| |Pypi Status| |Python version| |Package version| |PyPI - Downloads|\n|GitHub last commit| |Code style: black| |Build Status| |codecov|\n\nA selector expression for extracting data from JSON.\n\nQuickstarts\n<<<<<<<<<<<\n\n\nInstallation\n~~~~~~~~~~~~\n\nInstall the stable version from PYPI.\n\n.. code-block:: shell\n\n    pip install jsonpath-extractor\n\nOr install the latest version from Github.\n\n.. code-block:: shell\n\n    pip install git+https://github.com/linw1995/jsonpath.git@master\n\nUsage\n~~~~~\n\n.. code-block:: json\n\n    {\n        "goods": [\n            {"price": 100, "category": "Comic book"},\n            {"price": 200, "category": "magazine"},\n            {"price": 200, "no category": ""}\n        ],\n        "targetCategory": "book"\n    }\n\n\nHow to parse and extract all the comic book data from the above JSON file.\n\n.. code-block:: python3\n\n    import json\n\n    from jsonpath import parse\n\n    with open("example.json", "r") as f:\n        data = json.load(f)\n\n    assert parse("$.goods[contains(@.category, $.targetCategory)]").find(\n        data\n    ) == [{"price": 100, "category": "Comic book"}]\n\nOr use the `jsonpath.core <https://jsonpath.readthedocs.io/en/latest/api_core.html>`_ module to extract it.\n\n.. code-block:: python3\n\n    from jsonpath.core import Root, Contains, Self\n\n    assert Root().Name("goods").Predicate(\n        Contains(Self().Name("category"), Root().Name("targetCategory"))\n    ).find(data) == [{"price": 100, "category": "Comic book"}]\n\n\nUsage via CLI\n~~~~~~~~~~~~~\n\nThe faster way to extract by using CLI.\n\n.. code-block:: shell\n\n    jp -f example.json "$.goods[contains(@.category, $.targetCategory)]"\n\nOr pass content by pipeline.\n\n.. code-block:: shell\n\n    cat example.json | jp "$.goods[contains(@.category, $.targetCategory)]"\n\nThe output of the above commands.\n\n.. code-block:: json\n\n    [\n      {\n        "price": 100,\n        "category": "Comic book"\n      }\n    ]\n\nChangelog\n<<<<<<<<<\n\nv0.4.0\n~~~~~~\n\n- 9f8f039 New:Add Command-line interface support\n\n\n.. |license| image:: https://img.shields.io/github/license/linw1995/jsonpath.svg\n    :target: https://github.com/linw1995/jsonpath/blob/master/LICENSE\n\n.. |Pypi Status| image:: https://img.shields.io/pypi/status/jsonpath-extractor.svg\n    :target: https://pypi.org/project/jsonpath-extractor\n\n.. |Python version| image:: https://img.shields.io/pypi/pyversions/jsonpath-extractor.svg\n    :target: https://pypi.org/project/jsonpath-extractor\n\n.. |Package version| image:: https://img.shields.io/pypi/v/jsonpath-extractor.svg\n    :target: https://pypi.org/project/jsonpath-extractor\n\n.. |PyPI - Downloads| image:: https://img.shields.io/pypi/dm/jsonpath-extractor.svg\n    :target: https://pypi.org/project/jsonpath-extractor\n\n.. |GitHub last commit| image:: https://img.shields.io/github/last-commit/linw1995/jsonpath.svg\n    :target: https://github.com/linw1995/jsonpath\n\n.. |Code style: black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/ambv/black\n\n.. |Build Status| image:: https://img.shields.io/github/workflow/status/linw1995/jsonpath/Python%20package\n    :target: https://github.com/linw1995/jsonpath/actions?query=workflow%3A%22Python+package%22\n\n.. |codecov| image:: https://codecov.io/gh/linw1995/jsonpath/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/linw1995/jsonpath\n',
    'author': '林玮',
    'author_email': 'linw1995@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/linw1995/jsonpath',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
