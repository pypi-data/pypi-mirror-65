#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import GLXCurses


# Unittest
class TestArea(unittest.TestCase):

    def test_x(self):
        area = GLXCurses.Area()

        # Test default value
        self.assertEqual(None, area.x)

        # test if we can assign a value
        area.x = 42
        # can we get back ?
        self.assertEqual(42, area.x)

        # test error
        self.assertRaises(TypeError, setattr, area, 'x', 'Hello.42')

        # test None
        area.x = None
        self.assertEqual(None, area.x)

    def test_y(self):
        area = GLXCurses.Area()

        # Test default value
        self.assertEqual(None, area.y)

        # test if we can assign a value
        area.y = 42
        # can we get back ?
        self.assertEqual(42, area.y)

        # test error
        self.assertRaises(TypeError, setattr, area, 'y', 'Hello.42')

        # test None
        area.y = None
        self.assertEqual(None, area.y)

    def test_width(self):
        area = GLXCurses.Area()

        # Test default value
        self.assertEqual(None, area.width)

        # test if we can assign a value
        area.width = 42
        # can we get back ?
        self.assertEqual(42, area.width)

        # test error
        self.assertRaises(TypeError, setattr, area, 'width', 'Hello.42')

        # test None
        area.width = None
        self.assertEqual(None, area.width)

    def test_height(self):
        area = GLXCurses.Area()

        # Test default value
        self.assertEqual(None, area.height)

        # test if we can assign a value
        area.height = 42
        # can we get back ?
        self.assertEqual(42, area.height)

        # test error
        self.assertRaises(TypeError, setattr, area, 'height', 'Hello.42')

        # test None
        area.height = None
        self.assertEqual(None, area.height)

    def test_stdscr(self):
        """Test Area.set_screen()"""
        area = GLXCurses.Area()
        self.assertEqual(None, area.stdscr)

        area.stdscr = GLXCurses.Application().stdscr
        self.assertEqual(type(GLXCurses.Application().stdscr), type(area.stdscr))
        area.stdscr = None
        self.assertIsNone(area.stdscr)
        #
        self.assertRaises(TypeError, setattr, area, 'stdscr', 42)

    def test_subwin(self):
        """Test Area.subwin"""
        area = GLXCurses.Area()
        self.assertEqual(None, area.subwin)

        area.subwin = GLXCurses.Application().stdscr
        self.assertEqual(type(GLXCurses.Application().stdscr), type(area.subwin))
        area.subwin = None
        self.assertIsNone(area.subwin)

        self.assertRaises(TypeError, setattr, area, 'subwin', 42)

    def test_create_or_resize(self):
        area = GLXCurses.Area()
        area.stdscr = GLXCurses.Application().stdscr
        area.height, area.width = area.stdscr.getmaxyx()
        area.y, area.x = area.stdscr.getbegyx()
        area.create_or_resize()
        area.y = 42
        area.x = 42
        area.create_or_resize()
        area.height -= 1
        area.width -= 1
        area.create_or_resize()
        area.stdscr = None
