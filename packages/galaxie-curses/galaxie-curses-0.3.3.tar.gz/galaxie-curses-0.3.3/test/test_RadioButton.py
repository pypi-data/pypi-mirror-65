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
        self.radiobutton = GLXCurses.RadioButton()
        GLXCurses.Application().add_window(self.win)
        self.win.add(self.radiobutton)

    def test_text(self):
        self.radiobutton.text = None
        self.assertIsNone(self.radiobutton.text)
        self.radiobutton.text = 'Hello.42'
        self.assertEqual('Hello.42', self.radiobutton.text)

        self.assertRaises(TypeError, setattr, self.radiobutton, 'text', 42)

    def test_active(self):
        self.radiobutton.active = True
        self.assertTrue(self.radiobutton.active)
        self.radiobutton.active = False
        self.assertFalse(self.radiobutton.active)
        self.radiobutton.active = None
        self.assertFalse(self.radiobutton.active)

        self.assertRaises(TypeError, setattr, self.radiobutton, 'active', 'Hello.42')

    def test_color(self):
        self.radiobutton.text = 'Test color'
        self.assertEqual(11264, self.radiobutton.color)
        self.radiobutton.sensitive = False
        self.assertEqual(1059840, self.radiobutton.color)
        self.radiobutton.sensitive = True
        self.assertEqual(11264, self.radiobutton.color)

    def test_preferred_width(self):
        self.radiobutton.text = 'Hello.42'
        self.assertEqual(12, self.radiobutton.preferred_width)

    def test_preferred_height(self):
        self.radiobutton.text = 'Hello.42'
        self.assertEqual(0, self.radiobutton.preferred_height)

    def test_interface(self):
        self.radiobutton.text = 'Test Interface'
        self.radiobutton.active = False
        self.assertEqual('( ) ', self.radiobutton.interface)
        self.radiobutton.active = True
        self.assertEqual('(*) ', self.radiobutton.interface)
        self.radiobutton.active = False
        self.assertEqual('( ) ', self.radiobutton.interface)

    def test_draw_widget_in_area(self):
        self.radiobutton.text = 'Test Draw Widget In Area'
        self.radiobutton.active = True
        GLXCurses.Application().has_default = self.radiobutton
        GLXCurses.Application().has_focus = self.radiobutton
        GLXCurses.Application().has_prelight = self.radiobutton
        self.radiobutton.draw_widget_in_area()
        GLXCurses.Application().has_default = None
        GLXCurses.Application().has_focus = None
        GLXCurses.Application().has_prelight = None
        self.radiobutton.draw_widget_in_area()
        self.radiobutton.active = False
        self.radiobutton.draw_widget_in_area()


if __name__ == '__main__':
    unittest.main()
