#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved
import GLXCurses


class ChildProperty(object):
    def __init__(self):
        self.__expand = None
        self.__fill = None
        self.__pack_type = None
        self.__padding = None
        self.__position = None

        self.expand = False
        self.fill = True
        self.pack_type = GLXCurses.GLXC.PACK_START
        self.padding = 0
        self.position = 0

    @property
    def expand(self):
        """
        Whether the child should receive extra space when the parent grows.

        Note that the default value for this property is False for Box, but HBox, VBox and other subclasses
        use the old default of True.

        Note: The “hexpand” or “vexpand” properties are the preferred way to influence whether the child receives
        extra space, by setting the child’s expand property corresponding to the box’s orientation.

        In contrast to “hexpand”, the expand child property does not cause the box to expand itself.

        Flags: Read / Write
        Default value: False

        :return:
        """
        return self.__expand

    @expand.setter
    def expand(self, expand=None):
        if expand is None:
            expand = False
        if type(expand) != bool:
            raise TypeError('"expand" must be a boot type or None')
        if self.expand != expand:
            self.__expand = expand

    @property
    def fill(self):
        """
        Whether the child should fill extra space or use it as padding.

        Note: The “halign” or “valign” properties are the preferred way to influence whether the child fills available
        space, by setting the child’s align property corresponding to the box’s orientation to GLXC.ALIGN_FILL to fill,
        or to something else to refrain from filling.

        Flags: Read / Write

        Default value: ``True``

        :return: If ``True`` the child fill extra space or use it as padding
        :rtype: bool
        """
        return self.__fill

    @fill.setter
    def fill(self, fill=None):
        if fill is None:
            fill = True
        if type(fill) != bool:
            raise TypeError('"fill" must be a boot type or None')
        if self.fill != fill:
            self.__fill = fill

    @property
    def pack_type(self):
        """
        Whether the child should fill extra space or use it as padding.

        Note: The “halign” or “valign” properties are the preferred way to influence whether the child fills available
        space, by setting the child’s align property corresponding to the box’s orientation to GLXC.ALIGN_FILL to fill,
        or to something else to refrain from filling.

        Flags: Read / Write

        Default value: ``True``

        :return: If ``True`` the child fill extra space or use it as padding
        :rtype: bool
        """
        return self.__pack_type

    @pack_type.setter
    def pack_type(self, pack_type=None):
        if pack_type is None:
            pack_type = GLXCurses.GLXC.PACK_START
        if type(pack_type) != str:
            raise TypeError('"pack_type" must be a str type or None')
        if pack_type not in GLXCurses.GLXC.PackType:
            raise ValueError('"pack_type" must be in GLXC.PackType list')
        if self.pack_type != pack_type:
            self.__pack_type = pack_type

    @property
    def padding(self):
        """
        Extra space to put between the child and its neighbors, in chars.

        Flags: Read / Write

        Allowed values: <= G_MAXINT

        Default value: 0

        :return: Extra space to put between the child and its neighbors, in chars.
        :rtype: int
        """
        return self.__padding

    @padding.setter
    def padding(self, padding=None):
        if padding is None:
            padding = 0
        if type(padding) != int:
            raise TypeError('"padding" must be a int type or None')
        if self.padding != padding:
            self.__padding = padding

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
