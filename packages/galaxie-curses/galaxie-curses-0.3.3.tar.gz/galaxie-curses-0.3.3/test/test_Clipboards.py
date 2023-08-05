#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

from GLXCurses.Clipboards import Clipboard
from GLXCurses.Object import Object
from GLXCurses.Utils import glxc_type
from GLXCurses.Utils import get_os_temporary_dir
import unittest
import codecs
import json


# Unittest
class TestClipboards(unittest.TestCase):

    # Test
    def test_Clipboard_glxc_type(self):
        """Test Clipboards type"""
        clipboard = Clipboard()
        self.assertTrue(glxc_type(clipboard))

    def test_Clipboard_get(self):
        """Test Clipboard.get()"""
        clipboard = Clipboard()
        self.assertTrue(glxc_type(clipboard.get()))

    def test_Clipboard_set_text(self):
        """Test Clipboard.set_text()"""
        clipboard = Clipboard()
        the_thing = Object()
        clipboard.set_text(clipboard=None, text="Hello", length=-1)
        self.assertEqual(clipboard.text, "Hello")
        clipboard.set_text(clipboard=clipboard, text="Hello", length=-1)
        self.assertEqual(clipboard.text, "Hello")

        clipboard.set_text(clipboard=clipboard, text="Hello", length=0)
        self.assertEqual(clipboard.text, "")

        clipboard.set_text(clipboard=clipboard, text="Hello", length=2)
        self.assertEqual(clipboard.text, "He")

        clipboard.set_text(clipboard=clipboard, text="Hello", length=42)
        self.assertEqual(clipboard.text, "Hello")

        # clipboard is not a GLXC.Clipboard
        self.assertRaises(
            TypeError,
            clipboard.set_text,
            clipboard="Hello",
            text="Hello",
            length=-1
        )
        self.assertRaises(
            TypeError,
            clipboard.set_text,
            clipboard=the_thing,
            text="Hello",
            length=-1
        )
        # __text is not a str
        self.assertRaises(
            TypeError,
            clipboard.set_text,
            clipboard=clipboard,
            text=clipboard,
            length=-1
        )
        # length is not a int
        self.assertRaises(
            TypeError,
            clipboard.set_text,
            clipboard=clipboard,
            text="Hello",
            length="Hello"
        )

    def test_clipboard_wait_for_text(self):
        """Test Clipboard.wait_for_text()"""
        tested_text = 'Héllô 43'
        clipboard = Clipboard()
        the_thing = Object()

        # Test a empty clipboard
        clipboard.set_text(text=tested_text)
        clipboard.store()
        clipboard_content = clipboard.wait_for_text()
        self.assertEqual(tested_text, clipboard_content)

        # Test a full clipboard
        clipboard.set_text(clipboard=clipboard, text=tested_text)
        clipboard.store(clipboard=clipboard)
        clipboard_content = clipboard.wait_for_text(clipboard=clipboard)
        self.assertEqual(tested_text, clipboard_content)

        clipboard._use_pyperclip = False
        # Test a empty clipboard
        clipboard.set_text(text=tested_text)
        clipboard.store()
        clipboard_content = clipboard.wait_for_text()
        self.assertEqual(tested_text, clipboard_content)

        # Test a full clipboard
        clipboard.set_text(clipboard=clipboard, text=tested_text)
        clipboard.store(clipboard=clipboard)
        clipboard_content = clipboard.wait_for_text(clipboard=clipboard)
        self.assertEqual(tested_text, clipboard_content)

        # Check errors
        # clipboard is not a GLXC.Clipboard
        self.assertRaises(
            TypeError,
            clipboard.wait_for_text,
            clipboard="Hello"
        )
        self.assertRaises(
            TypeError,
            clipboard.wait_for_text,
            clipboard=the_thing,
        )

    def test_Clipboard_set_can_store(self):
        """Test Clipboard.set_can_store()"""
        clipboard = Clipboard()
        the_thing = Object()

        clipboard.can_store = False
        self.assertFalse(clipboard.can_store)
        clipboard.set_can_store()
        self.assertTrue(clipboard.can_store)

        # Check errors
        # clipboard is not a GLXC.Clipboard
        self.assertRaises(
            TypeError,
            clipboard.set_can_store,
            clipboard="Hello"
        )
        self.assertRaises(
            TypeError,
            clipboard.set_can_store,
            clipboard=the_thing,
        )

    def test_clipboard_store(self):
        """Test Clipboard.store()"""
        clipboard = Clipboard()
        the_thing = Object()

        # First try
        clipboard.set_text(clipboard=clipboard, text="Hello1")
        clipboard.store(clipboard=clipboard)
        with codecs.open(clipboard.file, mode='r', encoding='utf-8-sig') as f:
            clipboard_contents = json.load(f)
        self.assertEqual(clipboard_contents[clipboard.__class__.__name__]['__area_data'], clipboard.text)

        # Second try
        clipboard.set_text(clipboard=clipboard, text="Hello2")
        clipboard.store(clipboard=clipboard)
        with codecs.open(clipboard.file, mode='r', encoding='utf-8-sig') as f:
            clipboard_contents = json.load(f)
        self.assertEqual(clipboard_contents[clipboard.__class__.__name__]['__area_data'], clipboard.text)

        # With clipboard=None
        clipboard.set_text(text="hee")
        clipboard.store()

        clipboard._use_pyperclip = False

        # Frist try
        clipboard.set_text(clipboard=clipboard, text="Hello1")
        clipboard.store(clipboard=clipboard)

        with codecs.open(clipboard.file, mode='r', encoding='utf-8-sig') as f:
            clipboard_contents = json.load(f)
            f.close()
        self.assertEqual(clipboard_contents[clipboard.__class__.__name__]['__area_data'], clipboard.text)

        # Second try
        clipboard.set_text(clipboard=clipboard, text="Hello2")
        clipboard.store(clipboard=clipboard)
        with codecs.open(clipboard.file, mode="r", encoding='utf-8-sig') as f:
            clipboard_contents = json.load(f)
            f.close()
        self.assertEqual(clipboard_contents[clipboard.__class__.__name__]['__area_data'], clipboard.text)

        # With clipboard=None
        clipboard.set_text(text="hee")
        clipboard.store()

        # Check errors
        # clipboard is not a GLXC.Clipboard
        self.assertRaises(
            TypeError,
            clipboard.store,
            clipboard="Hello"
        )
        self.assertRaises(
            TypeError,
            clipboard.store,
            clipboard=the_thing,
        )

    def test_Clipboard__test_pyperclip(self):
        """Test Clipboard._test_pyperclip()"""
        clipboard = Clipboard()
        the_thing = Object()

        # Check errors
        # clipboard is not a GLXC.Clipboard
        self.assertRaises(
            TypeError,
            clipboard._test_pyperclip,
            clipboard="Hello"
        )
        self.assertRaises(
            TypeError,
            clipboard._test_pyperclip,
            clipboard=the_thing,
        )

    def test_Clipboard__pyperclip_paste(self):
        """Test Clipboard._pyperclip_paste()"""
        clipboard = Clipboard()
        the_thing = Object()

        if clipboard._use_pyperclip:
            clipboard.set_text(text='Hoooo yearrrr')
            clipboard.store()
            self.assertEqual(clipboard.text, clipboard._pyperclip_paste())

        # Check errors
        # clipboard is not a GLXC.Clipboard
        self.assertRaises(
            TypeError,
            clipboard._pyperclip_paste,
            clipboard="Hello"
        )
        self.assertRaises(
            TypeError,
            clipboard._pyperclip_paste,
            clipboard=the_thing,
        )

    def test_Clipboard__pyperclip_copy(self):
        """Test Clipboard._pyperclip_copy()"""
        clipboard = Clipboard()
        the_thing = Object()

        if clipboard._use_pyperclip:
            clipboard.set_text(text='Hoooo yearrrr')
            clipboard._pyperclip_copy()
            self.assertEqual(clipboard.text, clipboard._pyperclip_paste())

        # Check errors
        # clipboard is not a GLXC.Clipboard
        self.assertRaises(
            TypeError,
            clipboard._pyperclip_copy,
            clipboard="Hello"
        )
        self.assertRaises(
            TypeError,
            clipboard._pyperclip_copy,
            clipboard=the_thing,
        )

    def test_Clipboard__get_file(self):
        """Test Clipboard._get_file()"""
        import getpass
        import os

        clipboard = Clipboard()
        the_thing = Object()
        directory = get_os_temporary_dir()
        filename = str('')
        filename += str('GLXCurses-')
        filename += str(getpass.getuser())
        filename += str('.cb')

        file = os.path.normpath(os.path.join(directory, filename))

        self.assertEqual(file, clipboard._get_file())

        # Check errors
        # clipboard is not a GLXC.Clipboard
        self.assertRaises(
            TypeError,
            clipboard._get_file,
            clipboard="Hello"
        )
        self.assertRaises(
            TypeError,
            clipboard._get_file,
            clipboard=the_thing,
        )
