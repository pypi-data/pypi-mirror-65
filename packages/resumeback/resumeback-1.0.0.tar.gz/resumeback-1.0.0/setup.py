# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['resumeback', 'tests']

package_data = \
{'': ['*']}

extras_require = \
{'docs': ['sphinx>=2.4.4,<3.0.0', 'sphinx-readable-theme>=1.3.0,<2.0.0'],
 'flake8': ['flake8>=3.7.9,<4.0.0'],
 'test': ['pytest>=5.4.1,<6.0.0', 'pytest-cov>=2.8.1,<3.0.0']}

setup_kwargs = {
    'name': 'resumeback',
    'version': '1.0.0',
    'description': 'Library for using callbacks to resume your code.',
    'long_description': '============\n resumeback\n============\n\n.. image:: https://github.com/FichteFoll/resumeback/workflows/CI/badge.svg\n   :target: https://github.com/FichteFoll/resumeback/actions?query=workflow%3ACI+branch%3Amaster\n\n.. image:: https://coveralls.io/repos/FichteFoll/resumeback/badge.svg\n   :target: https://coveralls.io/github/FichteFoll/resumeback?branch=master\n\n.. image:: https://img.shields.io/pypi/v/resumeback.svg\n    :target: https://pypi.python.org/pypi/resumeback\n\n.. image:: https://img.shields.io/pypi/pyversions/resumeback.svg\n    :target: https://pypi.python.org/pypi/resumeback/\n\n.. .. image:: https://img.shields.io/pypi/dd/resumeback.svg\n..     :target: https://pypi.python.org/pypi/resumeback/\n\nA Python library for using callbacks to resume your code.\n\n``resumeback`` provides a utility function decorator\nthat enables using callback-based interfaces\nin **a single line of execution**\n-- a single function.\n\nDocumentation\n=============\n\nhttps://fichtefoll.github.io/resumeback/\n\n\nInstallation\n============\n\n.. code-block:: shell\n\n    $ pip install resumeback\n\n\nExample Usage\n=============\n\n.. code-block:: python\n\n    from threading import Thread\n    from resumeback import send_self\n\n    def ask_for_user_input(question, on_done):\n        def watcher():\n            result = input(question)\n            on_done(result)\n\n        Thread(target=watcher).start()\n\n    @send_self\n    def main(this):  # "this" is a reference to the created generator instance\n        arbitrary_value = 10\n\n        # Yield pauses execution until one of the generator methods is called,\n        # such as `.send`, which we provide as the callback parameter.\n        number = yield ask_for_user_input("Please enter a number", this.send)\n        number = int(number)\n        print("Result:", number * arbitrary_value)\n\n    if __name__ == "__main__":\n        main()\n\n\nDevelopment\n===========\n\nRequires Python, poetry, and GNU Make.\n\nUse ``make help`` to show the available targets.\n\n- poetry__ is used for dependency and virtualenv management.\n- tox__ is used as a test runner for multiple isolated environments.\n- flake8__ is used for code linting.\n- `Github Actions`__ are used for CI.\n\n__ https://python-poetry.org/\n__ https://tox.readthedocs.io/\n__ https://flake8.readthedocs.io/\n__ https://github.com/features/actions\n\n\nAcknowledgements\n================\n\nProject started initially after a `forum post`__ from `@Varriount`__\non the Sublime Text forum.\nI just took his idea "to the next (abstraction) level"\nand made it more convenient to use.\n\n__ https://forum.sublimetext.com/t/using-generators-for-fun-and-profit-utility-for-developers/14618\n__ https://github.com/Varriount\n',
    'author': 'FichteFoll',
    'author_email': 'fichtefoll2@googlemail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://fichtefoll.github.io/resumeback/',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
