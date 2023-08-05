#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import GLXCurses


class Misc(GLXCurses.Widget):
    """
    The Misc widget is an abstract widget which is not useful itself, but is used to derive subclasses which have
    alignment and padding attributes.

    The horizontal and vertical padding attributes allows extra space to be added around the widget.

    The horizontal and vertical alignment attributes enable the widget to be positioned within its allocated area.
    Note that if the widget is added to a container in such a way that it expands automatically to fill its allocated
    area, the alignment settings will not alter the widget's position.

    Note that the desired effect can in most cases be achieved by using the “halign”, “valign” and “margin”
    properties on the child widget

    .. warning:: To reflect this fact, all Misc API will be deprecated soon.
    """

    def __init__(self):
        """
        .. py:attribute:: xalign - The horizontal alignment, from 0.0 to 1.0
        .. py:attribute:: yalign - The vertical alignment, from 0.0 to 1.0
        .. py:attribute:: xpad   - The amount of space to add on the left and right of the widget, in characters
        .. py:attribute:: ypad   - The amount of space to add above and below the widget, in characters
        """
        # Load heritage
        GLXCurses.Widget.__init__(self)

        # It's a GLXCurse Type
        self.glxc_type = 'GLXCurses.Misc'
        self.name = '{0}{1}'.format(self.__class__.__name__, self.id)

        self.__xalign = None
        self.__yalign = None
        self.__xpad = None
        self.__ypad = None

        self.xalign = 0.5
        self.yalign = 0.5
        self.xpad = 0
        self.ypad = 0

    @property
    def xalign(self):
        return self.__xalign

    @xalign.setter
    def xalign(self, xalign=None):
        """
        The horizontal alignment. A value of 0.0 means left alignment (or right on RTL locales); a value of 1.0
        means right alignment (or left on RTL locales).

        Flags: Read / Write
        Allowed values: [0,1]
        Default value: 0.5

        :param xalign: The horizontal alignment
        :type xalign: float
        """
        if xalign is None:
            xalign = 0.5
        if type(xalign) != float:
            raise TypeError('"xalign" must be a float type or None')
        if not 0.0 <= xalign <= 1.0:
            raise ValueError('"xalign" have allowed value min: 0.0 max: 1.0')
        if self.xalign != xalign:
            self.__xalign = xalign

    @property
    def yalign(self):
        return self.__yalign

    @yalign.setter
    def yalign(self, yalign=None):
        """
        The horizontal alignment. A value of 0.0 means left alignment (or right on RTL locales); a value of 1.0
        means right alignment (or left on RTL locales).

        Flags: Read / Write
        Allowed values: [0,1]
        Default value: 0.5

        :param yalign: The horizontal alignment
        :type yalign: float
        """
        if yalign is None:
            yalign = 0.5
        if type(yalign) != float:
            raise TypeError('"yalign" must be a float type or None')
        if not 0.0 <= yalign <= 1.0:
            raise ValueError('"yalign" have allowed value min: 0.0 max: 1.0')
        if self.yalign != yalign:
            self.__yalign = yalign

    @property
    def xpad(self):
        """
        The amount of space to add on the left and right of the widget, in chars.

        :return: The amount of space in chars
        :raise: int
        """
        return self.__xpad

    @xpad.setter
    def xpad(self, xpad=None):
        """

        :param xpad:
        :return:
        """
        if xpad is None:
            xpad = 0
        if type(xpad) != int:
            raise TypeError('"xpad" must be a int type or None')
        if xpad < 0:
            raise ValueError('"xpad" allowed values >=0')
        if self.xpad != xpad:
            self.__xpad = xpad

    @property
    def ypad(self):
        """

        :return: The amount of space in chars
        :raise: int
        """
        return self.__ypad

    @ypad.setter
    def ypad(self, ypad=None):
        """

        :param ypad:
        :return:
        """
        if ypad is None:
            ypad = 0
        if type(ypad) != int:
            raise TypeError('"ypad" must be a int type or None')
        if ypad < 0:
            raise ValueError('"ypad" allowed values >=0')
        if self.ypad != ypad:
            self.__ypad = ypad
