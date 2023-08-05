#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from random import randint
import GLXCurses


# Unittest
class TestApplication(unittest.TestCase):
    # def setUp(self):
    #     # Before the test start
    #     application = GLXCurses.Application()
    #     # self.win_to_test = application.get_screen().subwin(
    #     #     0,
    #     #     0,
    #     #     0,
    #     #     0
    #     # )
    #     self.toolbar = None
    #     self.messagebar = None
    #     self.statusbar = None
    #     self.menubar = None
    #     self.window = None
    #

    # Test Size management
    # width
    def test_width(self):
        """Test Application.width property"""
        value_random_1 = int(randint(8, 250))
        application = GLXCurses.Application()
        application.width = value_random_1
        self.assertEqual(application.width, value_random_1)
        # Test Raise
        self.assertRaises(TypeError, application.width, float(randint(1, 250)))

    # height
    def test_height(self):
        """Test Application.height property"""
        application = GLXCurses.Application()
        value_random_1 = int(randint(8, 250))

        application.height = value_random_1
        self.assertEqual(application.height, value_random_1)

        # Test Raise
        self.assertRaises(TypeError, setattr, application, 'height', float(randint(1, 250)))

    def test_style(self):
        """Test Application.set_style()"""
        application = GLXCurses.Application()
        style = GLXCurses.Style()
        self.assertTrue(isinstance(application.style, GLXCurses.Style))

        application.style = style
        self.assertEqual(style, application.style)

        application.style = None
        self.assertTrue(isinstance(application.style, GLXCurses.Style))
        self.assertNotEquals(style, application.style)

        self.assertRaises(TypeError, setattr, application, 'style', 42)

    def test_add_window(self):
        """Test Application.add_window()"""
        application = GLXCurses.Application()
        # create a new window
        window = GLXCurses.Window()

        # check if window parent is not application
        self.assertNotEqual(window.parent, application)

        # check the size of the children windows list before add a window
        windows_list_size_before = len(application.children)

        # add a window to the application
        application.add_window(window)

        # check the size of the children windows list after add a window
        windows_list_size_after = len(application.children)

        # we must have one more children on the list
        self.assertGreater(windows_list_size_after, windows_list_size_before)

        # we get the last windows children element
        the_last_children_on_list = application.children[-1]

        # the last list element must contain the same reference to our window
        self.assertEqual(the_last_children_on_list.widget, window)

        # check if the application is the parent of our window
        self.assertEqual(window.parent, application)

        # test raise
        self.assertRaises(TypeError, application.add_window, int())

    def test_remove_window(self):
        """Test Application.remove_window()"""
        application = GLXCurses.Application()

        # create a new window
        window1 = GLXCurses.Window()
        window2 = GLXCurses.Window()

        # add a window to the application
        application.add_window(window1)

        # add a second window to the application
        application.add_window(window2)

        # the last list element must contain the same reference to our window
        self.assertEqual(application.active_window.widget, window2)

        application.remove_window(window2)

        # we get again the last windows children element
        self.assertEqual(application.active_window.widget, window1)

    def test_get_window_by_id(self):
        application = GLXCurses.Application()

        # create a new window
        window1 = GLXCurses.Window()
        window2 = GLXCurses.Window()

        # add a window to the application
        application.add_window(window1)

        # add a second window to the application
        application.add_window(window2)
        self.assertEqual(window1, application.get_window_by_id(identifier=window1.id).widget)
        self.assertEqual(window2, application.get_window_by_id(identifier=window2.id).widget)

    def test_active_window(self):
        """Test Application displayed Window"""
        app = GLXCurses.Application()
        win = GLXCurses.Window()
        self.assertIsNone(app.active_window)
        app.active_window = win
        self.assertEqual(win.id, app.active_window_id)

    # inhibit()
    # uninhibit()
    # is_inhibited()
    # prefers_app_menu()

    def test_refresh(self):
        """Test Application.refresh() method """
        application = GLXCurses.Application()
        application.refresh()

    def test_draw(self):
        """Test Application.draw() method """
        application = GLXCurses.Application()
        self.assertTrue(application, GLXCurses.Application)

    def test_set_get_tooltip(self):
        """Test Application.set_tooltip() and Application.get_tooltip()"""
        application = GLXCurses.Application()
        self.window = GLXCurses.Window()
        # nothing happen
        application.set_tooltip()
        # focus get_tooltip return None
        self.assertEqual(application.get_tooltip(), {
            'widget': None,
            'type': None,
            'id': None
        })
        # set_tooltip to the window
        application.set_tooltip(self.window)
        # check if the window have the focus
        self.assertEqual(application.get_tooltip()['id'], self.window.id)
        # Test None
        application.set_tooltip(None)
        # focus get_tooltip return None
        self.assertEqual(application.get_tooltip(), {
            'widget': None,
            'type': None,
            'id': None
        })

    # Test Internal methode
    def test__set_get_active_window_id(self):
        """Test Application._set_active_window_id() and Application._get_active_window_id()"""
        application = GLXCurses.Application()
        value1 = '1'
        value2 = '2'
        application.active_window_id = value1
        self.assertEqual(application.active_window_id, value1)
        self.assertNotEqual(application.active_window_id, value2)

        self.assertRaises(TypeError, setattr, application, 'active_window_id', float())

    def test_menubar(self):
        """Test menubar property"""
        application = GLXCurses.Application()
        menubar = GLXCurses.MenuBar()
        application.menubar = None
        self.assertIsNone(application.menubar)
        application.menubar = menubar
        self.assertEqual(application.menubar, menubar)
        application.menubar = None
        self.assertIsNone(application.menubar)
        self.assertRaises(TypeError, setattr, application, 'menubar', 42)

    def test_app_menu(self):
        """Test menubar property"""
        application = GLXCurses.Application()
        app_menu = GLXCurses.MenuBar()
        application.app_menu = None
        self.assertIsNone(application.app_menu)
        application.app_menu = app_menu
        self.assertEqual(application.app_menu, app_menu)
        application.app_menu = None
        self.assertIsNone(application.app_menu)
        self.assertRaises(TypeError, setattr, application, 'app_menu', 42)

    def test_children(self):
        """Test children property"""
        application = GLXCurses.Application()
        application.children = None
        self.assertEqual(application.children, [])
        application.children = ['Hello.42']
        self.assertEqual(application.children, ['Hello.42'])
        application.children = None
        self.assertEqual(application.children, [])
        self.assertRaises(TypeError, setattr, application, 'children', 42)

    def test_statusbar(self):
        """Test statusbar property"""
        application = GLXCurses.Application()
        statusbar = GLXCurses.StatusBar()
        application.statusbar = None
        self.assertIsNone(application.statusbar)
        application.statusbar = statusbar
        self.assertEqual(application.statusbar, statusbar)
        application.statusbar = None
        self.assertIsNone(application.statusbar)
        self.assertRaises(TypeError, setattr, application, 'statusbar', 42)

    def test_messagebar(self):
        """Test messagebar property"""
        application = GLXCurses.Application()
        messagebar = GLXCurses.MessageBar()
        application.messagebar = None
        self.assertIsNone(application.messagebar)
        application.messagebar = messagebar
        self.assertEqual(application.messagebar, messagebar)
        application.messagebar = None
        self.assertIsNone(application.messagebar)
        self.assertRaises(TypeError, setattr, application, 'messagebar', 42)

    def test_toolbar(self):
        """Test Application ToolBar"""
        application = GLXCurses.Application()
        toolbar = GLXCurses.ToolBar()
        application.toolbar = None
        self.assertIsNone(application.toolbar)
        application.toolbar = toolbar
        self.assertEqual(application.toolbar, toolbar)
        application.toolbar = None
        self.assertIsNone(application.toolbar)
        self.assertRaises(TypeError, setattr, application, 'toolbar', 42)

    def test_everything(self):
        """Test Application"""
        application = GLXCurses.Application()
        # Create a StatusBar
        self.menubar = GLXCurses.MenuBar()
        self.window = GLXCurses.Window()
        self.messagebar = GLXCurses.MessageBar()
        self.statusbar = GLXCurses.StatusBar()
        self.toolbar = GLXCurses.ToolBar()

        # Add the ToolBar to application and set ot parent
        application.menubar = self.menubar
        application.add_window(self.window)
        application.messagebar = self.messagebar
        application.statusbar = self.statusbar
        application.toolbar = self.toolbar
        # check if we have the same ToolBar

        # self.menubar.draw()
        # application.active_window.draw()
        # self.messagebar.draw()
        # self.statusbar.draw()
        # self.toolbar.draw()
