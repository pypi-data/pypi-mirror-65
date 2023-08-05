#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import unittest
import GLXCurses


# Unittest
class TestButton(unittest.TestCase):
    def tearDown(self):
        GLXCurses.Application().refresh()

    def setUp(self):
        self.win = GLXCurses.Window()
        self.checkbutton = GLXCurses.CheckButton()
        GLXCurses.Application().add_window(self.win)
        self.win.add(self.checkbutton)

    def test_text(self):
        self.checkbutton.text = None
        self.assertIsNone(self.checkbutton.text)
        self.checkbutton.text = 'Hello.42'
        self.assertEqual('Hello.42', self.checkbutton.text)

        self.assertRaises(TypeError, setattr, self.checkbutton, 'text', 42)

    def test_active(self):
        self.checkbutton.active = True
        self.assertTrue(self.checkbutton.active)
        self.checkbutton.active = False
        self.assertFalse(self.checkbutton.active)
        self.checkbutton.active = None
        self.assertFalse(self.checkbutton.active)

        self.assertRaises(TypeError, setattr, self.checkbutton, 'active', 'Hello.42')

    def test_color(self):
        self.checkbutton.text = 'Test color'
        self.assertEqual(11264, self.checkbutton.color)
        self.checkbutton.sensitive = False
        self.assertEqual(1059840, self.checkbutton.color)
        self.checkbutton.sensitive = True
        self.assertEqual(11264, self.checkbutton.color)

    def test_preferred_width(self):
        self.checkbutton.text = 'Hello.42'
        self.assertEqual(12, self.checkbutton.preferred_width)

    def test_preferred_height(self):
        self.checkbutton.text = 'Hello.42'
        self.assertEqual(0, self.checkbutton.preferred_height)

    def test_interface(self):
        self.checkbutton.text = 'Test Interface'
        self.checkbutton.active = False
        self.assertEqual('[ ] ', self.checkbutton.interface)
        self.checkbutton.active = True
        self.assertEqual('[x] ', self.checkbutton.interface)
        self.checkbutton.active = False
        self.assertEqual('[ ] ', self.checkbutton.interface)

    def test_draw_widget_in_area(self):
        self.checkbutton.text = 'Test Draw Widget In Area'
        self.checkbutton.active = True
        GLXCurses.Application().has_default = self.checkbutton
        GLXCurses.Application().has_focus = self.checkbutton
        GLXCurses.Application().has_prelight = self.checkbutton
        self.checkbutton.draw_widget_in_area()
        GLXCurses.Application().has_default = None
        GLXCurses.Application().has_focus = None
        GLXCurses.Application().has_prelight = None
        self.checkbutton.draw_widget_in_area()
        self.checkbutton.active = False
        self.checkbutton.draw_widget_in_area()


if __name__ == '__main__':
    unittest.main()
