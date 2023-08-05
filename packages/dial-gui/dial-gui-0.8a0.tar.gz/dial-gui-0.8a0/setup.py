# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dial_gui',
 'dial_gui.event_filters',
 'dial_gui.main_window',
 'dial_gui.node_editor',
 'dial_gui.project',
 'dial_gui.utils',
 'dial_gui.widgets',
 'dial_gui.widgets.editor_tabwidget',
 'dial_gui.widgets.log',
 'dial_gui.widgets.menus',
 'dial_gui.widgets.node_panels',
 'dial_gui.widgets.plugin',
 'dial_gui.widgets.plugin.plugins_table']

package_data = \
{'': ['*']}

install_requires = \
['PySide2>=5.12.6,<6.0.0',
 'dependency-injector>=3.15.6,<4.0.0',
 'dial-core==v0.12a0',
 'qimage2ndarray>=1.8.3,<2.0.0',
 'tensorflow==2.0.0b1']

setup_kwargs = {
    'name': 'dial-gui',
    'version': '0.8a0',
    'description': 'A node-based GUI for Deep Learning tasks',
    'long_description': "# dial-gui\nGUI for the __dial-core__ framework.\n\n| Build | Coverage | Quality | Version | Python | Docs | License |\n|-------|----------|---------|---------|--------|------|---------|\n| [![Build Status](https://travis-ci.com/dial-app/dial-gui.svg?branch=master)](https://travis-ci.com/dial-app/dial-gui) \t| [![codecov](https://codecov.io/gh/dial-app/dial-gui/branch/master/graph/badge.svg)](https://codecov.io/gh/dial-app/dial-gui) \t| [![Codacy Badge](https://api.codacy.com/project/badge/Grade/eb5224f0cc3f481aa5d419b4bfc86f41)](https://www.codacy.com/gh/dial-app/dial-gui?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=dial-app/dial-gui&amp;utm_campaign=Badge_Grade) \t| [![PyPI](https://img.shields.io/pypi/v/dial-gui)](https://pypi.org/project/dial-gui/) \t| [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dial-gui?color=green)](https://pypi.org/project/dial-gui/) \t| [![ReadTheDocs](https://readthedocs.org/projects/dial-gui/badge/?version=latest)](https://dial-gui.readthedocs.io/) \t| [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) |\n\n## Images\n\n![Dial GUI Preview](https://i.imgur.com/Diu9MUp.png)\n\nThis is a __work in progress__ project. Expect most of the interface to change over time.\n\n## Documentation\n\nThis project's documentation lives at [readthedocs.io](https://dial-gui.readthedocs.io).\n\n## License\n\nAll code is provided under the __GPL-3.0__ license. See [LICENSE](LICENSE) for more details.\n\n## Authors\n\n* **David Afonso (davafons)**: [Github](https://github.com/davafons) [Twitter](https://twitter.com/davafons)\n",
    'author': 'David Afonso',
    'author_email': 'davafons@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dial-app/dial-gui',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.8',
}


setup(**setup_kwargs)
