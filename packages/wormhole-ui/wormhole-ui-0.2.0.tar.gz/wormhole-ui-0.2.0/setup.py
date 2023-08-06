# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wormhole_ui',
 'wormhole_ui.protocol',
 'wormhole_ui.protocol.transit',
 'wormhole_ui.widgets.ui']

package_data = \
{'': ['*'],
 'wormhole_ui': ['resources/*',
                 'widgets/connect_dialog.py',
                 'widgets/connect_dialog.py',
                 'widgets/connect_dialog.py',
                 'widgets/connect_dialog.py',
                 'widgets/connect_dialog.py',
                 'widgets/connect_dialog.py',
                 'widgets/connect_dialog.py',
                 'widgets/errors.py',
                 'widgets/errors.py',
                 'widgets/errors.py',
                 'widgets/errors.py',
                 'widgets/errors.py',
                 'widgets/errors.py',
                 'widgets/errors.py',
                 'widgets/main_window.py',
                 'widgets/main_window.py',
                 'widgets/main_window.py',
                 'widgets/main_window.py',
                 'widgets/main_window.py',
                 'widgets/main_window.py',
                 'widgets/main_window.py',
                 'widgets/message_table.py',
                 'widgets/message_table.py',
                 'widgets/message_table.py',
                 'widgets/message_table.py',
                 'widgets/message_table.py',
                 'widgets/message_table.py',
                 'widgets/message_table.py',
                 'widgets/save_file_dialog.py',
                 'widgets/save_file_dialog.py',
                 'widgets/save_file_dialog.py',
                 'widgets/save_file_dialog.py',
                 'widgets/save_file_dialog.py',
                 'widgets/save_file_dialog.py',
                 'widgets/save_file_dialog.py',
                 'widgets/shutdown_message.py',
                 'widgets/shutdown_message.py',
                 'widgets/shutdown_message.py',
                 'widgets/shutdown_message.py',
                 'widgets/shutdown_message.py',
                 'widgets/shutdown_message.py',
                 'widgets/shutdown_message.py',
                 'widgets/ui_dialog.py',
                 'widgets/ui_dialog.py',
                 'widgets/ui_dialog.py',
                 'widgets/ui_dialog.py',
                 'widgets/ui_dialog.py',
                 'widgets/ui_dialog.py',
                 'widgets/ui_dialog.py']}

install_requires = \
['PySide2==5.13.1',
 'humanize==0.5.1',
 'magic_wormhole>=0.11.2,<0.13.0',
 'qt5reactor>=0.6,<0.7']

entry_points = \
{'console_scripts': ['wormhole-ui = wormhole_ui.main:run']}

setup_kwargs = {
    'name': 'wormhole-ui',
    'version': '0.2.0',
    'description': 'UI for Magic Wormhole - get things from one computer to another safely',
    'long_description': '# Magic Wormhole UI\n\nA GUI for the [Magic Wormhole](https://github.com/warner/magic-wormhole/). Get things from one computer to another safely.\n\n![Screenshot](docs/media/screenshot.png)\n\n[![PyPI](https://img.shields.io/pypi/v/wormhole-ui.svg)](https://pypi.python.org/pypi/wormhole-ui)\n[![Build Status](https://travis-ci.com/sneakypete81/wormhole-ui.svg?branch=master)](https://travis-ci.com/sneakypete81/wormhole-ui)\n\n## Installation\n\n### Windows\nDownload the [Windows installer](https://github.com/sneakypete81/wormhole-ui/releases/latest/download/Magic.Wormhole.Installer.exe).\n\n### MacOS\nDownload the [MacOS installer](https://github.com/sneakypete81/wormhole-ui/releases/latest/download/Magic.Wormhole.Installer.dmg).\n\n### Linux\nInstaller coming soon...\n\n### From Source\nThe recommended method to run from the Python source is with [pipx](https://pipxproject.github.io/pipx/):\n```sh\n  pipx install wormhole-ui\n  wormhole-ui\n```\n(or use pip if you prefer)\n\n## Development\n\nRequires [Poetry](https://poetry.eustace.io/).\n\n```sh\n  git clone https://github.com/sneakypete81/wormhole-ui.git\n  cd wormhole-ui\n  poetry install\n```\n\nThen you can use the following:\n\n```sh\n  poetry run wormhole-ui  # Run the app\n  poetry run pytest       # Run unit tests\n  poetry run flake8       # Run the linter\n  poetry run black .      # Run the code autoformatter\n  poetry run tox          # Run all checks across all supported Python versions\n```\n',
    'author': 'sneakypete81',
    'author_email': 'sneakypete81@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sneakypete81/wormhole-ui',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<3.8',
}


setup(**setup_kwargs)
