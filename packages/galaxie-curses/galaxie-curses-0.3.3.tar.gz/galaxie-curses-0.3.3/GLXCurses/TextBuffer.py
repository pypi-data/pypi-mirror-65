#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import GLXCurses
import logging
import curses


class TextBuffer(GLXCurses.Object):
    def __init__(self):
        GLXCurses.Object.__init__(self)
        # self.__copy_target_list = None
        self.__cursor_position = None
        self.__has_selection = None
        self.__paste_target_list = None
        self.__tag_table = None
        self.__text = None

        self.cursor_position = 0
        self.has_selection = False
        self.text = None

    @property
    def cursor_position(self):
        """
        The position of the insert mark (as offset from the beginning of the buffer).
        It is useful for getting notified when the cursor moves.

        :return: The cursor position
        :rtype: int
        """
        return self.__cursor_position

    @cursor_position.setter
    def cursor_position(self, value=0):
        """
        Set the ``cursor_position`` property value

        Default value is ``0``, and be restored when ``cursor_position`` is set to ``None``

        :param value: The value set here is padding
        :type value: int or None
        :raise TypeError: When value is not int type or None
        """
        if value is None:
            value = 0
        if type(value) != int:
            raise TypeError('"cursor_position" value must be a int type or None')
        if self.cursor_position != GLXCurses.clamp_to_zero(value):
            self.__cursor_position = GLXCurses.clamp_to_zero(value)

    @property
    def has_selection(self):
        """
        Whether the buffer has some text currently selected.

        :return: True when buffer have selection
        :rtype: bool
        """
        return self.__has_selection

    @has_selection.setter
    def has_selection(self, value=None):
        """
        Set the has_selection property value

        :param value: True when buffer have selection
        :type value: bool or None
        """
        if value is None:
            value = False
        if type(value) != bool:
            raise TypeError('"hast_selction" value must be a bool type of None')
        if self.has_selection != value:
            self.__has_selection = value


    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value=None):
        if value is not None and type(value) != str:
            raise TypeError('"text" value must be a str type or None')
        if self.__text != value:
            self.__text = value
