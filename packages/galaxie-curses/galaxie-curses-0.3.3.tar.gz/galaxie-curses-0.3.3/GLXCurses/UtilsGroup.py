#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import GLXCurses


class Group(object):
    def __init__(self):
        self.__members = None
        self.__position = None

        self.members = list()
        self.position = 0

    @property
    def members(self):
        return self.__members

    @members.setter
    def members(self, value=None):
        if value is None:
            value = list()
        if type(value) != list:
            raise TypeError('"members value must be a list type or None"')
        if self.members != value:
            self.__members = value

    @property
    def position(self):
        """
        Extra space to put between the child and its neighbors, in chars.

        Flags: Read / Write

        Allowed values: <= G_MAXINT

        Default value: 0

        :return: Extra space to put between the child and its neighbors, in chars.
        :rtype: int
        """
        return self.__position

    @position.setter
    def position(self, position=None):
        if position is None:
            position = 0
        if type(position) != int:
            raise TypeError('"position" must be a int type or None')
        if self.position != position:
            self.__position = position

    @property
    def widget(self):
        if len(self.members) > 0 and isinstance(self.members[self.position], GLXCurses.GroupElement):
            return self.members[self.position].widget
        return None

    def is_member(self, widget=None):
        if widget is None:
            return False
        if not isinstance(widget, GLXCurses.Widget):
            raise TypeError("'widget' must be an instance of GLXCurses.Widget")
        for member in self.members:
            if member.widget is not None and member.widget.id == widget.id:
                return True
        return False

    def add(self, widget=None):
        """
        Adds widget to the group .

        Typically used for group widget's , by example RadioButton, MenuElement, GlobalFocus

        For more complicated layout containers such as Box or Grid, this function will pick default packing
        parameters that may not be correct.

        :param widget: a widget to be placed inside container
        :type widget: Widget
        :raise TypeError: if ``widget`` is not a instance of Widget
        """
        # Try to exit as soon of possible
        if not isinstance(widget, GLXCurses.Widget):
            raise TypeError("'widget' must be an instance of GLXCurses.Widget")

        if not self.is_member(widget=widget):
            group_element = GLXCurses.GroupElement()
            group_element.widget = widget
            self.members.append(group_element)

    def remove(self, widget=None):
        if not isinstance(widget, GLXCurses.Widget):
            raise TypeError("'widget' must be an instance of GLXCurses.Widget")
        if self.is_member(widget):
            for member in self.members:
                if widget == member.widget:
                    self.members.remove(member)

    def up(self):
        if self.position + 1 > len(self.members) - 1:
            self.position = 0
        else:
            self.position += 1

    def down(self):
        if self.position - 1 < 0:
            self.position = len(self.members) - 1
        else:
            self.position -= 1
