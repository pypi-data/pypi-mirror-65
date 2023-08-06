#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Save command line history and provide a command line completer for python.
"""

from __future__ import division, print_function, absolute_import, unicode_literals

# Standard libraries.
from atexit import register
from readline import set_pre_input_hook

import __main__

from .history import History

__date__ = "2020/04/14 21:01:14 hoel"
__author__ = "Sunjoong LEE <sunjoong@gmail.com>"
__copyright__ = "Copyright © 2006 by Sunjoong LEE"
__credits__ = ["Sunjoong LEE", "Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berhoel@gmail.com"


__version__ = "1.1.3"


def save_history(history_path=None):
    from readline import write_history_file
    from .history import HISTORY_PATH

    if history_path is None:
        history_path = HISTORY_PATH
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
