#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import GLXCurses


class GroupElement(object):
    def __init__(self, widget=None):
        self.__widget = None

        self.widget = widget

    @property
    def widget(self):
        return self.__widget

    @widget.setter
    def widget(self, widget):
        if widget is not None and not isinstance(widget, GLXCurses.Widget) and \
                not isinstance(widget, GLXCurses.Adjustment):
            raise TypeError('"widget" must be a GLXCurses.Widget of None')
        if self.widget != widget:
            self.__widget = widget
