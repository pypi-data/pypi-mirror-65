#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import GLXCurses
# import logging
# import curses


# https://developer.gnome.org/gtk3/stable/GtkTextView.html
class TextView(GLXCurses.Container):
    def __init__(self):
        GLXCurses.Container.__init__(self)

        self.__accepts_tab = None
        self.__bottom_margin = None
        self.__buffer = None
        self.__cursor_visible = None
        self.__editable = None
        #   self.__im_module = None
        self.__indent = None
        self.__input_hints = None
        self.__input_purpose = None
        self.__justification = None
        self.__left_margin = None
        # self.__monospace = None
        self.__overwrite = None
        # self.__chars_above_lines = None
        # self.__chars_below_lines = None
        # self.__chars_inside_wrap = None
        self.__populate_all = None
        self.__right_margin = None
        self.__tabs = None
        self.__top_margin = None
        self.__wrap_mode = None

        self.__error_underline_color = None

        # Set default value
        self.accept_tab = True
        self.bottom_margin = 0
        self.buffer = GLXCurses.TextBuffer()
        self.cursor_visible = True
        self.editable = True
        self.indent = 0
        self.right_margin = 0
        self.input_hints = GLXCurses.GLXC.INPUT_HINTS_NONE
        self.input_purpose = GLXCurses.GLXC.INPUT_PURPOSE_FREE_FORM
        self.justification = GLXCurses.GLXC.JUSTIFY_CENTER
        self.left_margin = 0
        self.overwrite = False
        self.populate_all = True
        self.top_margin = 0

    @property
    def accept_tab(self):
        """
        Whether Tab will result in a tab character being entered.

        Default value is ``True``, and be restored when ``accept_tab`` is set to ``None``

        :return: If ``True`` Tab key will produce Tab char \t
        :rtype: bool
        """
        return self.__accepts_tab

    @accept_tab.setter
    def accept_tab(self, value=True):
        """
        Set the ``accept_tab`` property value

        :param value: If ``True`` Tab key will produce Tab char \t
        :type value: bool or None
        :raise TypeError: When value is not bool type or None
        """
        if value is None:
            value = True
        if type(value) != bool:
            raise TypeError('"accept_tab" value must be a bool type or None')
        if self.accept_tab != value:
            self.__accepts_tab = value

    @property
    def bottom_margin(self):
        """
        The bottom margin for text in the text view.

        :return: The bottom margin padding
        :rtype: int
        """
        return self.__bottom_margin

    @bottom_margin.setter
    def bottom_margin(self, value=0):
        """
        Set the ``bottom_margin`` property value

        Default value is ``0``, and be restored when ``bottom_margin`` is set to ``None``

        :param value: The value set here is padding
        :type value: int or None
        :raise TypeError: When value is not int type or None
        """
        if value is None:
            value = 0
        if type(value) != int:
            raise TypeError('"bottom_margin" value must be a int type or None')
        if self.bottom_margin != GLXCurses.clamp_to_zero(value):
            self.__bottom_margin = GLXCurses.clamp_to_zero(value)

    @property
    def buffer(self):
        """
        The buffer which is displayed.

        :return: a buffer
        :rtype: GLXCurses.TextBuffer
        """
        return self.__buffer

    @buffer.setter
    def buffer(self, value=None):
        """
        Set the ``buffer`` property value

        :param value: a Text Buffer
        :type value: GLXCurses.TextBuffer
        """
        if value is not None and not isinstance(value, GLXCurses.TextBuffer):
            raise TypeError('"buffer" value must be a GLXCurses.TextBuffer instance or None')
        if self.buffer != value:
            self.__buffer = value

    @property
    def cursor_visible(self):
        """
        If the insertion cursor is shown.

        Default value is ``True``, and be restored when ``cursor_visible`` is set to ``None``

        :return: If ``True`` the cursor will be visible
        :rtype: bool
        """
        return self.__cursor_visible

    @cursor_visible.setter
    def cursor_visible(self, value=True):
        """
        Set the ``cursor_visible`` property value

        :param value: If ``True`` the cursor will be visible
        :type value: bool or None
        :raise TypeError: When value is not bool type or None
        """
        if value is None:
            value = True
        if type(value) != bool:
            raise TypeError('"cursor_visible" value must be a bool type or None')
        if self.cursor_visible != value:
            self.__cursor_visible = value

    @property
    def editable(self):
        """
        Whether the text can be modified by the user.

        Default value is ``True``, and be restored when ``editable`` is set to ``None``

        :return: If ``True`` the text can be modified
        :rtype: bool
        """
        return self.__editable

    @editable.setter
    def editable(self, value=True):
        """
        Set the ``editable`` property value

        :param value: If ``True`` the text can be modified
        :type value: bool or None
        :raise TypeError: When value is not bool type or None
        """
        if value is None:
            value = True
        if type(value) != bool:
            raise TypeError('"editable" value must be a bool type or None')
        if self.editable != value:
            self.__editable = value

    @property
    def indent(self):
        """
        Amount to indent the paragraph, in chars.

        :return: indentation in chars
        :rtype: int
        """
        return self.__indent

    @indent.setter
    def indent(self, value=0):
        """
        Set the ``indent`` property value

        Default value is ``0``, and be restored when ``indent`` is set to ``None``

        :param value: Indentation of the paragraph, in chars.
        :type value: int or None
        :raise TypeError: When value is not int type or None
        """
        if value is None:
            value = 0
        if type(value) != int:
            raise TypeError('"indent" value must be a int type or None')
        if self.indent != GLXCurses.clamp_to_zero(value):
            self.__indent = GLXCurses.clamp_to_zero(value)

    @property
    def input_hints(self):
        """
        Additional hints (beyond “``input_purpose``”) that allow input methods to fine-tune their behaviour.

        :return: The right margin padding
        :rtype: int
        """
        return self.__input_hints

    @input_hints.setter
    def input_hints(self, value=None):
        """
        Set the ``input_hints`` property value

        Default value is ``GLXCurses.GLXC.INPUT_HINTS_NONE``, and be restored when ``input_hints`` is set to ``None``

        :param value: Additional hints (beyond “input-purpose”)
        :type value: GLXCurses.GLXC.InputHints
        :raise TypeError: When value is str type or None
        :raise ValueError: When value is not in GLXCurses.GLXC.InputHints
        """
        if value is None:
            value = GLXCurses.GLXC.INPUT_HINTS_NONE
        if type(value) != str:
            raise TypeError('"input_hints" value must be a str type or None')
        if value not in GLXCurses.GLXC.InputHints:
            raise ValueError('"input_hints" must be a valid GLXCurses.GLXC.InputHints')
        if self.input_hints != value:
            self.__input_hints = value

    @property
    def input_purpose(self):
        """
        The purpose of this text field.

        This property can be used by on-screen keyboards and other input methods to adjust their behaviour.

        :return: The right margin padding
        :rtype: int
        """
        return self.__input_purpose

    @input_purpose.setter
    def input_purpose(self, value=None):
        """
        Set the ``input_purpose`` property value

        Default value is ``GLXCurses.GLXC.INPUT_PURPOSE_FREE_FORM``, and be restored
        when ``input_purpose`` is set to ``None``

        :param value: The purpose of this text field
        :type value: str or None
        :raise TypeError: When value is not str type or None
        :raise ValueError: When value is not in GLXCurses.GLXC.InputPurpose
        """
        if value is None:
            value = GLXCurses.GLXC.INPUT_PURPOSE_FREE_FORM
        if type(value) != str:
            raise TypeError('"input_purpose" value must be a str type or None')
        if value not in GLXCurses.GLXC.InputPurpose:
            raise ValueError('"input_purpose" must be a valid GLXCurses.GLXC.InputPurpose')
        if self.input_purpose != value:
            self.__input_purpose = value

    @property
    def justification(self):
        """
        Left, right, or center justification.

        :return: str
        :rtype: GLXCurses.GLXC.Justification
        """
        return self.__justification

    @justification.setter
    def justification(self, value=None):
        """
        Left, right, or center justification.

        :param value: a justification
        :type value: str
        """
        if value is None:
            value = GLXCurses.GLXC.JUSTIFY_CENTER
        if type(value) != str:
            raise TypeError('"justification" value must be a str type or None')
        if value not in GLXCurses.GLXC.Justification:
            raise ValueError('"justification" must be a valid GLXCurses.GLXC.Justification')
        if self.justification != str(value).upper():
            self.__justification = str(value).upper()

    @property
    def left_margin(self):
        """
        The left margin for text in the text view.

        :return: The left margin padding
        :rtype: int
        """
        return self.__left_margin

    @left_margin.setter
    def left_margin(self, value=0):
        """
        Set the ``left_margin`` property value

        Default value is ``0``, and be restored when ``left_margin`` is set to ``None``

        :param value: The value set here is padding
        :type value: int or None
        :raise TypeError: When value is not int type or None
        """
        if value is None:
            value = 0
        if type(value) != int:
            raise TypeError('"left_margin" value must be a int type or None')
        if self.left_margin != GLXCurses.clamp_to_zero(value):
            self.__left_margin = GLXCurses.clamp_to_zero(value)

    # Monospace is not use

    @property
    def overwrite(self):
        """
        Whether entered text overwrites existing contents.

        Default value is ``False``, and be restored when ``overwrite`` is set to ``None``

        :return: If ``True`` text overwrites existing contents
        :rtype: bool
        """
        return self.__overwrite

    @overwrite.setter
    def overwrite(self, value=None):
        """
        Set the ``overwrite`` property value

        :param value: If ``True`` text overwrites existing contents
        :type value: bool or None
        :raise TypeError: When value is not bool type or None
        """
        if value is None:
            value = False
        if type(value) != bool:
            raise TypeError('"overwrite" value must be a bool type or None')
        if self.overwrite != value:
            self.__overwrite = value

    # The “pixels-above-lines” property

    # The “pixels-below-lines” property

    # The “pixels-inside-wrap” property

    @property
    def populate_all(self):
        return self.__populate_all

    @populate_all.setter
    def populate_all(self, value=None):
        if value is None:
            value = True
        if type(value) != bool:
            raise TypeError('"populate_all" value must be a bool type or None')
        if self.populate_all != value:
            self.__populate_all = value

    @property
    def right_margin(self):
        """
        The right margin for text in the text view.

        :return: The right margin padding
        :rtype: int
        """
        return self.__right_margin

    @right_margin.setter
    def right_margin(self, value=0):
        """
        Set the ``right_margin`` property value

        Default value is ``0``, and be restored when ``bottom_margin`` is set to ``None``

        :param value: The value set here is padding
        :type value: int or None
        :raise TypeError: When value is not int type or None
        """
        if value is None:
            value = 0
        if type(value) != int:
            raise TypeError('"right_margin" value must be a int type or None')
        if self.right_margin != GLXCurses.clamp_to_zero(value):
            self.__right_margin = GLXCurses.clamp_to_zero(value)

    # Tabs

    @property
    def top_margin(self):
        """
        The top margin for text in the text view.

        :return: The top margin padding
        :rtype: int
        """
        return self.__top_margin

    @top_margin.setter
    def top_margin(self, value=0):
        """
        Set the ``top_margin`` property value

        Default value is ``0``, and be restored when ``top_margin`` is set to ``None``

        :param value: The value set here is padding
        :type value: int or None
        :raise TypeError: When value is not int type or None
        """
        if value is None:
            value = 0
        if type(value) != int:
            raise TypeError('"top_margin" value must be a int type or None')
        if self.top_margin != GLXCurses.clamp_to_zero(value):
            self.__top_margin = GLXCurses.clamp_to_zero(value)

    @property
    def wrap_mode(self):
        return self.__wrap_mode

    @wrap_mode.setter
    def wrap_mode(self, value=None):
        if value is None:
            value = GLXCurses.GLXC.WRAP_NONE
        if type(value) != str:
            raise TypeError('"wrap_mode" value must be a str type or None')
        if value.upper() not in GLXCurses.GLXC.WrapMode:
            raise ValueError('"wrap_mode" value must be a valid GLXCurses.GLXC.WrapMode')
        if self.wrap_mode != value.upper():
            self.__wrap_mode = value.upper()
