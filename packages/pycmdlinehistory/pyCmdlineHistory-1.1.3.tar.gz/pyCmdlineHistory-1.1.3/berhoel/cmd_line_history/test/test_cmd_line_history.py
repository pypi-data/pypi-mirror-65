#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `cmd_line_history`.
"""
from __future__ import division, print_function, absolute_import, unicode_literals

# Standard libraries.
import sys

# Third party libraries.
import toml

from berhoel import cmd_line_history

try:
    from pathlib import Path
except:
    from pathlib2 import Path

__date__ = "2020/04/13 13:55:02 hoel"
__author__ = "Berthold Höllmann"
__copyright__ = "Copyright © 2020 by Berthold Höllmann"
__credits__ = ["Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berhoel@gmail.com"


__BASE = Path(__file__).parent.parent.parent.parent
__TOML = toml.load((__BASE / "pyproject.toml").open("r"))


def test_version():
    """Testing for consistent version number.
 """
    assert cmd_line_history.__version__ == __TOML["tool"]["poetry"]["version"]


# Local Variables:
# mode: python
# compile-command: "poetry run tox"
# time-stamp-pattern: "30/__date__ = \"%:y/%02m/%02d %02H:%02M:%02S %u\""
# End:
