#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import GLXCurses


class TextTagTable(GLXCurses.Object):
    def __init__(self):
        GLXCurses.Object.__init__(self)
        self.table = None

    def new(self):
        """
        Creates a new TextTagTable. The table contains no tags by default.

        :return: a new TextTagTable
        :rtype: TextTagTable
        """
        self.__init__()
        return self

    def add(self):
        pass

    def remove(self):
        pass

    def lookup(self):
        pass

    def foreach(self):
        pass

    def get_size(self):
        pass

