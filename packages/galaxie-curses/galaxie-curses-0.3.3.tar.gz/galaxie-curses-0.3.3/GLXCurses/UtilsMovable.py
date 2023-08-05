#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import GLXCurses


class Movable(object):
    def __init__(self):
        self.__y_offset = None
        self.__x_offset = None
        self.__justify = None
        self.__position_type = None

        self.y_offset = 0
        self.x_offset = 0
        self.justify = GLXCurses.GLXC.JUSTIFY_CENTER
        self.position_type = GLXCurses.GLXC.POS_CENTER

        self.preferred_width = 0
        self.preferred_height = 0
        self.width = 0
        self.height = 0

    @property
    def x_offset(self):
        """"
        ``x_offset`` for add offset value to ``x`` position of a GLXCurses.Area attach to a GLXCurses.Widget.
        """
        return self.__x_offset

    @x_offset.setter
    def x_offset(self, offset=None):
        """
        Set the ``x_offset`` property value.

        :param offset: the new value of ``x_offset`` property in chars
        :type offset: int or None
        """
        if offset is None:
            offset = 0
        if type(offset) != int:
            raise TypeError('"offset" must be int type or None')
        if self.x_offset != offset:
            self.__x_offset = offset

    @property
    def y_offset(self):
        """"
        ``y_offset`` for add offset value to ``y`` position of a GLXCurses.Area attach to a GLXCurses.Widget.
        """
        return self.__y_offset

    @y_offset.setter
    def y_offset(self, offset=None):
        """
        Set the ``y_offset`` property value.

        :param offset: the new value of ``y_offset`` property in chars
        :type offset: int or None
        """
        if offset is None:
            offset = 0
        if type(offset) != int:
            raise TypeError('"offset" must be int type or None')
        if self.y_offset != offset:
            self.__y_offset = offset

    @property
    def justify(self):
        """
        Return the Justify of the Button

         Justify:
          - LEFT
          - CENTER
          - RIGHT

        :return: str
        """
        return self.__justify

    @justify.setter
    def justify(self, value=None):
        """
        Set the Justify of the Vertical separator

         Justify:
          - LEFT
          - CENTER
          - RIGHT

        :param value: a Justify
        :type value: str
        """
        if value is None:
            value = GLXCurses.GLXC.JUSTIFY_CENTER
        if type(value) != str:
            raise TypeError('"justify" value must be a str type or None')
        if value not in GLXCurses.GLXC.Justification:
            raise ValueError('PositionType must be LEFT or CENTER or RIGHT')
        if self.justify != str(value).upper():
            self.__justify = str(value).upper()

    @property
    def position_type(self):
        """
        Return the Position Type

         **GLXCurses.GLXC.PositionType**
          *GLXCurses.GLXC.POS_TOP
          *GLXCurses.GLXC.POS_CENTER
          *GLXCurses.GLXC.POS_BOTTOM

        :return: the position_type property value
        :rtype: str
        """
        return self.__position_type

    @position_type.setter
    def position_type(self, value=None):
        """
        Set the Position type

         **GLXCurses.GLXC.PositionType**
          *GLXCurses.GLXC.POS_TOP
          *GLXCurses.GLXC.POS_CENTER
          *GLXCurses.GLXC.POS_BOTTOM

        :param value: a PositionType
        :type value: str
        """
        if value is None:
            value = GLXCurses.GLXC.POS_CENTER
        if type(value) != str:
            raise TypeError('"position_type" value must be a str type or None')
        if value not in GLXCurses.GLXC.PositionType:
            raise ValueError(
                'PositionType must be a value contain in GLXCurses.GLXC.PositionType , like CENTER or TOP or BOTTOM'
            )

        if self.position_type != value.upper():
            self.__position_type = value.upper()

    def check_justification(self):
        if self.justify == GLXCurses.GLXC.JUSTIFY_CENTER:
            self.x_offset = GLXCurses.clamp_to_zero(
                GLXCurses.round_down(self.width / 2, decimals=0) - GLXCurses.round_down(self.preferred_width / 2,
                                                                                    decimals=0)
            )
        elif self.justify == GLXCurses.GLXC.JUSTIFY_LEFT:
            self.x_offset = 0
        elif self.justify == GLXCurses.GLXC.JUSTIFY_RIGHT:
            self.x_offset = GLXCurses.clamp_to_zero(self.width - self.preferred_width)

    def check_position(self):
        if self.position_type == GLXCurses.GLXC.POS_CENTER:
            self.y_offset = GLXCurses.clamp_to_zero(
                GLXCurses.round_down(self.height / 2, decimals=0) - GLXCurses.round_down(self.preferred_height / 2,
                                                                                     decimals=0)
            )

        elif self.position_type == GLXCurses.GLXC.POS_TOP:
            self.y_offset = 0

        elif self.position_type == GLXCurses.GLXC.POS_BOTTOM:
            self.y_offset = GLXCurses.clamp_to_zero(self.height - self.preferred_height)
