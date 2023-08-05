#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import GLXCurses


class EventBusClient(object):
    """
    :Description:

    The ``EventBusClient`` object is The bus it interconnect Widget
    """

    def __init__(self):
        # Public attribute
        self.events_list = {}

    def emit(self, detailed_signal, data):
        """
        Every Object emit signal in direction to the Application.

        :param detailed_signal: a string containing the signal name
        :type detailed_signal: str
        :param data: additional parameters arg1, arg2
        :type data: dict
        """
        # If args is still None replace it by a empty list
        # if data is None:
        #     data = {}

        # Emit inside the Mainloop
        GLXCurses.Application().emit(detailed_signal, data)

    def connect(self, detailed_signal, handler, *args):
        """
        The connect() method adds a function or method (handler) to the end of the event list
        for the named detailed_signal but before the default class signal handler.
        An optional set of parameters may be specified after the handler parameter.
        These will all be passed to the signal handler when invoked.

        :param detailed_signal: a string containing the signal name
        :type detailed_signal: str
        :param handler: a function handler
        :type handler: handler
        :param args: additional parameters arg1, arg2
        :type args: list
         """

        # If args is still None replace it by a empty list
        # if args is None:
        #     args = []

        # If detailed_signal is not in the event list create it
        if detailed_signal not in self.get_events_list():
            self.get_events_list()[detailed_signal] = list()

        self.get_events_list()[detailed_signal].append(handler)

        if args:
            self.get_events_list()[detailed_signal].append(args)

    def disconnect(self, detailed_signal, handler):
        """
        The disconnect() method removes the signal handler with the specified handler
        from the list of signal handlers for the object.

        :param detailed_signal: a string containing the signal name
        :type detailed_signal: str
        :param handler: a function handler
        :type handler: handler
        """
        if detailed_signal in self.get_events_list():
            self.get_events_list()[detailed_signal].remove(handler)

    def events_flush(self, detailed_signal, args):
        if detailed_signal in self.get_events_list():
            for handler in self.get_events_list()[detailed_signal]:
                handler(self, detailed_signal, args)

    def events_dispatch(self, detailed_signal, args):
        """
        Inform every children or child about a event and execute a eventual callback

        :param detailed_signal: a string containing the signal name
        :type detailed_signal: str
        :param args: additional parameters arg1, arg2
        :type args: list
        """
        self.events_flush(detailed_signal, args)

        # Dispatch to every children and child
        if self.__class__.__name__ in GLXCurses.GLXC.CHILDREN_CONTAINER:
            if hasattr(self, 'children'):
                if self.children is not None:
                    for child in self.children:
                        child.widget.events_dispatch(detailed_signal, args)
        else:
            if hasattr(self, 'child'):
                if self.child is not None:
                    self.child.widget.events_dispatch(detailed_signal, args)
            if hasattr(self, '_action_area'):
                if self._action_area is not None:
                    for button in self._action_area:
                        button.widget.events_dispatch(detailed_signal, args)

    def get_events_list(self):
        # return Application().event_handlers
        return self.events_list
