#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Save command line history and provide a command line completer for python.
"""

from __future__ import division, print_function, absolute_import, unicode_literals

# Standard libraries.
from atexit import register
from readline import set_pre_input_hook

# Third party libraries.
import __main__

from .history import HISTORY_PATH, History

__date__ = "2020/04/13 16:55:33 hoel"
__author__ = "Sunjoong LEE <sunjoong@gmail.com>"
__copyright__ = "Copyright © 2006 by Sunjoong LEE"
__credits__ = ["Sunjoong LEE", "Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berhoel@gmail.com"


# History.py
#
# Store the file "History.py"
# in site-packages directory like "/usr/lib/python2.4/site-packages,"
# or a directory pointed by PYTHONPATH environment varable,
# or your home directory.
#
# Insert the line, "import History" to "~/.pystartup" file,
# and set an environment variable to point to it:
# "export PYTHONSTARTUP=${HOME}/.pystartup" in bash.
#
# References:
#     Guido van Rossum. Python Tutorial. Python Sfotware Foundation, 2005. 86
#     Jian Ding Chen. Indentable rlcompleter. Python Cookbook Recipe 496812
#     Guido van Rossum. rlcompleter.py. Python Sfotware Foundation, 2005
#
# 2006.06.29 Sunjoong LEE <sunjoong@gmail.com>
#
__version__ = "1.1.0"


def save_history(history_path=HISTORY_PATH):
    from readline import write_history_file

    write_history_file(history_path)


register(save_history)


def hook():
    from readline import set_pre_input_hook
    import __main__

    set_pre_input_hook()
    delattr(__main__, "History")
    delattr(__main__, "__file__")


set_pre_input_hook(hook)
setattr(__main__.__builtins__, "history", History())

# Local Variables:
# mode: python
# compile-command: "poetry run tox"
# time-stamp-pattern: "30/__date__ = \"%:y/%02m/%02d %02H:%02M:%02S %u\""
# End:
