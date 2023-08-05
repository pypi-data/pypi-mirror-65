# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wdldoc', 'wdldoc.bin', 'wdldoc.miniwdl', 'wdldoc.templates']

package_data = \
{'': ['*']}

install_requires = \
['cachecontrol[filecache]>=0.12.6,<0.13.0',
 'logzero>=1.5.0,<2.0.0',
 'miniwdl>=0.7.0,<0.8.0',
 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['wdldoc = wdldoc.__main__:main']}

setup_kwargs = {
    'name': 'wdldoc',
    'version': '1.2.0a0',
    'description': 'Create WDL documentation using Markdown.',
    'long_description': '<p align="center">\n  <h1 align="center">\n  wdldoc\n  </h1>\n\n  <p align="center">\n    Convert WDL documentation to Markdown for rendering.\n    <br />\n    <a href="https://github.com/stjudecloud/wdldoc/issues">Request Feature</a>\n    ·\n    <a href="https://github.com/stjudecloud/wdldoc/issues">Report Bug</a>\n    ·\n    ⭐ Consider starring the repo! ⭐\n    <br />\n  </p>\n</p>\n\n### Notice\n\nThis repository is still in development!\n\n## 📚 Getting Started\n\n### Installation\n\nCurrently, only local setup is supported using Python 3.8 or higher:\n\n```bash\npip install poetry>=1.0.5\npoetry install\n```\n\n## 🖥️ Development\n\nIf you are interested in contributing to the code, please first review\nour [CONTRIBUTING.md][contributing-md] document. To bootstrap a\ndevelopment environment, please use the following commands.\n\n```bash\n# Clone the repository\ngit clone git@github.com:stjudecloud/wdldoc.git\ncd wdldoc\n\n# Install the project using poetry\npoetry install\n\n# Ensure pre-commit is installed to automatically format\n# code using `black`.\nbrew install pre-commit\npre-commit install\npre-commit install --hook-type commit-msg\n```\n\n## 📝 License\n\nCopyright © 2020 [St. Jude Cloud Team](https://github.com/stjudecloud).<br />\nThis project is [MIT][license-md] licensed.\n\n[contributing-md]: https://github.com/stjudecloud/wdldoc/blob/master/CONTRIBUTING.md\n[license-md]: https://github.com/stjudecloud/wdldoc/blob/master/LICENSE.md\n',
    'author': 'Clay McLeod',
    'author_email': 'Clay.McLeod@STJUDE.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stjudecloud/wdldoc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
