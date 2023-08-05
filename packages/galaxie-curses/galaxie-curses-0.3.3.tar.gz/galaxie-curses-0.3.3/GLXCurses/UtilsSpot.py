#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import GLXCurses


class Spot(GLXCurses.Groups):
    def __init__(self):
        GLXCurses.Groups.__init__(self)
        self.widget_it_have_tooltip = {
            'widget': None,
            'type': None,
            'id': None
        }

        self.__has_default = None
        self.__has_focus = None
        self.__has_prelight = None
        self.__active_window_id = None
        self.__active_window_id_prev = None

    @property
    def active_window_id(self):
        return self.__active_window_id

    @active_window_id.setter
    def active_window_id(self, window_id=None):
        if window_id is not None and type(window_id) != str:
            raise TypeError('"window_id" must be a str or None')
        if self.active_window_id != window_id:
            self.__active_window_id_prev = self.active_window_id
            self.__active_window_id = window_id

    @property
    def active_window_id_prev(self):
        return self.__active_window_id_prev

    @active_window_id_prev.setter
    def active_window_id_prev(self, window_id=None):
        if window_id is not None and type(window_id) != str:
            raise TypeError('"window_id" must be a str or None')
        if self.active_window_id_prev != window_id:
            self.__active_window_id_prev = window_id

    @property
    def has_default(self):
        return self.__has_default

    @has_default.setter
    def has_default(self, widget=None):
        if widget is not None and not isinstance(widget, GLXCurses.Widget):
            raise TypeError('"widget" must be GLXCurses.Widget or None')

        if widget is None:
            if self.has_default is not None:
                self.__has_default = None
            return

        self.__has_default = GLXCurses.ChildElement(
            widget=widget,
            widget_name=widget.name,
            widget_id=widget.id
        )

    @property
    def has_focus(self):
        return self.__has_focus

    @has_focus.setter
    def has_focus(self, widget=None):
        if widget is not None and not isinstance(widget, GLXCurses.Widget):
            raise TypeError('"widget" must be GLXCurses.Widget or None')

        if widget is None:
            if self.has_focus is not None:
                self.__has_focus = None
            return

        self.__has_focus = GLXCurses.ChildElement(
            widget=widget,
            widget_name=widget.name,
            widget_id=widget.id
        )

    @property
    def has_prelight(self):
        return self.__has_prelight

    @has_prelight.setter
    def has_prelight(self, widget=None):
        if widget is not None and not isinstance(widget, GLXCurses.Widget):
            raise TypeError('"widget" must be GLXCurses.Widget or None')

        if widget is None:
            if self.has_prelight is not None:
                self.__has_prelight = None
                return

        self.__has_prelight = GLXCurses.ChildElement(
            widget=widget,
            widget_name=widget.name,
            widget_id=widget.id
        )

    def get_tooltip(self):
        """
        Return the unique id of the widget it have been set by \
        :func:`Application.set_tooltip() <GLXCurses.Application.Application.set_tooltip()>`

        .. seealso:: \
         :func:`Application.set_tooltip() <GLXCurses.Application.Application.set_tooltip()>`

         :func:`Widget.id <GLXCurses.Widget.Widget.id>`

        :return: a unique id generate by uuid module
        :rtype: long or None
        """
        return self.widget_it_have_tooltip

    def set_tooltip(self, widget=None):
        """
        Determines if the widget have to display a tooltip

        "Not implemented yet"

        .. seealso:: \
        :func:`Application.get_tooltip() <GLXCurses.Application.Application.get_tooltip()>`

        :param widget: a Widget
        :type widget: GLXCurses.Widget or None
        """
        if isinstance(widget, GLXCurses.Widget):
            info = {
                'widget': widget,
                'type': widget.glxc_type,
                'id': widget.id
            }
            if self.widget_it_have_tooltip != info:
                self.widget_it_have_tooltip = info
        else:
            info = {
                'widget': None,
                'type': None,
                'id': None
            }
            if self.widget_it_have_tooltip != info:
                self.widget_it_have_tooltip = info

