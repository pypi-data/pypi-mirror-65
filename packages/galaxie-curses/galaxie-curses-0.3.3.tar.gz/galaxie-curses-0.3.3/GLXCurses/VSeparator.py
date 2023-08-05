#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import GLXCurses
import curses


class VSeparator(GLXCurses.Widget, GLXCurses.Movable):
    def __init__(self):
        GLXCurses.Widget.__init__(self)
        GLXCurses.Movable.__init__(self)
        self.name = '{0}{1}'.format(self.__class__.__name__, self.id)

    def draw_widget_in_area(self):
        self.create_or_resize()

        if self.subwin is not None:
            self.preferred_width = 1
            self.preferred_height = self.height
            self.check_justification()

            try:
                for y_inc in range(self.y_offset, self.preferred_height):
                    self.subwin.delch(self.y_offset + y_inc,
                                      self.x_offset
                                      )
                    self.subwin.insch(self.y_offset + y_inc,
                                      self.x_offset,
                                      curses.ACS_VLINE,
                                      self.style.color(fg='GRAY', bg='BLUE') | curses.A_NORMAL
                                      )
            except curses.error:  # pragma: no cover
                pass
