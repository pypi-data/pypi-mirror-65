#!/usr/bin/env python
# -*- coding: utf-8 -*-
import GLXCurses
import curses


# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved


class HSeparator(GLXCurses.Widget, GLXCurses.Movable):
    def __init__(self):
        """
        The GLXCurses.HSeparator widget is a horizontal separator, used to visibly separate the widgets within a \
        window. It displays a horizontal line.
        """
        # Load heritage
        GLXCurses.Widget.__init__(self)
        GLXCurses.Movable.__init__(self)

        self.name = '{0}{1}'.format(self.__class__.__name__, self.id)

    def draw_widget_in_area(self):
        self.create_or_resize()

        if self.subwin:
            # Size
            self.preferred_height = 1
            self.preferred_width = self.width

            self.check_position()

            # Curses
            for x_inc in range(self.x_offset, self.preferred_width):
                try:
                    self.subwin.delch(self.y_offset,
                                      self.x_offset + x_inc)
                    self.subwin.insch(self.y_offset,
                                      self.x_offset + x_inc,
                                      curses.ACS_HLINE,
                                      self.style.color(fg='GRAY', bg='BLUE') | curses.A_NORMAL
                                      )
                except curses.error:  # pragma: no cover
                    pass
