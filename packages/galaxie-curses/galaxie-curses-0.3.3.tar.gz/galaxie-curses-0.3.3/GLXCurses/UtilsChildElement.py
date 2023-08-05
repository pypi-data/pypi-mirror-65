#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved
import GLXCurses


class ChildElement(object):
    def __init__(self, widget=None, widget_name=None, widget_type=None, widget_id=None, widget_properties=None):
        self.__widget = None
        self.__name = None
        self.__type = None
        self.__id = None
        self.__properties = None

        self.widget = widget
        self.name = widget_name
        self.type = widget_type
        self.id = widget_id
        if isinstance(widget_properties, GLXCurses.ChildProperty):
            self.properties = widget_properties
        else:
            self.properties = GLXCurses.ChildProperty()

    @property
    def widget(self):
        return self.__widget

    @widget.setter
    def widget(self, widget):
        if widget is not None and not isinstance(widget, GLXCurses.Widget) and \
                not isinstance(widget, GLXCurses.Adjustment):
            raise TypeError('"widget" must be a GLXCurses.Widget of None')
        if self.widget != widget:
            self.__widget = widget

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if name is not None and type(name) != str:
            raise TypeError('"name" must be a str type of None')
        if self.name != name:
            self.__name = name

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, glxctype):
        if glxctype is not None and type(glxctype) != str:
            raise TypeError('"glxctype" must be a str type of None')
        if glxctype is not None and str(glxctype).split('.')[0] != 'GLXCurses':
            raise ValueError('"glxctype" must GLXCurses type')

        if self.type != glxctype:
            self.__type = glxctype

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, glxcid):
        if glxcid is not None and type(glxcid) != str:
            raise TypeError('"id" must be a str type of None')
        if self.id != glxcid:
            self.__id = glxcid

    @property
    def properties(self):
        return self.__properties

    @properties.setter
    def properties(self, properties):
        if properties is not None and not isinstance(properties, GLXCurses.ChildProperty):
            raise TypeError('"properties" must be a GLXCurses.ChildProperty of None')
        if self.properties != properties:
            self.__properties = properties
