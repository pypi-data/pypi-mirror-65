#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import unittest

from GLXCurses import Widget
from GLXCurses import Window
from GLXCurses import Object
from GLXCurses import HBox
from GLXCurses import Style
from GLXCurses.Utils import glxc_type
from GLXCurses.Constants import GLXC


# Unittest
class TestWidget(unittest.TestCase):
    def test_preferred_height(self):
        widget = Widget()
        self.assertEqual(0, widget.preferred_height)
        widget.preferred_height = 42
        self.assertEqual(42, widget.preferred_height)
        widget.preferred_height = None
        self.assertEqual(0, widget.preferred_height)

        self.assertRaises(TypeError, setattr, widget, 'preferred_height', 'Hello.42')

    def test_preferred_width(self):
        widget = Widget()
        self.assertEqual(0, widget.preferred_width)
        widget.preferred_width = 42
        self.assertEqual(42, widget.preferred_width)
        widget.preferred_width = None
        self.assertEqual(0, widget.preferred_width)

        self.assertRaises(TypeError, setattr, widget, 'preferred_width', 'Hello.42')

    # Test property's
    def test_app_paintable(self):
        """Test Widget app_paintable property"""
        widget = Widget()
        self.assertFalse(widget.app_paintable)

        widget.app_paintable = True
        self.assertTrue(widget.app_paintable)

        self.assertRaises(TypeError, setattr, widget, 'app_paintable', None)

    def test_can_default(self):
        """Test Widget can_default property"""
        widget = Widget()
        self.assertFalse(widget.can_default)

        widget.can_default = True
        self.assertTrue(widget.can_default)

        self.assertRaises(TypeError, setattr, widget, 'can_default', None)

    def test_can_focus(self):
        """Test Widget can_focus property"""
        widget = Widget()
        self.assertFalse(widget.can_focus)

        widget.can_focus = True
        self.assertTrue(widget.can_focus)

        self.assertRaises(TypeError, setattr, widget, 'can_focus', None)

    def test_can_prelight(self):
        """Test Widget prelight property"""
        widget = Widget()
        self.assertFalse(widget.can_prelight)

        widget.can_prelight = True
        self.assertTrue(widget.can_prelight)

        self.assertRaises(TypeError, setattr, widget, 'can_prelight', None)

    def test_composite_child(self):
        """Test Widget composite_child property"""
        widget = Widget()
        self.assertFalse(widget.composite_child)

        widget.composite_child = True
        self.assertTrue(widget.composite_child)

        self.assertRaises(TypeError, setattr, widget, 'composite_child', None)

    def test_expand(self):
        """Test Widget expand property"""
        widget = Widget()
        self.assertFalse(widget.expand)

        widget.expand = True
        self.assertTrue(widget.expand)

        self.assertRaises(TypeError, setattr, widget, 'expand', None)

    def test_focus_on_click(self):
        """Test Widget focus_on_click property"""
        widget = Widget()
        self.assertTrue(widget.focus_on_click)

        widget.focus_on_click = False
        self.assertFalse(widget.focus_on_click)

        self.assertRaises(TypeError, setattr, widget, 'focus_on_click', None)

    def test_halign(self):
        """Test Widget halign property"""
        widget = Widget()
        self.assertEqual(GLXC.ALIGN_FILL, widget.halign)

        for align_type in GLXC.Align:
            widget.halign = align_type
            self.assertEqual(align_type, widget.halign)

        widget.halign = None
        self.assertEqual(GLXC.ALIGN_FILL, widget.halign)

        self.assertRaises(TypeError, setattr, widget, 'halign', 'Hello')

    def test_has_default(self):
        """Test Widget has_default property"""
        widget = Widget()
        self.assertFalse(widget.has_default)

        widget.has_default = True
        self.assertTrue(widget.has_default)
        widget.has_default = None
        self.assertFalse(widget.has_default)

        self.assertRaises(TypeError, setattr, widget, 'has_default', 'Hello.42')

    def test_has_focus(self):
        """Test Widget has_focus property"""
        widget = Widget()
        self.assertFalse(widget.has_focus)

        widget.has_focus = True
        self.assertTrue(widget.has_focus)
        widget.has_focus = None
        self.assertFalse(widget.has_focus)

        self.assertRaises(TypeError, setattr, widget, 'has_focus', 'Hello.42')

    def test_has_prelight(self):
        widget = Widget()
        self.assertFalse(widget.has_prelight)

        widget.has_prelight = True
        self.assertTrue(widget.has_prelight)
        widget.has_prelight = None
        self.assertFalse(widget.has_prelight)

        self.assertRaises(TypeError, setattr, widget, 'has_prelight', 'Hello.42')

    def test_has_tooltip(self):
        """Test Widget has_tooltip property"""
        widget = Widget()
        self.assertFalse(widget.has_tooltip)

        widget.has_tooltip = True
        self.assertTrue(widget.has_tooltip)

        self.assertRaises(TypeError, setattr, widget, 'has_tooltip', None)

    def test_has_window(self):
        widget = Widget()
        self.assertTrue(widget.has_window)
        widget.has_window = False
        self.assertFalse(widget.has_window)
        widget.has_window = None
        self.assertTrue(widget.has_window)
        self.assertRaises(TypeError, setattr, widget, 'has_window', 'Hello.42')

    def test_height_request(self):
        """Test Widget height_request property"""
        widget = Widget()
        self.assertEqual(-1, widget.height_request)

        widget.height_request = 0
        self.assertEqual(0, widget.height_request)

        widget.height_request = 42
        self.assertEqual(42, widget.height_request)

        widget.height_request = -1
        self.assertEqual(-1, widget.height_request)

        self.assertRaises(TypeError, setattr, widget, 'height_request', -2)
        self.assertRaises(TypeError, setattr, widget, 'height_request', None)

    def test_hexpand(self):
        """Test Widget hexpand property"""
        # Create a widget
        widget = Widget()
        # Test the default value
        self.assertFalse(widget.hexpand)
        # Look if it work
        widget.hexpand = True
        self.assertTrue(widget.hexpand)
        # Test if we can back to default
        widget.hexpand = None
        self.assertFalse(widget.hexpand)
        # Test Error
        self.assertRaises(TypeError, setattr, widget, 'hexpand', 'Hello')

    def test_hexpand_set(self):
        """Test Widget hexpand_set property"""
        # Create a widget
        widget = Widget()
        # Test the default value
        self.assertFalse(widget.hexpand_set)
        # Look if it work
        widget.hexpand_set = True
        self.assertTrue(widget.hexpand_set)
        # Test if we can back to default
        widget.hexpand_set = None
        self.assertFalse(widget.hexpand_set)
        # Test Error
        self.assertRaises(TypeError, setattr, widget, 'hexpand_set', 'Hello')

    def test_margin(self):
        """Test Widget margin property"""
        widget = Widget()

        self.assertEqual(0, widget.margin)

        widget.margin = 42
        self.assertEqual(42, widget.margin)

        self.assertRaises(TypeError, setattr, widget, 'margin', -1)
        self.assertRaises(TypeError, setattr, widget, 'margin', 32768)
        self.assertRaises(TypeError, setattr, widget, 'margin', None)

    def test_margin_bottom(self):
        """Test Widget margin_bottom property"""
        widget = Widget()

        self.assertEqual(0, widget.margin_bottom)

        widget.margin_bottom = 42
        self.assertEqual(42, widget.margin_bottom)

        self.assertRaises(TypeError, setattr, widget, 'margin_bottom', -1)
        self.assertRaises(TypeError, setattr, widget, 'margin_bottom', 32768)
        self.assertRaises(TypeError, setattr, widget, 'margin_bottom', None)

    def test_margin_end(self):
        """Test Widget margin_end property"""
        widget = Widget()

        self.assertEqual(0, widget.margin_end)

        widget.margin_end = 42
        self.assertEqual(42, widget.margin_end)

        self.assertRaises(TypeError, setattr, widget, 'margin_end', -1)
        self.assertRaises(TypeError, setattr, widget, 'margin_end', 32768)
        self.assertRaises(TypeError, setattr, widget, 'margin_end', None)

    def test_margin_start(self):
        """Test Widget margin_start property"""
        widget = Widget()

        self.assertEqual(0, widget.margin_start)

        widget.margin_start = 42
        self.assertEqual(42, widget.margin_start)

        self.assertRaises(TypeError, setattr, widget, 'margin_start', -1)
        self.assertRaises(TypeError, setattr, widget, 'margin_start', 32768)
        self.assertRaises(TypeError, setattr, widget, 'margin_start', None)

    def test_margin_top(self):
        """Test Widget margin_top property"""
        widget = Widget()

        self.assertEqual(0, widget.margin_top)

        widget.margin_top = 42
        self.assertEqual(42, widget.margin_top)

        self.assertRaises(TypeError, setattr, widget, 'margin_top', -1)
        self.assertRaises(TypeError, setattr, widget, 'margin_top', 32768)
        self.assertRaises(TypeError, setattr, widget, 'margin_top', None)

    def test_name(self):
        """Test Widget name property"""
        widget = Widget()

        self.assertEqual(None, widget.name)

        widget.name = "Hello"
        self.assertEqual("Hello", widget.name)

        widget.name = None
        self.assertEqual(None, widget.name)

        self.assertRaises(TypeError, setattr, widget, 'name', 42)

    def test_no_show_all(self):
        """Test Widget no_show_all property"""
        widget = Widget()
        self.assertFalse(widget.no_show_all)

        widget.no_show_all = True
        self.assertTrue(widget.no_show_all)

        self.assertRaises(TypeError, setattr, widget, 'no_show_all', None)

    def test_parent(self):
        """Test Widget parent Property"""
        widget = Widget()
        self.assertEqual(None, widget.parent)
        widget.parent = Window()

        self.assertTrue(isinstance(widget.parent, Window))

        widget.parent = None
        self.assertEqual(None, widget.parent)

        self.assertRaises(TypeError, setattr, widget, 'parent', 'Hello')

    def test_receives_default(self):
        """Test Widget().receives_default property"""
        widget = Widget()

        self.assertFalse(widget.receives_default)

        widget.receives_default = True

        self.assertTrue(widget.receives_default)

        self.assertRaises(TypeError, setattr, widget, 'receives_default', 42)

    def test_sensitive(self):
        """Test Widget().sensitive property"""
        widget = Widget()

        self.assertTrue(widget.sensitive)

        widget.sensitive = False

        self.assertFalse(widget.sensitive)

        self.assertRaises(TypeError, setattr, widget, 'sensitive', 42)

    def test_style(self):
        """Test Widget().style property"""
        widget = Widget()
        self.assertTrue(isinstance(widget.style, Style))

        old_style = widget.style
        new_style = Style()

        widget.style = new_style

        self.assertNotEqual(old_style, widget.style)

        self.assertRaises(TypeError, setattr, widget, 'style', 42)

    def test_tooltip_text(self):
        """Test Widget().tooltip_text property"""
        widget = Widget()
        # Test default value
        self.assertEqual(None, widget.tooltip_text)
        self.assertFalse(widget.has_tooltip)

        # Try to a __text
        widget.tooltip_text = "Hello"
        self.assertEqual("Hello", widget.tooltip_text)
        self.assertTrue(widget.has_tooltip)

        # Permit to return to the default value
        widget.tooltip_text = None
        self.assertEqual(None, widget.tooltip_text)
        self.assertFalse(widget.has_tooltip)

        self.assertRaises(TypeError, setattr, widget, 'tooltip_text', 42)

    def test_valign(self):
        """Test Widget().valign property"""
        widget = Widget()
        self.assertEqual(GLXC.ALIGN_FILL, widget.valign)

        for align_type in GLXC.Align:
            widget.valign = align_type
            self.assertEqual(align_type, widget.valign)

        widget.valign = None
        self.assertEqual(GLXC.ALIGN_FILL, widget.valign)

        self.assertRaises(TypeError, setattr, widget, 'valign', 'Hello')

    def test_vexpand(self):
        """Test Widget().vexpand property"""
        # Create a new Widget
        widget = Widget()
        # check the default value
        self.assertFalse(widget.vexpand)
        # Test if it work
        widget.vexpand = True
        self.assertTrue(widget.vexpand)
        # Test if we back on default value
        widget.vexpand = None
        self.assertFalse(widget.vexpand)
        # Test Error
        self.assertRaises(TypeError, setattr, widget, 'vexpand', 'Hello')

    def test_vexpand_set(self):
        """Test Widget().vexpand property"""
        # create a new Widget
        widget = Widget()
        # check the default value
        self.assertFalse(widget.vexpand_set)
        # Test if it work
        widget.vexpand_set = True
        self.assertTrue(widget.vexpand_set)
        # Test if we back on default value
        widget.vexpand_set = None
        self.assertFalse(widget.vexpand_set)
        # Test Error
        self.assertRaises(TypeError, setattr, widget, 'vexpand_set', 'Hello')

    def test_visible(self):
        """Test Widget().visible property"""
        # create a new Widget
        widget = Widget()
        # check the default value
        self.assertFalse(widget.visible)
        # Test if it work
        widget.visible = True
        self.assertTrue(widget.visible)
        # Test if we back on default value
        widget.visible = None
        self.assertFalse(widget.visible)
        # Test Error
        self.assertRaises(TypeError, setattr, widget, 'visible', 'Hello')

    def test_width_request(self):
        """Test Widget width_request property"""
        widget = Widget()
        self.assertEqual(-1, widget.width_request)

        widget.width_request = 0
        self.assertEqual(0, widget.width_request)

        widget.width_request = 42
        self.assertEqual(42, widget.width_request)

        widget.width_request = -1
        self.assertEqual(-1, widget.width_request)

        self.assertRaises(TypeError, setattr, widget, 'width_request', -2)
        self.assertRaises(TypeError, setattr, widget, 'width_request', None)

    # Test
    def test_glxc_type(self):
        """Test Widget Type"""
        widget = Widget()
        self.assertTrue(glxc_type(widget))

    def test_Widget_new(self):
        """Test Widget.new()"""
        widget = Widget().new()
        old_id = widget.id
        widget = Widget().new()

        self.assertNotEqual(old_id, widget.id)

    def test_Widget_destroy(self):
        """Test Widget.destroy()"""
        widget1 = Widget().new()
        widget2 = Widget().new()
        # check default setting
        widget2.parent = Window()
        self.assertFalse(widget1.in_destruction)
        self.assertTrue(isinstance(widget2.parent, Window))

        widget2.destroy()
        self.assertTrue(widget2.in_destruction)
        self.assertEqual(widget2.parent, None)

    def test_in_destruction(self):
        """Test Widget.in_destruction()"""
        widget = Widget()
        # check default value
        self.assertFalse(widget.in_destruction)
        # Make test
        widget.in_destruction = True
        self.assertTrue(widget.in_destruction)
        widget.in_destruction = None
        self.assertFalse(widget.in_destruction)

        self.assertRaises(TypeError, setattr, widget, 'in_destruction', 42)

    def test_Widget_destroyed(self):
        """Test Widget.destroyed()"""
        widget = Widget()
        # check default value
        self.assertTrue(glxc_type(widget))
        self.assertEqual(isinstance(widget, Widget), True)

        widget.destroyed(widget_pointer=widget)
        self.assertFalse(glxc_type(widget))
        self.assertEqual(isinstance(widget, Widget), True)

        # check errors
        obj = Object()
        widget = Widget()
        # widget is not GLXCurses type
        self.assertRaises(TypeError, widget.destroyed, widget=42, widget_pointer=widget)
        # widget is not a GLXC.Widget
        self.assertRaises(TypeError, widget.destroyed, widget=obj, widget_pointer=widget)
        # widget_pointer is not GLXCurses type
        self.assertRaises(TypeError, widget.destroyed, widget=widget, widget_pointer=42)
        # widget_pointer is not a GLXC.Widget
        self.assertRaises(TypeError, widget.destroyed, widget=widget, widget_pointer=obj)

    def test_Widget_unparent(self):
        """Test Widget.unparent()"""
        # Check error
        obj = Object()
        widget = Widget()
        # widget is not GLXCurses type
        self.assertRaises(TypeError, widget.unparent, widget=42)
        # widget is not a GLXC.Widget
        self.assertRaises(TypeError, widget.unparent, widget=obj)

    def test_Widget_show(self):
        """Test Widget.show()"""
        widget = Widget()
        # check default value
        self.assertFalse(widget.flags['TOPLEVEL'])
        self.assertFalse(widget.flags['REALIZED'])
        self.assertFalse(widget.flags['MAPPED'])
        self.assertFalse(widget.flags['VISIBLE'])
        # test 1
        widget.show()
        self.assertFalse(widget.flags['TOPLEVEL'])
        self.assertFalse(widget.flags['REALIZED'])
        self.assertFalse(widget.flags['MAPPED'])
        self.assertTrue(widget.flags['VISIBLE'])
        # test 2
        widget.flags['TOPLEVEL'] = True
        widget.show()
        self.assertTrue(widget.flags['TOPLEVEL'])
        self.assertTrue(widget.flags['REALIZED'])
        self.assertTrue(widget.flags['MAPPED'])
        self.assertTrue(widget.flags['VISIBLE'])

    def test_Widget_show_now(self):
        """Test Widget.show()"""
        widget = Widget()
        # check default value
        self.assertFalse(widget.flags['REALIZED'])
        self.assertFalse(widget.flags['MAPPED'])
        self.assertFalse(widget.flags['VISIBLE'])
        # test 1
        widget.show_now()
        self.assertTrue(widget.flags['REALIZED'])
        self.assertTrue(widget.flags['MAPPED'])
        self.assertTrue(widget.flags['VISIBLE'])

    def test_Widget_show_all(self):
        """Test Widget.show_all()"""
        window = Window()
        window.flags['TOPLEVEL'] = True
        hobox1 = HBox()
        hobox2 = HBox()
        hobox3 = HBox()

        hobox1.pack_end(hobox2)
        hobox1.pack_end(hobox3)
        window.add(hobox1)

        # check default value
        self.assertTrue(window.flags['TOPLEVEL'])
        self.assertFalse(window.flags['REALIZED'])
        self.assertFalse(window.flags['MAPPED'])
        self.assertFalse(window.flags['VISIBLE'])

        self.assertFalse(hobox1.flags['TOPLEVEL'])
        self.assertFalse(hobox1.flags['REALIZED'])
        self.assertFalse(hobox1.flags['MAPPED'])
        self.assertFalse(hobox1.flags['VISIBLE'])

        self.assertFalse(hobox2.flags['TOPLEVEL'])
        self.assertFalse(hobox2.flags['REALIZED'])
        self.assertFalse(hobox2.flags['MAPPED'])
        self.assertFalse(hobox2.flags['VISIBLE'])

        self.assertFalse(hobox3.flags['TOPLEVEL'])
        self.assertFalse(hobox3.flags['REALIZED'])
        self.assertFalse(hobox3.flags['MAPPED'])
        self.assertFalse(hobox3.flags['VISIBLE'])
        #
        # test 1
        window.show_all()
        self.assertTrue(window.flags['TOPLEVEL'])
        self.assertTrue(window.flags['REALIZED'])
        self.assertTrue(window.flags['MAPPED'])
        self.assertTrue(window.flags['VISIBLE'])

        self.assertFalse(hobox1.flags['TOPLEVEL'])
        self.assertFalse(hobox1.flags['REALIZED'])
        self.assertFalse(hobox1.flags['MAPPED'])
        # self.assertTrue(hobox1.flags['VISIBLE'])

        self.assertFalse(hobox2.flags['TOPLEVEL'])
        self.assertFalse(hobox2.flags['REALIZED'])
        self.assertFalse(hobox2.flags['MAPPED'])
        # self.assertTrue(hobox2.flags['VISIBLE'])

        self.assertFalse(hobox3.flags['TOPLEVEL'])
        self.assertFalse(hobox3.flags['REALIZED'])
        self.assertFalse(hobox3.flags['MAPPED'])
        # self.assertTrue(hobox3.flags['VISIBLE'])

    def test_map(self):
        widget = Widget()
        self.assertFalse(widget.flags['MAPPED'])
        self.assertEqual(widget.map, widget.flags['MAPPED'])
        widget.map = True
        self.assertTrue(widget.flags['MAPPED'])
        self.assertEqual(widget.map, widget.flags['MAPPED'])
        widget.map = None
        self.assertFalse(widget.flags['MAPPED'])
        self.assertEqual(widget.map, widget.flags['MAPPED'])

        self.assertRaises(TypeError, setattr, widget.map, 'Hello.42')

    def test_realize(self):
        widget = Widget()
        self.assertFalse(widget.flags['REALIZED'])
        self.assertEqual(widget.realize, widget.flags['REALIZED'])
        widget.realize = True
        self.assertTrue(widget.flags['REALIZED'])
        self.assertEqual(widget.realize, widget.flags['REALIZED'])
        widget.realize = None
        self.assertFalse(widget.flags['REALIZED'])
        self.assertEqual(widget.realize, widget.flags['REALIZED'])

        self.assertRaises(TypeError, setattr, widget.realize, 'Hello.42')

    # def test_Widget_get_double_buffered(self):
    #     """Test Widget.get_double_buffered()"""
    #     widget = Widget()
    #     self.assertRaises(NotImplementedError, widget.get_double_buffered)
    #
    # def test_Widget_set_double_buffered(self):
    #     """Test Widget.set_double_buffered()"""
    #     widget = Widget()
    #     self.assertRaises(NotImplementedError, widget.set_double_buffered)
    def test_attribute_states(self):
        """Test Style.get_attribute_states()"""
        # Load a valid Style
        widget = Widget()
        style = Style()
        style.attribute_states = style.get_default_attribute_states()

        # Load the Valid Style
        attribute_states = style.attribute_states
        # Check first level dictionary
        self.assertEqual(type(attribute_states), type(dict()))
        # For each key's
        for attribute in ['text_fg', 'bg', 'light', 'dark', 'mid', 'text', 'base', 'black', 'white']:
            # Check if the key value is a dictionary
            self.assertEqual(type(attribute_states[attribute]), type(dict()))
            # For each key value, in that case a sub dictionary
            for state in ['STATE_NORMAL', 'STATE_ACTIVE', 'STATE_PRELIGHT', 'STATE_SELECTED', 'STATE_INSENSITIVE']:
                # Check if the key value is a string
                self.assertEqual(type(attribute_states[attribute][state]), type(str()))

        # Try to change style
        attribute_states = style.get_default_attribute_states()
        attribute_states['text_fg']['STATE_NORMAL'] = 'YELLOW'
        style.attribute_states = attribute_states

        # Check if not a dictionary
        self.assertRaises(TypeError, setattr, widget, 'attribute_states', float(42.42))

        # Check raise with wrong Style
        attribute_states = dict()

        # Check with a empty dictionary
        self.assertRaises(KeyError, setattr, widget, 'attribute_states', attribute_states)

        # Check with first level dictionary it look ok
        attribute_states['text_fg'] = dict()
        attribute_states['bg'] = dict()
        attribute_states['light'] = dict()
        attribute_states['dark'] = dict()
        attribute_states['mid'] = dict()
        attribute_states['__text'] = dict()
        attribute_states['base'] = dict()
        attribute_states['black'] = dict()
        attribute_states['white'] = dict()
        self.assertRaises(KeyError, setattr, widget, 'attribute_states', attribute_states)

        attribute_states = style.get_default_attribute_states()
        attribute_states['text_fg'] = list()
        self.assertRaises(TypeError, setattr, widget, 'attribute_states', attribute_states)

        attribute_states = style.get_default_attribute_states()
        attribute_states['text_fg']['STATE_NORMAL'] = int(42)
        self.assertRaises(TypeError, setattr, widget, 'attribute_states', attribute_states)


if __name__ == '__main__':
    unittest.main()
