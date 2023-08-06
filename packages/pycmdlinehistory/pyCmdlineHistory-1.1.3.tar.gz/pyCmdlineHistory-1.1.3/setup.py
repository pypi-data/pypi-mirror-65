# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['berhoel', 'berhoel.cmd_line_history', 'berhoel.cmd_line_history.test']

package_data = \
{'': ['*']}

extras_require = \
{':python_version >= "2.7" and python_version < "3.0"': ['pathlib2>=2.3.5,<3.0.0']}

setup_kwargs = {
    'name': 'pycmdlinehistory',
    'version': '1.1.3',
    'description': 'Save command line history and provide a command line completer for python.',
    'long_description': '# pyCmdlineHistory #\n\nShield: [![CC BY-SA 4.0][cc-by-sa-shield]][cc-by-sa]\n\nThis work is licensed under a [Creative Commons Attribution-ShareAlike 4.0\nInternational License][cc-by-sa].\n\n[![CC BY-SA 4.0][cc-by-sa-image]][cc-by-sa]\n\nSave command line history and provide a command line completer for python.\n\nOriginal code is from [ActiveState Code » Recipes][as-496822]\n2006.06.29 by [Sunjoong LEE](<sunjoong@gmail.com>). ActiveState\ncontent is published under [CC BY-SA 3.0][cc-by-sa3].\n\n## Usage ##\n\nInsert the line,\n```python\nimport sys\nimport subprocess\n\ntry:\n    import berhoel.cmd_line_history\nexcept ImportError:\n    # checking if python is running under virtualenv of venv\n    is_venv = (\n        # This handles PEP 405 compliant virtual environments.\n        (sys.prefix != getattr(sys, "base_prefix", sys.prefix))\n        or\n        # This handles virtual environments created with pypa\'s virtualenv.\n        hasattr(sys, "real_prefix")\n    )\n\n    subprocess.check_call(\n        [sys.executable, "-m", "pip", "install"]\n        + ([] if is_venv else ["--user"])\n        + ["pyCmdlineHistory",]\n    )\n```\nto "~/.pystartup" file, and set an environment variable to point to it:\n```shell\nexport PYTHONSTARTUP=${HOME}/.pystartup\n```\nin bash.\n\nThis will locally install the module for each python you are calling.\n\n## References ##\n\n  - Guido van Rossum. Python Tutorial. Python Sfotware Foundation, 2005. 86\n  - Jian Ding Chen. Indentable rlcompleter. Python Cookbook Recipe 496812\n  - Guido van Rossum. rlcompleter.py. Python Sfotware Foundation, 2005\n\n2006.06.29 Sunjoong LEE <sunjoong@gmail.com>\n\n[cc-by-sa]: http://creativecommons.org/licenses/by-sa/4.0/\n[cc-by-sa3]: http://creativecommons.org/licenses/by-sa/3.0/\n[cc-by-sa-image]: https://licensebuttons.net/l/by-sa/4.0/88x31.png\n[cc-by-sa-shield]: https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg\n[as-496822]: http://code.activestate.com/recipes/496822-completer-with-history-viewer-support-and-more-fea/\n',
    'author': 'Sunjoong LEE',
    'author_email': 'sunjoong@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/berhoel/python/pyCmdlineHistory.git',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
