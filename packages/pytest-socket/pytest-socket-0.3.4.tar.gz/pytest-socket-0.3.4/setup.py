# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pytest_socket']
install_requires = \
['pytest>=3.6.3']

entry_points = \
{'pytest11': ['socket = pytest_socket']}

setup_kwargs = {
    'name': 'pytest-socket',
    'version': '0.3.4',
    'description': 'Pytest Plugin to disable socket calls during tests',
    'long_description': '=============\npytest-socket\n=============\n\n.. image:: https://img.shields.io/pypi/v/pytest-socket.svg\n    :target: https://pypi.python.org/pypi/pytest-socket\n\n.. image:: https://img.shields.io/pypi/pyversions/pytest-socket.svg\n    :target: https://pypi.python.org/pypi/pytest-socket\n\n.. image:: https://github.com/miketheman/pytest-socket/workflows/Python%20Tests/badge.svg\n    :target: https://github.com/miketheman/pytest-socket/actions?query=workflow%3A%22Python+Tests%22\n    :alt: Python Tests\n\n.. image:: https://api.codeclimate.com/v1/badges/1608a75b1c3a20211992/maintainability\n   :target: https://codeclimate.com/github/miketheman/pytest-socket/maintainability\n   :alt: Maintainability\n\n.. image:: https://app.fossa.io/api/projects/git%2Bgithub.com%2Fmiketheman%2Fpytest-socket.svg?type=shield\n   :target: https://app.fossa.io/projects/git%2Bgithub.com%2Fmiketheman%2Fpytest-socket?ref=badge_shield\n   :alt: FOSSA Status\n\n\nA plugin to use with Pytest to disable or restrict ``socket`` calls during tests to ensure network calls are prevented.\n\n----\n\nThis `Pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_\'s `Cookiecutter-pytest-plugin`_ template.\n\n\nFeatures\n--------\n\n* Disables all network calls flowing through Python\'s ``socket`` interface.\n\n\nRequirements\n------------\n\n* `Pytest`_ 3.6.3 or greater\n\n\nInstallation\n------------\n\nYou can install "pytest-socket" via `pip`_ from `PyPI`_::\n\n    $ pip install pytest-socket\n\n\nUsage\n-----\n\n* Run ``pytest --disable-socket``, tests should fail on any access to ``socket`` or libraries using\n  socket with a ``SocketBlockedError``.\n\n  To add this flag as the default behavior, add this section to your ``pytest.ini`` or ``setup.cfg``:\n\n  .. code:: ini\n\n    [pytest]\n    addopts = --disable-socket\n\n\n  or update your ``conftest.py`` to include:\n\n  .. code:: python\n\n    from pytest_socket import disable_socket\n\n    def pytest_runtest_setup():\n        disable_socket()\n\n\n* To enable specific tests use of ``socket``, pass in the fixture to the test or use a marker:\n\n  .. code:: python\n\n    def test_explicitly_enable_socket(socket_enabled):\n        assert socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n\n\n    @pytest.mark.enable_socket\n    def test_explicitly_enable_socket_with_mark():\n        assert socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n\n* To allow only specific hosts per-test:\n\n  .. code:: python\n\n    @pytest.mark.allow_hosts([\'127.0.0.1\'])\n    def test_explicitly_enable_socket_with_mark():\n        assert socket.socket.connect((\'127.0.0.1\', 80))\n\nor for whole test run\n\n  .. code:: ini\n\n    [pytest]\n    addopts = --allow-hosts=127.0.0.1,127.0.1.1\n\n\nContributing\n------------\nContributions are very welcome. Tests can be run with `pytest`_, please ensure\nthe coverage at least stays the same before you submit a pull request.\n\nLicense\n-------\n\nDistributed under the terms of the `MIT`_ license, "pytest-socket" is free and open source software\n\n.. image:: https://app.fossa.io/api/projects/git%2Bgithub.com%2Fmiketheman%2Fpytest-socket.svg?type=large\n   :target: https://app.fossa.io/projects/git%2Bgithub.com%2Fmiketheman%2Fpytest-socket?ref=badge_large\n   :alt: FOSSA Status\n\nIssues\n------\n\nIf you encounter any problems, please `file an issue`_ along with a detailed description.\n\n\nReferences\n----------\n\nThis plugin came about due to the efforts by `@hangtwenty`_ solving a `StackOverflow question`_,\nthen converted into a pytest plugin by `@miketheman`_.\n\n\n.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter\n.. _`@hackebrot`: https://github.com/hackebrot\n.. _`MIT`: http://opensource.org/licenses/MIT\n.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin\n.. _`file an issue`: https://github.com/miketheman/pytest-socket/issues\n.. _`pytest`: https://github.com/pytest-dev/pytest\n.. _`tox`: https://tox.readthedocs.io/en/latest/\n.. _`pip`: https://pypi.python.org/pypi/pip/\n.. _`PyPI`: https://pypi.python.org/pypi\n.. _`@hangtwenty`: https://github.com/hangtwenty\n.. _`StackOverflow question`: https://stackoverflow.com/a/30064664\n.. _`@miketheman`: https://github.com/miketheman\n',
    'author': 'Mike Fiedler',
    'author_email': 'miketheman@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/pytest-socket/',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
