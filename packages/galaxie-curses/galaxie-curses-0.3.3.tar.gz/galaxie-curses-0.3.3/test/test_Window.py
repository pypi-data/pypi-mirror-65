#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import unittest
import os
import curses
import GLXCurses

term = os.environ.get('TERM')


# Unittest
class TestWindow(unittest.TestCase):
    # Test Property
    def test_accept_focus(self):
        window = GLXCurses.Window()
        self.assertTrue(window.accept_focus)
        window.accept_focus = False
        self.assertFalse(window.accept_focus)
        self.assertRaises(TypeError, setattr, window, 'accept_focus', None)

    def test_application(self):
        window = GLXCurses.Window()
        self.assertIsNone(window.application)
        window.application = GLXCurses.Application()
        self.assertEqual(GLXCurses.Application(), window.application)

    def test_attached_to(self):
        window1 = GLXCurses.Window()
        window2 = GLXCurses.Window()

        window1.attached_to = window2
        self.assertEqual(window2, window1.attached_to)

        window1.attached_to = None
        self.assertEqual(None, window1.attached_to)

        self.assertRaises(TypeError, setattr, window1, 'attached_to', 42)

    def test_decorated(self):
        window = GLXCurses.Window()
        self.assertFalse(window.decorated)

        window.decorated = True
        self.assertTrue(window.decorated)

        self.assertRaises(TypeError, setattr, window, 'decorated', None)

    def test_default_height(self):
        window = GLXCurses.Window()
        self.assertEqual(0, window.default_height)
        window.default_height = None
        self.assertEqual(0, window.default_height)
        window.default_height = 42
        self.assertEqual(42, window.default_height)
        window.default_height = -1
        self.assertEqual(-1, window.default_height)

        self.assertRaises(TypeError, setattr, window, 'default_height', 'Hello')
        self.assertRaises(ValueError, setattr, window, 'default_height', -42)

    def test_default_width(self):
        window = GLXCurses.Window()
        self.assertEqual(0, window.default_width)
        window.default_width = None
        self.assertEqual(0, window.default_width)
        window.default_width = 42
        self.assertEqual(42, window.default_width)
        window.default_width = -1
        self.assertEqual(-1, window.default_width)

        self.assertRaises(TypeError, setattr, window, 'default_width', 'Hello')
        self.assertRaises(ValueError, setattr, window, 'default_width', -42)

    def test_deletable(self):
        window = GLXCurses.Window()
        self.assertFalse(window.deletable)

        window.deletable = True
        self.assertTrue(window.deletable)

        window.deletable = None
        self.assertFalse(window.deletable)

        self.assertRaises(TypeError, setattr, window, 'deletable', 'Hello')

    def test_destroy_with_parent(self):
        window = GLXCurses.Window()
        self.assertFalse(window.destroy_with_parent)
        window.destroy_with_parent = None
        self.assertFalse(window.destroy_with_parent)
        window.destroy_with_parent = True
        self.assertTrue(window.destroy_with_parent)

        self.assertRaises(TypeError, setattr, window, 'destroy_with_parent', 'Hello')

    def test_focus_on_map(self):
        window = GLXCurses.Window()
        self.assertTrue(window.focus_on_map)
        window.focus_on_map = False
        self.assertFalse(window.focus_on_map)
        window.focus_on_map = None
        self.assertTrue(window.focus_on_map)

        self.assertRaises(TypeError, setattr, window, 'focus_on_map', 'Hello')

    def test_focus_visible(self):
        window = GLXCurses.Window()
        self.assertTrue(window.focus_visible)
        window.focus_visible = False
        self.assertFalse(window.focus_visible)
        window.focus_visible = None
        self.assertTrue(window.focus_visible)

        self.assertRaises(TypeError, setattr, window, 'focus_visible', 'Hello')

    def test_gravity(self):
        window = GLXCurses.Window()
        self.assertEqual(GLXCurses.GLXC.GRAVITY_NORTH_WEST, window.gravity)
        window.gravity = GLXCurses.GLXC.GRAVITY_CENTER
        self.assertEqual(GLXCurses.GLXC.GRAVITY_CENTER, window.gravity)
        window.gravity = None
        self.assertEqual(GLXCurses.GLXC.GRAVITY_NORTH_WEST, window.gravity)

        self.assertRaises(TypeError, setattr, window, 'gravity', 42)
        self.assertRaises(ValueError, setattr, window, 'gravity', 'Hello')

    def test_has_resize_grip(self):
        window = GLXCurses.Window()
        self.assertFalse(window.has_resize_grip)
        window.has_resize_grip = False
        self.assertFalse(window.has_resize_grip)
        window.has_resize_grip = None
        self.assertFalse(window.has_resize_grip)

        self.assertRaises(TypeError, setattr, window, 'has_resize_grip', 'Hello')

    def test_has_toplevel_focus(self):
        window = GLXCurses.Window()
        self.assertFalse(window.has_toplevel_focus)
        window.has_toplevel_focus = False
        self.assertFalse(window.has_toplevel_focus)
        window.has_toplevel_focus = None
        self.assertFalse(window.has_toplevel_focus)

        self.assertRaises(TypeError, setattr, window, 'has_toplevel_focus', 'Hello')

    def test_hide_titlebar_when_maximized(self):
        window = GLXCurses.Window()
        self.assertFalse(window.hide_titlebar_when_maximized)
        window.hide_titlebar_when_maximized = False
        self.assertFalse(window.hide_titlebar_when_maximized)
        window.hide_titlebar_when_maximized = None
        self.assertFalse(window.hide_titlebar_when_maximized)

        self.assertRaises(TypeError, setattr, window, 'hide_titlebar_when_maximized', 'Hello')

    def test_icon(self):
        window = GLXCurses.Window()
        self.assertEqual(curses.ACS_DIAMOND, window.icon)
        window.icon = curses.ACS_CKBOARD
        self.assertEqual(curses.ACS_CKBOARD, window.icon)

        window.icon = None
        self.assertEqual(curses.ACS_DIAMOND, window.icon)

        self.assertRaises(TypeError, setattr, window, 'icon', 'Hello')

    def test_icon_name(self):
        window = GLXCurses.Window()
        self.assertEqual(None, window.icon_name)
        window.icon_name = 'Hello.42'
        self.assertEqual('Hello.42', window.icon_name)

        window.icon_name = None
        self.assertEqual(None, window.icon_name)

        self.assertRaises(TypeError, setattr, window, 'icon_name', 42)

    def test_is_active(self):
        window = GLXCurses.Window()
        self.assertFalse(window.is_active)
        window.is_active = True
        self.assertTrue(window.is_active)
        window.is_active = None
        self.assertFalse(window.is_active)

        self.assertRaises(TypeError, setattr, window, 'is_active', 'Hello')

    def test_is_maximized(self):
        window = GLXCurses.Window()
        self.assertFalse(window.is_maximized)
        window.is_maximized = True
        self.assertTrue(window.is_maximized)
        window.is_maximized = None
        self.assertFalse(window.is_maximized)

        self.assertRaises(TypeError, setattr, window, 'is_maximized', 'Hello')

    def test_mnemonics_visible(self):
        window = GLXCurses.Window()
        self.assertTrue(window.mnemonics_visible)
        window.mnemonics_visible = False
        self.assertFalse(window.mnemonics_visible)
        window.mnemonics_visible = None
        self.assertTrue(window.mnemonics_visible)

        self.assertRaises(TypeError, setattr, window, 'mnemonics_visible', 'Hello')

    def test_modal(self):
        window = GLXCurses.Window()
        self.assertFalse(window.modal)
        window.modal = True
        self.assertTrue(window.modal)
        window.modal = None
        self.assertFalse(window.modal)

        self.assertRaises(TypeError, setattr, window, 'modal', 'Hello')

    def test_role(self):
        window = GLXCurses.Window()
        self.assertIsNone(window.role)
        window.role = 'Hello.42'
        self.assertEqual('Hello.42', window.role)
        window.role = None
        self.assertIsNone(window.role)

        self.assertRaises(TypeError, setattr, window, 'role', 42)

    def test_screen(self):
        window = GLXCurses.Window()
        screen = GLXCurses.Screen()
        self.assertIsNone(window.screen)
        window.screen = screen
        self.assertEqual(screen, window.screen)
        window.screen = None
        self.assertIsNone(window.screen)

        self.assertRaises(TypeError, setattr, window, 'screen', 42)

    def test_skip_pager_hint(self):
        window = GLXCurses.Window()
        self.assertFalse(window.skip_pager_hint)
        window.skip_pager_hint = True
        self.assertTrue(window.skip_pager_hint)
        window.skip_pager_hint = None
        self.assertFalse(window.skip_pager_hint)

        self.assertRaises(TypeError, setattr, window, 'skip_pager_hint', 42)

    def test_skip_taskbar_hint(self):
        window = GLXCurses.Window()
        self.assertFalse(window.skip_taskbar_hint)
        window.skip_taskbar_hint = True
        self.assertTrue(window.skip_taskbar_hint)
        window.skip_taskbar_hint = None
        self.assertFalse(window.skip_taskbar_hint)

        self.assertRaises(TypeError, setattr, window, 'skip_taskbar_hint', 42)

    def test_startup_id(self):
        window = GLXCurses.Window()
        self.assertIsNone(window.startup_id)
        window.startup_id = 'Hello.42'
        self.assertEqual('Hello.42', window.startup_id)
        window.startup_id = None
        self.assertIsNone(window.startup_id)

        self.assertRaises(TypeError, setattr, window, 'startup_id', 42)

    def test_title(self):
        window = GLXCurses.Window()
        self.assertIsNone(window.title)
        window.title = 'Hello.42'
        self.assertEqual('Hello.42', window.title)
        window.title = None
        self.assertIsNone(window.title)
        self.assertRaises(TypeError, setattr, window, 'title', 42)

    def test_type(self):
        window = GLXCurses.Window()
        self.assertEqual(GLXCurses.GLXC.WINDOW_TOPLEVEL, window.type)
        window.type = GLXCurses.GLXC.WINDOW_POPUP
        self.assertEqual(GLXCurses.GLXC.WINDOW_POPUP, window.type)
        window.type = None
        self.assertEqual(GLXCurses.GLXC.WINDOW_TOPLEVEL, window.type)

        self.assertRaises(TypeError, setattr, window, 'type', 42)
        self.assertRaises(ValueError, setattr, window, 'type', 'Hello.42')

    def test_type_hint(self):
        window = GLXCurses.Window()
        self.assertEqual(GLXCurses.GLXC.WINDOW_TYPE_HINT_NORMAL, window.type_hint)
        for hint in [
            GLXCurses.GLXC.WINDOW_TYPE_HINT_NORMAL,
            GLXCurses.GLXC.WINDOW_TYPE_HINT_DIALOG,
            GLXCurses.GLXC.WINDOW_TYPE_HINT_MENU,
            GLXCurses.GLXC.WINDOW_TYPE_HINT_TOOLBAR,
            GLXCurses.GLXC.WINDOW_TYPE_HINT_SPLASHSCREEN,
            GLXCurses.GLXC.WINDOW_TYPE_HINT_UTILITY,
            GLXCurses.GLXC.WINDOW_TYPE_HINT_DOCK,
            GLXCurses.GLXC.WINDOW_TYPE_HINT_DESKTOP
        ]:
            window.type_hint = hint
            self.assertEqual(hint, window.type_hint)
        window.type_hint = None
        self.assertEqual(GLXCurses.GLXC.WINDOW_TYPE_HINT_NORMAL, window.type_hint)
        self.assertRaises(TypeError, setattr, window, 'type_hint', 42)
        self.assertRaises(ValueError, setattr, window, 'type_hint', 'Hello.42')

    def test_urgency_hint(self):
        window = GLXCurses.Window()
        self.assertFalse(window.urgency_hint)
        window.urgency_hint = True
        self.assertTrue(window.urgency_hint)
        window.urgency_hint = None
        self.assertFalse(window.urgency_hint)

        self.assertRaises(TypeError, setattr, window, 'urgency_hint', 'Hello')

    def test_window_position(self):
        window = GLXCurses.Window()
        self.assertEqual(GLXCurses.GLXC.WIN_POS_NONE, window.position)
        for position in [
            GLXCurses.GLXC.WIN_POS_NONE,
            GLXCurses.GLXC.WIN_POS_CENTER,
            GLXCurses.GLXC.WIN_POS_MOUSE,
            GLXCurses.GLXC.WIN_POS_CENTER_ALWAYS,
            GLXCurses.GLXC.WIN_POS_CENTER_ON_PARENT
        ]:
            window.position = position
            self.assertEqual(position, window.position)

        window.position = None
        self.assertEqual(GLXCurses.GLXC.WIN_POS_NONE, window.position)
        self.assertRaises(TypeError, setattr, window, 'position', 42)
        self.assertRaises(ValueError, setattr, window, 'position', 'Hello.42')

    def test_decoration_button_layout(self):
        window = GLXCurses.Window()
        self.assertEqual('menu:close', window.decoration_button_layout)
        window.decoration_button_layout = 'close'
        self.assertEqual('close', window.decoration_button_layout)
        window.decoration_button_layout = None
        self.assertEqual('menu:close', window.decoration_button_layout)

        self.assertRaises(TypeError, setattr, window, 'decoration_button_layout', 42)

    def test_decoration_resize_handle(self):
        window = GLXCurses.Window()
        self.assertEqual(0, window.decoration_resize_handle)
        window.decoration_resize_handle = 42
        self.assertEqual(42, window.decoration_resize_handle)
        window.decoration_resize_handle = None
        self.assertEqual(0, window.decoration_resize_handle)

        self.assertRaises(TypeError, setattr, window, 'decoration_resize_handle', 'Hello.42')
        self.assertRaises(ValueError, setattr, window, 'decoration_resize_handle', -42)

    # Test
    def test_window_glxc_type(self):
        """Test if Window is GLXCurses Type"""
        win = GLXCurses.Window()
        self.assertTrue(GLXCurses.glxc_type(win))

    def test_window_draw_widget_in_area(self):
        """Test Window.draw_widget_in_area()"""
        win = GLXCurses.Window()
        win.decorated = True
        win.title = 'GLXCurses Window tests'
        GLXCurses.Application().add_window(win)
        GLXCurses.Application().refresh()
        win.decorated = False
        GLXCurses.Application().refresh()
        win.decorated = True
        GLXCurses.Application().refresh()

    def test_window_add_accel_group(self):
        """Test Window.add_accel_group()"""
        window = GLXCurses.Window()
        self.assertRaises(NotImplementedError, window.add_accel_group)

    def test_window_remove_accel_group(self):
        """Test Window.remove_accel_group()"""
        window = GLXCurses.Window()
        self.assertRaises(NotImplementedError, window.remove_accel_group)

    def test_window_get_window_type(self):
        """Test Window.get_window_type()"""
        win = GLXCurses.Window()
        self.assertEqual(GLXCurses.GLXC.WINDOW_TOPLEVEL, win.get_window_type())


if __name__ == '__main__':
    unittest.main()
