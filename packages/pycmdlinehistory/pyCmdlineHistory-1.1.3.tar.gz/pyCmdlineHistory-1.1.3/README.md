# pyCmdlineHistory #

Shield: [![CC BY-SA 4.0][cc-by-sa-shield]][cc-by-sa]

This work is licensed under a [Creative Commons Attribution-ShareAlike 4.0
International License][cc-by-sa].

[![CC BY-SA 4.0][cc-by-sa-image]][cc-by-sa]

Save command line history and provide a command line completer for python.

Original code is from [ActiveState Code » Recipes][as-496822]
2006.06.29 by [Sunjoong LEE](<sunjoong@gmail.com>). ActiveState
content is published under [CC BY-SA 3.0][cc-by-sa3].

## Usage ##

Insert the line,
```python
import sys
import subprocess

try:
    import berhoel.cmd_line_history
except ImportError:
    # checking if python is running under virtualenv of venv
    is_venv = (
        # This handles PEP 405 compliant virtual environments.
        (sys.prefix != getattr(sys, "base_prefix", sys.prefix))
        or
        # This handles virtual environments created with pypa's virtualenv.
        hasattr(sys, "real_prefix")
    )

    subprocess.check_call(
        [sys.executable, "-m", "pip", "install"]
        + ([] if is_venv else ["--user"])
        + ["pyCmdlineHistory",]
    )
```
to "~/.pystartup" file, and set an environment variable to point to it:
```shell
export PYTHONSTARTUP=${HOME}/.pystartup
```
in bash.

This will locally install the module for each python you are calling.

## References ##

  - Guido van Rossum. Python Tutorial. Python Sfotware Foundation, 2005. 86
  - Jian Ding Chen. Indentable rlcompleter. Python Cookbook Recipe 496812
  - Guido van Rossum. rlcompleter.py. Python Sfotware Foundation, 2005

2006.06.29 Sunjoong LEE <sunjoong@gmail.com>

[cc-by-sa]: http://creativecommons.org/licenses/by-sa/4.0/
[cc-by-sa3]: http://creativecommons.org/licenses/by-sa/3.0/
[cc-by-sa-image]: https://licensebuttons.net/l/by-sa/4.0/88x31.png
[cc-by-sa-shield]: https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg
[as-496822]: http://code.activestate.com/recipes/496822-completer-with-history-viewer-support-and-more-fea/
