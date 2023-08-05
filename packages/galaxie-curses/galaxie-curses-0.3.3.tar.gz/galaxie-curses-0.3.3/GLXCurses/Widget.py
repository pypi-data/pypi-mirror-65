#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved


import GLXCurses
import curses
from curses import error as curses_error


# Inspired by: https://developer.gnome.org/gtk3/stable/GtkWidget.html
class Widget(GLXCurses.Object, GLXCurses.Area):
    def __init__(self):
        """

        :rtype: object
        """
        # Load heritage
        GLXCurses.Object.__init__(self)
        GLXCurses.Area.__init__(self)

        # It's a GLXCurse Type
        self.glxc_type = 'GLXCurses.Widget'

        # Widget Setting
        self.flags = self.default_flags

        self.state = dict()
        self.state['NORMAL'] = True
        self.state['ACTIVE'] = False
        # self.state['PRELIGHT'] = False

        self.state['SELECTED'] = False
        self.state['INSENSITIVE'] = False
        self.flags['HAS_FOCUS'] = False

        # Widget
        self.imposed_spacing = 0
        self.widget_decorated = False

        # Widget Parent
        # Set the Application
        self.__attribute_states = None

        # Property init
        # If True, the application will paint directly on the widget
        self.__app_paintable = False

        # If True, the widget can be the default widget
        self.__can_default = False

        # If True, the widget can accept the input focus
        self.__can_focus = False

        # If True, the widget have capability to display prelight color
        self.__can_prelight = False

        # If True, the widget is part of a composite widget
        self.__composite_child = False

        # If True, the widget is double buffered
        self.__double_buffered = False

        # The event mask that decides what kind of Event this widget gets.
        self.events = None

        # The mask that decides what kind of extension events this widget gets.
        self.extension_events = None

        # Whether to expand in both directions. Setting this sets both “hexpand” and “vexpand”
        self.__expand = False

        # Whether the widget should grab focus when it is clicked with the mouse.
        self.__focus_on_click = True

        # How to distribute horizontal space if widget gets extra space, see GLXC.Align
        self.__halign = GLXCurses.GLXC.ALIGN_FILL

        # If True, the widget is the default widget
        self.__has_default = False

        # If True, the widget has the input focus
        self.__has_focus = False

        # If True the widget is prelight like selected with hight light thing
        self.__has_prelight = False

        # A value of True indicates that widget can have a tooltip
        self.__has_tooltip = False

        # The height request of the widget, or 0 if natural/expendable request should be used.
        self.__height_request = -1

        # If True the widget will expand it self horizontally.
        self.__hexpand = False

        # If True the widget use the “hexpand” property
        self.__hexpand_set = False

        # If True, the widget is the focus widget within the toplevel.
        self.__is_focus = False

        # If read, returns max margin on any side.
        self.__margin = 0

        # Margin on bottom side of widget.
        self.__margin_bottom = 0

        # Margin on end of widget, horizontally.
        self.__margin_end = 0

        # Margin on start of widget, horizontally.
        self.__margin_start = 0

        # Margin on top side of widget.
        self.__margin_top = 0

        # The name of the widget
        # Widgets can be named, which allows you to refer to them from a GLXCStyle
        self.__name = None

        # If True show_all() should not affect this widget
        self.__no_show_all = False

        # The parent widget of this widget. Must be a Container widget.
        self.__parent = None

        # If True, the widget will receive the default action when it is focused.
        self.__receives_default = False

        # If True, the widget responds to input
        self.sensitive = True

        # The style of the widget, which contains information about how it will look (colors etc).
        # Each Widget come with it own Style by default
        # It can receive parent Style() or a new Style() during a set_parent() / un_parent() call
        # GLXCApplication is a special case where it have no parent, it role is to impose it own style to each Widget
        self.__style = GLXCurses.Style()

        self.style_backup = None

        # Sets the text of tooltip to be the given string.
        self.__tooltip_text = None

        # How to distribute vertical space if widget gets extra space, see GLXC.Align
        self.__valign = GLXCurses.GLXC.ALIGN_FILL

        # Whether to expand vertically. See Widget().set_vexpand().
        self.__vexpand = False

        # Whether to use the “vexpand” property. See Widget().get_vexpand_set().
        self.__vexpand_set = False

        # Whether the widget is visible.
        self.visible = False

        # The width request of the widget, or -1 if natural/expendable request should be used.
        self.__width_request = -1

        # The widget's window if realized, None otherwise.
        self.__window = None

        # Size
        self.__preferred_height = 0
        self.__preferred_width = 0
        self.preferred_height = 0
        self.preferred_width = 0

    # Internal
    @property
    def preferred_height(self):
        return self.__preferred_height

    @preferred_height.setter
    def preferred_height(self, preferred_height=None):
        if preferred_height is None:
            preferred_height = 0
        if type(preferred_height) != int:
            raise TypeError('"preferred_height" must be a int type or None')
        if self.preferred_height != preferred_height:
            self.__preferred_height = preferred_height

    @property
    def preferred_width(self):
        return self.__preferred_width

    @preferred_width.setter
    def preferred_width(self, preferred_width=None):
        if preferred_width is None:
            preferred_width = 0
        if type(preferred_width) != int:
            raise TypeError('"preferred_width" must be a int type or None')
        if self.preferred_width != preferred_width:
            self.__preferred_width = preferred_width

    #  Official
    @property
    def app_paintable(self):
        """
        Whether the application will paint directly on the widget.

        :return: True or False
        :rtype: bool
        """
        return self.__app_paintable

    @app_paintable.setter
    def app_paintable(self, app_paintable=False):
        """
        Set ``app_paintable`` property

        :param app_paintable:
        :type app_paintable: bool
        :raise TypeError: if ``app_paintable`` is not a bool
        """
        if not isinstance(app_paintable, bool):
            raise TypeError("'app_paintable' must be a bool type")

        if self.__app_paintable != app_paintable:
            self.__app_paintable = app_paintable

    @property
    def can_default(self):
        """
        Whether the widget can be the default widget.

        :return: True if widget can be a default widget, False otherwise
        :rtype: bool
        """
        return self.__can_default

    @can_default.setter
    def can_default(self, can_default=False):
        """
        Specifies whether widget can be a default widget.
        See Widget.grab_default() for details about the meaning of “default”.

        :param can_default: whether or not widget can be a default widget.
        :type can_default: bool
        :raise TypeError: if ``can_default`` is not a bool
        """
        if not isinstance(can_default, bool):
            raise TypeError("'can_default' must be a bool type")

        if self.__can_default != can_default:
            self.__can_default = can_default

    @property
    def can_focus(self):
        """
        Whether the widget can accept the input focus.

        :return: True or False
        :rtype: bool
        """
        return self.__can_focus

    @can_focus.setter
    def can_focus(self, can_focus=False):
        """
        Set ``can_focus`` property

        :param can_focus: True is the widget can take the default
        :type can_focus: bool
        :raise TypeError: if ``can_focus`` is not a bool
        """
        if not isinstance(can_focus, bool):
            raise TypeError("'can_default' must be a bool type")

        if self.__can_focus != can_focus:
            self.__can_focus = can_focus

    @property
    def can_prelight(self):
        """
        If True if the widget will display prelight color.

        By default that if False, by exemple a container is a hidden Widget and have no raison to display prelight.

        At the oposit the prelight of a button can be disable with it property

        :return: True or False
        :rtype: bool
        """
        return self.__can_prelight

    @can_prelight.setter
    def can_prelight(self, can_prelight=False):
        """
        Set ``can_prelight`` property

        :param can_prelight: True if the widget will display prelight color
        :type can_prelight: bool
        :raise TypeError: if ``can_prelight`` is not a bool
        """
        if not isinstance(can_prelight, bool):
            raise TypeError("'can_prelight' must be a bool type")

        if self.__can_prelight != can_prelight:
            self.__can_prelight = can_prelight

    @property
    def composite_child(self):
        """
        Whether the widget is part of a composite widget.

        :return: True or False
        :rtype: bool
        """
        return self.__composite_child

    @composite_child.setter
    def composite_child(self, composite_child=False):
        """
        Set ``composite_child`` property

        :param composite_child: True is the widget can take the default
        :type composite_child: bool
        :raise TypeError: if ``composite_child`` is not a bool
        """
        if not isinstance(composite_child, bool):
            raise TypeError("'composite_child' must be a bool type")

        if self.__composite_child != composite_child:
            self.__composite_child = composite_child

    @property
    def expand(self):
        """
        Whether to expand in both directions. Setting this sets both “hexpand” and “vexpand”

        :return: True or False
        :rtype: bool
        """
        return self.__expand

    @expand.setter
    def expand(self, expand=False):
        """
        Set ``expand`` property

        :param expand: True is the widget can take the default
        :type expand: bool
        :raise TypeError: if ``expand`` is not a bool
        """
        if not isinstance(expand, bool):
            raise TypeError("'expand' must be a bool type")

        if self.__expand != expand:
            self.__expand = expand

    @property
    def focus_on_click(self):
        """
        Whether the widget should grab focus when it is clicked with the mouse.

        This property is only relevant for widgets that can take focus.

        :return: True or False
        :rtype: bool
        """
        return self.__focus_on_click

    @focus_on_click.setter
    def focus_on_click(self, focus_on_click=False):
        """
        Set ``focus_on_click`` property

        :param focus_on_click: True is the widget can take the default
        :type focus_on_click: bool
        :raise TypeError: if ``focus_on_click`` is not a bool type
        """
        if not isinstance(focus_on_click, bool):
            raise TypeError("'focus_on_click' must be a bool type")

        if self.__focus_on_click != focus_on_click:
            self.__focus_on_click = focus_on_click

    @property
    def halign(self):
        """
        How to distribute horizontal space if widget gets extra space, see GLXC.Align

        Allowed value:
         Stretch to fill all space if possible, center if no meaningful way to stretch
          GLXC.ALIGN_FILL = 'FILL'
         Snap to left or top side, leaving space on right or bottom
          GLXC.ALIGN_START = 'START'
         Snap to right or bottom side, leaving space on left or top
          GLXC.ALIGN_END = 'END'
         Center natural width of widget inside the allocation
          GLXC.ALIGN_CENTER = 'CENTER'
         Align the widget according to the baseline.
          GLXC.ALIGN_BASELINE = 'BASELINE'

        :return: a GLXC.Align
        :rtype: str
        """
        return self.__halign

    @halign.setter
    def halign(self, halign=GLXCurses.GLXC.ALIGN_FILL):
        """
        Set the ``halign`` property

        :param halign: a GLXC.Align
        :type halign: str
        :raise TypeError: if ``halign`` value is not allowed by GLXC.Align
        """
        # Look if we back to default value
        if halign is None:
            if self.__halign is not GLXCurses.GLXC.ALIGN_FILL:
                self.__halign = GLXCurses.GLXC.ALIGN_FILL
            return

        if halign not in GLXCurses.GLXC.Align:
            raise TypeError("'halign' must be a GLXC.Align")

        # Make the job only if needed
        if halign != self.__halign:
            self.__halign = halign

    @property
    def has_default(self):
        """
        Whether the widget is the default widget.

        :return: True or False
        :rtype: bool
        """
        return self.flags['HAS_DEFAULT']

    @has_default.setter
    def has_default(self, has_default=None):
        """
        Set ``has_default`` property

        :param has_default: True is the widget can is the default widget
        :type has_default: bool
        :raise TypeError: if ``has_default`` is not a bool
        """
        if has_default is None:
            has_default = False
        if not isinstance(has_default, bool):
            raise TypeError("'has_default' must be a bool type or None")

        if self.has_default != has_default:
            self.flags['HAS_DEFAULT'] = has_default

    @property
    def has_focus(self):
        """
        Whether the widget has the input focus.

        :return: True or False
        :rtype: bool
        """
        return self.flags['HAS_FOCUS']

    @has_focus.setter
    def has_focus(self, has_focus=None):
        """
        Set ``has_focus`` property

        :param has_focus: True is the widget has focus
        :type has_focus: bool
        :raise TypeError: if ``has_focus`` is not a bool
        """
        if has_focus is None:
            has_focus = False
        if not isinstance(has_focus, bool):
            raise TypeError("'has_focus' must be a bool type")
        if self.flags['HAS_FOCUS'] != has_focus:
            self.flags['HAS_FOCUS'] = has_focus

    @property
    def has_prelight(self):
        """
        Whether the widget is pre light.

        :return: True or False
        :rtype: bool
        """
        return self.__has_prelight

    @has_prelight.setter
    def has_prelight(self, has_prelight=None):
        """
        Set ``has_focus`` property

        :param has_prelight: True is the widget has focus
        :type has_prelight: bool
        :raise TypeError: if ``has_focus`` is not a bool
        """
        if has_prelight is None:
            has_prelight = False
        if not isinstance(has_prelight, bool):
            raise TypeError("'has_prelight' must be a bool type")
        if self.has_prelight != has_prelight:
            self.__has_prelight = has_prelight

    @property
    def has_tooltip(self):
        """
        Enables or disables the emission of “query-tooltip” on widget .
        A value of ``True`` indicates that widget can have a tooltip, in this case the widget will be queried
        using “query-tooltip” to determine whether it will provide a tooltip or not.

        :return: True or False
        :rtype: bool
        """
        return self.__has_tooltip

    @has_tooltip.setter
    def has_tooltip(self, has_tooltip=False):
        """
        Set ``has_tooltip`` property

        :param has_tooltip: True if the widget emit of “query-tooltip”
        :type has_tooltip: bool
        :raise TypeError: if ``has_tooltip`` is not a bool
        """
        if not isinstance(has_tooltip, bool):
            raise TypeError("'has_tooltip' must be a bool type")

        if self.__has_tooltip != has_tooltip:
            self.__has_tooltip = has_tooltip

    @property
    def height_request(self):
        """
        Override for height request of the widget, or -1 if natural request should be used.

        :return: height_request property value
        :rtype: int
        """
        return self.__height_request

    @height_request.setter
    def height_request(self, height_request):
        """
        Set the ``height_request`` property

        :param height_request:  Allowed values >= -1
        :type height_request: int
        """
        if not isinstance(height_request, int):
            raise TypeError("'height_request' must be a int")
        if not height_request >= -1:
            raise TypeError("'height_request' must be a int >= -1")

        if self.__height_request != height_request:
            self.__height_request = height_request

    @property
    def hexpand(self):
        """
        Whether to expand horizontally.

        :return: True if the widget have to expand horizontally
        :rtype: bool
        """
        return self.__hexpand

    @hexpand.setter
    def hexpand(self, hexpand=False):
        """
        Set ``hexpand`` property

        Note: None assign the default value False

        :param hexpand:  If True the widget will expand it self horizontally
        :type hexpand: bool
        :raise TypeError: if ``hexpand`` is not a bool or None
        """
        # Look if we back to default value
        if hexpand is None:
            if self.__hexpand is not False:
                self.__hexpand = False
            return
        # Exit as soon of possible
        if not isinstance(hexpand, bool):
            raise TypeError("'hexpand' must be a bool type")
        # Make the job if needed
        if self.__hexpand != hexpand:
            self.__hexpand = hexpand

    @property
    def hexpand_set(self):
        """
        Whether to use the “hexpand” property

        :return: True if the widget use the “hexpand” property
        :rtype: bool
        """
        return self.__hexpand_set

    @hexpand_set.setter
    def hexpand_set(self, hexpand_set=False):
        """
        Set ``hexpand_set`` property

        :param hexpand_set:  If True the widget use the ``hexpand`` property
        :type hexpand_set: bool
        :raise TypeError: if ``hexpand_set`` is not a bool or None
        """
        # Look if we back to default value
        if hexpand_set is None:
            if self.__hexpand_set is not False:
                self.__hexpand_set = False
            return
        # Exit as soon of possible
        if not isinstance(hexpand_set, bool):
            raise TypeError("'hexpand_set' must be a bool type")
        # Make the job only if need
        if self.__hexpand_set != hexpand_set:
            self.__hexpand_set = hexpand_set

    @property
    def is_focus(self):
        """
        Whether the widget is the focus widget within the toplevel.

        :return: True if the widget is the focus widget within the toplevel.
        :rtype: bool
        """
        return self.__is_focus

    @is_focus.setter
    def is_focus(self, is_focus=False):
        """
        Set ``is_focus`` property

        :param is_focus:  If True the widget is the focus widget within the toplevel.
        :type is_focus: bool
        :raise TypeError: if ``is_focus`` is not a bool
        """
        if not isinstance(is_focus, bool):
            raise TypeError("'is_focus' must be a bool type")

        if self.__is_focus != is_focus:
            self.__is_focus = is_focus

    @property
    def margin(self):
        """
        All four sides' margin at once. If read, returns max margin on any side.

        Allowed values: [0,32767]

        :return: max margin on any side
        :rtype: int
        """
        return self.__margin

    @margin.setter
    def margin(self, margin):
        """
        Set ``margin`` property

        :param margin: int contain in range [0,32767]
        :type margin: int
        """
        if not isinstance(margin, int):
            raise TypeError("'margin' must be a int type")
        if not 0 <= margin <= 32767:
            raise TypeError("'margin' must be contain in range [0,32767]")

        if self.__margin != margin:
            self.__margin = margin

    @property
    def margin_bottom(self):
        """
        This property adds margin outside of the widget's normal size request, the margin will be added in addition
        to the size from Widget.set_size_request() for example.

        Allowed values: [0,32767]

        :return: Margin on bottom side of widget.
        :rtype: int
        """
        return self.__margin_bottom

    @margin_bottom.setter
    def margin_bottom(self, margin_bottom=0):
        """
        Set ``margin_bottom`` property

        :param margin_bottom: int contain in range [0,32767]
        :type margin_bottom: int
        """
        if not isinstance(margin_bottom, int):
            raise TypeError("'margin_bottom' must be a int type")
        if not 0 <= margin_bottom <= 32767:
            raise TypeError("'margin_bottom' must be contain in range [0,32767]")

        if self.__margin_bottom != margin_bottom:
            self.__margin_bottom = margin_bottom

    @property
    def margin_end(self):
        """
        Margin on end of widget, horizontally. This property supports left-to-right and right-to-left text directions.

        This property adds margin outside of the widget's normal size request, the margin will be added in addition
        to the size from Widget.set_size_request() for example.

        Allowed values: [0,32767]

        :return: Margin on end of widget, horizontally.
        :rtype: int
        """
        return self.__margin_end

    @margin_end.setter
    def margin_end(self, margin_end=0):
        """
        Set ``margin_end`` property

        :param margin_end: int contain in range [0,32767]
        :type margin_end: int
        """
        if not isinstance(margin_end, int):
            raise TypeError("'margin_end' must be a int type")
        if not 0 <= margin_end <= 32767:
            raise TypeError("'margin_end' must be contain in range [0,32767]")

        if self.__margin_end != margin_end:
            self.__margin_end = margin_end

    @property
    def margin_start(self):
        """
        Margin on start of widget, horizontally.
        This property supports left-to-right and right-to-left text directions.

        This property adds margin outside of the widget's normal size request, the margin will be added in addition
        to the size from Widget.set_size_request() for example.

        Allowed values: [0,32767]

        :return: Margin on start of widget, horizontally.
        :rtype: int
        """
        return self.__margin_start

    @margin_start.setter
    def margin_start(self, margin_start=0):
        """
        Set ``margin_start`` property

        :param margin_start: int contain in range [0,32767]
        :type margin_start: int
        """
        if not isinstance(margin_start, int):
            raise TypeError("'margin_start' must be a int type")
        if not 0 <= margin_start <= 32767:
            raise TypeError("'margin_start' must be contain in range [0,32767]")

        if self.__margin_start != margin_start:
            self.__margin_start = margin_start

    @property
    def margin_top(self):
        """
        Margin on top side of widget.

        This property adds margin outside of the widget's normal size request, the margin will be added in addition
        to the size from Widget.set_size_request() for example.

        Allowed values: [0,32767]

        :return: Margin on top side of widget.
        :rtype: int
        """
        return self.__margin_top

    @margin_top.setter
    def margin_top(self, margin_top=0):
        """
        Set ``margin_top`` property

        :param margin_top: int contain in range [0,32767]
        :type margin_top: int
        """
        if not isinstance(margin_top, int):
            raise TypeError("'margin_top' must be a int type")
        if not 0 <= margin_top <= 32767:
            raise TypeError("'margin_top' must be contain in range [0,32767]")

        if self.__margin_top != margin_top:
            self.__margin_top = margin_top

    @property
    def name(self):
        """
        The name of the widget.

        :return: name of the widget.
        :rtype: str
        """
        return self.__name

    @name.setter
    def name(self, name=None):
        """
        Set ``name`` property

        :param name: The name of the widget.
        :type name: str
        """
        if name is None:
            if self.__name is not None:
                self.__name = None
            return

        if not isinstance(name, str):
            raise TypeError("'name' must be a str type")

        if self.__name != name:
            self.__name = name

    @property
    def no_show_all(self):
        """
        Whether Widget.show_all() should not affect this widget.

        :return: If True, Widget.show_all() should not affect this widget
        :rtype: bool
        """
        return self.__no_show_all

    @no_show_all.setter
    def no_show_all(self, no_show_all=False):
        """
        Set ``no_show_all`` property

        :param no_show_all:  If True, Widget.show_all() should not affect this widget
        :type no_show_all: bool
        :raise TypeError: if ``no_show_all`` is not a bool
        """
        if not isinstance(no_show_all, bool):
            raise TypeError("'no_show_all' must be a bool type")

        if self.__no_show_all != no_show_all:
            self.__no_show_all = no_show_all

    @property
    def parent(self):
        """
        The parent widget of this widget. Must be a Container widget.

        :return: The parent of the widget
        :rtype: Container
        """
        return self.__parent

    @parent.setter
    def parent(self, parent=None):
        """
        The parent widget of this widget. Must be a Container widget.

        Note: Application is accept as container parent.

        :param parent: The parent of this widget or None if haven't
        :type parent: Container or None
        :raise TypeError: if parent is not a Container or None
        """
        if parent is None:
            if self.__parent is not None:
                self.__parent = None
            return

        if not isinstance(parent, GLXCurses.Container) and not isinstance(parent, GLXCurses.Application):
            raise TypeError("'parent' must be a GLXCurses.Container type")

        if self.__parent != parent:
            self.__parent = parent

        # self.stdscr = GLXCurses.application.stdscr

        # self.parent.adopt(self)

        # Widget start with own Style, and will use the Style of it parent when it add to a contener
        # GLXCApplication Widget is a special case where it parent is it self.
        self.style_backup = self.style
        self.style = GLXCurses.Application().style

    @property
    def receives_default(self):
        """
        If True, the widget will receive the default action when it is focused.

        :return: True if the widget receives default
        :rtype: bool
        """
        return self.__receives_default

    @receives_default.setter
    def receives_default(self, receives_default=False):
        """
        Set the ``receives_default`` property

        :param receives_default: If TRUE, the widget will receive the default action when it is focused.
        :type receives_default: bool
        :raise TypeError: If receives_default is not bool type
        """
        if not isinstance(receives_default, bool):
            raise TypeError("'receives_default' must be a bool type")

        if self.__receives_default != receives_default:
            self.__receives_default = receives_default

    @property
    def sensitive(self):
        """
        Whether the widget responds to input.

        :return: True if teh widget responds to input
        :rtype: bool
        """
        return self.state['INSENSITIVE']

    @sensitive.setter
    def sensitive(self, sensitive=None):
        """
        Set the ``sensitive`` property

        :param sensitive: True if the widget is responds to input
        :type sensitive: bool
        :raise TypeError: If sensitive parameter is not bool type
        """
        if sensitive is None:
            sensitive = True
        if not isinstance(sensitive, bool):
            raise TypeError("'sensitive' parameter must be a bool type")

        if self.state['INSENSITIVE'] != sensitive:
            self.state['INSENSITIVE'] = sensitive
        if not self.sensitive:
            self.is_focus = False

    @property
    def style(self):
        """
        The style of the widget, which contains information about how it will look (colors, etc).

        :return: a GLXCurses.Style instance
        :rtype: Style
        """
        return self.__style

    @style.setter
    def style(self, style):
        """
        Set the ``style`` property.


        :param style: a GLXCurses.Style instance
        :type style: Style
        """
        if style is None:
            style = GLXCurses.Style()
        if not isinstance(style, GLXCurses.Style):
            raise TypeError('"style" must be a GLXCurses.Style instance or None')
        if self.style != style:
            self.__style = style

    @property
    def tooltip_text(self):
        """
        This is a convenience property which will take care of getting the tooltip shown if the given string is not
        NULL: ``has-tooltip`` will automatically be set to TRUE and there will be taken care of “query-tooltip” in the
        default signal handler.

        :return: tooltip_text property value
        :rtype: str or None
        """
        return self.__tooltip_text

    @tooltip_text.setter
    def tooltip_text(self, tooltip_text):
        """
        Sets the text of tooltip to be the given string.

        :param tooltip_text: tooltip_text value
        :type: str or None
        """
        if tooltip_text is None:
            if self.__tooltip_text is not None:
                self.__tooltip_text = None
                if self.__tooltip_text is not False:
                    self.has_tooltip = False
            return

        if not isinstance(tooltip_text, str):
            raise TypeError("'tooltip_text' parameter must be a str type")

        if self.__tooltip_text != tooltip_text:
            self.__tooltip_text = tooltip_text
            if not self.__has_tooltip:
                self.has_tooltip = True

    @property
    def valign(self):
        """
        How to distribute vertical space if widget gets extra space, see GLXC.Align

        Default value: GLXC.ALIGN_FILL

        :return: The “valign” property
        :rtype: GLXC.Align
        """
        return self.__valign

    @valign.setter
    def valign(self, valign=GLXCurses.GLXC.ALIGN_FILL):
        """
        Set the valign property

        :param valign: The ``valign`` property
        :type: GLXC.Align
        """
        # Look if we back to default value
        if valign is None:
            if self.__valign is not GLXCurses.GLXC.ALIGN_FILL:
                self.__valign = GLXCurses.GLXC.ALIGN_FILL
            return
        # Exit as soon of possible
        if valign not in GLXCurses.GLXC.Align:
            raise TypeError("'valign' must be a GLXC.Align")

        # Make the job only if needed
        if valign != self.__valign:
            self.__valign = valign

    @property
    def vexpand(self):
        """
        Whether to expand vertically. See Widget().set_vexpand().

        :return: True if teh widget have to expand vertically
        :rtype: bool
        """
        return self.__vexpand

    @vexpand.setter
    def vexpand(self, vexpand=False):
        """
        Set ``vexpand`` property

        :param vexpand:  If True the widget will expand it self vertically
        :type vexpand: bool
        :raise TypeError: if ``vexpand`` is not a bool or None
        """
        # Look if we back to default value
        if vexpand is None:
            if self.__vexpand is not False:
                self.__vexpand = False
            return
        # Exit as soon of possible
        if not isinstance(vexpand, bool):
            raise TypeError("'vexpand' must be a bool type")
        # Make the job if needed
        if self.__vexpand != vexpand:
            self.__vexpand = vexpand

    @property
    def vexpand_set(self):
        """
        Whether to use the “vexpand” property

        :return: True if the widget use the “vexpand” property
        :rtype: bool
        """
        return self.__vexpand_set

    @vexpand_set.setter
    def vexpand_set(self, vexpand_set=False):
        """
        Set ``vexpand_set`` property

        :param vexpand_set:  If True the widget use the “vexpand” property
        :type vexpand_set: bool
        :raise TypeError: if ``vexpand_set`` is not a bool
        """
        # Look if we back to default value
        if vexpand_set is None:
            if self.__vexpand_set is not False:
                self.__vexpand_set = False
            return
        # Exit as soon of possible
        if not isinstance(vexpand_set, bool):
            raise TypeError("'vexpand_set' must be a bool type")
        # Make the job if needed
        if self.__vexpand_set != vexpand_set:
            self.__vexpand_set = vexpand_set

    @property
    def visible(self):
        """
        Whether the widget is visible.

        Default value: False

        :return: True if the widget is visible.
        :rtype: bool
        """
        return self.flags['VISIBLE']

    @visible.setter
    def visible(self, visible=False):
        """
        Set the ``visible`` property

        None will set False default value

        :param visible: True if the widget is visible.
        :type visible: bool or None
        """
        if visible is None:
            if self.visible is not False:
                self.flags['VISIBLE'] = False
            return

        if not isinstance(visible, bool):
            raise TypeError("'visible' must be a bool type or None")

        if self.visible != visible:
            self.flags['VISIBLE'] = visible

    @property
    def width_request(self):
        """
        Override for width request of the widget, or -1 if natural request should be used.

        :return: width_request property value
        :rtype: int
        """
        return self.__width_request

    @width_request.setter
    def width_request(self, width_request):
        """
        Set the ``width_request`` property

        :param width_request:  Allowed values >= -1
        :type width_request: int
        """
        if not isinstance(width_request, int):
            raise TypeError("'width_request' must be a int")
        if not width_request >= -1:
            raise TypeError("'width_request' must be a int >= -1")

        if self.__width_request != width_request:
            self.__width_request = width_request

    @property
    def window(self):
        """
        The widget's window if it is realized, ``None`` otherwise.

        :return: return the Window object if realized, None otherwise
        :rtype: GLXCurses.Window or None
        """
        return self.__window

    # Common Widget mandatory
    def new(self):
        """
        Not totally like GTK yet ...

        Actually:
         The Widget.New() "can be" and "is" overridden by each GLXCurses Components.

        Original GTK:
         This is a convenience function for creating a widget and setting its properties in one go.
         For example you might write:
         Widget().New(GLXC.TYPE_LABEL, "label", "Hello World", "xalign", 0.0, NULL)
         to create a left-aligned label.

        :return: the Widget
        :rtype: Widget
        """
        self.__init__()
        return self

    #         """
    #         Destroys a widget.
    #
    #         When a widget is destroyed all references it holds on other objects will be released:
    #          if the widget is inside a container, it will be removed from its parent
    #          if the widget is a container, all its children will be destroyed, recursively
    #          if the widget is a top level, it will be removed from the list of top level widgets that GLXCurses \
    #          maintains internally
    #
    #         It's expected that all references held on the widget will also be released;
    #         you should connect to the “destroy” signal if you hold a reference to widget and you wish to remove it when
    #         this function is called. It is not necessary to do so if you are implementing a GLXCurses.Container,
    #         as you'll be able to use the GLXCurses.Container.remove() virtual function for that.
    #
    #         It's important to notice that GLXCurses.Widget.destroy() will only cause the widget to be finalized if no
    #         additional references, acquired using Object_ref(), are held on it. In case additional references are in
    #         place, the widget will be in an "inert" state after calling this function; widget will still point to valid
    #         memory, allowing you to release the references you hold, but you may not query the widget's own state.
    #
    #         You should typically call this function on top level widgets, and rarely on child widgets.
    #
    #         :param widget: a GLXCurses.Widget
    #         :type widget: Widget
    #         :raise TypeError: if ``widget`` is not a valid GLXCurses type.
    #         :raise TypeError: if ``widget`` is not a instance of GLXCurses.Widget.
    #         """
    def destroy(self):
        if self.parent:
            self.unparent()
        if not self.in_destruction:
            self.in_destruction = True

    @property
    def in_destruction(self):
        """
        Returns whether the widget is currently being destroyed.

        This information can sometimes be used to avoid doing unnecessary work.

        :return: True if widget is being destroyed
        :rtype: bool
        """
        return self.flags['IN_DESTRUCTION']

    @in_destruction.setter
    def in_destruction(self, in_destruction=None):
        if in_destruction is None:
            in_destruction = False
        if type(in_destruction) != bool:
            raise TypeError('"in_destruction" must be a bool type or None')
        if self.in_destruction != in_destruction:
            self.flags['IN_DESTRUCTION'] = in_destruction

    #         """
    #         This function sets *widget_pointer to None if widget_pointer != None.
    #
    #         It’s intended to be used as a callback connected to the “destroy” signal of a widget.
    #         You connect GLXCurses.Widget.destroyed() as a signal handler, and pass the address of your widget
    #         variable as user __area_data.
    #         Then when the widget is destroyed, the variable will be set to None.
    #
    #         Useful for example to avoid multiple copies of the same dialog.
    #
    #         :param widget: a GLXCurses.Widget
    #         :type widget: Widget
    #         :param widget_pointer: address of a variable that contains widget .
    #         :type widget_pointer: Widget
    #         :raise TypeError: if ``widget`` is not a valid GLXCurses type.
    #         :raise TypeError: if ``widget`` is not a instance of GLXCurses.Widget.
    #         :raise TypeError: if ``widget_pointer`` is not a valid GLXCurses type.
    #         :raise TypeError: if ``widget_pointer`` is not a instance of GLXCurses.Widget.
    #         """
    def destroyed(self, widget=None, widget_pointer=None):
        # self be come the widget if it haven't one
        if widget is None:
            widget = self

        # Try to exit as soon of possible
        if not GLXCurses.glxc_type(widget):
            raise TypeError("'widget' must be a GLXCurses type")
        if not isinstance(widget, Widget):
            raise TypeError("'widget' must be an instance of GLXCurses.Widget")
        if not GLXCurses.glxc_type(widget_pointer):
            raise TypeError("'widget_pointer' must be a GLXCurses type")
        if not isinstance(widget_pointer, Widget):
            raise TypeError("'widget_pointer' must be an instance of GLXCurses.Widget")

        # Make the job
        delattr(widget_pointer, 'glxc_type')

    def unparent(self, widget=None):
        """
        This function is only for use in widget implementations.
        Should be called by implementations of the remove method on Container,
        to dissociate a child from the container.

        :param widget: a GLXCurses.Widget
        :type widget: Widget
        :raise TypeError: if ``widget`` is not a valid GLXCurses type.
        :raise TypeError: if ``widget`` is not a instance of GLXCurses.Widget.
        """
        # self be come the widget if it haven't one
        if widget is None:
            widget = self

        # Try to exit as soon of possible
        if not GLXCurses.glxc_type(widget):
            raise TypeError("'widget' must be a GLXCurses type")
        if not isinstance(widget, Widget):
            raise TypeError("'widget' must be an instance of GLXCurses.Widget")

        # Make the job
        if widget.parent is not None:
            if hasattr(widget.parent, 'get_children'):
                if bool(widget.parent.children):
                    count = 0
                    last_found = None
                    for children in widget.parent.children:
                        if widget == children.widget:
                            last_found = count
                        count += 1
                    if last_found is not None:
                        widget.parent.children.pop(last_found)

            if hasattr(widget.parent, 'get_child'):
                if bool(widget.parent.child()):
                    if widget.parent.child().widget == widget:
                        widget.parent.set_child(None)

        widget.parent = None
        widget.style = widget.style_backup

    def show(self):
        """
        Flags a widget to be displayed. Any widget that isn’t shown will not appear on the stdscr.

        If you want to show all the widgets in a container, it’s easier to call GLXCurses.Widget.show_all()
        on the container, instead of individually showing the widgets.

        Remember that you have to show the containers containing a widget, in addition to the widget itself,
        before it will appear onscreen.

        When a toplevel container is shown, it is immediately realized and mapped; other shown widgets are realized
        and mapped when their toplevel container is realized and mapped.

        """
        if self.flags['TOPLEVEL']:
            if not self.flags['REALIZED']:
                self.flags['REALIZED'] = True
            if not self.flags['MAPPED']:
                self.flags['MAPPED'] = True

        if not self.visible:
            self.visible = True

    def show_now(self):
        """
        Shows a widget.

        If the widget is an unmapped toplevel widget (i.e. a GLXCurses.Window that has not yet been shown),
        enter the main loop and wait for the window to actually be mapped.

        Be careful; because the main loop is running, anything can happen during this function.
        """
        if not self.flags['REALIZED']:
            self.flags['REALIZED'] = True
        if not self.flags['MAPPED']:
            self.flags['MAPPED'] = True
        if not self.visible:
            self.visible = True

    def hide(self):
        """
        Reverses the effects of GLXCurses.Widget.show(), causing the widget to be hidden (invisible to the user).

        """

        if self.flags['TOPLEVEL']:
            if self.flags['REALIZED']:
                self.flags['REALIZED'] = False
            if self.map:
                self.map = False

        if self.visible:
            self.visible = False

    def show_all(self):
        """
        Recursively shows a widget, and any child widgets (if the widget is a container).
        """
        # make the widget it self firt
        self.show()

        # then make it recursively
        if self.__class__.__name__ in GLXCurses.GLXC.CHILDREN_CONTAINER:
            # that is a container

            if hasattr(self, 'children'):
                # that is  multi children
                if bool(self.children):
                    for child in self.children:
                        child.widget.show()

            else:
                if hasattr(self, 'child'):
                    self.child.widget.show()

    @property
    def map(self):
        """
        This function is only for use in widget implementations.
        Causes a widget to be mapped if it isn’t already.

        """
        return self.flags['MAPPED']

    @map.setter
    def map(self, value=None):
        if value is None:
            value = False
        if type(value) != bool:
            raise TypeError('"map value" must be a bool type or None')
        if self.map != value:
            self.flags['MAPPED'] = value

    @property
    def realize(self):
        """
        Creates the GLXCurses (windowing system) resources associated with a widget.
        For example, widget->window will be created when a widget is realized.
        Normally realization happens implicitly; if you show a widget and all its parent containers,
        then the widget will be realized and mapped automatically.

        Realizing a widget requires all the widget’s parent widgets to be realized;
        calling Widget.realize() realizes the widget’s parents in addition to widget itself.
        If a widget is not yet inside a toplevel window when you realize it, bad things will happen.

        This function is primarily used in widget implementations, and isn’t very useful otherwise.
        Many times when you think you might need it, a better approach is to connect to a signal that will be called
        after the widget is realized automatically, such as “draw”.
        Or simply g_signal_connect() to the “realize” signal.

        :return: the ``realize`` property value
        :rtype: bool
        """
        return self.flags['REALIZED']

    @realize.setter
    def realize(self, value=None):
        """
        This function is only useful in widget implementations.

        (frees all GLXCurses resources associated with the widget, such as widget->window ).

        :param value: False Causes a widget to be unrealized
        :type value: bool or None
        :raise TypeError: if ``value`` is not a bool type or None.
        """
        if value is None:
            value = False
        if type(value) != bool:
            raise TypeError('"realize value" must be bool type or None')
        if self.realize != value:
            self.flags['REALIZED'] = value

    # The set_child_visible() method determines if the widget should be mapped along with its parent.
    # If is_visible is True the widget will be mapped with its parent if it has called the show() method.
    @property
    def child_visible(self):
        """
        he set_child_visible() method determines if the widget should be mapped along with its parent.

        :return:
        """
        return self.visible

    @child_visible.setter
    def child_visible(self, is_visible):
        self.visible = bool(is_visible)

    def get_toplevel(self):
        return self.flags['TOPLEVEL']

    def set_decorated(self, decorated):
        self.widget_decorated = decorated

    def get_decorated(self):
        return self.widget_decorated

    def refresh(self):
        self.draw()

    # Name management use for GLXCStyle color's
    def override_color(self, color):
        self.style.attribute_states['text']['STATE_NORMAL'] = str(color).upper()

    def override_background_color(self, color):
        self.style.attribute_states['bg']['STATE_NORMAL'] = str(color).upper()

    # State
    # Sets the sensitivity of a curses_subwin.
    # A curses_subwin is sensitive if the user can interact with it. Insensitive widgets are “grayed out”
    # and the user can’t interact with them.

    @property
    def attribute_states(self):
        """
        Return the ``__attribute_states`` attribute, it consist to a dictionary it store a second level of dictionary \
        with keys if have special name.

        :return: attribute states dictionary on Galaxie Curses Style format
        :rtype: dict
        """
        return self.__attribute_states

    @attribute_states.setter
    def attribute_states(self, attribute_states):
        """
        Set the ``__attribute_states`` attribute, it consist to a dictionary it store a second level of dictionary \
        with keys if have special name.

        see: get_default_attribute_states() for generate a default Style.

        :param attribute_states: a Dictionary with Galaxie Curses Style format
        :type attribute_states: dict(dict(str()))
        """
        # Try to found a way to not be execute
        # Check first level dictionary
        if type(attribute_states) != dict:
            raise TypeError('"__attribute_states" is not a dictionary')

        # For each key's
        for attribute in ['text_fg', 'bg', 'light', 'dark', 'mid', 'text', 'base', 'black', 'white']:
            # Check if the key value is a dictionary
            try:
                if type(attribute_states[attribute]) != dict:
                    raise TypeError('"attribute_states" key is not a dict')
            except KeyError:
                raise KeyError('"attribute_states" is not a Galaxie Curses Style')
            # For each key value, in that case a sub dictionary
            for state in ['STATE_NORMAL', 'STATE_ACTIVE', 'STATE_PRELIGHT', 'STATE_SELECTED', 'STATE_INSENSITIVE']:
                # Check if the key value is a string
                try:
                    if type(attribute_states[attribute][state]) != str:
                        raise TypeError('"__attribute_states" key is not a str')
                except KeyError:
                    raise KeyError('"__attribute_states" is not a Galaxie Curses Style')

        # If it haven't quit that ok
        if attribute_states != self.attribute_states:
            self.__attribute_states = attribute_states

    @property
    def has_window(self):
        """
        Determines whether widget has a GdkWindow of its own.

        See GLXCurses.Widget.set_has_window().

        :return: TRUE if widget has a window, FALSE otherwise
        :rtype: bool
        """
        return self.flags['NO_WINDOW']

    @has_window.setter
    def has_window(self, has_window=None):
        """
        Specifies whether widget has a GdkWindow of its own.
        Note that all realized widgets have a non-NULL “window” pointer (gtk_widget_get_window()
        never returns a NULL window when a widget is realized), but for many of them it’s actually
        the GdkWindow of one of its parent widgets. Widgets that do not create a window for themselves
        in “realize” must announce this by calling this function with has_window = FALSE.

        This function should only be called by widget implementations, and they should
        call it in their init() function.

        :param has_window: bool
        :type has_window: bool or None
        :raise TypeError: When has_window is not bool type or None
        """
        if has_window is None:
            has_window = True
        if type(has_window) != bool:
            raise TypeError('"has_window" must be a bool type or None')
        if self.flags['NO_WINDOW'] != has_window:
            self.flags['NO_WINDOW'] = has_window

    # DRAW
    def draw(self):

        self.draw_widget_in_area()

    def draw_widget_in_area(self):
        """
        Be here for be overwrite by every widget
        """
        pass

    def _draw_box(self):
        # Create a box and add the name of the windows like a king, who trust that !!!
        if self.subwin:
            self._draw_box_upper_left_corner()
            self._draw_box_top()
            self._draw_box_upper_right_corner()

            self._draw_box_left_side()
            self._draw_box_right_side()

            self._draw_box_bottom_left_corner()
            self._draw_box_bottom()
            self._draw_box_bottom_right_corner()

            # For future usage
            # self._draw_box_left_side(char='.')
            # self._draw_box_top(char='.')
            # self._draw_box_bottom(char='.')
            # self._draw_box_right_side(char='.')
            #
            # self._draw_box_upper_left_corner(char='.')
            # self._draw_box_upper_right_corner(char='.')
            # self._draw_box_bottom_left_corner(char='.')
            # self._draw_box_bottom_right_corner(char='.')

    def _draw_box_bottom(self, char=None):
        # Bottom
        if char is None:
            char = curses.ACS_HLINE
        try:
            for x_inc in range(0 + 1, self.width - 1):
                self.subwin.delch(self.height - 1, x_inc)
                self.subwin.insch(
                    self.height - 1,
                    x_inc,
                    char,
                    self.style.color(
                        fg=self.style.get_color_text('base', 'STATE_NORMAL'),
                        bg=self.style.get_color_text('bg', 'STATE_NORMAL')
                    )
                )

        except curses_error:
            pass

    def _draw_box_top(self, char=None):
        # Top
        if char is None:
            char = curses.ACS_HLINE

        for x_inc in range(0 + 1, self.width - 1):
            try:
                self.subwin.delch(0, x_inc)
                self.subwin.insch(
                    0,
                    x_inc,
                    char,
                    self.style.color(
                        fg=self.style.get_color_text('base', 'STATE_NORMAL'),
                        bg=self.style.get_color_text('bg', 'STATE_NORMAL')
                    )
                )
            except curses_error:
                pass

    def _draw_box_right_side(self, char=None):
        # Right side
        if char is None:
            char = curses.ACS_VLINE

        for y_inc in range(0 + 1, self.height):

            try:
                self.subwin.delch(y_inc, self.width - 1)
                self.subwin.insch(
                    y_inc,
                    self.width - 1,
                    char,
                    self.style.color(
                        fg=self.style.get_color_text('base', 'STATE_NORMAL'),
                        bg=self.style.get_color_text('bg', 'STATE_NORMAL')
                    )
                )
            except curses_error:
                pass

    def _draw_box_left_side(self, char=None):
        # Left side
        if char is None:
            char = curses.ACS_VLINE

        for y_inc in range(0 + 1, self.height):
            try:
                self.subwin.delch(y_inc, 0)
                self.subwin.insch(
                    y_inc,
                    0,
                    char,
                    self.style.color(
                        fg=self.style.get_color_text('base', 'STATE_NORMAL'),
                        bg=self.style.get_color_text('bg', 'STATE_NORMAL')
                    )
                )
            except curses_error:
                pass

            # self.subwin.vline(
            #     self.get_y() + 1,
            #     self.get_x(),
            #     char,
            #     self.height - 1,
            #     self.style.get_color_pair(
            #         foreground=self.style.get_color_text('base', 'STATE_NORMAL'),
            #         background=self.style.get_color_text('bg', 'STATE_NORMAL')
            #     )
            # )

    def _draw_box_upper_right_corner(self, char=None):
        # Upper-right corner
        if char is None:
            char = curses.ACS_URCORNER
        try:
            self.subwin.delch(0, self.width - 1)
            self.subwin.insch(
                0,
                self.width - 1,
                char,
                self.style.color(
                    fg=self.style.get_color_text('text', 'STATE_NORMAL'),
                    bg=self.style.get_color_text('bg', 'STATE_NORMAL')
                )
            )
        except curses_error:
            pass

    def _draw_box_upper_left_corner(self, char=None):
        # Upper-left corner
        if char is None:
            char = curses.ACS_ULCORNER
        try:
            self.subwin.delch(0, 0)
            self.subwin.insch(
                0,
                0,
                char,
                self.style.color(
                    fg=self.style.get_color_text('text', 'STATE_NORMAL'),
                    bg=self.style.get_color_text('bg', 'STATE_NORMAL')
                )
            )
        except curses_error:
            pass

    def _draw_box_bottom_right_corner(self, char=None):
        # Bottom-right corner
        if char is None:
            char = curses.ACS_LRCORNER
        try:
            self.subwin.delch(self.height - 1, self.width - 1)
            self.subwin.insch(
                self.height - 1,
                self.width - 1,
                char,
                self.style.color(
                    fg=self.style.get_color_text('text', 'STATE_NORMAL'),
                    bg=self.style.get_color_text('bg', 'STATE_NORMAL')
                )
            )
        except curses_error:
            pass

    def _draw_box_bottom_left_corner(self, char=None):
        # Bottom-left corner
        if char is None:
            char = curses.ACS_LLCORNER
        try:
            self.subwin.delch(self.height - 1, 0)
            self.subwin.insch(
                self.height - 1,
                0,
                char,
                self.style.color(
                    fg=self.style.get_color_text('text', 'STATE_NORMAL'),
                    bg=self.style.get_color_text('bg', 'STATE_NORMAL')
                )
            )
        except curses_error:
            pass

    # Internal
    def _get_imposed_spacing(self):
        return int(self.imposed_spacing)

    def _set_imposed_spacing(self, spacing):
        if self.imposed_spacing != int(spacing):
            self.imposed_spacing = int(spacing)

    def unchild(self, widget=None):

        if widget is None:
            widget = self

        if hasattr(widget, 'get_children'):
            if bool(widget.children):
                count = 0
                last_found = None
                for child in widget.children:
                    if widget == child.widget:
                        last_found = count
                    count += 1
                if last_found is not None:
                    widget.children.pop(last_found)

        if hasattr(widget, 'get_child'):
            if bool(widget.child):
                if widget.child.widget == widget:
                    widget.child = None

