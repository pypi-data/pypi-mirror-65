# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zshpower', 'zshpower.sections', 'zshpower.sections.lib']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0',
 'fastentrypoints>=0.12,<0.13',
 'snakypy>=0.3.5,<0.4.0',
 'tomlkit>=0.5.11,<0.6.0']

entry_points = \
{'console_scripts': ['zshpower = zshpower.cli:main',
                     'zshpower-shell = zshpower.prompt:main']}

setup_kwargs = {
    'name': 'zshpower',
    'version': '0.2.6',
    'description': 'ZSHPower is a theme with a manager for the Oh My ZSH framework.',
    'long_description': '.. image:: https://raw.githubusercontent.com/snakypy/snakypy-static/master/zshpower/logo/png/zshpower.png\n    :width: 505 px\n    :align: center\n    :alt: ZSHPower\n\n.. image:: https://github.com/snakypy/zshpower/workflows/Python%20package/badge.svg\n    :target: https://github.com/snakypy/zshpower\n\n.. image:: https://img.shields.io/pypi/v/zshpower.svg\n    :target: https://pypi.python.org/pypi/zshpower\n\n.. image:: https://travis-ci.com/snakypy/zshpower.svg?branch=master\n    :target: https://travis-ci.com/snakypy/zshpower\n\n.. image:: https://img.shields.io/pypi/wheel/zshpower\n    :alt: PyPI - Wheel\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n\n.. image:: https://pyup.io/repos/github/snakypy/zshpower/shield.svg\n    :target: https://pyup.io/repos/github/snakypy/zshpower/\n    :alt: Updates\n\n.. image:: https://img.shields.io/github/issues-raw/snakypy/zshpower\n    :alt: GitHub issues\n\n.. image:: https://img.shields.io/github/license/snakypy/zshpower\n    :alt: GitHub license\n    :target: https://github.com/snakypy/zshpower/blob/master/LICENSE\n\n\n`ZSHPower` is a theme for `Oh My Zsh`_ framework; especially\nfor the `Python`_ developer. Pleasant to look at, the **ZSHPower**\ncomforts you with its colors and icons vibrant.\n\nInstalling **ZSHPower** is the easiest thing you will see in any existing theme for Oh My Zsh,\nbecause ZSHPower has its own manager. With `ZSHPower`_,\nchanges to the theme become more dynamic through a configuration file, where the user can make various combinations\nof changes, such as: **enable**, **disable**, **open settings**, **reset settings**, **uninstall** and more;\nall in a simplified command line, without opening any files or creating symbolic links.\nIn addition, the **ZSHPower** manager downloads **Oh My Zsh** and the\n`zsh-autosuggestions`_ and `zsh-syntax-highlighting`_ plugins automatically, everything to make your ZSH very power.\n\n\nRequirements\n------------\n\nTo work correctly, you will first need:\n\n* `git`_ (v2.25 or recent) must be installed.\n* `zsh`_  (v5.2 or recent) must be installed.\n* `python`_ (v3.7 or recent) must be installed.\n* `pip`_ (v19.3 or recent) must be installed.\n* `nerd fonts`_ must be installed.\n\n\nFeatures\n--------\n\n* `Oh My Zsh`_ Installation Automatically;\n* Automatically install `zsh-autosuggestions`_ and `zsh-syntax-highlighting`_;\n* Automated installation and uninstallation;\n* Enable and disable `ZSHPower` anytime;\n* Upgrade `ZSHPower` effortlessly;\n* Reset the settings with one command only;\n* Current Git branch and rich repo status:\n    *  — untracked changes;\n    *  — new files added;\n    *  — deleted files;\n    *  — new modified files;\n    *  — commits made;\n* Python version shown (*with pyenv support*) on the active virtual machine (E.g: `[python_icon] py-3.x`);\n* Shows the version of the project if you use "**pyproject.toml**" (E.g: `[pkg_icon] 0.1.0`);\n* Enables **username** and **hostname** when connecting with SSH. (can change in the settings to show permanently);\n* and, many other dynamic settings in `$HOME/.config/snakypy/zshpower/config.toml`.\n\n\nInstalling\n----------\n\nGlobally:\n\n.. code-block:: shell\n\n    $ sudo pip install zshpower\n\nFor the user:\n\n.. code-block:: shell\n\n    $ pip install zshpower --user\n\n\nUsing\n-----\n\nBecause **ZSHPower** is a manager, usage information is in the\n`ZSHPower`_ project. Access the project, and see how to use **ZSHPower**.\n\nFor more command information, run:\n\n.. code-block:: shell\n\n    $ zshpower --help\n\nMore information: https://github.com/snakypy/zshpower\n\nDonation\n--------\n\nIf you liked my work, buy me a coffee <3\n\n.. image:: https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif\n    :target: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=YBK2HEEYG8V5W&source\n\nLicense\n-------\n\nThe gem is available as open source under the terms of the `MIT License`_ ©\n\nCredits\n-------\n\n* Name: William C. Canin\n* Country: Brazil - SP\n* E-Mail: william.costa.canin@gmail.com\n* Personal page: `William Canin`_\n\nThis package was created with Cookiecutter_ and the `williamcanin/pypkg-cookiecutter`_ project template.\n\nLinks\n-----\n\n* Code: https://github.com/snakypy/zshpower\n* Documentation: https://github.com/snakypy/zshpower/blob/master/README.md\n* Releases: https://pypi.org/project/zshpower/#history\n* Issue tracker: https://github.com/snakypy/zshpower/issues\n\n.. _Oh My Zsh: https://ohmyz.sh\n.. _Python: https://python.org\n.. _zsh-autosuggestions: https://github.com/zsh-users/zsh-autosuggestions\n.. _zsh-syntax-highlighting: https://github.com/zsh-users/zsh-syntax-highlighting\n.. _ZSHPower: https://github.com/snakypy/zshpower\n.. _git: https://git-scm.com/downloads\n.. _zsh: http://www.zsh.org/\n.. _`python`: https://python.org\n.. _pip: https://pip.pypa.io/en/stable/quickstart/\n.. _nerd fonts: https://www.nerdfonts.com/font-downloads\n.. _MIT License: https://github.com/snakypy/zshpower/blob/master/LICENSE\n.. _William Canin: http://williamcanin.github.io\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`williamcanin/pypkg-cookiecutter`: https://github.com/williamcanin/pypkg-cookiecutter\n',
    'author': 'William C. Canin',
    'author_email': 'william.costa.canin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/snakypy/zshpower',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
