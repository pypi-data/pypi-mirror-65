#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import sys
import os
from GLXCurses import Object
from GLXCurses.Utils import glxc_type

# Require when you haven't GLXCurses as default Package
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(current_dir))


# Unittest
class TestObject(unittest.TestCase):

    # Test
    def test_glxc_type(self):
        """Test Misc Type"""
        the_object = Object()
        self.assertTrue(glxc_type(the_object))

    def test_id(self):
        the_object = Object()
        self.assertEqual(str, type(the_object.id))

        the_object.id = 'Hello.42'
        self.assertEqual('Hello.42', the_object.id)

        the_object.id = None
        self.assertNotEqual('Hello.42', the_object.id)
        self.assertEqual(str, type(the_object.id))

        self.assertRaises(TypeError, setattr, the_object, 'id', 42)

    def test_children_property(self):
        """Test children property"""
        the_object = Object()
        the_object.children = None
        self.assertEqual(the_object.children, [])
        the_object.children = ['Hello.42']
        self.assertEqual(the_object.children, ['Hello.42'])
        the_object.children = None
        self.assertEqual(the_object.children, [])
        self.assertRaises(TypeError, setattr, the_object, 'children', 42)

    def test_default_flags(self):
        """Test Object.get_default_flags()"""
        the_object = Object()
        default_flags = the_object.default_flags
        # Check first level dictionary
        self.assertEqual(type(default_flags), type(dict()))
        valid_flags = ['IN_DESTRUCTION',
                       'FLOATING',
                       'TOPLEVEL',
                       'NO_WINDOW',
                       'REALIZED',
                       'MAPPED',
                       'VISIBLE',
                       'SENSITIVE',
                       'PARENT_SENSITIVE',
                       'CAN_FOCUS',
                       'HAS_FOCUS',
                       'CAN_DEFAULT',
                       'HAS_DEFAULT',
                       'HAS_GRAB',
                       'RC_STYLE',
                       'COMPOSITE_CHILD',
                       'NO_REPARENT',
                       'APP_PAINTABLE',
                       'RECEIVES_DEFAULT',
                       'DOUBLE_BUFFERED'
                       ]

        # Check if all keys are present
        for key in valid_flags:
            self.assertTrue(key in default_flags)

        # check default value
        self.assertEqual(default_flags['IN_DESTRUCTION'], False)
        self.assertEqual(default_flags['FLOATING'], True)
        self.assertEqual(default_flags['TOPLEVEL'], False)
        self.assertEqual(default_flags['NO_WINDOW'], True)
        self.assertEqual(default_flags['REALIZED'], False)
        self.assertEqual(default_flags['MAPPED'], False)
        self.assertEqual(default_flags['VISIBLE'], False)
        self.assertEqual(default_flags['SENSITIVE'], True)
        self.assertEqual(default_flags['PARENT_SENSITIVE'], True)
        self.assertEqual(default_flags['CAN_FOCUS'], False)
        self.assertEqual(default_flags['HAS_FOCUS'], False)
        self.assertEqual(default_flags['CAN_DEFAULT'], False)
        self.assertEqual(default_flags['HAS_DEFAULT'], False)
        self.assertEqual(default_flags['HAS_GRAB'], False)
        self.assertEqual(default_flags['RC_STYLE'], 'Default.yml')
        self.assertEqual(default_flags['COMPOSITE_CHILD'], False)
        self.assertEqual(default_flags['NO_REPARENT'], 'unused')
        self.assertEqual(default_flags['APP_PAINTABLE'], False)
        self.assertEqual(default_flags['RECEIVES_DEFAULT'], False)
        self.assertEqual(default_flags['DOUBLE_BUFFERED'], False)

    def test_flags(self):
        """Test Object.set_flags() and Object.get_flags()"""
        the_object = Object()
        default_flags = the_object.default_flags

        the_object.flags = default_flags

        self.assertEqual(the_object.flags, default_flags)
        the_object.flags = None
        self.assertEqual(the_object.flags, default_flags)

        flags = dict()
        flags['IN_DESTRUCTION'] = False
        flags['FLOATING'] = True
        flags['TOPLEVEL'] = False
        flags['NO_WINDOW'] = True
        flags['REALIZED'] = False
        flags['MAPPED'] = False
        flags['VISIBLE'] = False
        flags['SENSITIVE'] = True
        flags['PARENT_SENSITIVE'] = True
        flags['CAN_FOCUS'] = False
        flags['HAS_FOCUS'] = True
        flags['CAN_DEFAULT'] = False
        flags['HAS_DEFAULT'] = False
        flags['HAS_GRAB'] = False
        flags['RC_STYLE'] = 'Default.yml'
        flags['COMPOSITE_CHILD'] = False
        flags['NO_REPARENT'] = 'unused'
        flags['APP_PAINTABLE'] = False
        flags['RECEIVES_DEFAULT'] = False
        flags['DOUBLE_BUFFERED'] = False
        flags['FOCUS_ON_CLICK'] = True
        the_object.flags = flags
        self.assertEqual(flags, the_object.flags)
        # Test raise error
        self.assertRaises(TypeError, setattr, the_object, 'flags', 42)
        self.assertRaises(ValueError, setattr, the_object, 'flags', {'Hello': 42})

    def test_destroy(self):
        """Test Object.destroy()"""
        the_object = Object()
        flags = the_object.flags
        self.assertEqual(flags['IN_DESTRUCTION'], False)
        the_object.destroy()
        self.assertEqual(flags['IN_DESTRUCTION'], True)

    def test_Object_debug(self):
        """Test debug property"""
        the_object = Object()

        self.assertEqual(False, the_object.debug)
        the_object.debug = None
        self.assertEqual(False, the_object.debug)

        the_object.debug = True
        self.assertEqual(True, the_object.debug)
        self.assertRaises(TypeError, setattr, the_object, 'debug', 'Hello.42')

    def test_Object_debug_level(self):
        """Test debug_level property"""
        the_object = Object()

        self.assertEqual(0, the_object.debug_level)
        the_object.debug_level = None
        self.assertEqual(0, the_object.debug_level)
        the_object.debug_level = 3
        self.assertEqual(3, the_object.debug_level)

        self.assertRaises(TypeError, setattr, the_object, 'debug_level', 'Hello.42')
        self.assertRaises(ValueError, setattr, the_object, 'debug_level', 42)
