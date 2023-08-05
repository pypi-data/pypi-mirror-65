#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import GLXCurses


# Inspired from: https://developer.gnome.org/gtk3/stable/GtkTextTag.html
# Inspired from: https://developer.gnome.org/pygtk/stable/class-gtktexttag.html

class TextTag(GLXCurses.Object):
    def __init__(self):
        """
        You may wish to begin by reading the text widget conceptual overview which gives an overview of all the
        objects and data types related to the text widget and how they work together.

        Tags should be in the TextTagTable for a given TextBuffer before using them with that buffer.

        For each property of TextTag, there is a “set” property, e.g. “font-set” corresponds to “font”.
        These “set” properties reflect whether a property has been set or not.

        They are maintained by GLXCurses and you should not set them independently.
        """
        GLXCurses.Object.__init__(self)
        self.__accumulative_margin = None
        self.__background = None
        self.__background_full_height = None
        self.__background_full_height_set = None
        self.__background_rgb = None
        self.__background_set = None
        self.__direction = None
        self.__editable = None
        self.__editable_set = None
        self.__fallback = None
        self.__fallback_set = None
        self.__family = None
        self.__family_set = None
        self.__font = None
        self.__font_desc = None
        self.__font_features = None
        self.__font_features_set = None
        self.__foreground = None
        self.__foreground_rgb = None
        self.__foreground_set = None
        self.__indent = None
        self.__indent_set = None
        self.__invisible = None
        self.__invisible_set = None
        self.__justification = None
        self.__justification_set = None
        self.__language = None
        self.__language_set = None
        self.__left_margin = None
        self.__left_margin_set = None
        self.__letter_spacing = None
        self.__letter_spacing_set = None
        self.__name = None
        self.__paragraph_background = None
        self.__paragraph_background_rgb = None
        self.__paragraph_background_set = None
        self.__chars_above_lines = None
        self.__chars_above_lines_set = None
        self.__chars_below_lines = None
        self.__chars_below_lines_set = None
        self.__chars_inside_wrap = None
        self.__chars_inside_wrap_set = None
        self.__right_margin = None
        self.__right_margin_set = None
        self.__rise = None
        self.__rise_set = None
        self.__scale = None
        self.__scale_set = None
        self.__size = None
        self.__size_points = None
        self.__size_set = None
        self.__stretch = None
        self.__stretch_set = None
        self.__strikethrough = None
        self.__strikethrough_rgb = None
        self.__strikethrough_rgb_set = None
        self.__strikethrough_set = None
        self.__style = None
        self.__style_set = None
        self.__tabs = None
        self.__tabs_set = None
        self.__underline = None
        self.__underline_rgb = None
        self.__underline_rgb_set = None
        self.__underline_set = None
        self.__variant = None
        self.__variant_set = None
        self.__weight = None
        self.__weight_set = None
        self.__wrap_mode = None
        self.__wrap_mode_set = None

        self.accumulative_margin = False
        self.background = 'BLUE'
        self.background_full_height = False

    @property
    def accumulative_margin(self):
        """
        Whether the margins accumulate or override each other.

        When set to ``True`` the margins of this tag are added to the margins of any other non-accumulative
        margins present.

        When set to ``False`` the margins override one another (the default).

        Default value is ``False`` and be restore when ``accumulative_margin`` is set to ``None``

        :return: If ``True`` the margins of this tag are added to the margins of any other non-accumulative
        :rtype: bool
        """
        return self.__accumulative_margin

    @accumulative_margin.setter
    def accumulative_margin(self, value=None):
        """
        Set the ``accumulative_margin`` property value

        :param value: If ``True`` the margins of this tag are added to the margins of any other non-accumulative
        :type value: boot or None
        :raise TypeError: When  ``accumulative_margin`` value is not a bool type or None
        """
        if value is None:
            value = False
        if type(value) != bool:
            raise TypeError('"value" must be a bool type or None')
        if self.accumulative_margin != value:
            self.__accumulative_margin = value

    @property
    def background(self):
        """
        Background color as a string.

        :return: color as a string
        :rtype: str
        """
        return self.__background

    @background.setter
    def background(self, value=None):
        """
        Set the ``background`` property value

        :param value: color as a string
        :type value: boot or None
        :raise TypeError: If ``background`` value is not a str type or None
        """
        if value is None:
            value = 'BLUE'
        if type(value) != str:
            raise TypeError('"value" must be a str type or None')
        if self.background != value:
            self.__background = value

    @property
    def background_full_height(self):
        """
        Whether the background color fills the entire line height or only the height of the tagged characters.

        When set to ``True`` the background color fills the entire line height

        Default value is ``False`` and be restore when ``background_full_height`` is set to ``None``

        :return: If ``True`` the background color fills the entire line height
        :rtype: bool
        """
        return self.__background_full_height

    @background_full_height.setter
    def background_full_height(self, value=None):
        """
        Set the ``background_full_height`` property value

        :param value: If ``True`` the background color fills the entire line height
        :type value: boot or None
        :raise TypeError: When  ``background_full_height`` value is not a bool type or None
        """
        if value is None:
            value = False
        if type(value) != bool:
            raise TypeError('"value" must be a bool type or None')
        if self.background_full_height != value:
            self.__background_full_height = value

    @property
    def background_full_height_set(self):
        """
        Whether this tag affects background height.

        When set to ``True`` this tag affects background height

        Default value is ``False`` and be restore when ``background_full_height_set`` is set to ``None``

        :return: ``True`` If this tag affects background height
        :rtype: bool
        """
        return self.__background_full_height_set

    @background_full_height_set.setter
    def background_full_height_set(self, value=None):
        """
        Set the ``background_full_height_set`` property value

        :param value: If ``True``  this tag affects background height
        :type value: boot or None
        :raise TypeError: When  ``background_full_height_set`` value is not a bool type or None
        """
        if value is None:
            value = False
        if type(value) != bool:
            raise TypeError('"background_full_height_set" value must be a bool type or None')
        if self.background_full_height_set != value:
            self.__background_full_height_set = value
