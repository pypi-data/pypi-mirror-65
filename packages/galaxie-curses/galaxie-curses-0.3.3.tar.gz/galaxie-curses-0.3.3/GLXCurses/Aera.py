#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import curses


class Area(object):
    """
    Internal class it define a Area

    .. note:: it never have a clamp value or a float to int conversion, each set method have role to raise a error \
    if value type is not respect during a set.
    """

    def __init__(self, x=None, y=None, width=None, height=None, screen=None, subwin=None):
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__stdscr = screen
        self.__subwin = subwin

    @property
    def x(self):
        """
        ``x`` property

        It represent the x location, 0 for Left

        :return: ``x`` location in char, 0 correspond to left
        :rtype: int or None
        """
        return self.__x

    @x.setter
    def x(self, x=None):
        """
        ``x`` location of the area
        Set the :class:`Area <GLXCurses.Area.Area>` :py:obj:`x` property value.

        .. seealso:: :func:`Area.get_x() <GLXCurses.Area.Area.get_x()>`

        :param x: ``x`` location of the area in char, 0 correspond to left
        :type x: int or None
        :raise TypeError: if ``x`` parameter is not a :py:data:`int` type or None
        """
        # We exit as soon of possible
        if x is not None and type(x) != int:
            raise TypeError("'x' parameter is not int type or None")

        if self.x != x:
            self.__x = x

    @property
    def y(self):
        """
        ``y`` location of the area

        :return: ``y`` location in char, 0 correspond to top
        :rtype: int
        """
        return self.__y

    @y.setter
    def y(self, y=None):
        """
        ``y`` location of the area

        Note: it have no clamp value  or float to int conversion. The ``y`` must be a int.


        :param y: ``y`` location of the area in char, 0 correspond to top
        :type y: int or None
        :raise TypeError: if ``y`` parameter is not a :py:data:`int` type or None
        """
        if y is not None and type(y) != int:
            raise TypeError("'y' parameter is not int type")

        if self.y != y:
            self.__y = y

    @property
    def width(self):
        """
        Get :py:obj:`width` property value.

        :return: :py:obj:`width` property
        :rtype: int or None
        """
        return self.__width

    @width.setter
    def width(self, width=None):
        """
        Set :py:obj:`width` property value.

        :param width: :py:obj:`width` property value
        :type width: int or None
        :raise TypeError: if ``width`` parameter is not a :py:data:`int` type or None
        """
        # We exit as soon of possible
        if width is not None and not isinstance(width, int):
            raise TypeError("'width' argument must be a int type or None")

        if self.width != width:
            self.__width = width

    @property
    def height(self):
        """
        Get :py:obj:`height` property value.

        :return: :py:obj:`height` property
        :rtype: int or None
        """
        return self.__height

    @height.setter
    def height(self, height=None):
        """
        Set ``height`` property value.

        :param height: :py:obj:`height` property value
        :type height: int or None
        :raise TypeError: if ``height`` parameter is not a :py:data:`int` type or None
        """
        if height is not None and type(height) != int:
            raise TypeError("'height' argument must be a int type or None")

        if self.height != height:
            self.__height = height

    @property
    def stdscr(self):
        """
        Get the :py:obj:`stdscr` property value.

        :return: A Curses window object`
        :rtype: _curses.curses window or None
        """
        return self.__stdscr

    @stdscr.setter
    def stdscr(self, stdscr=None):
        """
        Set the :py:obj:`stdscr` property value.

        It correspond to curses stdscr initialized by the :class:`Application <GLXCurses.Application.Application>`

        :param stdscr: A Curses window curses type as return by curses.initrc() or curses.newwin()
        :type stdscr: _curses.curses window or None
        :raise TypeError: if ``stdscr`` is not a valid _curses.curses window type or None
        """

        if stdscr is not None and \
                str(type(stdscr)) != "<type '_curses.curses window'>" and \
                str(type(stdscr)) != "<class '_curses.window'>" and \
                str(type(stdscr)) != "<class 'unittest.mock.MagicMock'>":
            # print(str(type(stdscr)))
            raise TypeError(str(type(stdscr)))

        if self.stdscr != stdscr:
            self.__stdscr = stdscr

    @property
    def subwin(self):
        """
        Get the ``subwin`` property value.

        :return: A Curses window object`
        :rtype: _curses.curses window or None
        """
        return self.__subwin

    @subwin.setter
    def subwin(self, subwin=None):
        """
        Set the ``subwin`` property value.

        :param subwin: A Curses window curses type as return by curses.initrc() or curses.newwin()
        :type subwin: _curses.curses window or None
        :raise TypeError: if ``subwin`` is not a valid _curses.curses window type or None
        """
        if subwin is not None and \
                str(type(subwin)) != "<type '_curses.curses window'>" and \
                str(type(subwin)) != "<class '_curses.window'>":
            raise TypeError("'stdscr' must be a curses type as return by curses.initrc() or curses.newwin()")

        if self.subwin != subwin:
            self.__subwin = subwin

    def create_or_resize(self):
        # Look if we have to create a derwin or resize/move the existing one.
        if self.x is None:
            self.x = 0
        if self.y is None:
            self.y = 0
        if self.height is None:
            self.height = 0
        if self.width is None:
            self.width = 0
        if self.subwin is None:
            try:
                self.subwin = self.stdscr.derwin(
                    self.height,
                    self.width,
                    self.y,
                    self.x
                )
            except curses.error:  # pragma: no cover
                pass

        else:
            height, width = self.subwin.getmaxyx()
            y, x = self.subwin.getbegyx()
            if y != self.y or x != self.x or self.height != height or self.width != width:
                try:
                    self.subwin.mvderwin(self.y, self.x)
                except curses.error:  # pragma: no cover
                    pass

                try:
                    self.subwin.resize(self.height, self.width)
                except curses.error:  # pragma: no cover
                    pass
