#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import unittest
import GLXCurses


class TestHSeparator(unittest.TestCase):
    def test_draw_widget_in_area(self):
        win = GLXCurses.Window()
        hline = GLXCurses.HSeparator()

        win.add(hline)

        GLXCurses.Application().add_window(win)
        for position in GLXCurses.GLXC.PositionType:
            hline.position_type = position
            GLXCurses.Application().refresh()

        self.assertEqual(hline.preferred_width, hline.width)
        self.assertEqual(hline.preferred_height, 1)
