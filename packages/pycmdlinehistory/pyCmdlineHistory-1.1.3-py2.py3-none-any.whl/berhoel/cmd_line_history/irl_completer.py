#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Command line comleter helper for python.
"""
from __future__ import division, print_function, absolute_import, unicode_literals

# Standard libraries.
from os import listdir
from pwd import getpwall
from os.path import split, expanduser
from rlcompleter import Completer

__date__ = "2020/04/13 17:53:33 hoel"
__author__ = "Sunjoong LEE <sunjoong@gmail.com>"
__copyright__ = "Copyright © 2006 by Sunjoong LEE"
__credits__ = ["Sunjoong LEE", "Berthold Höllmann"]
__maintainer__ = "Berthold Höllmann"
__email__ = "berhoel@gmail.com"


class IrlCompleter(Completer, object):
    def __init__(self, *args, **kw):
        super(IrlCompleter, self).__init__(*args, **kw)
        self.matches = ""

    def complete(self, text, state):
        if text == "":
            # you could replace '    ' to \t if you indent via tab
            return ["    ", None][state]
        if text.count("'") == 1:
            if not state:
                self.file_matches(text, "'")
            try:
                return self.matches[state]
            except IndexError:
                return None
        if text.count('"') == 1:
            if not state:
                self.file_matches(text, '"')
            try:
                return self.matches[state]
            except IndexError:
                return None
        else:
            return Completer.complete(self, text, state)

    def file_matches(self, text, mark):
        if "~" in text:
            if "/" in text:
                text = "{}{}{}".format(
                    mark,
                    expanduser(text[text.find("~") : text.find("/")]),
                    text[text.find("/") :],
                )
            else:
                self.user_matches(text, mark)
                return

        text1 = text[1:]
        delim = "/"

        if not text1:
            directory = ""
        elif text1 == ".":
            directory = "."
        elif text1 == "..":
            directory = ".."
        elif text1 == "/":
            directory = "/"
            delim = ""
        elif text1.endswith("/"):
            directory = text1[:-1]
            delim = text1[len(directory) :]
        else:
            directory, partial = split(text1)
            delim = text1[len(directory) :][: -len(partial)]

        if directory:
            listing = [
                "{}{}{}{}".format(mark, directory, delim, x) for x in listdir(directory)
            ]
        else:
            listing = ["{}{}".format(mark, x) for x in listdir(".")]

        n = len(text)
        self.matches = [x for x in listing.__iter__() if x[:n] == text]

    def user_matches(self, text, mark):
        n = len(text)
        self.matches = [
            "{}~{}".format(mark, x[0]) for x in getpwall() if x.startswith(text)
        ]


# Local Variables:
# mode: python
# compile-command: "poetry run tox"
# time-stamp-pattern: "30/__date__ = \"%:y/%02m/%02d %02H:%02M:%02S %u\""
# End:
