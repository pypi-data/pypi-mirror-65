#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import GLXCurses

import unittest


# Unittest
class TestEntry(unittest.TestCase):

    # Test
    def test_glxc_type(self):
        """Test Entry type"""
        entry = GLXCurses.Entry()
        self.assertTrue(GLXCurses.glxc_type(entry))

    def test_Entry(self):
        """Test Entry"""
        entry = GLXCurses.Entry()
        # check default value
        self.assertEqual(entry.activates_default, False)
        self.assertEqual(entry.attributes, list())
        self.assertEqual(entry.glxc_type, 'GLXCurses.Entry')
        self.assertTrue(GLXCurses.glxc_type(entry.buffer))
        self.assertEqual(entry.caps_locks_warning, True)
        self.assertEqual(entry.completion, None)
        self.assertEqual(entry._cursor_position, 0)
        self.assertEqual(entry.editable, True)
        self.assertEqual(entry.has_frame, True)
        self.assertEqual(entry.inner_border, GLXCurses.GLXC.BORDER_STYLE_NONE)
        self.assertEqual(entry.input_hints, None)
        self.assertEqual(entry.purpose, GLXCurses.GLXC.INPUT_PURPOSE_FREE_FORM)
        self.assertEqual(entry.invisible_char, '*')
        self.assertEqual(entry.invisible_char_set, False)
        self.assertEqual(entry.max_length, 0)
        self.assertEqual(entry.max_width_chars, -1)
        self.assertEqual(entry.overwrite_mode, False)
        self.assertEqual(entry.placeholder_text, None)
        self.assertEqual(entry.populate_all, False)
        self.assertEqual(entry.progress_fraction, 0.0)
        self.assertEqual(entry.progress_pulse_step, 0.1)
        self.assertEqual(entry.scroll_offset, 0)
        self.assertEqual(entry.selection_bound, 0)
        self.assertEqual(entry.shadow_type, GLXCurses.GLXC.SHADOW_IN)
        self.assertEqual(entry.tabs, list())
        self.assertEqual(entry.text, "")
        self.assertEqual(entry.text_length, 0)
        self.assertEqual(entry.truncate_multiline, False)
        self.assertEqual(entry.visibility, True)
        self.assertEqual(entry.width_chars, -1)
        self.assertEqual(entry.xalign, 0)

    def test_Entrey_draw_widget_in_area(self):
        win = GLXCurses.Window()
        entry = GLXCurses.Entry()

        win.add(entry)

        GLXCurses.Application().add_window(win)
        # Main loop
        # entry.draw_widget_in_area()
        GLXCurses.Application().refresh()

    def test_Entry_new(self):
        """Test Entry.new()"""
        entry = GLXCurses.Entry().new()
        # check default value
        self.assertEqual(entry.activates_default, False)
        self.assertEqual(entry.attributes, list())
        self.assertEqual(entry.glxc_type, 'GLXCurses.Entry')
        self.assertTrue(GLXCurses.glxc_type(entry.buffer))
        self.assertEqual(entry.caps_locks_warning, True)
        self.assertEqual(entry.completion, None)
        self.assertEqual(entry._cursor_position, 0)
        self.assertEqual(entry.editable, True)
        self.assertEqual(entry.has_frame, True)
        self.assertEqual(entry.inner_border, GLXCurses.GLXC.BORDER_STYLE_NONE)
        self.assertEqual(entry.input_hints, None)
        self.assertEqual(entry.purpose, GLXCurses.GLXC.INPUT_PURPOSE_FREE_FORM)
        self.assertEqual(entry.invisible_char, '*')
        self.assertEqual(entry.invisible_char_set, False)
        self.assertEqual(entry.max_length, 0)
        self.assertEqual(entry.max_width_chars, -1)
        self.assertEqual(entry.overwrite_mode, False)
        self.assertEqual(entry.placeholder_text, None)
        self.assertEqual(entry.populate_all, False)
        self.assertEqual(entry.progress_fraction, 0.0)
        self.assertEqual(entry.progress_pulse_step, 0.1)
        self.assertEqual(entry.scroll_offset, 0)
        self.assertEqual(entry.selection_bound, 0)
        self.assertEqual(entry.shadow_type, GLXCurses.GLXC.SHADOW_IN)
        self.assertEqual(entry.tabs, list())
        self.assertEqual(entry.text, "")
        self.assertEqual(entry.text_length, 0)
        self.assertEqual(entry.truncate_multiline, False)
        self.assertEqual(entry.visibility, True)
        self.assertEqual(entry.width_chars, -1)
        self.assertEqual(entry.xalign, 0)

    def test_Entry_new_with_buffer(self):
        """Test Entry.new_with_buffer()"""
        entry_buffer = GLXCurses.EntryBuffer().new()
        entry = GLXCurses.Entry().new_with_buffer(entry_buffer)

        # That the same object
        self.assertEqual(entry.buffer.id, entry_buffer.id)
        self.assertEqual(entry.buffer, entry_buffer)

        # Test raise
        entry = GLXCurses.Entry()
        self.assertRaises(TypeError, entry.new_with_buffer)
        self.assertRaises(TypeError, entry.new_with_buffer, buffer=int())
        entry_buffer = GLXCurses.EntryBuffer()
        entry_buffer.id = '0'
        self.assertRaises(TypeError, entry.new_with_buffer, buffer=entry_buffer)

    def test_Entry_get_buffer(self):
        """Test Entry.get_buffer()"""
        entry_buffer = GLXCurses.EntryBuffer().new()
        entry = GLXCurses.Entry().new_with_buffer(entry_buffer)
        self.assertEqual(entry.get_buffer().id, entry_buffer.id)
        # check error
        entry = GLXCurses.Entry().new()
        entry.buffer = None
        self.assertRaises(TypeError, entry.get_buffer)

    def test_Entry_set_buffer(self):
        """Test Entry.set_buffer()"""
        entry_buffer = GLXCurses.EntryBuffer().new()
        entry = GLXCurses.Entry()
        entry.set_buffer(buffer=entry_buffer)
        self.assertEqual(entry.get_buffer().id, entry_buffer.id)

    def test_Entry_set_text(self):
        """Test Entry.set_text()"""
        entry_buffer = GLXCurses.EntryBuffer().new()
        entry = GLXCurses.Entry()
        entry.set_buffer(buffer=entry_buffer)
        entry.set_text("Hello")
        self.assertEqual(entry.buffer.text, entry_buffer.text)
        # check if the EntryBuffer deal with error
        self.assertRaises(TypeError, entry.set_text, chr(128))

    def test_Entry_get_text(self):
        """Test Entry.get_text()"""
        entry_buffer = GLXCurses.EntryBuffer().new()
        entry_buffer.set_text("Hello")
        entry = GLXCurses.Entry()
        entry.set_buffer(buffer=entry_buffer)
        self.assertEqual(entry.get_text(), entry_buffer.text)

    def test_Entry_get_text_length(self):
        """Test Entry.get_text_length()"""
        entry_buffer = GLXCurses.EntryBuffer().new()
        entry_buffer.set_text("Hello")
        entry = GLXCurses.Entry()
        entry.set_buffer(buffer=entry_buffer)
        self.assertEqual(entry.get_text_length(), entry_buffer.get_length())

    # def test_Entry_get_text_area(self):
    #     """Test Entry.get_text_area()"""
    #     entry = Entry()
    #     self.assertRaises(NotImplementedError, entry.get_text_area)

    def test_Entry_set_visibility(self):
        """Test Entry.set_visibility()"""
        entry = GLXCurses.Entry()
        entry.set_visibility(True)
        self.assertEqual(entry.visibility, True)
        entry.set_visibility(False)
        self.assertEqual(entry.visibility, False)
        # check error
        self.assertRaises(TypeError, entry.set_visibility, "Hello")

    def test_Entry_set_invisible_char(self):
        """Test Entry.set_invisible_char()"""
        entry = GLXCurses.Entry()

        entry.set_invisible_char('#')
        self.assertEqual(entry.invisible_char, '#')

        entry.set_invisible_char('*' + chr(128))
        self.assertEqual(entry.invisible_char, '*')

        self.assertRaises(TypeError, entry.set_invisible_char, chr(128))

    def test_Entry_unset_invisible_char(self):
        """Test Entry.unset_invisible_char()"""
        entry = GLXCurses.Entry()
        entry.set_invisible_char('#')
        self.assertEqual(entry.invisible_char, '#')
        entry.unset_invisible_char()
        self.assertEqual(entry.invisible_char, '*')

    def test_Entry_set_max_length(self):
        """Test Entry.set_max_length()"""
        entry_buffer = GLXCurses.EntryBuffer().new()
        entry = GLXCurses.Entry()
        entry.set_buffer(buffer=entry_buffer)
        entry.set_max_length(42)
        self.assertEqual(entry.buffer.max_length, entry_buffer.max_length)
        # check if the EntryBuffer deal with error
        self.assertRaises(TypeError, entry.set_max_length, "Hello")

    def test_Entry_get_activates_default(self):
        """Test Entry.get_activates_default()"""
        entry = GLXCurses.Entry()
        entry.activates_default = True
        self.assertEqual(entry.get_activates_default(), True)
        entry.activates_default = False
        self.assertEqual(entry.get_activates_default(), False)
        entry.activates_default = 1
        self.assertEqual(entry.get_activates_default(), True)
        entry.activates_default = None
        self.assertEqual(entry.get_activates_default(), False)
        entry.activates_default = 1
        self.assertEqual(type(entry.get_activates_default()), bool)

    def test_Entry_get_has_frame(self):
        """Test Entry.get_has_frame()"""
        entry = GLXCurses.Entry()
        entry.has_frame = True
        self.assertEqual(entry.get_has_frame(), True)
        entry.has_frame = False
        self.assertEqual(entry.get_has_frame(), False)
        entry.has_frame = 1
        self.assertEqual(entry.get_has_frame(), True)
        entry.has_frame = None
        self.assertEqual(entry.get_has_frame(), False)
        entry.has_frame = 1
        self.assertEqual(type(entry.get_has_frame()), bool)

    def test_Entry_get_inner_border(self):
        """Test Entry.get_inner_border()"""
        entry = GLXCurses.Entry()
        for value in GLXCurses.GLXC.BorderStyle:
            entry.inner_border = value
            self.assertEqual(entry.inner_border, entry.get_inner_border())

        entry.inner_border = "Hello"
        self.assertEqual(GLXCurses.GLXC.BORDER_STYLE_NONE, entry.get_inner_border())

    def test_Entry_get_width_chars(self):
        """Test Entry.get_width_chars()"""
        entry = GLXCurses.Entry()
        entry.width_chars = 42
        self.assertEqual(entry.get_width_chars(), 42)

    def test_Entry_get_max_width_chars(self):
        """Test Entry.get_max_width_chars()"""
        entry = GLXCurses.Entry()
        entry.max_width_chars = 42
        self.assertEqual(entry.get_max_width_chars(), 42)

    def test_Entry_set_activates_default(self):
        """Test Entry.get_max_width_chars()"""
        entry = GLXCurses.Entry()
        entry.set_activates_default(True)
        self.assertEqual(entry.activates_default, True)
        # check error
        self.assertRaises(TypeError, entry.set_activates_default, "Hello")

    def test_Entry_set_has_frame(self):
        """Test Entry.set_has_frame()"""
        entry = GLXCurses.Entry()
        entry.set_has_frame(True)
        self.assertEqual(entry.has_frame, True)
        entry.set_has_frame(False)
        self.assertEqual(entry.has_frame, False)
        # check error
        self.assertRaises(TypeError, entry.set_has_frame, "Hello")

    def test_Entry_set_inner_border(self):
        """Test Entry.set_inner_border()"""
        entry = GLXCurses.Entry()
        for style in GLXCurses.GLXC.BorderStyle:
            entry.set_inner_border(style)
            self.assertEqual(entry.inner_border, style)

        entry.set_inner_border()
        self.assertEqual(GLXCurses.GLXC.BORDER_STYLE_NONE, entry.inner_border)

        # check error
        self.assertRaises(TypeError, entry.set_inner_border, str('42'))
        self.assertRaises(TypeError, entry.set_inner_border, int(42))

    def test_Entry_set_width_chars(self):
        """Test Entry.set_width_chars()"""
        entry = GLXCurses.Entry()

        entry.set_width_chars(42)
        self.assertEqual(42, entry.width_chars)

        entry.set_width_chars()
        self.assertEqual(-1, entry.width_chars)

        # check error
        self.assertRaises(TypeError, entry.set_width_chars, str('42'))

    def test_Entry_set_max_width_chars(self):
        """Test Entry.set_max_width_chars()"""
        entry = GLXCurses.Entry()

        entry.set_max_width_chars(42)
        self.assertEqual(42, entry.max_width_chars)

        entry.set_max_width_chars()
        self.assertEqual(-1, entry.max_width_chars)

        # check error
        self.assertRaises(TypeError, entry.set_max_width_chars, str('42'))

    def test_Entry_get_invisible_char(self):
        """Test Entry.get_invisible_char()"""
        # look a bit we test python it self ...
        entry = GLXCurses.Entry()

        self.assertEqual(entry.get_invisible_char(), "*")

        entry.invisible_char = "#"
        self.assertEqual(entry.get_invisible_char(), "#")

    def test_Entry_set_alignment(self):
        """Test Entry.set_alignment()"""
        entry = GLXCurses.Entry()

        self.assertEqual(entry.xalign, 0.0)

        entry.set_alignment(0.5)
        self.assertEqual(entry.xalign, 0.5)

        entry.set_alignment(42.42)
        self.assertEqual(entry.xalign, 1.0)

        entry.set_alignment(-42.42)
        self.assertEqual(entry.xalign, 0.0)

        # check error
        self.assertRaises(TypeError, entry.set_alignment, str('42'))
        self.assertRaises(TypeError, entry.set_alignment, int(42))

    def test_Entry_get_alignment(self):
        """Test Entry.get_alignment()"""
        entry = GLXCurses.Entry()
        # check default value
        self.assertEqual(entry.get_alignment(), 0.0)

        entry.set_alignment(0.5)
        self.assertEqual(entry.get_alignment(), 0.5)

        entry.set_alignment(42.42)
        self.assertEqual(entry.get_alignment(), 1.0)

        entry.set_alignment(-42.42)
        self.assertEqual(entry.get_alignment(), 0.0)

    def test_Entry_set_placeholder_text(self):
        """Test Entry.set_placeholder_text()"""
        entry = GLXCurses.Entry()
        # check default value
        self.assertEqual(entry.placeholder_text, None)
        # make a test
        entry.set_placeholder_text("Hello")
        self.assertEqual(entry.placeholder_text, "Hello")
        # test to the limit size
        super_string = "x" * entry._max_length_hard_limit
        entry.set_placeholder_text(super_string)
        self.assertEqual(entry.placeholder_text, super_string)
        # test if the hard limiter work
        mega_string = "x" * (entry._max_length_hard_limit + 1)
        entry.set_placeholder_text(mega_string)
        self.assertEqual(entry.placeholder_text, super_string)
        # check error
        self.assertRaises(TypeError, entry.set_placeholder_text, int(42))

    def test_Entry_get_placeholder_text(self):
        """Test Entry.get_placeholder_text()"""
        entry = GLXCurses.Entry()
        # check default value
        self.assertEqual(entry.get_placeholder_text(), None)
        # make a test
        entry.placeholder_text = "Hello"
        self.assertEqual(entry.get_placeholder_text(), "Hello")

    def test_Entry_set_overwrite_mode(self):
        """Test Entry.set_overwrite_mode()"""
        entry = GLXCurses.Entry()
        # check default value
        self.assertEqual(entry.overwrite_mode, False)
        # make test
        entry.set_overwrite_mode(True)
        self.assertEqual(entry.overwrite_mode, True)
        entry.set_overwrite_mode(False)
        self.assertEqual(entry.overwrite_mode, False)
        # check the default value back
        entry.overwrite_mode = "Hello"
        entry.set_overwrite_mode()
        self.assertEqual(entry.overwrite_mode, False)
        # check error
        self.assertRaises(TypeError, entry.set_overwrite_mode, str("Hello"))

    def test_Entry_get_overwrite_mode(self):
        """Test Entry.get_overwrite_mode()"""
        entry = GLXCurses.Entry()
        # check default value
        self.assertEqual(entry.get_overwrite_mode(), False)
        # make test
        # it look like we check python it self, but that is coupled with self.set_overwrite_mode() tests
        entry.overwrite_mode = True
        self.assertEqual(entry.get_overwrite_mode(), True)
        entry.overwrite_mode = False
        self.assertEqual(entry.get_overwrite_mode(), False)
        entry.overwrite_mode = "Hello"
        self.assertEqual(entry.get_overwrite_mode(), "Hello")

    def test_Entry_get_layout(self):
        """ Test Entry.get_layout()"""
        entry = GLXCurses.Entry()
        self.assertRaises(NotImplementedError, entry.get_layout)

    def test_Entry_get_layout_offsets(self):
        """ Test Entry.get_layout_offsets()"""
        entry = GLXCurses.Entry()
        self.assertRaises(NotImplementedError, entry.get_layout_offsets)

    def test_Entry_layout_index_to_text_index(self):
        """ Test Entry.layout_index_to_text_index()"""
        entry = GLXCurses.Entry()
        self.assertRaises(NotImplementedError, entry.layout_index_to_text_index)

    def test_Entry_text_index_to_layout_index(self):
        """ Test Entry.text_index_to_layout_index()"""
        entry = GLXCurses.Entry()
        self.assertRaises(NotImplementedError, entry.text_index_to_layout_index)

    def test_Entry_set_attributes(self):
        """ Test Entry.set_attributes()"""
        entry = GLXCurses.Entry()
        self.assertRaises(NotImplementedError, entry.set_attributes)

    def test_Entry_get_attributes(self):
        """ Test Entry.get_attributes()"""
        entry = GLXCurses.Entry()
        self.assertRaises(NotImplementedError, entry.get_attributes)

    def test_Entry_get_max_length(self):
        """Test Entry.get_max_length()"""
        entry_buffer = GLXCurses.EntryBuffer().new()
        entry_buffer.max_length = 42
        entry = GLXCurses.Entry()
        entry.buffer = entry_buffer
        entry.max_length = 42
        self.assertEqual(entry.get_max_length(), entry_buffer.get_max_length())

    def test_Entry_get_visibility(self):
        """Test Entry.get_visibility()"""
        entry = GLXCurses.Entry()
        # check default value
        self.assertEqual(entry.get_visibility(), True)
        # make test
        entry.visibility = False
        self.assertEqual(entry.get_visibility(), False)
        entry.visibility = True
        self.assertEqual(entry.get_visibility(), True)

    def test_Entry_set_completion(self):
        """Test Entry.set_completion()"""
        entry = GLXCurses.Entry()
        entry_completion = GLXCurses.EntryCompletion()
        # check default value
        self.assertEqual(entry.completion, None)
        # make the test
        entry.set_completion(completion=entry_completion)
        self.assertEqual(entry.completion, entry_completion)
        # back to default
        entry.set_completion()
        self.assertEqual(entry.completion, None)
        # check error
        self.assertRaises(TypeError, entry.set_completion, str("Hello"))

    def test_Entry_get_completion(self):
        """Test Entry.get_completion()"""
        entry = GLXCurses.Entry()
        entry_completion = GLXCurses.EntryCompletion()
        # check default value
        self.assertEqual(entry.get_completion(), None)
        # make the test
        entry.completion = entry_completion
        self.assertEqual(entry.get_completion(), entry_completion)

    def test_Entry_set_cursor_hadjustment(self):
        """Test Entry.set_cursor_hadjustment()"""
        entry = GLXCurses.Entry()
        adjustment = GLXCurses.Adjustment()
        # check default value
        self.assertNotEqual(entry.cursor_hadjustment, None)
        # make the test
        entry.set_cursor_hadjustment(adjustment=adjustment)
        self.assertEqual(entry.cursor_hadjustment, adjustment)
        # back to default
        entry.set_cursor_hadjustment()
        self.assertEqual(entry.cursor_hadjustment, None)
        # check error
        self.assertRaises(TypeError, entry.set_cursor_hadjustment, str("Hello"))

    def test_Entry_get_cursor_hadjustment(self):
        """Test Entry.get_completion()"""
        entry = GLXCurses.Entry()
        adjustment = GLXCurses.Adjustment()
        # check default value
        self.assertNotEqual(entry.get_cursor_hadjustment(), None)
        # make the test
        entry.cursor_hadjustment = adjustment
        self.assertEqual(entry.get_cursor_hadjustment(), adjustment)

    def test_Entry_set_progress_fraction(self):
        """Test Entry.set_progress_fraction()"""
        entry = GLXCurses.Entry()
        # check default value
        self.assertEquals(entry.progress_fraction, 0.0)
        # make the test
        entry.set_progress_fraction(fraction=0.42)
        self.assertEquals(entry.progress_fraction, 0.42)
        # check clamp
        entry.set_progress_fraction(fraction=-0.42)
        self.assertEquals(entry.progress_fraction, 0.0)
        entry.set_progress_fraction(fraction=42.0)
        self.assertEquals(entry.progress_fraction, 1.0)
        # check error
        self.assertRaises(TypeError, entry.set_progress_fraction, str("Hello"))

    def test_Entry_get_progress_fraction(self):
        """Test Entry.get_progress_fraction()"""
        entry = GLXCurses.Entry()
        # check default value
        self.assertEqual(entry.get_progress_fraction(), 0.0)
        # make the test
        entry.progress_fraction = 0.42
        self.assertEqual(entry.get_progress_fraction(), 0.42)

    def test_Entry_set_progress_pulse_step(self):
        """Test Entry.set_progress_pulse_step()"""
        entry = GLXCurses.Entry()
        # check default value
        self.assertEquals(entry.progress_pulse_step, 0.1)
        # make the test
        entry.set_progress_pulse_step(fraction=0.42)
        self.assertEquals(entry.progress_pulse_step, 0.42)
        # check clamp
        entry.set_progress_pulse_step(fraction=-0.42)
        self.assertEquals(entry.progress_pulse_step, 0.0)
        entry.set_progress_pulse_step(fraction=42.0)
        self.assertEquals(entry.progress_pulse_step, 1.0)
        # check error
        self.assertRaises(TypeError, entry.set_progress_pulse_step, str("Hello"))

    def test_Entry_get_progress_pulse_step(self):
        """Test Entry.get_progress_pulse_step()"""
        entry = GLXCurses.Entry()
        # check default value
        self.assertEqual(entry.get_progress_pulse_step(), 0.1)
        # make the test
        entry.progress_pulse_step = 0.42
        self.assertEqual(entry.get_progress_pulse_step(), 0.42)

    def test_Entry_progress_pulse(self):
        """ Test Entry.progress_pulse()"""
        entry = GLXCurses.Entry()
        self.assertRaises(NotImplementedError, entry.progress_pulse)

    def test_Entry_im_context_filter_keypress(self):
        """ Test Entry.im_context_filter_keypress()"""
        entry = GLXCurses.Entry()
        self.assertRaises(NotImplementedError, entry.im_context_filter_keypress)

    def test_Entry_reset_im_context(self):
        """ Test Entry.reset_im_context()"""
        entry = GLXCurses.Entry()
        self.assertRaises(NotImplementedError, entry.reset_im_context)

    def test_Entry_get_tabs(self):
        """ Test Entry.get_tabs()"""
        entry = GLXCurses.Entry()
        self.assertRaises(NotImplementedError, entry.get_tabs)

    def test_Entry_set_tabs(self):
        """ Test Entry.set_tabs()"""
        entry = GLXCurses.Entry()
        self.assertRaises(NotImplementedError, entry.set_tabs)

    def test_Entry_set_icon_from_pixbuf(self):
        """ Test Entry.set_icon_from_pixbufself()"""
        entry = GLXCurses.Entry()
        self.assertRaises(NotImplementedError, entry.set_icon_from_pixbuf)

    def test_Entry_set_icon_from_stock(self):
        """ Test Entry.set_icon_from_pixbufself()"""
        entry = GLXCurses.Entry()
        self.assertRaises(NotImplementedError, entry.set_icon_from_stock)

    def test_Entry_set_icon_from_icon_name(self):
        """ Test Entry.set_icon_from_icon_name()"""
        entry = GLXCurses.Entry()
        self.assertRaises(NotImplementedError, entry.set_icon_from_icon_name)

    def test_Entry_set_icon_from_gicon(self):
        """ Test Entry.set_icon_from_gicon()"""
        entry = GLXCurses.Entry()
        self.assertRaises(NotImplementedError, entry.set_icon_from_gicon)

    def test_Entry_get_icon_storage_type(self):
        """ Test Entry.get_icon_storage_type()"""
        entry = GLXCurses.Entry()
        self.assertRaises(NotImplementedError, entry.get_icon_storage_type)

    def test_Entry_get_icon_pixbuf(self):
        """ Test Entry.get_icon_pixbuf()"""
        entry = GLXCurses.Entry()
        self.assertRaises(NotImplementedError, entry.get_icon_pixbuf)

    def test_Entry_get_icon_stock(self):
        """ Test Entry.get_icon_stock()"""
        entry = GLXCurses.Entry()
        self.assertRaises(NotImplementedError, entry.get_icon_stock)

    def test_Entry_get_icon_name(self):
        """ Test Entry.get_icon_name()"""
        entry = GLXCurses.Entry()
        self.assertRaises(NotImplementedError, entry.get_icon_name)

    def test_Entry_get_icon_gicon(self):
        """ Test Entry.get_icon_gicon()"""
        entry = GLXCurses.Entry()
        self.assertRaises(NotImplementedError, entry.get_icon_gicon)

    def test_Entry_set_icon_activatable(self):
        """ Test Entry.set_icon_activatable()"""
        entry = GLXCurses.Entry()
        self.assertRaises(NotImplementedError, entry.set_icon_activatable)

    def test_Entry_get_icon_activatable(self):
        """ Test Entry.get_icon_activatable()"""
        entry = GLXCurses.Entry()
        self.assertRaises(NotImplementedError, entry.get_icon_activatable)

    def test_Entry_set_icon_sensitive(self):
        """ Test Entry.set_icon_sensitive()"""
        entry = GLXCurses.Entry()
        self.assertRaises(NotImplementedError, entry.set_icon_sensitive)

    def test_Entry_get_icon_sensitive(self):
        """ Test Entry.get_icon_sensitive()"""
        entry = GLXCurses.Entry()
        self.assertRaises(NotImplementedError, entry.get_icon_sensitive)

    def test_Entry_get_icon_at_pos(self):
        """ Test Entry.get_icon_at_pos()"""
        entry = GLXCurses.Entry()
        self.assertRaises(NotImplementedError, entry.get_icon_at_pos)

    def test_Entry_set_icon_tooltip_text(self):
        """ Test Entry.set_icon_tooltip_text()"""
        entry = GLXCurses.Entry()
        self.assertRaises(NotImplementedError, entry.set_icon_tooltip_text)

    def test_Entry_get_icon_tooltip_text(self):
        """ Test Entry.get_icon_tooltip_text()"""
        entry = GLXCurses.Entry()
        self.assertRaises(NotImplementedError, entry.get_icon_tooltip_text)

    def test_Entry_set_icon_tooltip_markup(self):
        """ Test Entry.set_icon_tooltip_markup()"""
        entry = GLXCurses.Entry()
        self.assertRaises(NotImplementedError, entry.set_icon_tooltip_markup)

    def test_Entry_get_icon_tooltip_markup(self):
        """ Test Entry.get_icon_tooltip_markup()"""
        entry = GLXCurses.Entry()
        self.assertRaises(NotImplementedError, entry.get_icon_tooltip_markup)

    def test_Entry_set_icon_drag_source(self):
        """ Test Entry.set_icon_drag_source()"""
        entry = GLXCurses.Entry()
        self.assertRaises(NotImplementedError, entry.set_icon_drag_source)

    def test_Entry_get_current_icon_drag_source(self):
        """ Test Entry.get_current_icon_drag_source()"""
        entry = GLXCurses.Entry()
        self.assertRaises(NotImplementedError, entry.get_current_icon_drag_source)

    def test_Entry_get_icon_area(self):
        """ Test Entry.get_icon_area()"""
        entry = GLXCurses.Entry()
        self.assertRaises(NotImplementedError, entry.get_icon_area)

    def test_Entry_set_input_purpose(self):
        """ Test Entry.set_input_purpose()"""
        entry = GLXCurses.Entry()
        self.assertRaises(NotImplementedError, entry.set_input_purpose)

    def test_Entry_get_input_purpose(self):
        """ Test Entry.get_input_purpose()"""
        entry = GLXCurses.Entry()
        self.assertRaises(NotImplementedError, entry.get_input_purpose)

    def test_Entry_set_input_hints(self):
        """ Test Entry.set_input_hints()"""
        entry = GLXCurses.Entry()
        self.assertRaises(NotImplementedError, entry.set_input_hints)

    def test_Entry_get_input_hints(self):
        """ Test Entry.get_input_hints()"""
        entry = GLXCurses.Entry()
        self.assertRaises(NotImplementedError, entry.get_input_hints)

    def test_Entry_grab_focus_without_selecting(self):
        """Test Entry.grab_focus_without_selecting()"""
        entry = GLXCurses.Entry()
        # app = GLXCurses.Application()
        self.assertFalse(entry.get_selection_bounds())
        self.assertEqual(entry._focus_without_selecting, False)

        entry.grab_focus_without_selecting()
        # self.assertEqual(app.get_is_focus()['id'], entry.get_widget_id())
        self.assertEqual(entry._focus_without_selecting, True)
        self.assertFalse(entry.get_selection_bounds())

    def test_Entry__emit_activate_signal(self):
        """Test Entry._emit_activate_signal()"""
        entry = GLXCurses.Entry()
        entry._emit_activate_signal()
        self.assertRaises(TypeError, entry._emit_activate_signal, user_data=int(42))

    def test_Entry__emit_backspace_signal(self):
        """Test Entry._emit_backspace_signal()"""
        entry = GLXCurses.Entry()
        entry._emit_backspace_signal()
        self.assertRaises(TypeError, entry._emit_backspace_signal, user_data=int(42))

    def test_Entry__emit_copy_clipboard_signal(self):
        """Test Entry._emit_copy_clipboard_signal()"""
        entry = GLXCurses.Entry()
        entry._emit_copy_clipboard_signal()
        self.assertRaises(TypeError, entry._emit_copy_clipboard_signal, user_data=int(42))

    def test_Entry__emit_cut_clipboard_signal(self):
        """Test Entry._emit_cut_clipboard_signal()"""
        entry = GLXCurses.Entry()
        entry._emit_cut_clipboard_signal()
        self.assertRaises(TypeError, entry._emit_cut_clipboard_signal, user_data=int(42))

    def test_Entry__emit_delete_from_cursor_signal(self):
        """Test Entry._emit_delete_from_cursor_signal()"""
        entry = GLXCurses.Entry()
        entry._emit_delete_from_cursor_signal()
        self.assertRaises(TypeError, entry._emit_delete_from_cursor_signal, delete_type=int(42))
        self.assertRaises(TypeError, entry._emit_delete_from_cursor_signal, count=str("Hello"))
        self.assertRaises(TypeError, entry._emit_delete_from_cursor_signal, user_data=str("Hello"))


if __name__ == '__main__':
    unittest.main()
