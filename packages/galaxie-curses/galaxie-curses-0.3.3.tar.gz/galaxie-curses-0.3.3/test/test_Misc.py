#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import sys
import os
from GLXCurses import Misc
from GLXCurses.Utils import glxc_type

# Require when you haven't GLXCurses as default Package
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(current_dir))


# Unittest
class TestMisc(unittest.TestCase):

    # Test
    def test_glxc_type(self):
        """Test Misc Type"""
        misc = Misc()
        self.assertTrue(glxc_type(misc))

    def test_xalign(self):
        misc = Misc()
        self.assertEqual(0.5, misc.xalign)
        misc.xalign = 1.0
        self.assertEqual(1.0, misc.xalign)
        misc.xalign = None
        self.assertEqual(0.5, misc.xalign)
        self.assertRaises(TypeError, setattr, misc, 'xalign', 'Hello.42')
        self.assertRaises(ValueError, setattr, misc, 'xalign', 4.2)

    def test_yalign(self):
        misc = Misc()
        self.assertEqual(0.5, misc.yalign)
        misc.yalign = 1.0
        self.assertEqual(1.0, misc.yalign)
        misc.yalign = None
        self.assertEqual(0.5, misc.yalign)
        self.assertRaises(TypeError, setattr, misc, 'yalign', 'Hello.42')
        self.assertRaises(ValueError, setattr, misc, 'yalign', 4.2)

    def test_xpad(self):
        misc = Misc()
        self.assertEqual(0, misc.xpad)
        misc.xpad = 42
        self.assertEqual(42, misc.xpad)
        misc.xpad = None
        self.assertEqual(0, misc.xpad)
        self.assertRaises(TypeError, setattr, misc, 'xpad', 'Hello.42')
        self.assertRaises(ValueError, setattr, misc, 'xpad', -42)

    def test_ypad(self):
        misc = Misc()
        self.assertEqual(0, misc.ypad)
        misc.ypad = 42
        self.assertEqual(42, misc.ypad)
        misc.ypad = None
        self.assertEqual(0, misc.ypad)
        self.assertRaises(TypeError, setattr, misc, 'ypad', 'Hello.42')
        self.assertRaises(ValueError, setattr, misc, 'ypad', -42)
