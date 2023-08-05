#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import GLXCurses
import curses
import locale

# Locales Setting
locale.setlocale(locale.LC_ALL, '')
code = locale.getpreferredencoding()

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
            cls.instance = super(Singleton, cls).__call__(*args)
        return cls.instance


# https://developer.gnome.org/gtk3/stable/GtkApplication.html

class EventBus(GLXCurses.EventBusClient):
    def __init__(self):
        GLXCurses.EventBusClient.__init__(self)

    def emit(self, detailed_signal, args):
        """
        Emit signal in direction to the Mainloop.

        :param detailed_signal: a string containing the signal name
        :type detailed_signal: str
        :param args: additional parameters arg1, arg2
        :type args: list
        """
        GLXCurses.MainLoop().emit(detailed_signal, args)

    def events_dispatch(self, detailed_signal, args):
        """
        Flush Mainloop event to Child's father's for a Widget's recursive event dispatch

        :param detailed_signal: a string containing the signal name
        :type detailed_signal: str
        :param args: additional parameters arg1, arg2
        :type args: list
        """
        self.events_flush(detailed_signal, args)

        # if GLXCurses.Application().has_default
        if GLXCurses.Application().active_window.widget:
            GLXCurses.Application().active_window.widget.events_dispatch(detailed_signal, args)

        if not isinstance(GLXCurses.Application().active_window.widget, GLXCurses.Dialog):

            if GLXCurses.Application().menubar:
                GLXCurses.Application().menubar.events_dispatch(detailed_signal, args)
            if GLXCurses.Application().toolbar:
                GLXCurses.Application().toolbar.events_dispatch(detailed_signal, args)


class Application(EventBus,
                  GLXCurses.Area,
                  GLXCurses.Spot,
                  metaclass=Singleton):
    """
    :Description:

    Create a Application singleton instance.

    That class have the role of a Controller and a NCurses Wrapper.

    It have particularity to not be a GLXCurses.Widget, then have a tonne of function for be a fake GLXCurses.Widget.

    From GLXCurses point of view everything start with it component. All widget will be display and store inside it
    component.
    """

    def __init__(self):
        EventBus.__init__(self)
        GLXCurses.Area.__init__(self)
        GLXCurses.Spot.__init__(self)
        # Hidden vars
        self.__style = None
        self.__parent = None
        self.__active_window = None
        self.__app_menu = None
        self.__menubar = None
        self.__register_session = None
        self.__screensaver_active = None

        self.__children = None
        self.__active_window_id = None
        self.__statusbar = None
        self.__messagebar = None
        self.__toolbar = None

        self.screen = GLXCurses.Screen()
        self.stdscr = self.screen.stdscr
        self.style = GLXCurses.Style()

        # Store object
        self.children = None
        self.menubar = None
        self.main_window = None
        self.statusbar = None
        self.messagebar = None
        self.toolbar = None

        # Store Variables
        self.id = GLXCurses.new_id()
        self.name = '{0}{1}'.format(self.__class__.__name__, self.id)

    @property
    def active_window(self):
        """
        Gets the “active_window” for the application.

        The active :class:`Window <GLXCurses.Window.Window>` is the one that was most recently focused
        (within the application).

        This window may not have the focus at the moment if another application
        has it — this is just the most recently-focused window within this application.

        :return: the active :class:`Window <GLXCurses.Window.Window>`, or None if there isn't one.
        :rtype: GLXCurses.Window or None
        """
        windows_to_display = None
        for child in self.children:
            if child.id == self.active_window_id:
                windows_to_display = child

        # If a active window is found
        if windows_to_display is not None:
            return windows_to_display
        else:
            return None

    @active_window.setter
    def active_window(self, window=None):
        """
        Set the ``active_window`` property

        :param window: The window it be active in the Application
        :type window: GLXCurses.Window or None
        """
        # if window is not None and not isinstance(window, GLXCurses.Window):
        #     raise TypeError('"active_window" must be a GLXCurses.Window or None')
        if window.id != self.active_window_id:
            self.active_window_id = window.id

    @property
    def app_menu(self):
        return self.__app_menu

    @app_menu.setter
    def app_menu(self, app_menu=None):
        if not isinstance(app_menu, GLXCurses.MenuBar) and app_menu is not None:
            raise TypeError("'app_menu' must be a GLXCurses.MenuBar instance")
        if isinstance(app_menu, GLXCurses.MenuBar):
            app_menu.parent = self
        elif app_menu is None and isinstance(self.app_menu, GLXCurses.MenuBar):
            self.app_menu.parent = None
        if self.app_menu != app_menu:
            self.__app_menu = app_menu

    @property
    def menubar(self):
        """
        The MenuModel for the menubar.

        :return: menubar property value
        :rtype: GLXCurses.menubar or None
        """
        return self.__menubar

    @menubar.setter
    def menubar(self, menubar=None):
        """
        menubar property

        :param menubar: a GLXCurses.menubar object or None for remove one.
        :type menubar: GLXCurses.menubar or None
        :return:
        """
        if not isinstance(menubar, GLXCurses.MenuBar) and menubar is not None:
            raise TypeError("'menubar' must be a GLXCurses.MenuBar instance")
        if isinstance(menubar, GLXCurses.MenuBar):
            menubar.parent = self
        elif menubar is None and isinstance(self.menubar, GLXCurses.MenuBar):
            self.menubar.parent = None
        if self.menubar != menubar:
            self.__menubar = menubar

    @property
    def register_session(self):
        return self.__register_session

    @register_session.setter
    def register_session(self, register_session=None):
        if self.register_session != register_session:
            self.__register_session = register_session

    @property
    def screensaver_active(self):
        return self.__screensaver_active

    @screensaver_active.setter
    def screensaver_active(self, screensaver_active=None):
        if self.screensaver_active != screensaver_active:
            self.__screensaver_active = screensaver_active

    # internal property
    @property
    def style(self):
        """
        The style of the Application, which contains information about how it will look (colors, etc).

        The Application Style is impose to each widget

        :return: a GLXCurses.Style instance
        :rtype: Style
        """
        return self.__style

    @style.setter
    def style(self, style=None):
        """
        Set the ``style`` property.

        :param style: a GLXCurses.Style instance
        :type style: Style
        :raise TypeError: When style is not a GLXCurses.Style instance or None
        """
        if style is None:
            style = GLXCurses.Style()
        if not isinstance(style, GLXCurses.Style):
            raise TypeError('"style" must be a GLXCurses.Style instance or None')
        if self.style != style:
            self.__style = style

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
    def statusbar(self):
        return self.__statusbar

    @statusbar.setter
    def statusbar(self, statusbar=None):
        if statusbar is not None and not isinstance(statusbar, GLXCurses.StatusBar):
            raise TypeError('"statusbar" must be a StatusBar instance or None')
        if self.statusbar != statusbar:
            self.__statusbar = statusbar
            if isinstance(self.statusbar, GLXCurses.StatusBar):
                self.statusbar.parent = self

    @property
    def messagebar(self):
        """
        Sets the messagebar of application .

        This can only be done in the primary instance of the application, after it has been registered.
        “startup” is a good place to call this.

        :return: the ``messagebar`` property value
        :rtype: MessageBar or None
        """
        return self.__messagebar

    @messagebar.setter
    def messagebar(self, messagebar=None):
        """
        Set the ``messagebar`` property value

        :param messagebar: a :class:`MessageBar <GLXCurses.MessageBar.MessageBar>`
        :type messagebar: GLXCurses.MessageBar
        :raise TypeError: if ``messagebar`` parameter is not a MessageBar type or None
        """
        if messagebar is not None and not isinstance(messagebar, GLXCurses.MessageBar):
            raise TypeError('"messagebar" must be a MessageBar instance or None')
        if self.messagebar != messagebar:
            self.__messagebar = messagebar
            if isinstance(self.messagebar, GLXCurses.MessageBar):
                self.messagebar.parent = self

    @property
    def toolbar(self):
        return self.__toolbar

    @toolbar.setter
    def toolbar(self, toolbar=None):
        if toolbar is not None and not isinstance(toolbar, GLXCurses.ToolBar):
            raise TypeError('"toolbar" must be a ToolBar instance or None')
        if self.toolbar != toolbar:
            self.__toolbar = toolbar

    # GLXCApplication function
    # Re Order
    def add_window(self, window):
        """
        Add a :class:`Window <GLXCurses.Window.Window>` widget to the\
        :class:`Application <GLXCurses.Application.Application>` windows children's list.

        This call can only happen after the application has started; typically, you should add new application windows
        in response to the emission of the “activate” signal.

        This call is equivalent to setting the “application” property of window to application .

        Normally, the connection between the application and the window will remain until the window is destroyed,
        but you can explicitly remove it with application.remove_window().

        Galaxie-Curses will keep the application running as long as it has any windows.

        :param window: a window to add
        :type window: GLXCurses.Window
        :raise TypeError: if ``window`` parameter is not a :class:`Window <GLXCurses.Window.Window>` type
        """
        # Exit as soon of possible
        # Check if window is a Galaxie Window
        if not isinstance(window, GLXCurses.Window):
            raise TypeError("'window' must be a GLXCurses.Window instance")

        # set application
        window.application = self
        # set the Application it self as parent of the child window
        window.parent = self
        window.stdscr = self.stdscr

        # create a dictionary structure for add it to windows list
        self.children.append(
            GLXCurses.ChildElement(
                widget_name=window.name,
                widget_id=window.id,
                widget=window,
                widget_type=window.glxc_type
            )
        )

        # Make the last added element active
        if self.active_window != self.children[-1]:
            self.active_window = self.children[-1]

    def remove_window(self, window):
        """
        Remove a :class:`Window <GLXCurses.Window.Window>` widget from the\
        :class:`Application <GLXCurses.Application.Application>` windows children's list.

        Set"application" and "parent' attribute of the :func:`GLXCurses.Window <GLXCurses.Window.Window>`
        to :py:obj:`None`.

        :param window: a window to add
        :type window: GLXCurses.Window
        :raise TypeError: if ``window`` parameter is not a :class:`Window <GLXCurses.Window.Window>` type
        """
        # Exit as soon of possible
        # Check if window is a Galaxie Window
        if not isinstance(window, GLXCurses.Window):
            raise TypeError("'window' must be a GLXCurses.Window instance")

        # Detach the children
        window.parent = None
        window.application = None

        # Search for the good window id and delete it from the window list
        count = 0
        last_found = None
        for child in self.children:
            if child.id == window.id:
                last_found = count
            count += 1

        if last_found is not None:
            self.children.pop(last_found)
            if len(self.children) - 1 >= 0:
                self.active_window = self.children[-1]

    def get_window_by_id(self, identifier=None):
        """
        Returns the GtkApplicationWindow with the given ID.

        :param identifier: an identifier number
        :type identifier: int
        :return: the window with ID ``identifier`` , or None if there is no window with this ID.
        :rtype: int or None
        :raise TypeError: when ``identifier`` is nt a int type
        """
        if not GLXCurses.is_valid_id(identifier):
            raise TypeError('"identifier" must be a int type')
        for child in self.children:
            if child.id == identifier:
                return child
        return None

    # inhibit()
    # uninhibit()
    # is_inhibited()
    # prefers_app_menu()

    def refresh(self):
        """
        Refresh the NCurses Screen, and redraw each contain widget's

        It's a central refresh point for the entire application.
        """
        self.screen.clear()
        self.check_sizes()

        if self.height > 0 and self.active_window:
            if isinstance(self.active_window.widget, GLXCurses.Dialog) or \
                    Application().has_focus is not None and \
                    isinstance(Application().has_focus.widget, GLXCurses.Menu):
                prev_child = None
                for child in self.children:
                    if child.id == GLXCurses.Application().active_window_id_prev:
                        prev_child = child

                if prev_child:
                    prev_child.widget.x = self.x
                    prev_child.widget.y = self.y
                    prev_child.widget.width = self.width
                    prev_child.widget.height = self.height
                    prev_child.widget.draw()

        if self.active_window:
            self.active_window.widget.draw()

        if self.messagebar:
            self.messagebar.draw()

        if self.statusbar:
            self.statusbar.draw()

        if self.menubar:
            self.menubar.draw()

        if self.toolbar:
            self.toolbar.draw()

        self.screen.refresh()

    def check_sizes(self):
        """
        Just a internal method for compute every size.

        It consist to a serial of testable function call
        """
        # Get stdscr information
        screen_y, screen_x = self.stdscr.getbegyx()
        screen_height, screen_width = self.stdscr.getmaxyx()

        # Area of Application is a zone where the active Windows will have it sizes impose by it.
        self.create_or_resize(parent_height=screen_height, parent_width=screen_width)

        # If we have a active windows, (must be a Container for true, but we impose a Window with add_window())
        if self.active_window:
            # Dialog use screen location
            if isinstance(self.active_window.widget, GLXCurses.Dialog):
                self.active_window.widget.stdscr = self.stdscr
                self.active_window.widget.x = screen_x
                self.active_window.widget.y = screen_y
                self.active_window.widget.width = screen_width
                self.active_window.widget.height = screen_height
            else:
                # Impose the Window area setting, it can be use like that by all Widget inside the Window container
                # that the role of teh container to impose it Area size to every children. Here that is the root of
                # the area
                self.active_window.widget.stdscr = self.stdscr
                self.active_window.widget.style = self.style
                self.active_window.widget.y = self.y
                self.active_window.widget.x = self.x
                self.active_window.widget.width = self.width
                self.active_window.widget.height = self.height

        if self.menubar:
            self.menubar.stdscr = self.stdscr
            self.menubar.y = screen_y
            self.menubar.x = screen_x
            self.menubar.width = screen_width
            self.menubar.height = 1

        if self.messagebar:

            to_remove = 0
            if self.statusbar:
                to_remove += 1
            if self.toolbar:
                to_remove += 1

            self.messagebar.stdscr = self.stdscr
            self.messagebar.y = screen_height - 1 - to_remove
            self.messagebar.x = screen_x
            self.messagebar.width = screen_width
            self.messagebar.height = 1

        if self.statusbar:

            to_remove = 0
            if isinstance(self.toolbar, GLXCurses.ToolBar):
                to_remove += 1

            self.statusbar.stdscr = self.stdscr
            self.statusbar.y = screen_height - 1 - to_remove
            self.statusbar.x = screen_x
            self.statusbar.width = screen_width
            self.statusbar.height = 1

        if self.toolbar:
            to_remove = 0

            self.toolbar.stdscr = self.stdscr
            self.toolbar.y = screen_height - 1 - to_remove
            self.toolbar.x = screen_x
            self.toolbar.width = screen_width
            self.toolbar.height = 1

    def getch(self):
        """
        Use by the Mainloop for interact with teh keyboard and the mouse.

        getch() returns an integer corresponding to the key pressed. If it is a normal character, the integer value
        will be equivalent to the character. Otherwise it returns a number which can be matched with the constants
        defined in curses.h.

        For example if the user presses F1, the integer returned is 265.

        This can be checked using the macro KEY_F() defined in curses.h. This makes reading keys portable and easy
        to manage.

        .. code-block:: python

           ch = Application.getch()

        getch() will wait for the user to press a key, (unless you specified a timeout) and when user presses a key,
        the corresponding integer is returned. Then you can check the value returned with the constants defined in
        curses.h to match against the keys you want.

        .. code-block:: python

           if ch == curses.KEY_LEFT
               print("Left arrow is pressed")


        :return: an integer corresponding to the key pressed.
        :rtype: int
        """
        return self.stdscr.getch()

    # Internal
    def create_or_resize(self, parent_height=0, parent_width=0):
        # parent_height, parent_width = self.stdscr.getmaxyx()

        menu_bar_height = 0
        message_bar_height = 0
        status_bar_height = 0
        tool_bar_height = 0

        if self.menubar:
            menu_bar_height += 1
        if self.messagebar:
            message_bar_height += 1
        if self.statusbar:
            status_bar_height += 1
        if self.toolbar:
            tool_bar_height += 1

        interface_elements_height = 0
        interface_elements_height += menu_bar_height
        interface_elements_height += message_bar_height
        interface_elements_height += status_bar_height
        interface_elements_height += tool_bar_height

        # The Application widget consider is a widget with the area as size
        # That is it size we impose to children
        # The stdscr know very well it size :)
        self.height = parent_height - interface_elements_height
        self.width = parent_width
        self.x = 0
        self.y = menu_bar_height

        # Look if we have to create a derwin or resize/move the existing one.
        if self.subwin is None:
            self.subwin = self.stdscr.derwin(
                self.height,
                self.width,
                self.y,
                self.x
            )
        else:
            subwin_height, subwin_width = self.subwin.getmaxyx()
            curses_derwin_y, curses_derwin_x = self.subwin.getbegyx()

            if self.width != subwin_width or \
                    self.height != subwin_height or \
                    self.y != curses_derwin_y or \
                    self.x != curses_derwin_x:
                try:
                    self.subwin.resize(self.height, self.width)
                    self.subwin.mvderwin(self.y, self.x)
                except curses.error:  # pragma: no cover
                    pass
