#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import GLXCurses


# Ref Doc: https://developer.gnome.org/gobject/stable/gobject-The-Base-Object-Type.html#GObject-struct
class Object(GLXCurses.EventBusClient):
    """
    :Description:

    Object is the fundamental type providing the common attributes and methods for all object types in GLXCurses.

    The Object class provides methods for object construction and destruction, property access methods, and signal
    support.

    Signals are described in detail here.

    """

    def __init__(self):
        # property
        self.__id = None
        self.__debug = None
        self.__debug_level = None
        self.__flags = None
        self.__children = None

        # Load heritage
        GLXCurses.EventBusClient.__init__(self)

        # It's a GLXCurse Type
        self.glxc_type = 'GLXCurses.Object'

        self.id = GLXCurses.new_id()
        self.debug = False
        self.debug_level = 0
        self.flags = self.default_flags

        # Signal
        # self.signal_handlers = dict()
        # self.blocked_handler = list()
        # self.blocked_function = list()
        # self.__area_data = dict()
        self.children = None
        # init

    @property
    def id(self):
        """
        Return the ``id`` property value

        :return: a unique id
        :rtype: str
        """
        return self.__id

    @id.setter
    def id(self, value=None):
        """
        Set the ``id`` property value

        Every Object generate a id via Utility.new_id()

        Note: None restore default value

        Default Value: Generate a unique id via Utility.

        :param value: a id it should be unique
        :type value: str
        :raise TypeError: If value is not a str type or None
        """
        if value is None:
            value = GLXCurses.new_id()
        if type(value) != str:
            raise TypeError('"id" must be a str type')
        if self.id != value:
            self.__id = value

    @property
    def children(self):
        return self.__children

    @children.setter
    def children(self, children=None):
        if children is None:
            children = []
        if type(children) != list:
            raise TypeError('"children" must be a list type or None')
        if self.children != children:
            self.__children = children

    @property
    def debug(self):
        return self.__debug

    @debug.setter
    def debug(self, debug=None):
        """
        Set the debugging level of information'ss display on the stdscr.

        Generally it highly stress the console and is here for future maintenance of that Application.

        Enjoy future dev it found it function ;)

        :param debug: True is debugging mode is enable, False for disable it.
        :type debug: bool
        :raise TypeError: when "debug" argument is not a :py:__area_data:`bool`
        """
        if debug is None:
            debug = False
        if type(debug) != bool:
            raise TypeError('"debug" must be a boolean type')
        if self.debug != debug:
            self.__debug = debug

    @property
    def debug_level(self):
        """
        Get the debugging information's level to display on the stdscr.

        Range: 0 to 3

        :return: The ``debug_level`` property value
        :rtype: int
        """
        return self.__debug_level

    @debug_level.setter
    def debug_level(self, debug_level=None):
        """
        Set the debugging level of information's to display on the stdscr.

        Generally it highly stress the console and is here for future maintenance of that Application.

        Enjoy future dev it found it function ;)

        :param debug_level: The Debug level to set
        :type debug_level: int
        :raise TypeError: when "debug_level" argument is not a :py:__area_data:`int`
        :raise ValueError: when "debug_level" is not in range 0 to 3
        """
        if debug_level is None:
            debug_level = 0
        if type(debug_level) != int:
            raise TypeError('"debug_level" must be a int type')
        if debug_level not in [0, 1, 2, 3]:
            raise ValueError('"debug_level" must be in range 0 top 3')
        if self.debug_level != debug_level:
            self.__debug_level = debug_level

    @property
    def flags(self):
        """
        Return the ``flags`` attribute, it consist to a dictionary it store keys with have special name.

        :return: a Dictionary with Galaxie Curses Object Flags format
        :rtype: dict
        """
        return self.__flags

    @flags.setter
    def flags(self, flags=None):
        """
        Set the ``flags`` property value.

        Note: None restore default value
        Default Value: ``default_flags`` property

        :param flags: a dictionary with a structure like return by ``default_flags`` property
        :type flags: dict
        :raise TypeError: When flags is not a dictionary
        """
        if flags is not None and type(flags) != dict:
            raise TypeError('"flags" must be a dict type or None')
        if flags is None:
            flags = self.default_flags
        for key, value in list(flags.items()):
            if key not in [
                'IN_DESTRUCTION',
                'FLOATING',
                'TOPLEVEL',
                'NO_WINDOW',
                'REALIZED',
                'MAPPED',
                'VISIBLE',
                'SENSITIVE',
                'PARENT_SENSITIVE',
                'CAN_FOCUS',
                'HAS_FOCUS',
                'CAN_DEFAULT',
                'HAS_DEFAULT',
                'HAS_GRAB',
                'RC_STYLE',
                'COMPOSITE_CHILD',
                'NO_REPARENT',
                'APP_PAINTABLE',
                'RECEIVES_DEFAULT',
                'DOUBLE_BUFFERED',
                'FOCUS_ON_CLICK'
            ]:
                raise ValueError('"flags" is incorrect see default_flags property')
        if self.flags != flags:
            self.__flags = flags

    @property
    def default_flags(self):
        flags = dict()

        # The object is currently being destroyed.
        flags['IN_DESTRUCTION'] = False

        # The object is orphaned.
        flags['FLOATING'] = True

        # Widget flags
        # widgets without a real parent (e.g. Window and Menu) have this flag set throughout their lifetime.
        flags['TOPLEVEL'] = False

        # A widget that does not provide its own Window.
        # Visible action (e.g. drawing) is performed on the parent's Window.
        flags['NO_WINDOW'] = True

        # The widget has an associated Window.
        flags['REALIZED'] = False

        # The widget can be displayed on the stdscr.
        flags['MAPPED'] = False

        # The widget will be mapped as soon as its parent is mapped.
        flags['VISIBLE'] = False

        # The sensitivity of a widget determines whether it will receive certain events (e.g. button or key presses).
        # One requirement for the widget's sensitivity is to have this flag set.
        flags['SENSITIVE'] = True

        # This is the second requirement for the widget's sensitivity.
        # Once a widget has SENSITIVE and PARENT_SENSITIVE set, its state is effectively sensitive.
        flags['PARENT_SENSITIVE'] = True

        # The widget is able to handle focus grabs.
        flags['CAN_FOCUS'] = False

        # The widget has the focus - assumes that CAN_FOCUS is set
        flags['HAS_FOCUS'] = False

        # The widget is allowed to receive the default action.
        flags['CAN_DEFAULT'] = False

        # The widget currently will receive the default action.
        flags['HAS_DEFAULT'] = False

        # The widget is in the grab_widgets stack, and will be the preferred one for receiving events.
        flags['HAS_GRAB'] = False

        # The widgets style has been looked up through the RC mechanism.
        # It does not imply that the widget actually had a style defined through the RC mechanism.
        flags['RC_STYLE'] = 'Default.yml'

        # The widget is a composite child of its parent.
        flags['COMPOSITE_CHILD'] = False

        # unused
        flags['NO_REPARENT'] = 'unused'

        # Set on widgets whose window the application directly draws on,
        # in order to keep GLXCurse from overwriting the drawn stuff.
        flags['APP_PAINTABLE'] = False

        # The widget when focused will receive the default action and have HAS_DEFAULT set
        # even if there is a different widget set as default.
        flags['RECEIVES_DEFAULT'] = False

        # Exposes done on the widget should be double-buffered.
        flags['DOUBLE_BUFFERED'] = False

        # TRUE if the widget should grab focus when it is clicked with the mouse
        flags['FOCUS_ON_CLICK'] = True

        return flags

    def destroy(self):
        """
        Destroy the object
        """
        self.flags['IN_DESTRUCTION'] = True
