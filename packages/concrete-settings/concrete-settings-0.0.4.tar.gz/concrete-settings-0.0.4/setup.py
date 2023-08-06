# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['concrete_settings',
 'concrete_settings.contrib',
 'concrete_settings.contrib.behaviors',
 'concrete_settings.contrib.frameworks',
 'concrete_settings.contrib.sources',
 'concrete_settings.contrib.validators',
 'concrete_settings.sources',
 'concrete_settings.validators']

package_data = \
{'': ['*']}

install_requires = \
['sphinx>=2.3,<3.0', 'typeguard>=2.7,<3.0', 'typing_extensions>=3.7.4,<4.0.0']

extras_require = \
{'pyyaml': ['pyyaml>=5.3,<6.0']}

setup_kwargs = {
    'name': 'concrete-settings',
    'version': '0.0.4',
    'description': 'TODO',
    'long_description': "Concrete Settings\n#################\n\n.. image:: https://travis-ci.org/BasicWolf/concrete-settings.svg?branch=master\n    :target: https://travis-ci.org/BasicWolf/concrete-settings\n\n.. image:: https://basicwolf.github.io/concrete-settings/_static/img/codestyle_black.svg\n    :target: https://github.com/ambv/black\n\n.. image:: https://basicwolf.github.io/concrete-settings/_static/img/mypy_checked.svg\n   :target: https://github.com/python/mypy\n\nWelcome to Concrete Settings\n============================\n\n**Concrete Settings** is a Python library which facilitates\nconfiguration management in big and small programs.\n\nThe project was born out of necessity to manage a huge\ndecade-old Django-based SaaS solution with more than two hundred\ndifferent application settings scattered around ``settings.py``.\n*What does this setting do?*\n*What type is it?*\n*Why does it have such a weird format?*\n*Is this the final value, or it changes somewhere on the way?*\nSometimes developers spent *hours* seeking answers to these\nquestions.\n\n**Concrete Settigns** tackles these problems altogether.\nIt was designed to be developer and end-user friendly.\nThe settings are defined via normal Python code with few\ntricks which significantly improve readability\nand maintainability.\n\nTake a look at a small example of Settings class with one\nboolean setting ``DEBUG``. A developer defines the\nsettings in application code, while an end-user\nchooses to store the configuration in a YAML file:\n\n.. code-block:: python\n\n   # settings.py\n\n   from concrete_settings import Settings\n\n   class AppSettings(Settings):\n\n       #: Turns debug mode on/off\n       DEBUG: bool = False\n\n\n   app_settings = AppSettings()\n   app_settings.update('/path/to/user/settings.yml')\n   app_settings.is_valid(raise_exception=True)\n\n.. code-block:: yaml\n\n   # settings.yml\n\n   DEBUG: true\n\n\nAccessing settings:\n\n.. code-block:: pycon\n\n   >>>  print(app_settings.DEBUG)\n   True\n\n   >>> print(AppSettings.DEBUG.__doc__)\n   Turns debug mode on/off\n\n\nAs you can see, settings are **defined in classes**. Python mechanism\nof inheritance and nesting apply here, so settings can be **mixed** (multiple inheritance)\nand be **nested** (settings as class fields).\nSettings are **type-annotated** and are **validated**.\nDocumentation matters! Each settings can be documented in Sphinx-style comments ``#:`` written\nabove its definition.\nAn instance of ``Settings`` can be updated i.e. read from any kind of source:\nYAML, JSON or Python files, environmental variables, Python dicts, and you can add more!\n\nFinally, **Concrete Settings** comes with batteries like Django 3.0 support out of the box.\n\nConcrete Settings are here to improve configuration handling\nwhether you are starting from scratch, or dealing with an\nold legacy Cthulhu.\nAre you ready to try it out?\n\n``pip install concrete-settings`` and welcome to the `documentation <https://basicwolf.github.io/concrete-settings>`_!\n",
    'author': 'Zaur Nasibov',
    'author_email': 'comments@znasibov.info',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/basicwolf/concrete-settings',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
