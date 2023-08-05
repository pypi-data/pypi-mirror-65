#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved


import GLXCurses
import logging
import curses


class Window(GLXCurses.Bin):
    def __init__(self, window_type=GLXCurses.GLXC.WINDOW_TOPLEVEL):
        """
        Creates a new :class:`Window <GLXCurses.Window.Window>`, which is a toplevel window
        that can contain other widgets.

        Nearly always, the type of the window should be GLXC.WINDOW_TOPLEVEL.

        If you’re implementing something like a popup menu from scratch (which is a bad idea, just use Menu),
        you might use GLXC.WINDOW_POPUP. GLXC.WINDOW_POPUP is not for dialogs,
        though in some other toolkits dialogs are called “popups”.

        If you simply want an undecorated window (no window borders), use ``decorated`` property,
        don’t use GLXC.WINDOW_POPUP.

        :param window_type: type of window contain on GLXC.WindowType list
        :type window_type: str
        :return: a new Window.
        :rtype: Window
        :raise TypeError: if ``window_type`` is not in valid GLXC.WindowType list
        """
        # Load heritage
        GLXCurses.Bin.__init__(self)

        # It's a GLXCurse Type
        self.glxc_type = 'GLXCurses.Window'
        self.name = '{0}{1}'.format(self.__class__.__name__, self.id)

        # Make a Style heritage attribute
        # if self.style.attribute_states:
        #     if self.attribute_states != self.style.attribute_states:
        #         self.attribute_states = self.style.attribute_states

        # Properties
        self.__accept_focus = None
        self.__application = None
        self.__attached_to = None
        self.__decorated = None
        self.__default_height = None
        self.__default_width = None
        self.__deletable = None
        self.__destroy_with_parent = None
        self.__focus_on_map = None
        self.__focus_visible = None
        self.__gravity = None
        self.__has_resize_grip = None
        self.__has_toplevel_focus = None
        self.__hide_titlebar_when_maximized = None
        self.__icon = None
        self.__icon_name = None
        self.__is_active = None
        self.__is_maximized = None
        self.__mnemonics_visible = None
        self.__modal = None
        self.__resizable = None
        self.__resize_grip_visible = None
        self.__role = None
        self.__screen = None
        self.__skip_pager_hint = None
        self.__skip_taskbar_hint = None
        self.__startup_id = None
        self.__title = None
        self.__transient_for = None
        self.__type = None
        self.__type_hint = None
        self.__urgency_hint = None
        self.__position = None

        # Style Property Details
        self.__decoration_button_layout = None
        self.__decoration_resize_handle = None

        # Property's first init
        self.application = None
        self.accept_focus = True
        self.attached_to = None
        self.decorated = False
        self.default_height = 0
        self.default_width = 0
        self.deletable = False
        self.destroy_with_parent = False
        self.focus_on_map = True
        self.focus_visible = True
        self.gravity = GLXCurses.GLXC.GRAVITY_NORTH_WEST
        self.has_toplevel_focus = False
        self.icon = curses.ACS_DIAMOND
        self.icon_name = None
        self.is_active = False
        self.is_maximized = False
        self.mnemonics_visible = True
        self.modal = False
        self.resizable = True
        self.role = None
        self.skip_pager_hint = False
        self.skip_taskbar_hint = False
        self.title = None
        self.transient_for = None
        self.type = window_type
        self.type_hint = GLXCurses.GLXC.WINDOW_TYPE_HINT_NORMAL
        self.urgency_hint = False
        self.position = GLXCurses.GLXC.WIN_POS_NONE

        self.decoration_button_layout = 'menu:close'
        self.decoration_resize_handle = 0

        # Don't know
        self.allow_grow = True
        self.allow_shrink = False

    # PROPERTY
    @property
    def accept_focus(self):
        """
        Whether the window should receive the input focus.

        :return: the accept_focus property value
        :rtype: bool
        """
        return self.__accept_focus

    @accept_focus.setter
    def accept_focus(self, accept_focus=None):
        """
        Set the accept_focus property value

        :param accept_focus: If True the window can receive the input focus
        :type accept_focus: bool
        :raise TypeError: When accept_focus is not a bool type
        """
        if type(accept_focus) != bool:
            raise TypeError('"accept_focus" must be a bool type')

        if self.accept_focus != accept_focus:
            self.__accept_focus = accept_focus

    @property
    def application(self):
        """
        The :class:`Application <GLXCurses.Application.Application>` associated with the window.

        The application will be kept alive for at least as long as it has any windows associated with it
        (see application_hold() for a way to keep it alive without windows).

        Normally, the connection between the application and the window will remain until the window is destroyed,
        but you can explicitly remove it by setting the :application property to NULL.

        :return: The :class:`Application <GLXCurses.Application.Application>` associated with the window or None
        :rtype: GLXCurses.Application.Application or None
        """
        return self.__application

    @application.setter
    def application(self, application=None):

        if not isinstance(application, GLXCurses.Application) and application is not None:
            raise TypeError("'application' must be an instance of Application")

        if application is None:
            if self.application is not None:
                self.__application = None
        else:
            if self.application != application:
                self.__application = application

    @property
    def attached_to(self):
        """
        The widget to which this window is attached. See Window.set_attached_to().

        Examples of places where specifying this relation is useful are for instance a Menu created by a ComboBox,
        a completion popup window created by Entry or a typeahead search entry created by TreeView.

        :return: The ``attached_to`` property value
        :rtype: Widget or None
        """
        return self.__attached_to

    @attached_to.setter
    def attached_to(self, attached_to=None):
        """
        Set the ``attached_to`` property value

        :param attached_to: The widget to which this window is attached
        :type attached_to: Widget or None
        :raise TypeError: When attached_to is not a Widget or  None
        """
        if attached_to is not None and not isinstance(attached_to, GLXCurses.Widget):
            raise TypeError('"attached_to" must be a Widget type or None')

        if self.attached_to != attached_to:
            self.__attached_to = attached_to

    @property
    def decorated(self):
        """
        Whether the window should be decorated by the window manager.

        Default is ``True``
        :return: the ``decorated`` property value
        :rtype: bool
        """
        return self.__decorated

    @decorated.setter
    def decorated(self, decorated=None):
        """
        Set the ``decorated`` property value

        :param decorated: If True the window will be decorated by the window manager.
        :type decorated: bool
        :raise TypeError: When decorated is not bool type
        """
        if type(decorated) != bool:
            raise TypeError('"decorated" must be a bool type')

        if self.decorated != decorated:
            self.__decorated = decorated

    @property
    def default_height(self):
        """
        The default height of the window, used when initially showing the window.

        :return: the ``default_height`` property value
        :rtype: int
        """
        return self.__default_height

    @default_height.setter
    def default_height(self, default_height=None):
        """
        Set the ``default_height`` property value

        Default value: 0

        :param default_height: The default height of the window
        :type default_height: int or None
        :raise TypeError: When default_height is not int or None type
        :raise ValueError: When default_height value is < -1
        """
        if default_height is None:
            default_height = 0
        if type(default_height) != int:
            raise TypeError('"default_height" must be a int type')
        if default_height < -1:
            raise ValueError('"default_height" allowed values: >= -1')

        if self.default_height != default_height:
            self.__default_height = default_height

    @property
    def default_width(self):
        """
        The default width of the window, used when initially showing the window.

        :return: the ``default_width`` property value
        :rtype: int
        """
        return self.__default_width

    @default_width.setter
    def default_width(self, default_width=None):
        """
        Set the ``default_height`` property value

        Default value: 0

        :param default_width: The default width of the window
        :type default_width: int or None
        :raise TypeError: When default_width is not int or None type
        :raise ValueError: When default_width value is < -1
        """
        if default_width is None:
            default_width = 0
        if type(default_width) != int:
            raise TypeError('"default_width" must be a int type')
        if default_width < -1:
            raise ValueError('"default_width" allowed values: >= -1')

        if self.default_width != default_width:
            self.__default_width = default_width

    @property
    def deletable(self):
        """
        Whether the window frame should have a close button.

        :return: The ``deletable`` property value
        :rtype: bool
        """
        return self.__deletable

    @deletable.setter
    def deletable(self, deletable=None):
        """
        Set the ``deletable`` property value

        Note: ``None`` will restore default

        Default value: False

        :param deletable: If ``True`` the windows have a close button
        :type deletable: bool or None
        :raise TypeError: When deletable is not bool or None type
        """
        if deletable is None:
            deletable = False
        if type(deletable) != bool:
            raise TypeError('"deletable" must be a bool type or None')
        if self.deletable != deletable:
            self.__deletable = deletable

    @property
    def destroy_with_parent(self):
        """
        Get the ``destroy_with_parent`` property value

        :return: ``True`` if the window will be destroyed when the parent is destroyed.
        :rtype: bool
        """
        return self.__destroy_with_parent

    @destroy_with_parent.setter
    def destroy_with_parent(self, destroy_with_parent=None):
        """
        Set the ``destroy_with_parent`` property value

        Note: None restore Default Value.

        Default Value: False

        :param destroy_with_parent: If ``True`` the window will be destroyed when the parent is destroyed.
        :type destroy_with_parent: bool or None
        :raise TypeError: when ``destroy_with_parent`` is not bool or None
        """
        if destroy_with_parent is None:
            destroy_with_parent = False
        if type(destroy_with_parent) != bool:
            raise TypeError('"destroy_with_parent" must be bool type or None')
        if self.destroy_with_parent != destroy_with_parent:
            self.__destroy_with_parent = destroy_with_parent

    @property
    def focus_on_map(self):
        """
        Whether the window should receive the input focus when mapped.

        :return: the focus_on_map property value
        :rtype: bool
        """
        return self.__focus_on_map

    @focus_on_map.setter
    def focus_on_map(self, focus_on_map=None):
        """
        Set the ``focus_on_map`` property value

        Note: None restore default value
        Default Value: True

        :param focus_on_map: If True the window will receive the input focus when mapped.
        :type focus_on_map: bool or None
        :raise TypeError: When focus_on_map is not a bool type or None
        """
        if focus_on_map is None:
            focus_on_map = True
        if type(focus_on_map) != bool:
            raise TypeError('"focus_on_map" must be a bool type or None')
        if self.focus_on_map != focus_on_map:
            self.__focus_on_map = focus_on_map

    @property
    def focus_visible(self):
        """
        Whether 'focus rectangles' are currently visible in this window.

        :return: The focus_visible property value
        :rtype: bool
        """
        return self.__focus_visible

    @focus_visible.setter
    def focus_visible(self, focus_visible=None):
        """
        Set the ``focus_visible`` property value

        Note: None restore default value
        Default Value: True

        :param focus_visible: If True the 'focus rectangles' are visible in this window.
        :type focus_visible: bool or None
        :raise TypeError: When focus_visible is not a bool type or None
        """
        if focus_visible is None:
            focus_visible = True
        if type(focus_visible) != bool:
            raise TypeError('"focus_visible" must be a bool type or None')
        if self.focus_visible != focus_visible:
            self.__focus_visible = focus_visible

    @property
    def gravity(self):
        """
        Window gravity defines the meaning of coordinates passed to Window.move().

        See Window.move() for more details.

        The default window gravity is GLXC.GRAVITY_NORTH_WEST which will typically “do what you mean.”

        :return: window gravity
        :rtype: str
        """
        return self.__gravity

    @gravity.setter
    def gravity(self, gravity=None):
        """
        Set the ``gravity`` property value

        Note: ``None`` restore default value
        Default Value: ``GLXC.GRAVITY_NORTH_WEST``

        :param gravity: The window gravity of the window.
        :type gravity: str or None
        :raise TypeError: When gravity is not a str type or None
        :raise ValueError: When gravity is not in GLX.GRAVITY
        """
        if gravity is None:
            gravity = GLXCurses.GLXC.GRAVITY_NORTH_WEST
        if type(gravity) != str:
            raise TypeError('"gravity" must be a str type or None')
        if gravity not in GLXCurses.GLXC.Gravity:
            raise ValueError('"gravity" must be a in GLXC.Gravity')
        if self.gravity != gravity:
            self.__gravity = gravity

    @property
    def has_resize_grip(self):
        """
        Whether the window has a corner resize grip.

        Note that the resize grip is only shown if the window is actually resizable and not maximized.

        Use “resize-grip-visible” to find out if the resize grip is currently shown.

        :return: The has_resize_grip property value
        :rtype: bool
        """
        return self.__has_resize_grip

    @has_resize_grip.setter
    def has_resize_grip(self, has_resize_grip=None):
        """
        Set the ``has_resize_grip`` property value

        Note: None restore default value
        Default Value: False

        :param has_resize_grip: If True the window has a corner resize grip.
        :type has_resize_grip: bool or None
        :raise TypeError: When has_resize_grip is not a bool type or None
        """
        if has_resize_grip is None:
            has_resize_grip = False
        if type(has_resize_grip) != bool:
            raise TypeError('"has_resize_grip" must be a bool type or None')
        if self.has_resize_grip != has_resize_grip:
            self.__has_resize_grip = has_resize_grip

    @property
    def has_toplevel_focus(self):
        """
        Whether the input focus is within this Window.

        :return: The ``has_toplevel_focus`` property value
        :rtype: bool
        """
        return self.__has_toplevel_focus

    @has_toplevel_focus.setter
    def has_toplevel_focus(self, has_toplevel_focus=None):
        """
        Set the ``has_toplevel_focus`` property value

        Note: None restore default value
        Default Value: False

        :param has_toplevel_focus: If True the input focus is within this window
        :type has_toplevel_focus: bool or None
        :raise TypeError: When has_toplevel_focus is not a bool type or None
        """
        if has_toplevel_focus is None:
            has_toplevel_focus = False
        if type(has_toplevel_focus) != bool:
            raise TypeError('"has_toplevel_focus" must be a bool type or None')
        if self.has_toplevel_focus != has_toplevel_focus:
            self.__has_toplevel_focus = has_toplevel_focus

    @property
    def hide_titlebar_when_maximized(self):
        """
        Whether the titlebar should be hidden during maximization.

        :return: The ``hide_titlebar_when_maximized`` property value
        :rtype: bool
        """
        return self.__hide_titlebar_when_maximized

    @hide_titlebar_when_maximized.setter
    def hide_titlebar_when_maximized(self, hide_titlebar_when_maximized=None):
        """
        Set the ``hide_titlebar_when_maximized`` property value

        Note: None restore default value
        Default Value: False

        :param hide_titlebar_when_maximized: If True the titlebar will be hidden during maximization.
        :type hide_titlebar_when_maximized: bool or None
        :raise TypeError: When hide_titlebar_when_maximized is not a bool type or None
        """
        if hide_titlebar_when_maximized is None:
            hide_titlebar_when_maximized = False
        if type(hide_titlebar_when_maximized) != bool:
            raise TypeError('"hide_titlebar_when_maximized" must be a bool type or None')
        if self.hide_titlebar_when_maximized != hide_titlebar_when_maximized:
            self.__hide_titlebar_when_maximized = hide_titlebar_when_maximized

    @property
    def icon(self):
        """
        Icon for this window.

        :return: The ``icon`` property value
        :rtype: curses Extended Characters
        """
        return self.__icon

    @icon.setter
    def icon(self, icon=None):
        """
        Set the ``icon`` property value

        Note: None restore default value
        Default Value: curses Extended Characters

        :param icon: Icon for this window.
        :type icon: curses Extended Characters or None
        :raise TypeError: When icon is not curses.ACS_DIAMOND or curses.ACS_CKBOARD or None
        """
        if icon is None:
            icon = curses.ACS_DIAMOND
        if icon not in [curses.ACS_DIAMOND, curses.ACS_CKBOARD]:
            raise TypeError('"icon" is not really implemented, use curses.ACS_DIAMOND or curses.ACS_CKBOARD')
        if self.icon != icon:
            self.__icon = icon

    @property
    def icon_name(self):
        """
        The ``icon_name`` property specifies the name of the themed icon to use as the window icon.

        See IconTheme for more details.

        :return: The ``icon_name`` property value
        :rtype: str or None
        """
        return self.__icon_name

    @icon_name.setter
    def icon_name(self, icon_name=None):
        """
        Set the ``icon_name`` property value

        Note: ``None`` restore default value
        Default Value: ``None``

        :param icon_name: Icon name use for theme
        :type icon_name: str or None
        :raise TypeError: When icon_name is not curses.ACS_DIAMOND or curses.ACS_CKBOARD or None
        """
        if icon_name is not None and type(icon_name) != str:
            raise TypeError('"icon_name" must be astr type or None')
        if self.icon_name != icon_name:
            self.__icon_name = icon_name

    @property
    def is_active(self):
        """
        Whether the toplevel is the current active window.

        :return: The ``is_active`` property value
        :rtype: bool
        """
        return self.__is_active

    @is_active.setter
    def is_active(self, is_active=None):
        """
        Set the ``is_active`` property value

        Note: None restore default value
        Default Value: False

        :param is_active: If ``True`` the toplevel is the current active window.
        :type is_active: bool or None
        :raise TypeError: When is_active is not a bool type or None
        """
        if is_active is None:
            is_active = False
        if type(is_active) != bool:
            raise TypeError('"is_active" must be a bool type or None')
        if self.is_active != is_active:
            self.__is_active = is_active

    @property
    def is_maximized(self):
        """
        Whether the window is maximized.

        :return: The ``is_maximized`` property value
        :rtype: bool
        """
        return self.__is_maximized

    @is_maximized.setter
    def is_maximized(self, is_maximized=None):
        """
        Set the ``is_maximized`` property value

        Note: None restore default value
        Default Value: False

        :param is_maximized: If ``True`` the window is maximized.
        :type is_maximized: bool or None
        :raise TypeError: When is_maximized is not a bool type or None
        """
        if is_maximized is None:
            is_maximized = False
        if type(is_maximized) != bool:
            raise TypeError('"is_maximized" must be a bool type or None')
        if self.is_maximized != is_maximized:
            self.__is_maximized = is_maximized

    @property
    def mnemonics_visible(self):
        """
        Whether mnemonics are currently visible in this window.

        This property is maintained by GLXCurses based on user input, and should not be set by applications.

        :return: The ``mnemonics_visible`` property value
        :rtype: bool
        """
        return self.__mnemonics_visible

    @mnemonics_visible.setter
    def mnemonics_visible(self, mnemonics_visible=None):
        """
        Set the ``mnemonics_visible`` property value

        Note: None restore default value
        Default Value: True

        :param mnemonics_visible: If ``True`` mnemonics are currently visible in this window.
        :type mnemonics_visible: bool or None
        :raise TypeError: When is_active is not a bool type or None
        """
        if mnemonics_visible is None:
            mnemonics_visible = True
        if type(mnemonics_visible) != bool:
            raise TypeError('"mnemonics_visible" must be a bool type or None')
        if self.mnemonics_visible != mnemonics_visible:
            self.__mnemonics_visible = mnemonics_visible

    @property
    def modal(self):
        """
        If `True``, the window is modal (other windows are not usable while this one is up).

        :return: The ``modal`` property value
        :rtype: bool
        """
        return self.__modal

    @modal.setter
    def modal(self, modal=None):
        """
        Sets a window modal or non-modal.

        Modal windows prevent interaction with other windows in the same application.

        To keep modal dialogs on top of main application windows, use ``transient_for`` property to make the
        dialog transient for the parent; most window managers will then disallow lowering the dialog below the parent.

        Note: None restore default value
        Default Value: False

        :param modal: If ``True``, the window is modal (other windows are not usable while this one is up).
        :type modal: bool or None
        :raise TypeError: When modal is not a bool type or None
        """
        if modal is None:
            modal = False
        if type(modal) != bool:
            raise TypeError('"modal" must be a bool type or None')
        if self.modal != modal:
            self.__modal = modal

    @property
    def resizable(self):
        """
        Gets the value set to ``resizable`` property.

        :return: ``True`` if the user can resize the window
        :rtype: bool
        """
        return self.__resizable

    @resizable.setter
    def resizable(self, resizable=None):
        """
        Sets whether the user can resize a window. Windows are user resizable by default.

        Note: None restore default value
        Default Value: True

        :param resizable: If ``True``, users can resize this window.
        :type resizable: bool or None
        :raise TypeError: When modal is not a bool type or None
        """
        if resizable is None:
            resizable = True
        if type(resizable) != bool:
            raise TypeError('"resizable" must be a bool type or None')
        if self.resizable != resizable:
            self.__resizable = resizable

    @property
    def role(self):
        """
        Unique identifier for the window to be used when restoring a session.

        :return: A unique identifier
        :rtype: str or None
        """
        return self.__role

    @role.setter
    def role(self, role=None):
        """
        Set the ``role`` property value

        Note: ``None`` restore default value
        Default Value: None

        :param role: Unique identifier for the window to be used when restoring a session.
        :type role: str or None
        :raise TypeError: When role is not a str type or None
        """
        if role is not None and type(role) != str:
            raise TypeError('"modal" must be a str type or None')
        if self.role != role:
            self.__role = role

    @property
    def screen(self):
        """
        The screen where this window will be displayed.

        :return: The screen where this window will be displayed
        :rtype: GLXCurses.Screen or None
        """
        return self.__screen

    @screen.setter
    def screen(self, screen=None):
        """
        Set the ``screen`` property value

        Note: ``None`` restore default value
        Default Value: None

        :param screen: The screen where this window will be displayed.
        :type screen: GLXCurses.Screen or None
        :raise TypeError: When screen is not a GLXCurses.Screen instance or None
        """
        if screen is not None and not isinstance(screen, GLXCurses.Screen):
            raise TypeError('"screen" must be a GLXCurses.Screen instance or None')
        if self.screen != screen:
            self.__screen = screen

    @property
    def skip_pager_hint(self):
        """
        ``True`` if the window should not be in the pager.

        :return: The ``skip_pager_hint`` property value
        :rtype: bool
        """
        return self.__skip_pager_hint

    @skip_pager_hint.setter
    def skip_pager_hint(self, skip_pager_hint=None):
        """
        Set the ``skip_pager_hint`` property value

        Note: None restore default value
        Default Value: False

        :param skip_pager_hint: ``True`` if the window should not be in the pager.
        :type skip_pager_hint: bool or None
        :raise TypeError: When skip_pager_hint is not a bool type or None
        """
        if skip_pager_hint is None:
            skip_pager_hint = False
        if type(skip_pager_hint) != bool:
            raise TypeError('"skip_pager_hint" must be a bool type or None')
        if self.skip_pager_hint != skip_pager_hint:
            self.__skip_pager_hint = skip_pager_hint

    @property
    def skip_taskbar_hint(self):
        """
        ``True`` if the window should not be in the task bar.

        :return: The ``skip_taskbar_hint`` property value
        :rtype: bool
        """
        return self.__skip_taskbar_hint

    @skip_taskbar_hint.setter
    def skip_taskbar_hint(self, skip_taskbar_hint=None):
        """
        Set the ``skip_taskbar_hint`` property value

        Note: None restore default value
        Default Value: False

        :param skip_taskbar_hint: ``True`` if the window should not be in the task bar.
        :type skip_taskbar_hint: bool or None
        :raise TypeError: When skip_taskbar_hint is not a bool type or None
        """
        if skip_taskbar_hint is None:
            skip_taskbar_hint = False
        if type(skip_taskbar_hint) != bool:
            raise TypeError('"skip_taskbar_hint" must be a bool type or None')
        if self.skip_taskbar_hint != skip_taskbar_hint:
            self.__skip_taskbar_hint = skip_taskbar_hint

    @property
    def startup_id(self):
        """
        The ``startup_id`` was originally write-only property for setting window's startup notification identifier.

        See Window.set_startup_id() for more details.

        :return: A identifier or None
        :rtype: str or None
        """
        return self.__startup_id

    @startup_id.setter
    def startup_id(self, startup_id=None):
        """
        Set the ``startup_id`` property value

        Note: ``None`` restore default value
        Default Value: None

        :param startup_id: setting window's startup notification identifier.
        :type startup_id: str or None
        :raise TypeError: When startup_id is not a str type or None
        """
        if startup_id is not None and type(startup_id) != str:
            raise TypeError('"startup_id" must be a str type or None')
        if self.startup_id != startup_id:
            self.__startup_id = startup_id

    @property
    def title(self):
        """
        The title of the window.

        Default value: None

        :return: the ``title`` property value
        :rtype: str or None
        """
        return self.__title

    @title.setter
    def title(self, title=None):
        """
        Set the ``title`` property value

        Sets the title of the Window. The title of a window will be displayed in its title bar,
        the title bar is rendered by the window manager, so exactly how the title appears to users may
        vary according to a user’s exact configuration.

        The title should help a user distinguish this window from other windows they may have open.

        A good title might include the application name and current document filename, for example.

        :param title: the title of the window.
        :type title: str or None
        """
        if type(title) != str and title is not None:
            raise TypeError('"title" must be a str type')
        if self.title != title:
            self.__title = title

    @property
    def transient_for(self):
        """
        Fetches the transient parent for this window.

        See transient_for.setter for more details about transient windows.

        :return: the transient parent for this window, or None if no transient parent has been set.
        :rtype: Window or None
        """
        return self.__transient_for

    @transient_for.setter
    def transient_for(self, parent=None):
        """
        Dialog windows should be set transient for the main application window they were spawned from.

        This allows window managers to e.g. keep the dialog on top of the main window, or center the dialog
        over the main window.

        Passing ``None`` for ``parent`` unsets the current transient window.

        :param parent: parent window, or None.
        :type parent:  GLXCurses.Window or None
        """
        if parent is not None and not isinstance(parent, Window):
            raise TypeError('"parent" must be a GLXCurses.Window instance or None')
        if self.transient_for != parent:
            self.__transient_for = parent

    @property
    def type(self):
        """
        Return the ``type`` property

        :return: GLXC.WindowType
        :rtype: str
        """
        return self.__type

    @type.setter
    def type(self, window_type=None):
        """
        Set the window ``type`` property

        Note: ``None`` restore default value
        Default value: GLXC.WINDOW_TOPLEVEL

        :param window_type: The type of the window.
        :type window_type: GLXC.WindowType
        :raise TypeError: When window_type is not a str type or None
        :raise ValueError: When window_type is not in GLXC.WindowType list
        """
        if window_type is None:
            window_type = GLXCurses.GLXC.WINDOW_TOPLEVEL
        if window_type is not None and type(window_type) != str:
            raise TypeError('"window_type" must be a str type or None')
        if window_type not in GLXCurses.GLXC.WindowType:
            raise ValueError('"window_type" must be in GLXC.WindowType')
        if self.type != window_type:
            self.__type = window_type

    @property
    def type_hint(self):
        """
        Hint to help the desktop environment understand what kind of window this is and how to treat it.

        These are hints for the window manager that indicate what type of function the window has.

        The window manager can use this when determining decoration and behaviour of the window.

        The hint must be set before mapping the window.

        :return: hint for the window manager
        :rtype: str
        """
        return self.__type_hint

    @type_hint.setter
    def type_hint(self, type_hint=None):
        """
        set the ``type_hint`` property value.

        Note: ``None restore the default value
        Default Value: GLXC.WINDOW_TYPE_HINT_NORMAL

        :param type_hint: Ahint for the window manager
        :type type_hint: GLXC.WindowTypeHint or None
        :raise TypeError: When type_hint is not a str type or None
        :raise ValueError: When type_hint is not in GLXC.WindowTypeHint list
        """
        if type_hint is None:
            type_hint = GLXCurses.GLXC.WINDOW_TYPE_HINT_NORMAL
        if type(type_hint) != str:
            raise TypeError('"type_hint" must be a str type or None')
        if type_hint not in GLXCurses.GLXC.WindowTypeHint:
            raise ValueError('"type_hint" must be in GLXC.WindowTypeHint list')
        if self.type_hint != type_hint:
            self.__type_hint = type_hint

    @property
    def urgency_hint(self):
        """
        ``True`` if the window should be brought to the user's attention.

        :return: tthe ``urgency_hint`` property value
        :rtype: boot
        """
        return self.__urgency_hint

    @urgency_hint.setter
    def urgency_hint(self, urgency_hint=None):
        """
        Set the ``urgency_hint`` property value

        Note: None restore default value
        Default Value: False

        :param urgency_hint: ``True`` if the window should be brought to the user's attention.
        :type urgency_hint: bool or None
        :raise TypeError: When urgency_hint is not a bool type or None
        """
        if urgency_hint is None:
            urgency_hint = False
        if type(urgency_hint) != bool:
            raise TypeError('"urgency_hint" must be a bool type or None')
        if self.urgency_hint != urgency_hint:
            self.__urgency_hint = urgency_hint

    @property
    def position(self):
        """
        The initial position of the window.

        :return: position constraint
        :rtype: str
        """
        return self.__position

    @position.setter
    def position(self, position=None):
        """
        Sets a position constraint for this window.

        If the old or new constraint is GLXC.WIN_POS_CENTER_ALWAYS, this will also cause the window to be repositioned
        to satisfy the new constraint.

        Note: ``None restore the default value
        Default Value: GLXC.WIN_POS_NONE

        :param position: a position constraint.
        :type position: a GLXC.WindowPosition or None
        :raise TypeError: When position is not a str type or None
        :raise ValueError: When position is not in GLXC.WindowPosition list
        """
        if position is None:
            position = GLXCurses.GLXC.WIN_POS_NONE
        if type(position) != str:
            raise TypeError('"position" must be a str type or None')
        if position not in GLXCurses.GLXC.WindowPosition:
            raise ValueError('"position" must be in GLXC.WindowPosition list')
        if self.position != position:
            self.__position = position

    # STYLE PROPERTY
    @property
    def decoration_button_layout(self):
        """
        Decorated button layout property

        :return: a layout
        :rtype: str
        """
        return self.__decoration_button_layout

    @decoration_button_layout.setter
    def decoration_button_layout(self, decoration_button_layout=None):
        """
        Decorated button layout.

        :param decoration_button_layout: Decorated button layout.
        :type: str or None
        :raise TypeError: When decoration_button_layout is not a str type or None
        """
        if decoration_button_layout is None:
            decoration_button_layout = 'menu:close'
        if type(decoration_button_layout) != str:
            raise TypeError('"decoration_button_layout" must be a str type or None')
        if self.decoration_button_layout != decoration_button_layout:
            self.__decoration_button_layout = decoration_button_layout

    @property
    def decoration_resize_handle(self):
        """
        The ``decoration_resize_handle`` property

        :return: Decoration resize handle size.
        :rtype: int
        """
        return self.__decoration_resize_handle

    @decoration_resize_handle.setter
    def decoration_resize_handle(self, decoration_resize_handle=None):
        """
        set the ``decoration_resize_handle`` property value

        :param decoration_resize_handle: Decoration resize handle size.
        :type decoration_resize_handle: int or None
        :raise TypeError: When decoration_resize_handle is not a int type or None
        :raise ValueError: When decoration_resize_handle is < 0
        """
        if decoration_resize_handle is None:
            decoration_resize_handle = 0
        if type(decoration_resize_handle) != int:
            raise TypeError('"decoration_resize_handle" must be a int type or None')
        if decoration_resize_handle < 0:
            raise ValueError('"decoration_resize_handle" must be  >= 0')
        if self.decoration_resize_handle != decoration_resize_handle:
            self.__decoration_resize_handle = decoration_resize_handle

    def draw_widget_in_area(self):
        # Create the subwin
        self.create_or_resize()

        #  May be it have no parent or that the first init, then test if subwin creation have work
        if self.subwin:

            # Debug message
            if self.debug:
                logging.debug('Draw {0}'.format(self))
                logging.debug(
                    "In Area -> x: {0}, y: {1}, width: {2}, height:{3}".format(
                        self.x,
                        self.y,
                        self.width,
                        self.height
                    )
                )

            # Draw the background
            if self.parent and isinstance(self.parent, GLXCurses.Application):
                self.subwin.bkgd(ord(' '), self.style.color(fg='GRAY', bg='BLUE'))
                self.subwin.bkgdset(ord(' '), self.style.color(fg='GRAY', bg='BLUE'))

            if self.decorated:
                self._draw_box()

            # Draw the child.
            if self.child:

                self.child.widget.stdscr = GLXCurses.Application().stdscr
                self.child.widget.style = self.style

                if self.decorated:
                    self.child.widget.x = self.x + 1
                    self.child.widget.y = self.y + 1
                    self.child.widget.width = self.width - 2
                    self.child.widget.height = self.height - 2
                else:
                    self.child.widget.x = self.x
                    self.child.widget.y = self.y
                    self.child.widget.width = self.width
                    self.child.widget.height = self.height

                if self.debug:
                    logging.debug(
                        "Set child -> x: {0}, y: {1}, width: {2}, height:{3}".format(
                            self.child.widget.x,
                            self.child.widget.y,
                            self.child.widget.width,
                            self.child.widget.height
                        )
                    )

                self.child.widget.draw()

            if self.title:
                self._draw_title()

    def _draw_title(self):
        if self.decorated:
            decorated_space = 1
        else:
            decorated_space = 0
        for x_inc in range(0, len(GLXCurses.resize_text(self.title, self.width - 2, '~'))):
            try:
                self.subwin.delch(0,
                                  0 + decorated_space + x_inc
                                  )
                self.subwin.insch(0,
                                  0 + decorated_space + x_inc,
                                  GLXCurses.resize_text(self.title, self.width - 2, '~')[x_inc],
                                  self.style.color(fg='GRAY', bg='BLUE')
                                  )
            except curses.error:
                pass

    @staticmethod
    def add_accel_group():
        """
        Not implemented

        :raise NotImplementedError: because ``AccelGroup`` is not implemented
        """
        # Todo AccelGroup
        raise NotImplementedError('AccelGroup is not implemented yet')

    @staticmethod
    def remove_accel_group():
        """
        Not implemented

        :raise NotImplementedError: because ``AccelGroup`` is not implemented
        """
        # Todo AccelGroup
        raise NotImplementedError('AccelGroup is not implemented yet')

    def activate_focus(self):
        """
        Activates the current focused widget within the window.

        :return: True if a widget got activated.
        :rtype: bool
        """
        # Check if we got a child via GLXCurses.Bin heritage
        if self.child().widget:
            if self.child().widget.has_focus:
                return True

        # If we are here , then we return False
        return False

    def activate_default(self):
        """
        Activates the default widget for the window, unless the current focused widget has been configured
        to receive the default action (see gtk_widget_set_receives_default()), in which case the focused widget
        is activated.

        :return:
        """
        pass

    def get_focus(self):
        """
        The get_focus() method returns the current focused widget within the window.

        The focus widget is the widget that would have the focus if the toplevel window is focused.

        :return: The current focused widget
        :rtype: Widget or None
        """
        if self.child().widget:
            if self.child().widget.has_focus and self.is_focus:
                return self.child()
            else:
                return None

    def set_default(self, default_widget=None):
        """
        The default widget is the widget that’s activated when the user presses Enter in a dialog (for example).
        This function sets or unsets the default widget for a :class:`Window <GLXCurses.Window.Window>`.
        When setting (rather than unsetting) the default widget it’s generally easier to call
        :func:`Widget.grab_default() <GLXCurses.Widget.Widget.grab_default>` on the widget.
        Before making a widget the default widget, you must call
        :func:`Widget.set_can_default() <GLXCurses.Widget.Widget.set_can_default>` on the widget you’d like to
        make the default.


        :param default_widget: a Window or None of unset
        :type default_widget: Window
        :raise TypeError: if ``default_widget`` is not a GLXCurses.Window instance .
        """
        # check default_widget=None case
        if default_widget is None:
            self.has_default = False
            return
        # exit as soon of possible
        if not isinstance(default_widget, GLXCurses.Widget):
            raise TypeError("'default_widget' must be an instance of GLXCurses.Widget")

        # only if the widget can be default
        if default_widget.can_default:
            self.has_default = default_widget

    # The activate_default() method activates the default widget.
    # If there is no default widget or the default widget cannot be activated,
    # the window's focus widget (if any) is activated.
    # This method returns False if no default widget could be activated or there is no focus widget.
    def activate_default(self):
        if not self.child():
            return False
        elif not self.child().has_default:
            return False
        else:
            return 'sa maman'

    def get_window_type(self):
        """
        Gets the type of the window.

        Constants.GLXC.WindowType are GLXC.WINDOW_TOPLEVEL and GLXC.WINDOW_POPUP

        :return: the type of the window
        :rtype: GLXC.WINDOW_TOPLEVEL or GLXC.WINDOW_POPUP
        """
        return self.type
