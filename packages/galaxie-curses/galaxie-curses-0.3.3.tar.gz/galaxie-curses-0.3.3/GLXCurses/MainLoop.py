#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved
import sys
import GLXCurses
import curses
import logging

import threading

lock = threading.Lock()


# class Singleton(type):
#     _instances = {}
#
#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             with lock:
#                 if cls not in cls._instances:
#                     cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
#         return cls._instances[cls]

class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kw)
        return cls.instance


# https://developer.gnome.org/glib/stable/glib-The-Main-Event-Loop.html
class MainLoop(object, metaclass=Singleton):
    """
    :Description:

    The MainLoop is something close to a infinity loop with a start() and stop() method
     . Refresh the Application for the first time
     . Start the Loop
     . Wait for a Curses events then dispatch events and signals over Application Children's
     . Refresh the Application if a event or a signal have been detect
     . If MainLoop is stop the Application will close and should be follow by a sys.exit()

    Attributes:
        event_buffer       -- A List, Default Value: list()
        started            -- A Boolean, Default Value: False

    Methods:
        get_event_buffer() -- get the event_buffer attribute
        get_started()      -- get the started attribute
        start()            -- start the mainloop
        stop()             -- stop the mainloop
        emit()             -- emit a signal

    .. warning:: you have to start the mainloop from you application via MainLoop().start()
    """

    def __init__(self):
        """
        Creates a new MainLoop structure.
        """
        self.event_buffer = list()
        self._is_running = False

        self.debug = True
        self.debug_level = 0

    def get_event_buffer(self):
        """
        Return the event_buffer list attribute, it lis can be edited or modify as you need

        :return: event buffer
        :rtype: list()
        """
        return self.event_buffer

    def is_running(self):
        """
        Checks to see if the MainLoop is currently being run via run().

        :return: TRUE if the mainloop is currently being run.
        :rtype: Boolean
        """
        return self._is_running

    def run(self):
        """
        Runs a MainLoop until quit() is called on the loop. If this is called for the thread of the loop's
        , it will process events from the loop, otherwise it will simply wait.
        """
        self._set_is_running(True)
        if self.debug:
            logging.info('Starting ' + self.__class__.__name__)
        self._run()

    def quit(self):
        """
        Stops a MainLoop from running. Any calls to run() for the loop will return.

        Note that sources that have already been dispatched when quit() is called will still be executed.

        .. :warning: A MainLoop quit() call will certainly cause the end of you programme
        """
        self._set_is_running(False)
        logging.debug(self.__class__.__name__ + ': Stopping')

    def emit(self, signal, args):
        """
        Emit a signal, it consist to add the signal structure inside a global event list

        .. code-block:: python

           args = dict(
               'uuid': Widget().get_widget_id()
               'key1': value1
               'key2': value2
           )
           structure = list(
               detailed_signal,
               args
           )

        :param signal: a string containing the signal name
        :param args: additional parameters arg1, arg2
        """

        if self.debug_level > 2:
            logging.info(signal + ' ' + str(args))

        self.get_event_buffer().insert(0, [signal, args])

        # GLXCurses.application.refresh()

    # Internal Method's
    def _set_is_running(self, boolean):
        """
        Set the is_running attribute

        :param boolean: 0 or True
        :type boolean: Boolean
        """
        self._is_running = bool(boolean)

    def _pop_last_event(self):
        # noinspection PyBroadException
        try:
            if self.get_event_buffer():
                return self.get_event_buffer().pop()

        except Exception as the_error:
            logging.debug(self.__class__.__name__ + ": Error %s" % str(the_error))

    def _handle_curses_input(self, input_event):
        # width = GLXCurses.application.width
        # height = GLXCurses.application.height
        if input_event == curses.KEY_MOUSE:
            self.emit('MOUSE_EVENT', curses.getmouse())
        # elif input_event == curses.KEY_RESIZE:
        #     self.emit('RESIZE', {
        #         'class': GLXCurses.Application().__class__.__name__,
        #         'type': 'Resize',
        #         'id': GLXCurses.Application().id,
        #         'width': GLXCurses.Application().width,
        #         'height': GLXCurses.Application().height,
        #     })
        else:
            self.emit('CURSES', input_event)

    def _handle_event(self):
        try:
            event = self._pop_last_event()
            if event:
                while event:
                    # If it have event dispatch it
                    logging.debug(self.__class__.__name__ + ": Dispatch %s" % str(event[0]))
                    logging.debug(self.__class__.__name__ + ": Dispatch %s" % str(event[1]))
                    GLXCurses.Application().events_dispatch(event[0], event[1])
                    # Delete the last event inside teh event list
                    event = self._pop_last_event()

        # except KeyError as the_error:
        #     # Mouse Wheel bug ?
        #     if str(the_error) == '134217728':
        #         pass
        #         # logging.debug(self.__class__.__name__ + ": Error %s" % str(the_error))
        except Exception as the_error:
            logging.debug(self.__class__.__name__ + ": Error %s" % str(the_error))

    def _run(self):
        if self.is_running():
            # A bit light for notify about we are up and running, but we are really inside the main while(1) loop
            logging.debug(self.__class__.__name__ + ': Started')

            # That normally the first refresh of the application, it can be considered as the first stdscr display.
            try:
                GLXCurses.Application().refresh()
            except Exception:
                self.quit()
                GLXCurses.Application().screen.close()
                sys.stdout.write("{0}\n".format(sys.exc_info()[0]))
                sys.stdout.flush()
                raise

        # The loop
        while self.is_running():
            try:
                # Wait for a event
                input_event = GLXCurses.Application().getch()
                # logging.debug(self.event_buffer)

                # Wait for a event
                # logging.debug(input_event)
                if input_event != -1:
                    self._handle_curses_input(input_event)

                # Do something with event
                self._handle_event()

                # In case it was a graphic event we refresh the stdscr, ncurse have a optimization mechanism for refresh
                # only character's it need.
                GLXCurses.Application().refresh()

            except KeyboardInterrupt:
                # Check is the focused widget is a Editable, because Ctrl + c,  is a Copy to Clipboard action
                if isinstance(GLXCurses.Application().has_focus, GLXCurses.ChildElement) and \
                        isinstance(GLXCurses.Application().has_focus.widget, GLXCurses.Editable):
                    # Consider as Ctrl + c
                    self.emit('CURSES', 3)
                else:
                    # The user have manually stop operations
                    self.emit('KEYBOARD_INTERRUPT', str(sys.exc_info()))
                    self.quit()
                    GLXCurses.Application().screen.close()
                    sys.stdout.write("{0}: {1}\n".format('KeyboardInterrupt', sys.exc_info()[2]))
                    sys.stdout.flush()

            except Exception:
                self.quit()
                GLXCurses.Application().screen.close()
                sys.stdout.write("{0}\n".format(sys.exc_info()[0]))
                sys.stdout.flush()
                raise

        # Here self.get_started() == False , then the GLXCurse.Mainloop() should be close
        GLXCurses.Application().screen.close()
        sys.exit(0)
