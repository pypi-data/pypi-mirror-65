#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import GLXCurses


class Groups(object):
    def __init__(self):
        self.__groups = None
        self.__position = None

        self.groups = list()
        self.position = 0

    @property
    def groups(self):
        return self.__groups

    @groups.setter
    def groups(self, value=None):
        if value is None:
            value = list()
        if type(value) != list:
            raise TypeError('"groups value must be a list type or None"')
        if self.groups != value:
            self.__groups = value

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
    def group(self):
        if len(self.groups) > 0 and isinstance(self.groups[self.position], GLXCurses.Group):
            return self.groups[self.position]
        return None

    def is_group(self, group=None):
        if group is None:
            return False
        if not isinstance(group, GLXCurses.Group):
            raise TypeError("'group' must be an instance of GLXCurses.Group or None")
        if group in self.groups:
            return True
        return False

    def add_group(self, group=None):
        """
        Adds group to the Application groups list .

        Typically used to permit Application to manage Widgets Groups

        For more complicated layout containers such as Box or Grid, this function will pick default packing
        parameters that may not be correct.

        :param group: a widget to be placed inside container
        :type group: Group
        :raise TypeError: if ``group`` is not a instance of Group
        """
        if not isinstance(group, GLXCurses.Group):
            raise TypeError("'group' must be an instance of GLXCurses.Group")
        if not self.is_group(group):
            self.groups.append(group)

    def remove_group(self, group=None):
        if not isinstance(group, GLXCurses.Group):
            raise TypeError("'group' must be an instance of GLXCurses.Group")
        if self.is_group(group):
            self.groups.remove(group)

    def up(self):
        if self.position + 1 > len(self.groups) - 1:
            self.position = 0
        else:
            self.position += 1

    def down(self):
        if self.position - 1 < 0:
            self.position = len(self.groups) - 1
        else:
            self.position -= 1
