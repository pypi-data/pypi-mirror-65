#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import unittest
import GLXCurses


class TestVSeparator(unittest.TestCase):
    def test_draw_widget_in_area(self):
        win = GLXCurses.Window()
        vline = GLXCurses.VSeparator()

        win.add(vline)

        GLXCurses.Application().add_window(win)
        for justify in GLXCurses.GLXC.Justification:
            vline.justify = justify
            GLXCurses.Application().refresh()

        self.assertEqual(vline.preferred_width, 1)
        self.assertEqual(vline.preferred_height, vline.height)
