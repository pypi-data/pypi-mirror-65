# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dotctrl']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0', 'snakypy>=0.3.6,<0.4.0']

entry_points = \
{'console_scripts': ['dotctrl = dotctrl.cli:main']}

setup_kwargs = {
    'name': 'dotctrl',
    'version': '1.1.2',
    'description': 'Dotctrl is a package for managing your dotfiles on Linux.',
    'long_description': '.. image:: https://raw.githubusercontent.com/snakypy/snakypy-static/master/dotctrl/logo/png/dotctrl.png\n    :width: 441 px\n    :align: center\n    :alt: Dotctrl\n\n\n.. image:: https://github.com/snakypy/dotctrl/workflows/Python%20package/badge.svg\n    :target: https://github.com/snakypy/dotctrl\n\n.. image:: https://img.shields.io/pypi/v/dotctrl.svg\n    :target: https://pypi.python.org/pypi/dotctrl\n\n.. image:: https://travis-ci.com/snakypy/dotctrl.svg?branch=master\n    :target: https://travis-ci.com/snakypy/dotctrl\n\n.. image:: https://img.shields.io/pypi/wheel/dotctrl\n    :alt: PyPI - Wheel\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n\n.. image:: https://pyup.io/repos/github/snakypy/dotctrl/shield.svg\n    :target: https://pyup.io/repos/github/snakypy/dotctrl\n    :alt: Updates\n\n.. image:: https://img.shields.io/github/issues-raw/snakypy/dotctrl\n    :alt: GitHub issues\n\n.. image:: https://img.shields.io/github/license/snakypy/dotctrl\n    :alt: GitHub license\n    :target: https://github.com/snakypy/dotctrl/blob/master/LICENSE\n\n\n`Dotctrl` is a package for managing your "dotfiles" on Linux. `Dotctrl` works on top of a configuration file that contains the absolute paths of the place of origin of dotfiles.\n\nFeatures\n--------\n\n* Automatically manages dotfiles ending with rc in the user\'s HOME;\n* Automatically manages the main configuration files of the editors: Atom, Sublime Text, Visual Studio Code;\n* The `Dotctrl` repository stores the same path structure as the configuration files with the user\'s HOME files;\n\nRequirements\n------------\n\nTo work correctly, you will first need:\n\n* `python`_ (v3.8 or recent) must be installed.\n* `pip`_ (v19.3 or recent) must be installed.\n\nInstalling\n----------\n\nGlobally:\n\n.. code-block:: shell\n\n    $ sudo pip install dotctrl\n\nFor the user:\n\n.. code-block:: shell\n\n    $ pip install dotctrl --user\n\n\nUsing\n-----\n\nTo know the commands of `Dotctrl`, run the command:\n\n.. code-block:: shell\n\n    $ dotctrl -h\n\nAlso visit the Dotctrl `home page`_ and see more about settings and usability.\n\nLinks\n-----\n\n* Code: https://github.com/snakypy/dotctrl\n* Documentation: https://github.com/snakypy/dotctrl/blob/master/README.md\n* Releases: https://pypi.org/project/dotctrl/#history\n* Issue tracker: https://github.com/snakypy/dotctrl/issues\n\nDonation\n--------\n\nIf you liked my work, buy me a coffee <3\n\n.. image:: https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif\n    :target: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=YBK2HEEYG8V5W&source\n\nLicense\n-------\n\nThe gem is available as open source under the terms of the `MIT License`_ ©\n\nCredits\n-------\n\nSee, `AUTHORS`_.\n\n.. _`AUTHORS`: https://github.com/snakypy/dotctrl/blob/master/AUTHORS.rst\n.. _`home page`: https://github.com/snakypy/dotctrl\n.. _`python`: https://python.org\n.. _pip: https://pip.pypa.io/en/stable/quickstart/\n.. _MIT License: https://github.com/snakypy/dotctrl/blob/master/LICENSE\n.. _William Canin: http://williamcanin.github.io\n',
    'author': 'William C. Canin',
    'author_email': 'william.costa.canin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/snakypy/dotctrl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
