#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import unittest
import GLXCurses


class TestLabel(unittest.TestCase):
    def test_Label_get_justify(self):
        """Test Label.get_justify()"""
        label = GLXCurses.Label()
        self.assertEqual(GLXCurses.GLXC.JUSTIFY_LEFT, label.get_justify())

        label.justify = GLXCurses.GLXC.JUSTIFY_RIGHT
        self.assertEqual(GLXCurses.GLXC.JUSTIFY_RIGHT, label.get_justify())

    def test_Label_set_justify(self):
        """Test Label.set_justify()"""
        label = GLXCurses.Label()

        self.assertEqual(GLXCurses.GLXC.JUSTIFY_LEFT, label.justify)

        for jutify in GLXCurses.GLXC.Justification:
            label.set_justify(jutify)
            self.assertEqual(jutify, label.justify)

        self.assertRaises(TypeError, label.set_justify, 'Hello')

    def test_Label_get_line_wrap(self):
        """Test Label.get_line_wrap()"""
        label = GLXCurses.Label()
        self.assertEqual(False, label.get_line_wrap())

        label.wrap = True
        self.assertEqual(True, label.get_line_wrap())

    def test_Label_set_line_wrap(self):
        """Test Label.set_line_wrape()"""
        label = GLXCurses.Label()
        self.assertEqual(False, label.wrap)

        label.set_line_wrap(True)
        self.assertEqual(True, label.wrap)

        self.assertRaises(TypeError, label.set_line_wrap, 'Hello')

    def test_Label_get_width_chars(self):
        """Test Label.get_width_chars()"""
        label = GLXCurses.Label()
        self.assertEqual(-1, label.get_width_chars())

        label.width_chars = 42
        self.assertEqual(42, label.get_width_chars())

    def test_Label_set_width_chars(self):
        """Test Label.set_width_chars()"""
        label = GLXCurses.Label()
        self.assertEqual(-1, label.width_chars)

        label.set_width_chars(42)
        self.assertEqual(42, label.width_chars)

        self.assertRaises(TypeError, label.set_width_chars, 'Hello')

    def test_text(self):
        label = GLXCurses.Label()
        self.assertIsNone(label.text)

        label.text = 'Hello.42'
        self.assertEqual('Hello.42', label.text)

        label.text = None
        self.assertIsNone(label.text)

        self.assertRaises(TypeError, setattr, label, 'text', 42)


if __name__ == '__main__':
    unittest.main()
