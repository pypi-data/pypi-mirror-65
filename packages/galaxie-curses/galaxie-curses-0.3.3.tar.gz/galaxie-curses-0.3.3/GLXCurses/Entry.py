#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import GLXCurses
import curses
import logging
import re


class Entry(GLXCurses.Widget, GLXCurses.Editable, GLXCurses.Movable):
    """
    Entry — A single line text entry field
    """

    def __init__(self):
        """
        **Property Details**

        .. py:attribute:: activates-default

           Whether to activate the default widget (such as the default button in a dialog) when Enter is pressed.

              :rtype: object
              :Type: bool
              :Flags: Read / Write
              :Default value: False

        .. py:attribute:: attributes

           A list of Pango attributes to apply to the text of the entry.

           This is mainly useful to change the size or weight of the text.

           The PangoAttribute's start_index and end_index must refer to the GtkEntryBuffer text, i.e. without the
           preedit string.

              :Type: list
              :Flags: Read / Write

        .. py:attribute:: buffer

           Text buffer object which actually stores entry text.

              :Type: :func:`GLXCurses.EntryBuffer <GLXCurses.EntryBuffer.EntryBuffer>`
              :Flags: Read / Write / Construct

        .. py:attribute:: caps-lock-warning

           Whether password entries will show a warning when Caps Lock is on

              :Type: bool
              :Flags: Read / Write
              :Default Value: true

        .. py:attribute:: completion

           The auxiliary completion object to use with the entry.

              :Type: :func:`GLXCurses.EntryCompletion <GLXCurses.EntryCompletion.EntryCompletion>`
              :Flags: Read / Write

        .. py:attribute:: cursor-position

           The current position of the insertion cursor in chars.

              :Type: int
              :Flags: Read / Write
              :Allowed values: [0,65535]
              :Default value: 0

        .. py:attribute:: editable

           Whether the entry contents can be edited.

              :Type: bool
              :Flags: Read / Write
              :Default value: True

        .. py:attribute:: has-frame

           False removes outside bevel from entry.

              :Type: bool
              :Flags: Read / Write
              :Default value: True

        .. py:attribute:: im-module

           Which IM (input method) module should be used for this entry. See IMContext.

           Setting this to a non-NULL value overrides the system-wide IM module setting.
           See the GLXCSettings “glxc-im-module” property.

              :Type: str
              :Flags: Read / Write
              :Default value: None

        .. py:attribute:: inner-border

           Sets the text area's border between the text and the frame.

              :Type: Border
              :Flags: Read / Write

        .. py:attribute:: input-hints

           Additional hints (beyond “input-purpose”) that allow input methods to fine-tune their behaviour.

              :Type: GLXCInputHints
              :Flags: Read / Write

        .. py:attribute:: input-purpose

           The purpose of this text field.

           This property can be used by on-stdscr keyboards and other input methods to adjust their behaviour.

           .. note:: the purpose to glxc.INPUT_PURPOSE_PASSWORD or glxc.INPUT_PURPOSE_PIN is independent from setting \
           “visibility”.

              :Type: GLXCInputPurpose
              :Flags: Read / Write
              :Default value: glxc.INPUT_PURPOSE_FREE_FORM

        .. py:attribute:: invisible-char

           The invisible character is used when masking entry contents (in \"password mode\")").
           When it is not explicitly set with the “invisible-char” property, GTK+ determines the character to
           use from a list of possible candidates, depending on availability in the current font.

           This style property allows the theme to prepend a character to the list of candidates.

              :Type: int
              :Flags: Read / Write
              :Default value: '*'

        .. py:attribute:: invisible-char-set

           Whether the invisible char has been set for the GLXCurses.Entry.

              :Type: bool
              :Flags: Read / Write
              :Default value: False

        .. py:attribute:: max-length

           Maximum number of characters for this entry. Zero if no maximum.

              :Type: bool
              :Flags: Read / Write
              :Allowed values: [0,65535]
              :Default value: 0

        .. py:attribute:: max-width-chars

           The desired maximum width of the entry, in characters. If this property is set to -1,
           the width will be calculated automatically.

              :Type: int
              :Flags: Read / Write
              :Allowed values: >= -1
              :Default value: -1

        .. py:attribute:: overwrite-mode

           If text is overwritten when typing in the GLXCurses.Entry.

              :Type: bool
              :Flags: Read / Write
              :Default value: False

        .. py:attribute:: placeholder-text

           The text that will be displayed in the GLXCurses.Entry when it is empty and unfocused.

              :Type: str
              :Flags: Read / Write
              :Default value: None

        .. py:attribute:: populate-all

           If :populate-all is True, the “populate-popup” signal is also emitted for touch popups.

              :Type: bool
              :Flags: Read / Write
              :Default value: False

        .. py:attribute:: progress-fraction

           The current fraction of the task that's been completed.

              :Type: float
              :Flags: Read / Write
              :Allowed values: [0,1]
              :Default value: 0

        .. py:attribute:: progress-pulse-step

           The fraction of total entry width to move the progress bouncing block for each call to
           glxc_entry_progress_pulse().

              :Type: float
              :Flags: Read / Write
              :Allowed values: [0,1]
              :Default value: 0.1

        .. py:attribute:: scroll-offset

           Number of chars of the entry scrolled off the stdscr to the left.

              :Type: int
              :Flags: Read
              :Allowed values: >= 0
              :Default value: 0

        .. py:attribute:: selection-bound

           The position of the opposite end of the selection from the cursor in chars.

              :Type: int
              :Flags: Read
              :Allowed values: [0,65535]
              :Default value: 0

        .. py:attribute:: shadow-type

           Which kind of shadow to draw around the entry when “has-frame” is set to True.

              :Type: glxc.ShadowType
              :Flags: Read / Write
              :Default value: glxc.SHADOW_IN

        .. py:attribute:: tabs

           A list of tabstop locations to apply to the text of the entry.

              :Type: TabArray
              :Flags: Read / Write

        .. py:attribute:: text

           The contents of the entry.

              :Type: char
              :Flags: Read / Write
              :Default value: ''

        .. py:attribute:: text-length

           The contents of the entry.

              :Type: int
              :Flags: Read
              :Allowed values: <= 65535
              :Default value: 0

        .. py:attribute:: truncate-multiline

           When True, pasted multi-line text is truncated to the first line.

              :Type: bool
              :Flags: Read / Write
              :Default value: False

        .. py:attribute:: visibility

           False displays the "invisible char" instead of the actual text (password mode).

              :Type: bool
              :Flags: Read / Write
              :Default value: True

        .. py:attribute:: width-chars

           Number of characters to leave space for in the entry.

              :Type: int
              :Flags: Read / Write
              :Allowed values: >= -1
              :Default value: -1

        .. py:attribute:: xalign

           The horizontal alignment, from 0 (left) to 1 (right). Reversed for RTL layouts.

              :Type: float
              :Flags: Read / Write
              :Allowed values: [0,1]
              :Default value: 0

        **Description**

        The :func:`GLXCurses.Entry <GLXCurses.Entry.Entry>` widget is a single line text entry widget.
        A fairly large set of key bindings are supported by default. If the entered text is longer than the allocation
        of the widget, the widget will scroll so that the cursor position is visible.

        When using an entry for passwords and other sensitive information, it can be put into “password mode” using
        :func:`GLXCurses.Entry.set_visibility() <GLXCurses.Entry.Entry.set_visibility()>`. In this mode, entered text
        is displayed using a “invisible” character. By default, GLXCurses picks the best invisible character
        that is available in the current font, but it can be changed with
        :func:`GLXCurses.Entry.set_invisible_char() <GLXCurses.Entry.Entry.set_invisible_char()>`.
        GLXCurses displays a warning when Caps Lock or input methods might interfere with entering text
        in a password entry. The warning can be turned off with the “caps-lock-warning” property.

        """
        # Load heritage
        GLXCurses.Widget.__init__(self)
        GLXCurses.Movable.__init__(self)
        GLXCurses.Editable.__init__(self)

        # It's a GLXCurse Type
        self.glxc_type = 'GLXCurses.Entry'
        self.name = '{0}{1}'.format(self.__class__.__name__, self.id)

        # Make a Widget Style heritage attribute as local attribute
        # if self.style.attribute_states:
        #     if self.attribute_states != self.style.attribute_states:
        #         self.attribute_states = self.style.attribute_states

        ##############
        # Property's #
        ##############

        self.activates_default = False
        self.cursor_hadjustment = GLXCurses.Adjustment()
        self.attributes = list()
        self.buffer = GLXCurses.EntryBuffer()
        self.caps_locks_warning = True
        self.completion = None
        self._cursor_position = 0
        self.editable = True
        self.has_frame = True
        self.inner_border = GLXCurses.GLXC.BORDER_STYLE_NONE
        self.input_hints = None
        self.purpose = GLXCurses.GLXC.INPUT_PURPOSE_FREE_FORM
        self.invisible_char = '*'
        self.invisible_char_set = False
        self.max_length = int(0)
        self.max_width_chars = int(-1)
        self.overwrite_mode = bool(False)
        self.placeholder_text = None
        self.populate_all = bool(False)
        self.progress_fraction = float(0.0)
        self.progress_pulse_step = float(0.1)
        self.scroll_offset = 0
        self.selection_bound = 0
        self.shadow_type = GLXCurses.GLXC.SHADOW_IN
        self.tabs = list()
        self.text = ""
        self.text_length = 0
        self.truncate_multiline = False
        self.visibility = True
        self.width_chars = -1
        self.xalign = 0.0

        # Size management
        self.preferred_height = 1

        # Internal Properties
        self._min_length_hard_limit = 0
        self._max_length_hard_limit = 65535

        # Internal Widget Setting

        # Interface
        self.interface_normal = '[^]'
        self.interface_prelight = '[-]'
        self.button_completion = self.interface_normal
        # self._cursor_position = 0
        # self._cursor_position_is_after_text = False

        # Size management
        self._update_preferred_sizes()

        # States
        self.curses_mouse_states = {
            curses.BUTTON1_PRESSED: 'BUTTON1_PRESS',
            curses.BUTTON1_RELEASED: 'BUTTON1_RELEASED',
            curses.BUTTON1_CLICKED: 'BUTTON1_CLICKED',
            curses.BUTTON1_DOUBLE_CLICKED: 'BUTTON1_DOUBLE_CLICKED',
            curses.BUTTON1_TRIPLE_CLICKED: 'BUTTON1_TRIPLE_CLICKED',

            curses.BUTTON2_PRESSED: 'BUTTON2_PRESSED',
            curses.BUTTON2_RELEASED: 'BUTTON2_RELEASED',
            curses.BUTTON2_CLICKED: 'BUTTON2_CLICKED',
            curses.BUTTON2_DOUBLE_CLICKED: 'BUTTON2_DOUBLE_CLICKED',
            curses.BUTTON2_TRIPLE_CLICKED: 'BUTTON2_TRIPLE_CLICKED',

            curses.BUTTON3_PRESSED: 'BUTTON3_PRESSED',
            curses.BUTTON3_RELEASED: 'BUTTON3_RELEASED',
            curses.BUTTON3_CLICKED: 'BUTTON3_CLICKED',
            curses.BUTTON3_DOUBLE_CLICKED: 'BUTTON3_DOUBLE_CLICKED',
            curses.BUTTON3_TRIPLE_CLICKED: 'BUTTON3_TRIPLE_CLICKED',

            curses.BUTTON4_PRESSED: 'BUTTON4_PRESSED',
            curses.BUTTON4_RELEASED: 'BUTTON4_RELEASED',
            curses.BUTTON4_CLICKED: 'BUTTON4_CLICKED',
            curses.BUTTON4_DOUBLE_CLICKED: 'BUTTON4_DOUBLE_CLICKED',
            curses.BUTTON4_TRIPLE_CLICKED: 'BUTTON4_TRIPLE_CLICKED',

            curses.BUTTON_SHIFT: 'BUTTON_SHIFT',
            curses.BUTTON_CTRL: 'BUTTON_CTRL',
            curses.BUTTON_ALT: 'BUTTON_ALT'
        }

        # Sensitive
        self.can_default = True
        self.can_focus = True
        self.sensitive = True
        self.states_list = None
        self._focus_without_selecting = False

        # Subscription
        self.connect('MOUSE_EVENT', Entry._handle_mouse_event)
        self.connect('CURSES', Entry._handle_key_event)  # Keyboard

        # self.connect('active', Entry._emit_activate_signal)
        # self.connect('backspace', Entry._emit_backspace_signal)
        # self.connect('copy-clipboard', Entry._emit_copy_clipboard_signal)
        # self.connect('cut-clipboard', Entry._emit_cut_clipboard_signal)
        # self.connect('delete-from-cursor', Entry._emit_delete_from_cursor_signal)
        # self.connect('icon-press', Entry._emit_icon_press_signal)
        # self.connect('icon-release', Entry._emit_icon_release_signal)
        # self.connect('insert-at-cursor', Entry._emit_insert_at_cursor_signal)
        # self.connect('move-cursor', Entry._emit_move_cursor_signal)
        # self.connect('paste-clipboard', Entry._emit_paste_clipboard_signal)
        # self.connect('populate-popup', Entry._emit_populate_popup_signal)
        # self.connect('preedit-changed', Entry._emit_preedit_changed_signal)
        # self.connect('toggle-overwrite', Entry._emit_toggle_overwrite_signal)

    def draw_widget_in_area(self):
        self.create_or_resize()
        # Many Thing's
        # Check if the text can be display
        # text_have_necessary_width = (self.preferred_width >= 1)
        # text_have_necessary_height = (self.get_preferred_height() >= 1)
        # if not text_have_necessary_height or not text_have_necessary_width:
        #     return

        self._draw_entry()

    def new(self):
        """
        Creates a new entry.

        :return: A new GLXCurse Entry Widget
        :rtype: GLXCurse.Widget
        """
        self.__init__()
        return self

    def new_with_buffer(self, buffer=None):
        """
        Creates a new entry with the specified text buffer.

        .. note:: :func:`Utils.is_valid_id() <GLXCurses.Utils.is_valid_id()>` and \
        :func:`Utils.new_id() <GLXCurses.Utils.new_id()>` are used for identify if the ``buffer`` is a Galaxie-Curses \
        component. That GLXCurses ID is automatically generate at the widget creation.

        :param buffer: The buffer to use for the new :func:`GLXCurses.Entry <GLXCurses.Entry.Entry>`.
        :return: A Entry Buffer object.
        :rtype: :func:`GLXCurses.Entry <GLXCurses.Entry.Entry>`
        :raise TypeError: if ``buffer`` is not :func:`GLXCurses.EntryBuffer <GLXCurses.EntryBuffer.EntryBuffer>` Type
        :raise TypeError: if ``buffer`` haven't a valid GLXCurses ID
        """
        # Exit as soon of possible
        if not GLXCurses.glxc_type(buffer):
            raise TypeError('"buffer" must be GLXCurses.EntryBuffer Type')
        if not GLXCurses.is_valid_id(buffer.id):
            raise TypeError('"buffer" must have a valid GLXCurses ID')

        # Why not init a new Entry
        self.__init__()

        # Set the buffer after the init :)
        self.set_buffer(buffer)

        # Return th Entry
        return self

    def get_buffer(self):
        """
        Get the GLXCurses.EntryBuffer object which holds the text for this widget.

        :return: A EntryBuffer object.
        :rtype: GLXCurse.Widget
        """
        # Exit as soon of possible
        if not GLXCurses.glxc_type(self.buffer) or not GLXCurses.is_valid_id(self.buffer.id):
            raise TypeError('"buffer" must be GLXCurses.EntryBuffer Type')

        # Ok here we are we return the buffer
        return self.buffer

    def set_buffer(self, buffer=None):
        """
        Set the EntryBuffer object which holds the text for this widget.

        :param buffer: The buffer to use for the GLXCurses.Entry.
        """
        self.buffer = buffer

    def set_text(self, text):
        """
        Sets the text in the widget to the given value, replacing the current contents.

        .. seealso:: GLXCurses.EntryBuffer().set_text()

        :param text: The new text
        :type text: String
        """
        self.get_buffer().set_text(text)

    def get_text(self):
        """
        Retrieves the contents of the entry widget. See also GLXCurses.Editable.get_chars().

        This is equivalent to:
        ``
        self.buffer = GLXCurses.EntryBuffer()
        self.buffer.get_text()
        ``
        :return: A pointer to the contents of the widget as a string. \
        This string points to internally allocated storage in the widget and must not be freed, \
        modified or stored.
        :rtype: String
        """
        return self.get_buffer().get_text()

    def get_text_length(self):
        """
        Retrieves the current length of the text in entry .

        This is equivalent to:
        ``
        self.buffer = GLXCurses.EntryBuffer()
        self.buffer.get_length()
        ``

        :return: The current number of characters in GtkEntry, or 0 if there are none.
        :rtype: Int in range 0-65536
        """
        return self.get_buffer().get_length()

    # def get_text_area(self):
    #     """
    #     NotImplemented
    #
    #     Gets the area where the entry’s text is drawn.
    #     This function is useful when drawing something to the entry in a draw callback.
    #
    #     If the entry is not realized, text_area is filled with zeros.
    #
    #     :return: A list of information X, Y and Size Width, Height . returned information are the complete allowed area,
    #     :rtype: List(X, Y , Width, Height)
    #     """
    #     padding = 0
    #     self.height - (padding * 2),
    #     self.width - (padding * 2),
    #     self.get_y() + padding,
    #     self.get_x() + padding
    #
    #     raise NotImplementedError

    def set_visibility(self, visible=None):
        """
        Sets whether the contents of the entry are visible or not. When visibility is set to FALSE, characters are
        displayed as the invisible char, and will also appear that way when the text in the entry widget is copied
        elsewhere.

        By default, GLXCurse picks the best invisible character available in the current font,
        but it can be changed with set_invisible_char().

        .. note:: You probably want to set “input_purpose” to glx.INPUT_PURPOSE_PASSWORD or glx.INPUT_PURPOSE_PIN to \
        inform input methods about the purpose of this entry, in addition to setting visibility to FALSE.

        :param visible: True if the contents of the entry are displayed as plaintext
        :type visible: bool
        :raise TypeError: if ``visible`` is not boolean type
        """
        if type(visible) != bool:
            raise TypeError('"visible" must be bool type')

        if bool(visible):
            self.visibility = True
        else:
            self.visibility = False

    def set_invisible_char(self, ch='*'):
        """
        Sets the character to use in place of the actual text when set_visibility() has been called to set text
        visibility to FALSE.

        .. note:: this is the character used in “password mode” to show the user how many characters have been typed.

        By default, GLXCurse picks the best invisible char available in the current font.

        .. note:: If you set the invisible char to 0, then the user will get no feedback at all; \
        there will be no text on the stdscr as they type

        :param ch: a character
        :type ch: str
        :raise TypeError: if ``ch`` is not printable str
        """
        # try to exit as soon of possible
        if ch is not None:
            if ch.split()[0][0] not in GLXCurses.GLXC.Printable:
                raise TypeError('"ch" must be printable string')
        # in case i an do nothing
        if self.invisible_char != ch.split()[0][0]:
            self.invisible_char = ch.split()[0][0]

    def unset_invisible_char(self):
        """"
        Unset the invisible char previously set with set_invisible_char().
        So that the default invisible char is used again.
        """
        self.set_invisible_char(ch='*')

    def set_max_length(self, max=None):
        """
        Sets the maximum allowed length of the contents of the widget.
        If the current contents are longer than the given length, then they will be truncated to fit.

        This is equivalent to:
           self.buffer = GLXCurses.EntryBuffer()
           self.buffer.set_max_length()

        :param max: The maximum length of the entry, or 0 for no maximum. (other than the maximum length of entries.) \
        The value passed in will be clamped to the range 0-65536.
        :type max: int
        """
        self.get_buffer().set_max_length(max)

    def get_activates_default(self):
        """
        Retrieves the value set by set_activates_default().

        :return: TRUE if the entry will activate the default widget
        :rtype: bool
        """
        return bool(self.activates_default)

    def get_has_frame(self):
        """
        Gets the value set by set_has_frame().

        :return: whether the entry has a beveled frame
        :rtype: bool
        """
        return bool(self.has_frame)

    def get_inner_border(self):
        """
        This function returns the entry’s “inner-border” property. See set_inner_border() for more information.

        GLXC.BorderStyle Members:

        GLXC.BORDER_STYLE_NONE      No visible border
        GLXC.BORDER_STYLE_SOLID     A single line segment
        GLXC.BORDER_STYLE_INSET     Looks as if the content is sunken into the canvas
        GLXC.BORDER_STYLE_OUTSET    Looks as if the content is coming out of the canvas
        GLXC.BORDER_STYLE_HIDDEN    Same as glxc.BORDER_STYLE_NONE
        GLXC.BORDER_STYLE_DOTTED    A series of round dots
        GLXC.BORDER_STYLE_DASHED    A series of square-ended dashes
        GLXC.BORDER_STYLE_DOUBLE    Two parallel lines with some space between them
        GLXC.BORDER_STYLE_GROOVE    Looks as if it were carved in the canvas
        GLXC.BORDER_STYLE_RIDGE     Looks as if it were coming out of the canvas

        :return: a GLXC.BorderStyle type Constant or GLXC.BORDER_STYLE_NONE if none was set
        :rtype: str
        """
        if self.inner_border in GLXCurses.GLXC.BorderStyle:
            return self.inner_border
        else:
            self.set_inner_border(GLXCurses.GLXC.BORDER_STYLE_NONE)
            return GLXCurses.GLXC.BORDER_STYLE_NONE

    def get_width_chars(self):
        """
        Gets the value set by set_width_chars()

        :return: number of chars to request space for, or negative if unset
        """
        return self.width_chars

    def get_max_width_chars(self):
        """
        Retrieves the desired maximum width of entry , in characters.

        set_max_width_chars().

        :return: the maximum width of the entry, in characters
        :rtype: int
        """
        return self.max_width_chars

    def set_activates_default(self, setting):
        """
        If setting is True, pressing Enter in the entry will activate the default widget for the window containing
        the entry.

        This usually means that the dialog box containing the entry will be closed, since the default
        widget is usually one of the dialog buttons.

        (For experts: if setting is True, the entry calls activate_default() on the window containing the entry,
        in the default handler for the “activate” signal.)

        :param setting: True to activate window’s default widget on Enter keypress
        :type setting: bool
        :raise TypeError: if ``setting`` is not bool type
        """
        # Try to exit as soon of possible
        if type(setting) != bool:
            raise TypeError('"setting" must be a bool type')
        # For be sure we really have something to do
        if self.activates_default != bool(setting):
            self.activates_default = bool(setting)

    def set_has_frame(self, setting=True):
        """
        Sets whether the entry has a beveled frame around it.

        :param setting: False removes outside bevel from entry
        :type setting: bool
        :raise TypeError: if ``setting`` is not bool type
        """
        # Try to exit as soon of possible
        if type(setting) != bool:
            raise TypeError('"setting" must be a bool type')
        # For be sure we really have something to do
        if self.has_frame != bool(setting):
            self.has_frame = bool(setting)

    def set_inner_border(self, border=GLXCurses.GLXC.BORDER_STYLE_NONE):
        """
        Sets entry’s inner-border property to border , or clears it if None is passed.
        The inner-border is the area around the entry’s text, but inside its frame.

        If set, this property overrides the inner-border style property. Overriding the style-provided border is
        useful when you want to do in-place editing of some text in a canvas or list widget, where pixel-exact
        positioning of the entry is important.

        **GLXC.BorderStyle**

        Describes how the border of a UI element should be rendered.

        **Members:**
           GLXC.BORDER_STYLE_NONE      No visible border
           GLXC.BORDER_STYLE_SOLID     A single line segment
           GLXC.BORDER_STYLE_INSET     Looks as if the content is sunken into the canvas
           GLXC.BORDER_STYLE_OUTSET    Looks as if the content is coming out of the canvas
           GLXC.BORDER_STYLE_HIDDEN    Same as glxc.BORDER_STYLE_NONE
           GLXC.BORDER_STYLE_DOTTED    A series of round dots
           GLXC.BORDER_STYLE_DASHED    A series of square-ended dashes
           GLXC.BORDER_STYLE_DOUBLE    Two parallel lines with some space between them
           GLXC.BORDER_STYLE_GROOVE    Looks as if it were carved in the canvas
           GLXC.BORDER_STYLE_RIDGE     Looks as if it were coming out of the canvas

        :param border: a valid GLXC.BorderStyle
        :type border: str
        :raise TypeError: if ``border`` is not str type
        :raise TypeError: if ``border`` is not a valid GLXC.BorderStyle
        """
        # Try to exit as soon of possible
        if type(border) != str:
            raise TypeError('"setting" must be a str type')
        if border not in GLXCurses.GLXC.BorderStyle:
            raise TypeError('"border" must be a valid GLXC.BorderStyle')

        # just verify if it have to do something
        if self.inner_border != border:
            self.inner_border = border

    def set_width_chars(self, n_chars=-1):
        """
        Changes the size request of the entry to be about the right size for n_chars characters. Note that it changes
        the size request, the size can still be affected by how you pack the widget into containers.

        If n_chars is -1, the size reverts to the default entry size.

        :param n_chars: width in chars
        :type n_chars: int
        :raise TypeError: if ``n_chars`` is not int type
        """
        # Try to exit as soon of possible
        if type(n_chars) != int:
            raise TypeError('"n_chars" must be a int type')

        # just verify if it have to do something
        if self.width_chars != n_chars:
            self.width_chars = n_chars

    def set_max_width_chars(self, n_chars=-1):
        """
        Sets the desired maximum width in characters of entry

        :param n_chars: the new desired maximum width, in characters
        :type n_chars: int
        :raise TypeError: if ``n_chars`` is not int type
        """
        # Try to exit as soon of possible
        if type(n_chars) != int:
            raise TypeError('"n_chars" must be a int type')

        # just verify if it have to do something
        if self.max_width_chars != n_chars:
            self.max_width_chars = n_chars

    def get_invisible_char(self):
        """
        Retrieves the character displayed in place of the real characters for entries with visibility set to false.

        .. seealso:: set_invisible_char().

        :return: the current invisible char, or 0, if the entry does not show invisible text at all.
        """
        return self.invisible_char

    def set_alignment(self, xalign=0.0):
        """
        Sets the alignment for the contents of the entry. This controls the horizontal positioning of the contents
        when the displayed text is shorter than the width of the entry.

        :param xalign: The horizontal alignment, from 0 (left) to 1 (right). Reversed for RTL layouts
        :type xalign: float
        :raise TypeError: if ``xalign`` is not float type
        """
        # Try to exit as soon of possible
        if type(xalign) != float:
            raise TypeError('"xalign" must be a float type')

        # clamp value
        xalign = GLXCurses.clamp(value=xalign, smallest=0.0, largest=1.0)

        # just verify if it have to do something
        if self.xalign != xalign:
            self.xalign = xalign

    def get_alignment(self):
        """
        Gets the value set by :func:`GLXCurses.Entry.set_alignment() <GLXCurses.Entry.Entry.set_alignment>`.

        :return: The horizontal alignment, from 0 (left) to 1 (right).
        :rtype: float
        """
        return self.xalign

    def set_placeholder_text(self, text=None):
        """
        Sets text to be displayed in entry when it is empty and unfocused.
        This can be used to give a visual hint of the expected contents of the
        :func:`GLXCurses.Entry <GLXCurses.Entry.Entry>`.

        .. note::  that since the placeholder text gets removed when the entry received focus, \
        using this feature is a bit problematic if the entry is given the initial focus in a window. \
        Sometimes this can be worked around by delaying the initial focus setting until the first key event arrives.

        :param text: a string to be displayed when entry is empty and unfocused, or None.
        :type text: str or None
        :raise TypeError: if ``text`` is not str or None type
        """
        # Try to exit as soon of possible
        if type(text) != str and text is not None:
            raise TypeError("'text' must be an str type or None")

        # just for not receive to mush character why load a 100Gb str on a ncurses application ?
        text = text[:self._get_max_length_hard_limit()]

        # My dream is do nothing
        if self.placeholder_text != text:
            self.placeholder_text = text

    def get_placeholder_text(self):
        """
        Retrieves the text that will be displayed when entry is empty and unfocused

        :return: a pointer to the placeholder text as a string. \
        This string points to internally allocated storage in the widget and must not be freed, modified or stored.
        """
        return self.placeholder_text

    def set_overwrite_mode(self, overwrite=bool(False)):
        """
        Sets whether the text is overwritten when typing in the :func:`GLXCurses.Entry <GLXCurses.Entry.Entry>`.

        :param overwrite: new value
        :type overwrite: bool
        :raise TypeError: if ``overwrite`` is not bool type
        """
        # we crash as soon of possible
        if type(overwrite) != bool:
            raise TypeError('"overwrite" must be bool type')
        # why move where we can do nothing ...
        if self.overwrite_mode != overwrite:
            self.overwrite_mode = overwrite

    def get_overwrite_mode(self):
        """
        Gets the value set by :func:`GLXCurses.Entry.set_overwrite_mode() <GLXCurses.Entry.Entry.set_overwrite_mode()>`.

        :return: whether the text is overwritten when typing.
        :rtype: bool
        """
        return self.overwrite_mode

    def get_layout(self):
        """
        :raise NotImplementedError: GLXCurses don't get Pango management
        """
        raise NotImplementedError

    def get_layout_offsets(self):
        """
        :raise NotImplementedError: GLXCurses don't get Pango management
        """
        raise NotImplementedError

    def layout_index_to_text_index(self):
        """
        :raise NotImplementedError: GLXCurses don't get Pango management
        """
        raise NotImplementedError

    def text_index_to_layout_index(self):
        """
        :raise NotImplementedError: GLXCurses don't get Pango management
        """
        raise NotImplementedError

    def set_attributes(self):
        """
        :raise NotImplementedError: GLXCurses don't get Pango management
        """
        raise NotImplementedError

    def get_attributes(self):
        """
        :raise NotImplementedError: GLXCurses don't get Pango management
        """
        raise NotImplementedError

    def get_max_length(self):
        """
        Retrieves the maximum allowed length of the text in entry . See
        :func:`GLXCurses.Entry.set_max_length() <GLXCurses.Entry.Entry.set_max_length()>`.

        This is equivalent to getting entry 's :class:`GLXCurses.EntryBuffer <GLXCurses.EntryBuffer.EntryBuffer>`
        and calling :func:`GLXCurses.EntryBuffer.get_max_length()
        <GLXCurses.EntryBuffer.EntryBuffer.get_max_length()>` on it.

        :return: the maximum allowed number of characters in GLXCurses.Entry, or 0 if there is no maximum.
        :rtype: int
        """
        return self.get_buffer().get_max_length()

    def get_visibility(self):
        """
        Retrieves whether the text in entry is visible.

        .. note:: :func:`GLXCurses.EntryBuffer.set_visibility() <GLXCurses.EntryBuffer.EntryBuffer.set_visibility()>`

        :return: True if the text is currently visible
        :rtype: bool
        """
        return self.visibility

    def set_completion(self, completion=None):
        """
        Sets completion to be the auxiliary completion object to use with entry .
        All further configuration of the completion mechanism is done on completion using the GtkEntryCompletion API.
        Completion is disabled if completion is set to None.

        :param completion: The GLXCurses.EntryCompletion.EntryCompletion or None.
        :type completion: GLXCurses.EntryCompletion.EntryCompletion or None
        :raise TypeError: when completion is not GLXCurses.EntryCompletion.EntryCompletion or None
        """
        if completion is None:
            self.completion = None
        else:
            if GLXCurses.glxc_type(completion):
                if completion != self.completion:
                    self.completion = completion
            else:
                raise TypeError("'completion' must be GLXCurses.EntryCompletion or None")

    def get_completion(self):
        """
        Returns the auxiliary completion object currently in use by entry .

        :return: The auxiliary completion object currently in use by entry .
        :rtype: GLXCurses.EntryCompletion or None
        """
        return self.completion

    def set_cursor_hadjustment(self, adjustment=None):
        """
        Hooks up an adjustment to the cursor position in an entry, so that when the cursor is moved, the adjustment is
        scrolled to show that position.
        See scrolled_window_get_hadjustment() for a typical way of obtaining the adjustment.

        The adjustment has to be in char units and in the same coordinate system as the entry.

        :param adjustment: an adjustment which should be adjusted when the cursor is moved, or None.
        :type adjustment: GLXCurses.Adjustment.Adjustment or None
        :raise TypeError: when completion is not GLXCurses.Adjustment.Adjustment or None
        """
        if adjustment is None:
            self.cursor_hadjustment = None
        else:
            if GLXCurses.glxc_type(adjustment):
                if adjustment != self.cursor_hadjustment:
                    self.cursor_hadjustment = adjustment
            else:
                raise TypeError("'adjustment' must be GLXCurses.Adjustment.Adjustment or None")

    def get_cursor_hadjustment(self):
        """
        Retrieves the horizontal cursor adjustment for the entry. See
        GLXCurses.Adjustment.Adjustment.set_cursor_hadjustment().

        :return: the horizontal cursor adjustment, or NULL if none has been set.
        :rtype: GLXCurses.Adjustment.Adjustment or None
        """
        return self.cursor_hadjustment

    def set_progress_fraction(self, fraction=0.0):
        """
        Causes the entry’s progress indicator to “fill in” the given fraction of the bar.
        The fraction should be between 0.0 and 1.0, inclusive.

        :param fraction: fraction of the task that’s been completed
        :type fraction: float
        :raise TypeError: when fraction is not float type
        """
        # exit as soon of possible
        if type(fraction) != float:
            raise TypeError("'fraction' must be a float between 0.0 and 1.0")
        # clamp to the range 0.0 to 1.0
        fraction = GLXCurses.clamp(fraction, smallest=0.0, largest=1.0)
        # just in case we can do nothing
        if fraction != self.progress_fraction:
            self.progress_fraction = fraction

    def get_progress_fraction(self):
        """
        Returns the current fraction of the task that’s been completed.
        See GLXCurses.Entry.Entry.set_progress_fraction().

        :return: a fraction from 0.0 to 1.0
        :rtype: float
        """
        return self.progress_fraction

    def set_progress_pulse_step(self, fraction=0.1):
        """
        Sets the fraction of total entry width to move the progress bouncing block for each call to
        GLXCurses.Entry.Entry.progress_pulse().

        :param fraction: fraction between 0.0 and 1.0
        :type fraction: float
        :raise TypeError: when fraction is not float type
        """
        # exit as soon of possible
        if type(fraction) != float:
            raise TypeError("'fraction' must be a float between 0.0 and 1.0")
        # clamp to the range 0.0 to 1.0
        fraction = GLXCurses.clamp(fraction, smallest=0.0, largest=1.0)
        # just in case we can do nothing
        if fraction != self.progress_pulse_step:
            self.progress_pulse_step = fraction

    def get_progress_pulse_step(self):
        """
        Retrieves the pulse step set with GLXCurses.Entry.Entry.set_progress_pulse_step().

        :return: a fraction from 0.0 to 1.0
        :rtype: float
        """
        return self.progress_pulse_step

    def progress_pulse(self):
        """
        Indicates that some progress is made, but you don’t know how much.
        Causes the entry’s progress indicator to enter “activity mode,” where a block bounces back and forth.
        Each call to GLXCurses.Entry.Entry.progress_pulse() causes the block to move by a little bit
        (the amount of movement per pulse is determined by GLXCurses.Entry.Entry.set_progress_pulse_step()).

        :raise NotImplementedError: GLXCurses don't deal with that yet.
        """
        raise NotImplementedError

    def im_context_filter_keypress(self):
        """
        Allow the GLXCurses.Entry input method to internally handle key press and release events.

        If this function returns TRUE, then no further processing should be done for this key event.

        See GLXCurses.Entry.im_context_filter_keypress().

        Note that you are expected to call this function from your handler when overriding key event handling.
        This is needed in the case when you need to insert your own key handling between the input method and the
        default key event handling of the GLXCurses.Entry.

        See GLXCurses.Entry.text_view_reset_im_context() for an example of use.

        :raise NotImplementedError: GLXCurses don't deal with that yet.
        """
        raise NotImplementedError

    def reset_im_context(self):
        """
        Reset the input method context of the entry if needed.

        This can be necessary in the case where modifying the buffer would confuse on-going input method behavior.

        :raise NotImplementedError: GLXCurses don't deal with that yet.
        """
        raise NotImplementedError

    def get_tabs(self):
        """
        Gets the tabstops that were set on the entry using gtk_entry_set_tabs(), if any.

        :raise NotImplementedError: GLXCurses don't deal with that yet.
        """
        raise NotImplementedError

    def set_tabs(self):
        """
        Sets a PangoTabArray; the tabstops in the array are applied to the entry text.

        :raise NotImplementedError: GLXCurses don't deal with that yet.
        """
        raise NotImplementedError

    def set_icon_from_pixbuf(self):
        """
        :raise NotImplementedError: GLXCurses don't get icon's management
        """
        raise NotImplementedError

    def set_icon_from_stock(self):
        """
        :raise NotImplementedError: GLXCurses don't get icon's management
        """
        raise NotImplementedError

    def set_icon_from_icon_name(self):
        """
        :raise NotImplementedError: GLXCurses don't get icon's management
        """
        raise NotImplementedError

    def set_icon_from_gicon(self):
        """
        :raise NotImplementedError: GLXCurses don't get icon's management
        """
        raise NotImplementedError

    def get_icon_storage_type(self):
        """
        :raise NotImplementedError: GLXCurses don't get icon's management
        """
        raise NotImplementedError

    def get_icon_pixbuf(self):
        """
        :raise NotImplementedError: GLXCurses don't get icon's management
        """
        raise NotImplementedError

    def get_icon_stock(self):
        """
        :raise NotImplementedError: GLXCurses don't get icon's management
        """
        raise NotImplementedError

    def get_icon_name(self):
        """
        :raise NotImplementedError: GLXCurses don't get icon's management
        """
        raise NotImplementedError

    def get_icon_gicon(self):
        """
        :raise NotImplementedError: GLXCurses don't get icon's management
        """
        raise NotImplementedError

    def set_icon_activatable(self):
        """
        :raise NotImplementedError: GLXCurses don't get icon's management
        """
        raise NotImplementedError

    def get_icon_activatable(self):
        """
        :raise NotImplementedError: GLXCurses don't get icon's management
        """
        raise NotImplementedError

    def set_icon_sensitive(self):
        """
        :raise NotImplementedError: GLXCurses don't get icon's management
        """
        raise NotImplementedError

    def get_icon_sensitive(self):
        """
        :raise NotImplementedError: GLXCurses don't get icon's management
        """
        raise NotImplementedError

    def get_icon_at_pos(self):
        """
        :raise NotImplementedError: GLXCurses don't get icon's management
        """
        raise NotImplementedError

    def set_icon_tooltip_text(self):
        """
        :raise NotImplementedError: GLXCurses don't get icon's management
        """
        raise NotImplementedError

    def get_icon_tooltip_text(self):
        """
        :raise NotImplementedError: GLXCurses don't get icon's management
        """
        raise NotImplementedError

    def set_icon_tooltip_markup(self):
        """
        :raise NotImplementedError: GLXCurses don't get icon's management
        """
        raise NotImplementedError

    def get_icon_tooltip_markup(self):
        """
        :raise NotImplementedError: GLXCurses don't get icon's management
        """
        raise NotImplementedError

    def set_icon_drag_source(self):
        """
        :raise NotImplementedError: GLXCurses don't get icon's management
        """
        raise NotImplementedError

    def get_current_icon_drag_source(self):
        """
        :raise NotImplementedError: GLXCurses don't get icon's management
        """
        raise NotImplementedError

    def get_icon_area(self):
        """
        :raise NotImplementedError: GLXCurses don't get icon's management
        """
        raise NotImplementedError

    def set_input_purpose(self):
        """
        :raise NotImplementedError: GLXCurses don't get icon's management
        """
        raise NotImplementedError

    def get_input_purpose(self):
        """
        :raise NotImplementedError: GLXCurses don't get icon's management
        """
        raise NotImplementedError

    def set_input_hints(self):
        """
        :raise NotImplementedError: GLXCurses don't deal with hints
        """
        raise NotImplementedError

    def get_input_hints(self):
        """
        :raise NotImplementedError: GLXCurses don't deal with hints
        """
        raise NotImplementedError

    def grab_focus_without_selecting(self):
        """
        Causes entry to have keyboard focus.

        It behaves like gtk_widget_grab_focus(), except that it doesn't select the contents of the entry.
        You only want to call this on some special entries which the user usually doesn't want to replace all text in,
        such as search-as-you-type entries.
        """
        GLXCurses.Application().has_focus = self
        self._set_focus_without_selecting(True)
        self._grab_focus(select_all=False)

    # Signals
    def _emit_activate_signal(self, user_data=None):
        """
        The activate signal is emitted when the user hits the Enter key.

        While this signal is used as a keybinding signal, it is also commonly used by applications to intercept
        activation of entries.

        The default bindings for this signal are all forms of the Enter key.

        :param user_data: user __area_data set when the signal handler was connected.
        :type user_data: list or None
        :raise TypeError: When user_data is not a list type or None
        """
        #  Try to exit as soon of possible
        if user_data is None:
            user_data = list()

        if type(user_data) != list:
            raise TypeError("'user_data' must be a list type or None")

        # Create a Dict with everything
        instance = {
            'class': self.__class__.__name__,
            'id': self.id,
            'type': 'activate',
            'widget': self,
            'user_data': user_data
        }
        # EVENT EMIT
        self.emit('SIGNAL', instance)

    def _emit_backspace_signal(self, user_data=None):
        """
        The ::backspace signal is a keybinding signal which gets emitted when the user asks for it.

        The default bindings for this signal are Backspace and Shift-Backspace

        :param user_data: user __area_data set when the signal handler was connected.
        :type user_data: list or None
        :raise TypeError: When user_data is not a list type or None
        """
        #  Try to exit as soon of possible
        if user_data is None:
            user_data = list()

        if type(user_data) != list:
            raise TypeError("'user_data' must be a list type or None")

        # Create a Dict with everything
        instance = {
            'class': self.__class__.__name__,
            'id': self.id,
            'type': 'backspace',
            'widget': self,
            'user_data': user_data
        }
        # EVENT EMIT
        self.emit('SIGNAL', instance)

    def _emit_copy_clipboard_signal(self, user_data=None):
        """
        The copy-clipboard signal is a keybinding signal which gets emitted to copy the selection to the clipboard.

        The default bindings for this signal are Ctrl-c and Ctrl-Insert.

        :param user_data: user __area_data set when the signal handler was connected.
        :type user_data: list or None
        :raise TypeError: When user_data is not a list type or None
        """
        #  Try to exit as soon of possible
        if user_data is None:
            user_data = list()

        if type(user_data) != list:
            raise TypeError("'user_data' must be a list type or None")

        # Create a Dict with everything
        instance = {
            'class': self.__class__.__name__,
            'id': self.id,
            'type': 'copy-clipboard',
            'widget': self,
            'user_data': user_data
        }
        # EVENT EMIT
        self.emit('SIGNAL', instance)

    def _emit_cut_clipboard_signal(self, user_data=None):
        """
        The cut-clipboard signal is a keybinding signal which gets emitted to cut the selection to the clipboard.

        The default bindings for this signal are Ctrl-x and Shift-Delete.

        :param user_data: user __area_data set when the signal handler was connected.
        :type user_data: list or None
        :raise TypeError: When user_data is not a list type or None
        """
        #  Try to exit as soon of possible
        if user_data is None:
            user_data = list()

        if type(user_data) != list:
            raise TypeError("'user_data' must be a list type or None")

        # Create a Dict with everything
        instance = {
            'class': self.__class__.__name__,
            'id': self.id,
            'type': 'cut-clipboard',
            'widget': self,
            'user_data': user_data
        }
        # EVENT EMIT
        self.emit('SIGNAL', instance)

    def _emit_delete_from_cursor_signal(self, delete_type=GLXCurses.GLXC.DELETE_CHARS, count=1, user_data=list()):
        """
        The delete-from-cursor signal is a keybinding signal which gets emitted when the user
        initiates a text deletion.

        If the type is GLXC.DELETE_CHARS, GLXCurses deletes the selection if there is one,
        otherwise it deletes the requested number of characters.

        The default bindings for this signal are Delete for deleting a character and Ctrl-Delete for deleting a word.

        :param delete_type: the granularity of the deletion, as a GLXC.DeleteType
        :type delete_type: a GLXC.DeleteType
        :param count: the number of type units to delete
        :type count: int
        :param user_data: the object which received the signal
        :type user_data: list
        """
        #  Try to exit as soon of possible
        if delete_type not in GLXCurses.GLXC.DeleteType:
            raise TypeError("'delete_type' must be a valid GLXC.DeleteType or None")
        if type(count) != int:
            raise TypeError("'count' must be a int type or None")
        if type(user_data) != list:
            raise TypeError("'user_data' must be a list type or None")

        # Create a Dict with everything
        instance = {
            'class': self.__class__.__name__,
            'id': self.id,
            'type': 'delete-from-cursor',
            'widget': self,
            'delete_type': delete_type,
            'count': count,
            'user_data': user_data
        }
        # EVENT EMIT
        self.emit('SIGNAL', instance)

    def _emit_icon_press_signal(self, user_data=None):
        """

        :param user_data: the object which received the signal
        """
        if user_data is None:
            user_data = list()
        # TODO: Everything cher's
        pass

    def _emit_icon_release_signal(self, user_data=None):
        """

        :param user_data: the object which received the signal
        """
        if user_data is None:
            user_data = list()
        # TODO: Everything cher's
        pass

    def _emit_insert_at_cursor_signal(self, user_data=None):
        """

        :param user_data: the object which received the signal
        """
        if user_data is None:
            user_data = list()
        # TODO: Everything cher's
        pass

    def _emit_move_cursor_signal(self, user_data=None):
        """

        :param user_data: the object which received the signal
        """
        if user_data is None:
            user_data = list()

        # Create a Dict with everything
        instance = {
            'class': self.__class__.__name__,
            'type': 'move-cursor',
            'id': self.id,
            'user_data': user_data
        }

        # Emit the signal
        self.emit('SIGNALS', instance)

    def _emit_paste_clipboard_signal(self, user_data=None):
        """

        :param user_data: the object which received the signal
        """
        if user_data is None:
            user_data = list()
        # TODO: Everything cher's
        pass

    def _emit_populate_popup_signal(self, user_data=None):
        """

        :param user_data: the object which received the signal
        """
        if user_data is None:
            user_data = list()
        # TODO: Everything cher's
        pass

    def _emit_preedit_changed_signal(self, user_data=None):
        """

        :param user_data: the object which received the signal
        """
        if user_data is None:
            user_data = list()
        # TODO: Everything cher's
        pass

    def _emit_toggle_overwrite_signal(self, user_data=None):
        """
        The “toggle-overwrite” signal

        The ::toggle-overwrite signal is a keybinding signal which gets emitted to toggle the overwrite mode of the
        entry.

        The default bindings for this signal is Insert.

        :param user_data: the object which received the signal
        """
        if user_data is None:
            user_data = list()

        # Create a Dict with everything
        instance = {
            'class': self.__class__.__name__,
            'type': 'toggle-overwrite',
            'id': self.id,
            'user_data': user_data
        }
        # EVENT EMIT
        self.emit('SIGNALS', instance)

    # INTERNAL
    # Internal

    def _get_min_length_hard_limit(self):
        return self._min_length_hard_limit

    def _get_max_length_hard_limit(self):
        return self._max_length_hard_limit

    # State
    def get_states(self):
        return self.states_list

    # Internal
    def _draw_entry(self):
        self._check_selected()
        self._update_preferred_sizes()
        self._check_justify()
        self._check_position_type()

        # if not self.sensitive:
        #     self._draw_the_good_entry(
        #         color=self.style.get_color_pair(
        #             foreground=self.style.get_color_text('bg', 'STATE_NORMAL'),
        #             background=self.style.get_color_text('dark', 'STATE_NORMAL')
        #         )
        #     )
        # elif self.state['PRELIGHT']:
        #     self._draw_the_good_entry(
        #         color=self.style.get_color_pair(
        #             foreground=self.style.get_color_text('dark', 'STATE_NORMAL'),
        #             background=self.style.get_color_text('bg', 'STATE_PRELIGHT')
        #         )
        #     )
        # elif self.state['NORMAL']:
        #
        #     )
        self._draw_the_good_entry()

    def _draw_the_good_entry(self, color=None):

        if color is None:
            color = self.style.color(
                bg=self.style.get_color_text('black', 'STATE_NORMAL'),
                fg=self.style.get_color_text('bg', 'STATE_SELECTED')
            )
        try:
            # compute interface completion size
            completion_interface_size = 0
            if self.get_completion() is not None:
                completion_interface_size += len(self.button_completion)

            # Draw the with Justification and PositionType
            message_to_display = GLXCurses.resize_text_wrap_char(
                text=self._get_message_to_display(),
                max_width=self.width - completion_interface_size
            )
            for x in range(self.x_offset, self.width - completion_interface_size):
                self.subwin.addstr(
                    self.y_offset,
                    self.x_offset + x,
                    " ",
                    color
                )
            self.subwin.addstr(
                self.y_offset,
                self.x_offset,
                message_to_display,
                color
            )

            if self.can_focus:
                if isinstance(GLXCurses.Application().has_focus, GLXCurses.ChildElement) and \
                        GLXCurses.Application().has_focus.id == self.id:
                    # Cursor print

                    try:
                        # Test cursos with curses
                        # self.subwin.keypad(1)
                        # self.win.subwin(self.__y_offset, self.x_offset + self.get_position())
                        #  It work
                        self.subwin.attron(curses.A_BLINK)
                        self.subwin.addstr(
                            self.y_offset,
                            self.x_offset + self.get_position(),
                            self._get_message_to_display()[self.get_position()],
                            color | curses.A_REVERSE
                        )
                        self.subwin.attroff(curses.A_BLINK)
                    except IndexError:
                        self.subwin.attron(curses.A_BLINK)
                        self.subwin.addstr(
                            self.y_offset,
                            self.x_offset + self.get_position(),
                            " ",
                            color | curses.A_REVERSE
                        )
                        self.subwin.attroff(curses.A_BLINK)
                    # Selection
                    if self.get_selection_bounds():
                        if self.start_pos < self.end_pos:
                            for value in range(self.start_pos, self.end_pos, 1):
                                try:
                                    self.subwin.addstr(
                                        self.y_offset,
                                        self.x_offset + value,
                                        self._get_message_to_display()[value],
                                        color | curses.A_REVERSE
                                    )
                                except IndexError:
                                    pass
                        elif self.start_pos > self.end_pos:
                            for value in range(self.end_pos, self.start_pos, 1):
                                try:
                                    self.subwin.addstr(
                                        self.y_offset,
                                        self.x_offset + value,
                                        self._get_message_to_display()[value],
                                        color | curses.A_REVERSE
                                    )
                                except IndexError:
                                    pass
        except curses.error:
            pass

        # Interface management
        if self.get_completion() is not None:

            if self.has_prelight:
                color = self.style.color(
                    fg=self.style.get_color_text('dark', 'STATE_NORMAL'),
                    bg=self.style.get_color_text('bg', 'STATE_PRELIGHT')
                )

            elif self.state['NORMAL']:
                color = self.style.color(
                    fg=self.style.get_color_text('text', 'STATE_NORMAL'),
                    bg=self.style.get_color_text('bg', 'STATE_NORMAL')
                )
            else:
                color = self.style.color(
                    fg=self.style.get_color_text('text', 'STATE_NORMAL'),
                    bg=self.style.get_color_text('bg', 'STATE_NORMAL')
                )

            try:
                self.subwin.insstr(
                    self.y_offset,
                    self.x_offset + (self.width - len(self.button_completion)),
                    self.button_completion,
                    color
                )
            except curses.error:
                pass

    def _handle_key_event(self, event_signal, *event_args):
        # Check if we have to care about keyboard event
        if self.sensitive and \
                isinstance(GLXCurses.Application().has_focus, GLXCurses.ChildElement) and \
                GLXCurses.Application().has_focus.id == self.id:
            # setting
            key = event_args[0]

            # Ctrl + a
            if key == 1:
                self.select_region(
                    start_pos=0,
                    end_pos=self.get_text_length()
                )

            # Ctrl + c
            if key == 3:
                self._emit_copy_clipboard_signal()
                self.copy_clipboard()

            # Ctrl + v
            if key == 22:
                self.paste_clipboard()

            # Ctrl-x and Shift-Delete
            if key == 24 or key == 383:
                self._emit_cut_clipboard_signal()
                self.cut_clipboard()

            # Shit + End
            if key == 386:
                self.set_position(
                    position=self.get_position()
                )
                self.select_region(
                    start_pos=self.get_position(),
                    end_pos=len(self.get_text())
                )
                self.set_position(
                    position=len(self.get_text())
                )

            # Shit + Home
            if key == 391:
                self.set_position(
                    position=GLXCurses.clamp_to_zero(self.get_position())
                )
                self.select_region(
                    start_pos=0,
                    end_pos=self.get_position()
                )
                self.set_position(
                    position=GLXCurses.clamp_to_zero(self.get_position() + 1)
                )

            # Shit + Left Arrow
            if key == 393:
                if self.start_pos is None:
                    self.select_region(
                        start_pos=GLXCurses.clamp_to_zero(self.get_position() + 1),
                        end_pos=GLXCurses.clamp_to_zero(self.get_position() - 1)
                    )
                    self.set_position(
                        position=GLXCurses.clamp_to_zero(self.get_position() - 1)
                    )
                else:
                    self.set_position(
                        position=GLXCurses.clamp_to_zero(self.get_position())
                    )
                    self.select_region(end_pos=GLXCurses.clamp_to_zero(self.get_position() - 1)
                                       )
                    self.set_position(
                        position=GLXCurses.clamp_to_zero(self.get_position() - 1)
                    )

            # Shit + Right Arrow
            if key == 402:
                if self.start_pos is None:
                    self.select_region(
                        start_pos=GLXCurses.clamp_to_zero(self.get_position()),
                        end_pos=GLXCurses.clamp_to_zero(self.get_position() + 1)
                    )
                    self.set_position(position=GLXCurses.clamp_to_zero(self.get_position() + 1)
                                      )
                else:
                    self.set_position(
                        position=GLXCurses.clamp_to_zero(self.get_position())
                    )
                    self.select_region(
                        end_pos=GLXCurses.clamp_to_zero(self.get_position() + 1)
                    )
                    self.set_position(
                        position=GLXCurses.clamp_to_zero(self.get_position() + 1)
                    )

            # Touch Escape
            if key == GLXCurses.GLXC.KEY_ESC:
                if self.get_selection_bounds():
                    self.select_region()
                    # self.set_position(-1)

                else:
                    GLXCurses.Application().has_focus = None

                    self.is_focus = False
                    self.has_focus = False
                    self._check_selected()

            # Touch Supp
            if key == curses.KEY_DC:
                if self.get_selection_bounds():
                    start_pos_bkp = self.start_pos
                    self.delete_selection()
                    self.set_position(start_pos_bkp)
                else:
                    if self.get_text_length() >= 1:
                        self.delete_text(
                            start_pos=self.get_position()
                        )
                    else:
                        self.set_text("")
                        self.set_position(
                            position=0
                        )

            # Touch Del
            if key == curses.KEY_BACKSPACE or key == GLXCurses.GLXC.KEY_DEL:
                if self.get_selection_bounds():
                    start_pos_bkp = self.start_pos
                    self.delete_selection()
                    self.set_position(start_pos_bkp)
                else:
                    if self.get_position() > 0:
                        if len(self.get_text()) >= 0:
                            self.delete_text(
                                start_pos=GLXCurses.clamp_to_zero(self.get_position() - 1)
                            )
                            self.set_position(
                                position=GLXCurses.clamp_to_zero(self.get_position() - 1)
                            )
                        elif len(self.get_text()) >= 1:
                            self.delete_text(
                                start_pos=GLXCurses.clamp_to_zero(self.get_position() - 1)
                            )
                            self.set_position(
                                position=GLXCurses.clamp_to_zero(self.get_position() - 1)
                            )
                        else:
                            self.set_text("")
                            self.set_position(

                                position=0
                            )
                    if self.get_position() == 0 and self.get_text_length() == 1:
                        self.set_text("")
                        self.set_position(
                            position=0
                        )
                self._emit_backspace_signal()
            if key == 391:
                if self.get_selection_bounds():
                    self.select_region(
                        start_pos=0,
                        end_pos=self.get_position()
                    )
                    self.set_position(
                        position=0
                    )
            if key == curses.KEY_HOME:
                self.select_region()
                self.set_position(
                    position=0
                )

            # END Touch
            if key == curses.KEY_END:
                self.select_region()
                self.set_position(
                    position=self.get_text_length()
                )

            if key == curses.KEY_RIGHT:
                self.set_position(

                    position=self.get_position() + 1
                )
                self.select_region()

            if key == curses.KEY_LEFT:
                self.set_position(

                    position=GLXCurses.clamp_to_zero(self.get_position() - 1)
                )
                self.select_region()

            # Insert Text
            if key == curses.KEY_ENTER or key == GLXCurses.GLXC.KEY_LF:
                self._emit_activate_signal()
            elif chr(key) in GLXCurses.GLXC.Printable:
                self.insert_text(
                    new_text=chr(key),
                    position=self.get_position()
                )

    def _handle_mouse_event(self, event_signal, event_args):
        if self.sensitive:
            (mouse_event_id, x, y, z, event) = event_args
            # Be sure we select really the Button
            y -= self.y
            x -= self.x

            if self.y_offset >= y > self.y_offset - self.preferred_height:
                if (self.x_offset - 1) + self.width >= x > (self.x_offset - 1):
                    self._grab_focus()
                    # We are sure about the button have been clicked
                    self.states_list = '; '.join(state_string for state, state_string
                                                 in self.curses_mouse_states.items()
                                                 if event & state)

                    # check what is the small button
                    position_interface_start = self.x_offset - 1
                    position_interface_start += self.width

                    position_interface_end = self.x_offset - 1
                    position_interface_end += self.width
                    position_interface_end -= len(self.button_completion)

                    # we check if we can draw the cursor
                    if position_interface_start > x <= position_interface_end:
                        if self.get_editable():
                            # for finally set the thing
                            self.set_position(
                                position=x
                            )
                    # INTERNAL METHOD
                    # BUTTON1
                    if event == curses.BUTTON1_PRESSED:
                        self._grab_focus()

                        if not position_interface_start > x <= position_interface_end:
                            self._set_state_prelight(True)
                        if self.get_selection_bounds():
                            self.select_region()
                        if self.start_pos is None:
                            self.select_region(start_pos=x)
                        else:
                            if self.start_pos < x:
                                self.select_region(
                                    start_pos=self.start_pos,
                                    end_pos=x
                                )
                            else:
                                self.select_region(
                                    start_pos=self.start_pos + 1,
                                    end_pos=x
                                )
                        self._check_selected()
                    elif event == curses.BUTTON1_RELEASED:

                        self._grab_focus()
                        self._check_selected()
                        self._set_state_prelight(False)
                        if self.start_pos < x:
                            self.select_region(
                                start_pos=self.start_pos,
                                end_pos=x
                            )
                        else:
                            self.select_region(
                                start_pos=self.start_pos + 1,
                                end_pos=x
                            )

                    if event == curses.BUTTON1_CLICKED:
                        self.select_region()
                        self._grab_focus()

                    if event == curses.BUTTON1_DOUBLE_CLICKED:
                        self._grab_focus()

                        # Remove the actual selection
                        self.select_region()
                        if self.get_visibility():
                            # searching for start_pos and end_pos
                            mini = 0
                            maxi = 0
                            regexp = r"\s+"
                            for letter in range(x, 0, -1):
                                if re.match(regexp, self.get_text()[letter]):
                                    mini = letter + 1
                                    break

                            for letter in range(x, self.get_text_length(), 1):
                                if re.match(regexp, self.get_text()[letter]):
                                    maxi = letter - 1
                                    break
                            # create a selection
                            self.select_region(start_pos=mini, end_pos=maxi)
                            # set the cursor position
                            self.set_position(position=maxi)
                        else:
                            # create a selection
                            self.select_region(start_pos=0, end_pos=self.get_text_length())
                            # set the cursor position
                            self.set_position(position=self.get_text_length() - 1)

                    if event == curses.BUTTON1_TRIPLE_CLICKED:
                        self.select_region(
                            start_pos=0,
                            end_pos=len(self.get_text())
                        )
                        self._grab_focus()

                    # BUTTON2
                    if event == curses.BUTTON2_PRESSED:
                        self._grab_focus()
                        self._check_selected()
                        if not position_interface_start > x <= position_interface_end:
                            self._set_state_prelight(True)
                    elif event == curses.BUTTON2_RELEASED:
                        self._set_state_prelight(False)
                        self._grab_focus()
                        self.paste_clipboard()

                    if event == curses.BUTTON2_CLICKED:
                        self._grab_focus()

                    if event == curses.BUTTON2_DOUBLE_CLICKED:
                        self._grab_focus()

                    if event == curses.BUTTON2_TRIPLE_CLICKED:
                        self._grab_focus()

                    # BUTTON3
                    if event == curses.BUTTON3_PRESSED:
                        self._grab_focus()
                        self._check_selected()
                        if not position_interface_start > x <= position_interface_end:
                            self._set_state_prelight(True)
                    elif event == curses.BUTTON3_RELEASED:
                        self._set_state_prelight(False)
                        self._grab_focus()

                    if event == curses.BUTTON3_CLICKED:
                        self._grab_focus()

                    if event == curses.BUTTON3_DOUBLE_CLICKED:
                        self._grab_focus()

                    if event == curses.BUTTON3_TRIPLE_CLICKED:
                        self._grab_focus()

                    # BUTTON4
                    if event == curses.BUTTON4_PRESSED:
                        self._grab_focus()
                        self._check_selected()
                        if not position_interface_start > x <= position_interface_end:
                            self._set_state_prelight(True)
                    elif event == curses.BUTTON4_RELEASED:
                        self._set_state_prelight(False)
                        self._grab_focus()

                    if event == curses.BUTTON4_CLICKED:
                        self._grab_focus()

                    if event == curses.BUTTON4_DOUBLE_CLICKED:
                        self._grab_focus()

                    if event == curses.BUTTON4_TRIPLE_CLICKED:
                        self._grab_focus()

                    if event == curses.BUTTON_SHIFT | curses.BUTTON1_CLICKED:

                        if self.start_pos is None:
                            self.select_region(
                                start_pos=x,
                            )
                        else:
                            self.select_region(
                                end_pos=x
                            )
                    if event == curses.BUTTON_CTRL:
                        pass
                    if event == curses.BUTTON_ALT:
                        pass

                    # Create a Dict with everything
                    instance = {
                        'class': self.__class__.__name__,
                        'id': self.id
                    }
                    # EVENT EMIT
                    # Application().emit(self.curses_mouse_states[event], instance)
                    self.emit(self.curses_mouse_states[event], instance)
            else:
                # Nothing the better is to clean the prelight
                self._set_state_prelight(False)
        else:
            # create a log chain text
            log_text = self.__class__.__name__
            log_text += ': '
            log_text += self.get_text()
            log_text += ' '
            log_text += self.id
            log_text += 'is not sensitive.'
            # make the log
            logging.debug(log_text)

    def _check_selected(self):
        if self.can_focus:
            if isinstance(GLXCurses.Application().has_focus, GLXCurses.ChildElement) and \
                    GLXCurses.Application().has_focus.id == self.id:
                self.is_focus = True
                self._update_preferred_sizes()

            else:
                self.is_focus = False
                self._update_preferred_sizes()

        else:
            pass

    def _set_state_prelight(self, value):
        if bool(value):
            self.has_prelight = True
            self.button_completion = self.interface_prelight
        else:
            self.has_prelight = False
            self.button_completion = self.interface_normal

    def _get_state_prelight(self):
        return self.has_prelight

    def _check_justify(self):
        """Check the justification of the X axe"""
        width = self.width
        preferred_width = self.preferred_width

        self.x_offset = 0
        if self.justify == GLXCurses.GLXC.JUSTIFY_CENTER:
            # Clamp value and impose the center
            if width is None:
                estimated_width = 0
            elif width <= 0:
                estimated_width = 0
            elif width == 1:
                estimated_width = 0
            else:
                estimated_width = int(width / 2)

            # Clamp value and impose the center
            if preferred_width is None:
                estimated_preferred_width = 0
            elif preferred_width <= 0:
                estimated_preferred_width = 0
            elif preferred_width == 1:
                estimated_preferred_width = 0
            else:
                estimated_preferred_width = int(preferred_width / 2)

            # Make the compute
            final_value = int(estimated_width - estimated_preferred_width)

            # clamp the result
            if final_value <= 0:
                final_value = 0

            # Finally set the value
            self.x_offset = 0
            # self._set_x_offset(final_value)

        elif self.justify == GLXCurses.GLXC.JUSTIFY_LEFT:

            # Finally set the value
            self.x_offset = 0

        elif self.justify == GLXCurses.GLXC.JUSTIFY_RIGHT:
            # Clamp estimated_width
            estimated_width = GLXCurses.clamp_to_zero(width)

            # Clamp preferred_width
            estimated_preferred_width = GLXCurses.clamp_to_zero(preferred_width)

            # Make the compute
            final_value = int(estimated_width - estimated_preferred_width)

            # clamp the result
            if final_value <= 0:
                final_value = 0

            # Finally set the value
            self.x_offset = 0
            # self.x_offset = final_value

    def _check_position_type(self):
        # PositionType: CENTER, TOP, BOTTOM
        height = self.height
        preferred_height = self.preferred_height

        if self.position_type == GLXCurses.GLXC.POS_CENTER:
            # Clamp height
            if height is None:
                estimated_height = 0
            elif height <= 0:
                estimated_height = 0
            elif height == 1:
                # prevent a 1/2 = float(0.5) case
                estimated_height = 0
            else:
                estimated_height = int(height / 2)

            # Clamp preferred_height
            if preferred_height is None:
                estimated_preferred_height = 0
            elif preferred_height <= 0:
                estimated_preferred_height = 0
            elif preferred_height == 1:
                # prevent a 1/2 = float(0.5) case
                estimated_preferred_height = 0
            else:
                estimated_preferred_height = int(preferred_height / 2)

            # Make teh compute
            final_value = int(estimated_height - estimated_preferred_height)

            # Clamp the result to a positive
            if final_value <= 0:
                final_value = 0

            self.y_offset = final_value

        elif self.position_type == GLXCurses.GLXC.POS_TOP:
            self.y_offset = 0

        elif self.position_type == GLXCurses.GLXC.POS_BOTTOM:
            # Clamp height
            estimated_height = GLXCurses.clamp_to_zero(height)

            # Clamp preferred_height
            estimated_preferred_height = GLXCurses.clamp_to_zero(preferred_height)

            # Make the compute
            final_value = int(estimated_height - estimated_preferred_height)

            # Clamp the result to a positive
            if final_value <= 0:
                final_value = 0

            # Clamp height
            estimated_height = GLXCurses.clamp_to_zero(height)

            # Clamp preferred_height
            estimated_preferred_height = GLXCurses.clamp_to_zero(preferred_height)

            # Make the compute
            final_value = int(estimated_height - estimated_preferred_height)

            # Clamp the result to a positive
            if final_value <= 0:
                final_value = 0

            self.y_offset = final_value

    def _update_preferred_sizes(self):
        self.preferred_width = self._get_estimated_preferred_width()
        self.preferred_height = self._get_estimated_preferred_height()

    def _get_estimated_preferred_width(self):
        """
        Estimate a preferred width, by consider X Location, allowed width

        :return: a estimated preferred width
        :rtype: int
        """
        completion_interface_size = 0
        if self.get_completion() is not None:
            completion_interface_size += len(self.button_completion)

        if self.get_text():
            estimated_preferred_width = self.width
            estimated_preferred_width -= completion_interface_size

        else:
            estimated_preferred_width = 0
            estimated_preferred_width += completion_interface_size

        return estimated_preferred_width

    def _get_estimated_preferred_height(self):
        """
        Estimate a preferred height, by consider Y Location

        :return: a estimated preferred height
        :rtype: int
        """
        estimated_preferred_height = 1
        return estimated_preferred_height

    def _get_message_to_display(self):
        if self.get_visibility():
            return self.get_text()
        else:
            return self._get_invisible_char() * self.get_text_length()

    def _get_invisible_char(self):
        """
        Return the invisible_char

        :return: the invisible_char
        :rtype: str
        """
        return self.invisible_char

    def _grab_focus(self, select_all=True):
        """
        Internal method, for Select the contents of the Entry it take focus.

        See: grab_focus_without_selecting ()

        :param select_all: True if all the text is selected when the entry grab focus
        :type select_all: bool
        """
        if self.can_focus:
            GLXCurses.Application().has_focus = self
            GLXCurses.Application().has_default = self
            GLXCurses.Application().has_prelight = self
            # self.has_focus = True
            # self.has_prelight = True
            # self.has_default = True
            if not self._get_focus_without_selecting():
                if select_all:
                    self.select_region(start_pos=0, end_pos=-1)

    def _set_focus_without_selecting(self, boolean=None):
        """
        Internal function for set _focus_without_selecting attribute. It attribut is check during focus grab entrence.

        see: grab_focus_without_selecting()

        boolean=None for back to default.

        :param boolean: False if select the contents of the entry when grab focus.
        :type boolean: bool or None
        :raise TypeError: When ``boolean`` is not a bool type or None
        """
        # Exit as soon of possible
        if boolean is None:
            boolean = False
        if type(boolean) != bool:
            raise TypeError("'boolean' must be a bool type or None")

        # make the job
        if self._focus_without_selecting != boolean:
            self._focus_without_selecting = boolean

    def _get_focus_without_selecting(self):
        """
        Internal function for get self._focus_without_selecting attribute value

        :return: self._focus_without_selecting attribute value
        :rtype: bool
        """
        return self._focus_without_selecting

    # Unimplemented
    def _enter(self):
        raise NotImplementedError

    def _leave(self):
        raise NotImplementedError
