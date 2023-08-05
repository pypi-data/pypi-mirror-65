# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiohttp_tus']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0']

setup_kwargs = {
    'name': 'aiohttp-tus',
    'version': '1.0.0rc1',
    'description': 'tus.io protocol implementation for aiohttp.web applications',
    'long_description': '===========\naiohttp-tus\n===========\n\n.. image:: https://github.com/pylotcode/aiohttp-tus/workflows/ci/badge.svg\n    :target: https://github.com/pylotcode/aiohttp-tus/actions?query=workflow%3A%22ci%22\n    :alt: CI Workflow\n\n.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n    :target: https://github.com/pre-commit/pre-commit\n    :alt: pre-commit\n\n.. image:: https://img.shields.io/pypi/v/aiohttp-tus.svg\n    :target: https://pypi.org/project/aiohttp-tus/\n    :alt: Latest Version\n\n.. image:: https://img.shields.io/pypi/pyversions/aiohttp-tus.svg\n    :target: https://pypi.org/project/aiohttp-tus/\n    :alt: Python versions\n\n.. image:: https://img.shields.io/pypi/l/aiohttp-tus.svg\n    :target: https://github.com/pylotcode/aiohttp-tus/blob/master/LICENSE\n    :alt: BSD License\n\n.. image:: https://readthedocs.org/projects/aiohttp-tus/badge/?version=latest\n    :target: http://aiohttp-tus.readthedocs.org/en/latest/\n    :alt: Documentation\n\n`tus.io <https://tus.io>`_ server implementation for\n`aiohttp.web <https://docs.aiohttp.org/en/stable/web.html>`_ applications.\n\nFor uploading large files, please consider using\n`aiotus <https://pypi.org/project/aiotus/>`_ (Python 3.7+) library instead.\n\n- Works on Python 3.6+\n- Works with aiohttp 3.5+\n- BSD licensed\n- Latest documentation `on Read The Docs\n  <https://aiohttp-tus.readthedocs.io/>`_\n- Source, issues, and pull requests `on GitHub\n  <https://github.com/pylotcode/aiohttp-tus>`_\n\nQuickstart\n==========\n\nCode belows shows how to enable tus-compatible uploads on ``/uploads`` URL for\n``aiohttp.web`` application. After upload, files will be available at ``../uploads``\ndirectory.\n\n.. code-block:: python\n\n    from pathlib import Path\n\n    from aiohttp import web\n    from aiohttp_tus import setup_tus\n\n\n    app = setup_tus(\n        web.Application(),\n        upload_url="/uploads",\n        upload_path=Path(__file__).parent.parent / "uploads",\n    )\n\nChunk Size\n==========\n\nPlease, make sure to configure ``client_max_size`` for ``aiohttp.web`` Application and\nsupply proper ``chunkSize`` for Uppy.io or other tus.io client.\n\n`Documentation <https://aiohttp-tus.readthedocs.io/en/latest/usage.html#understanding-tus-io-chunk-size>`_\n\nExamples\n========\n\n`examples/ <https://github.com/pylotcode/aiohttp-tus/tree/master/examples>`_ directory\ncontains several examples, which illustrate how to use ``aiohttp-tus`` with some tus.io\nclients, such as `tus.py <https://pypi.org/project/tus.py/>`_ and\n`Uppy.io <https://uppy.io>`_.\n',
    'author': 'Igor Davydenko',
    'author_email': 'iam@igordavydenko.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pylotcode/aiohttp-tus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
