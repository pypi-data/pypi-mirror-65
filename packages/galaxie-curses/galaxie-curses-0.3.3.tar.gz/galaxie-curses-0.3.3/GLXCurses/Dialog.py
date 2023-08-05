#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import GLXCurses
import logging
import curses


class Dialog(GLXCurses.Window, GLXCurses.Movable):
    def __init__(self):
        self.__buttons_list = None
        self.__action_area = None
        self.__content_area = None
        self.__use_header_bar = None
        self.__action_area_border = None
        self.__button_spacing = None
        self.__content_area_border = None
        self.__content_area_spacing = None
        self.__sub_sub_win = None

        self._action_area = []
        self._content_area = GLXCurses.VBox()
        # Style Property
        self.action_aera_border = 0
        self.button_spacing = 6
        self.content_area_border = 2
        self.content_area_spacing = 0

        # Load heritage
        GLXCurses.Window.__init__(self)
        GLXCurses.Movable.__init__(self)

        # It's a GLXCurse Type
        self.glxc_type = 'GLXCurses.Dialog'

        # Widgets can be named, which allows you to refer to them from a GLXCStyle
        self.name = '{0}{1}'.format(self.__class__.__name__, self.id)

        # Default Setting
        self.decorated = True

        # Subscription
        self.connect('BUTTON1_CLICKED', Dialog._handle_mouse_event)  # Mouse Button
        self.connect('BUTTON1_RELEASED', Dialog._handle_mouse_event)
        # Keyboard
        self.connect('CURSES', Dialog._handle_key_event)

    def _handle_mouse_event(self, event_signal, event_args=None):
        if event_args is None:
            event_args = dict()

        logging.debug(str(event_args))
        logging.debug('i GOT')
        for button in self.get_action_area():
            button_id = self.get_widget_for_response(self.get_response_for_widget(button.widget)).id
            if event_args['id'] == button_id:
                self.emit('RESPONSE', {'id': self.get_response_for_widget(button.widget)})
                return

    def _handle_key_event(self, event_signal, *event_args):
        key = event_args[0]
        logging.debug('HANDLE KEY: ' + str(key))

        # Touch Escape
        if key == GLXCurses.GLXC.KEY_ESC:
            self.emit('RESPONSE', {'id': 42})
            self.close()

    @property
    def _content_area(self):
        """
        The content area is a GtkVBox, and is where widgets such as a GtkLabel or a GtkEntry should be packed.

        It VBox will be display on top of the Dialog window.

        :return:
        """
        return self.__content_area

    @_content_area.setter
    def _content_area(self, vbox=None):
        """
        Set the ``_content_area`` property value

        :param vbox: a GLXCurses.Vbox object
        :type vbox: VBox
        :raise TypeError: when ``vbox`` is not a VBox type
        """
        if vbox is None:
            vbox = GLXCurses.VBox()
        if type(vbox) != GLXCurses.VBox:
            raise TypeError('"vbox" must be a Vbox type')
        if self._content_area != vbox:
            self.__content_area = vbox

    @property
    def _action_area(self):
        """
        Internal property it store the Dialog buttons list

        :return: the ``_buttons_list`` property value
        :rtype: list
        """
        return self.__buttons_list

    @_action_area.setter
    def _action_area(self, value=None):
        """
        set the ``_buttons_list`` property

        :param value: a list
        :type value: list
        :raise TypeError: is ``value`` is not a list type
        """
        if value is None:
            value = []
        if type(value) != list:
            raise TypeError('"value" must be a list type')

        if self._action_area != value:
            self.__buttons_list = value

    @property
    def action_aera_border(self):
        """
        The default border width used around the action area of the dialog, as returned by Dialog.get_action_area(),
        unless GLXCurses.Container.set_border_width() was called on that widget directly.

        :return: the ``action_aera_border```property value
        :rtype: int
        """
        return self.__action_area_border

    @action_aera_border.setter
    def action_aera_border(self, value=5):
        """
        Set the ``action_aera_border`` property value

        allowed values: >= 0

        :param value: a positive int value
        :type value: int
        :raise TypeError: when value is not a int type
        :raise ValueError: when value is not >= 0
        """
        if type(value) != int:
            raise TypeError('"value" must be a int type')
        if not value >= 0:
            raise ValueError('"value" must be >= 0')
        if self.action_aera_border != value:
            self.__action_area_border = value

    @property
    def button_spacing(self):
        """
        Spacing between buttons in Chars

        :return: the ``button_spacing`` property value
        :rtype: int
        """
        return self.__button_spacing

    @button_spacing.setter
    def button_spacing(self, value=None):
        """
        Set the ``button_spacing`` property value

        allowed values: >= 0

        :param value: a positive int value in Chars
        :type value: int
        :raise TypeError: when value is not a int type
        :raise ValueError: when value is not >= 0
        """
        if type(value) != int:
            raise TypeError('"value" must be a int type')
        if not value >= 0:
            raise ValueError('"value" must be >= 0')

        if self.button_spacing != value:
            self.__button_spacing = value

    @property
    def content_area_border(self):
        """

        The default border width used around the content area of the dialog, as returned by
        dialog_get_content_area(), unless container_set_border_width() was called on that widget directly.

        :return: the ``content_area_border`` property value
        :rtype: int
        """
        return self.__content_area_border

    @content_area_border.setter
    def content_area_border(self, value=None):
        """
        Set the ``content_area_border`` property value

        allowed values: >= 0

        :param value: a positive int value in Chars
        :type value: int
        :raise TypeError: when value is not a int type
        :raise ValueError: when value is not >= 0
        """
        if type(value) != int:
            raise TypeError('"value" must be a int type')
        if not value >= 0:
            raise ValueError('"value" must be >= 0')

        if self.content_area_border != value:
            self.__content_area_border = value

    @property
    def content_area_spacing(self):
        """
        The default spacing used between elements of the content area of the dialog, as returned by
        dialog_get_content_area(), unless box_set_spacing() was called on that widget directly.

        :return: the ``content_area_spacing`` property value
        :rtype: int
        """
        return self.__content_area_spacing

    @content_area_spacing.setter
    def content_area_spacing(self, value=None):
        """
        Set the ``content_area_spacing`` property value

        allowed values: >= 0

        :param value: a positive int value in Chars
        :type value: int
        :raise TypeError: when value is not a int type
        :raise ValueError: when value is not >= 0
        """
        if type(value) != int:
            raise TypeError('"value" must be a int type')
        if not value >= 0:
            raise ValueError('"value" must be >= 0')

        if self.content_area_spacing != value:
            self.__content_area_spacing = value

    def new_with_buttons(self, title, parent, *flags):
        """

        :param title: Title of the dialog, or None
        :type title: str or None
        :param parent: Transient parent of the dialog, or None
        :type parent: GLXCurses Parent or None
        :param flags:
        :type flags: argv
        """
        self.__init__()
        self.title = title
        self.parent = parent
        self.add_buttons(*flags)

    def run(self):
        """
        Inform Application about the Dialog is the active window.

        Cause Application to forward event only inside the Dialog.

        The Mainloop/Application will work with the dialog like a normal window because dialog is a subclass of window.
        """
        self.emit('RUN', {
            'widget': self,
            'name': self.name
        })
        GLXCurses.Application().active_window_id = self.id

    def response(self, response_id=None):
        """
        Emits the “response” signal with the given response ID.

        Used to indicate that the user has responded to the dialog in some way; typically either you or
        Dialog().run() will be monitoring the ::response signal and take appropriate action.

        :param response_id: response ID
        :type response_id: str
        :raise TypeError: when ``response_id`` is not a str type
        """
        if type(response_id) != str:
            raise TypeError('"response_id" must be a str type')

        self.emit(
            detailed_signal='CURSES',
            data={'response_id': response_id}
        )

    def add_button(self, button_text=None, response_id=None):
        """
        Adds a button with the given ``text`` and sets things up so that clicking the button will emit the “response”
        signal with the given ``response_id`` .

        The button is appended to the end of the dialog’s action area.

        The button widget is returned, but usually you don’t need it.

        :param button_text: text of button
        :type button_text: str
        :param response_id: response ID for the button
        :type response_id: str
        :return: the GLXCurses.Button widget that was added.
        :rtype: GLXCurses.Button
        :raise TypeError: when ``button_text`` is not a str type
        :raise TypeError: when ``response_id`` is not a int type
        """
        if type(button_text) != str:
            raise TypeError('"button_text" must be a str type')
        if type(response_id) != str:
            raise TypeError('"response_id" must be a str type')

        button_widget = GLXCurses.Button()
        button_widget.text = button_text

        child_to_add = GLXCurses.ChildElement()
        child_to_add.widget = button_widget
        child_to_add.name = button_widget.name
        child_to_add.type = button_widget.glxc_type
        child_to_add.id = response_id
        child_to_add.properties.position = len(self._action_area) + 1
        child_to_add.widget.has_default = False
        child_to_add.widget.id = response_id
        child_to_add.widget.bg = 'WHITE'
        child_to_add.widget.fg = 'BLACK'

        self._action_area.append(child_to_add)

        return button_widget

    def add_buttons(self, *args):
        """
        Adds more buttons, same as calling Dialog.add_button() repeatedly.

        The data in arguments (args) must form a couple ``button_text``, ``response_id``.

        Example: Dialog.add_buttons('Hello.42', 42, 'Hello.43', 43, 'Hello.44', 44)

        Each button must have both text and response ID.

        :param args: couple ``button_text``, ``response_id``
        """
        for button_text, response_id in (args[i:i + 2] for i in range(0, int(len(args) / 2 * 2), 2)):
            self.add_button(button_text=button_text, response_id=response_id)

    def add_action_widget(self, child=None, response_id=None):
        """
        Adds an activatable widget to the action area of a GLXCurses.Dialog, connecting a signal handler
        that will emit the “response” signal on the dialog when the widget is activated.

        The widget is appended to the end of the dialog’s action area.

        If you want to add a non-activatable widget, simply pack it into the action_area field of the
        GLXCurses.Dialog struct.

        :param child: an activatable widget
        :type child: Widget
        :param response_id: response ID for child
        :type response_id: str
        :raise TypeError: when ``child`` is not a Widget instance
        :raise TypeError: when ``response_id`` is not a str type
        """
        if not isinstance(child, GLXCurses.Widget):
            raise TypeError('"child" must be a valid Widget')
        if type(response_id) != str:
            raise TypeError('"response_id" must be a int type')

        child_to_add = GLXCurses.ChildElement()
        child_to_add.widget = child
        child_to_add.name = child.name
        child_to_add.type = child.glxc_type
        child_to_add.id = response_id
        child_to_add.properties.position = len(self._action_area) + 1
        child_to_add.widget.has_default = False
        child_to_add.widget.id = response_id
        child_to_add.widget.bg = 'WHITE'
        child_to_add.widget.fg = 'BLACK'

        self._action_area.append(child_to_add)

    def set_default_response(self, response_id=None):
        """
        Sets the last widget in the dialog’s action area with the given response_id as the
        default widget for the dialog.

        Pressing “Enter” normally activates the default widget.

        :param response_id: a response ID
        :type response_id: str
        :raise TypeError: when ``response_id`` is not a dtr type
        """
        if type(response_id) != str:
            raise TypeError('"response_id" must be a int type')

        if type(self._action_area) == list and len(self._action_area) > 0:
            tmp_list = []
            for item in self._action_area:
                if item.id == response_id:
                    tmp_list.append(item)

            if len(tmp_list) > 0:
                tmp_list[-1].widget.has_default = True
                GLXCurses.Application().has_default = tmp_list[-1].widget

            del tmp_list

    def set_response_sensitive(self, response_id=None, setting=None):
        """
        Calls gtk_widget_set_sensitive (widget, @setting) for each widget in the dialog’s action area
        with the given response_id .

        A convenient way to sensitize/desensitize dialog buttons.

        :param response_id: a response ID
        :type response_id: str
        :param setting: True for sensitive
        :type setting: bool
        :raise TypeError: when ``response_id`` is not a str type
        :raise TypeError: when ``setting`` is not a bool type
        """
        if type(response_id) != str:
            raise TypeError('"response_id" must be a int type')
        if type(setting) != bool:
            raise TypeError('"setting" must be a bool type')

        if type(self._action_area) == list and len(self._action_area) > 0:
            for item in self._action_area:
                if item.id == response_id:
                    item.widget.sensitive = setting

    def get_response_for_widget(self, widget=None):
        """
        Gets the response id of a widget in the action area of a dialog.

        Note: That the return None if the widget is not found in action area.

        :param widget: a widget in the action area of dialog
        :type widget: Widget
        :return: the response id of widget , or GLXC.RESPONSE_NONE if widget doesnt have a response id set else None.
        :rtype: int or GLXC.RESPONSE_NONE or None
        """
        if not isinstance(widget, GLXCurses.Widget):
            raise TypeError('"widget" must be a GLXCurses Widget')

        if type(self._action_area) == list and len(self._action_area) > 0:
            for item in self._action_area:
                if item.widget == widget:
                    return item.id
        return GLXCurses.GLXC.RESPONSE_NONE

    def get_widget_for_response(self, response_id=None):
        """
        Gets the widget button that uses the given response ID in the action area of a dialog.

        :param response_id: the response ID used by the dialog widget
        :type response_id: str
        :return: the widget button that uses the given ``response_id`` , or ``None``.
        """
        if type(response_id) != str:
            raise TypeError('"response_id" must be a int type')

        if type(self._action_area) == list and len(self._action_area) > 0:
            for item in self._action_area:
                if isinstance(item.widget, GLXCurses.Button):
                    if item.id == response_id:
                        return item.widget

        return GLXCurses.GLXC.RESPONSE_NONE

    def get_action_area(self):
        """
        has been deprecated since version GTK3.12, GLXCurses return the internal _action_area.

        Here the structure:

        ```
        [
            {
                'widget': button_widget,
                'response_id': response_id,
                'default_response': False
            },
            {
                'widget': button_widget,
                'response_id': response_id,
                'default_response': False
            }
        ]
        ```

        Returns the action area of dialog .

        :return: the action area.
        :rtype: list
        """
        return self._action_area

    def get_content_area(self):
        """
        Returns the content area of dialog .

        :return: the content area GLXCurses Box.
        :rtype: VBox
        """
        return self._content_area

    # Signals
    def close(self):
        """
        Signal emitted when the user uses a keybinding to close the dialog.

        :return:
        """
        if isinstance(GLXCurses.Application().active_window.widget, GLXCurses.Dialog):
            if len(GLXCurses.Application().children) > 1:
                if GLXCurses.Application().children[1]:
                    GLXCurses.Application().active_window_id = GLXCurses.Application().active_window_id_prev

    def _update_preferred_sizes(self):
        self.preferred_width = self._get_estimated_preferred_width()
        self.preferred_height = self._get_estimated_preferred_height()

    def _update_preferred_position(self):
        self.y_offset = 0
        self.y_offset += int(self.height / 2)
        self.y_offset -= int(self.preferred_height / 2)

        self.x_offset = 0
        self.x_offset += int(self.width / 2)
        self.x_offset -= int(self.preferred_width / 2)

    def _get_estimated_preferred_width(self):
        """
        Estimate a preferred width, by consider X Location, allowed width

        :return: a estimated preferred width
        :rtype: int
        """
        estimated_preferred_width = 0
        if self.decorated:
            estimated_preferred_width += 2

        content_area_width = 0
        if len(self._content_area.children) > 0:
            for child in self._content_area.children:
                content_area_width += child.preferred_width

        action_area_width = 0
        # if len(self._action_area) > 0:
        #     for button in self._action_area:
        #         action_area_width += button.widget.preferred_width

        if self.title:
            estimated_preferred_width += max(content_area_width, max(action_area_width, len(self.title)))
        else:
            estimated_preferred_width += max(content_area_width, max(action_area_width, 0))

        if len(self._action_area) > 0:
            estimated_preferred_width += len(self._action_area)
            estimated_preferred_width += 3
        return estimated_preferred_width + 4

    def _get_estimated_preferred_height(self):
        """
        Estimate a preferred height, by consider Y Location

        :return: a estimated preferred height
        :rtype: int
        """
        estimated_preferred_height = 4
        if self._action_area:
            # One for the Line Tee , One for the button action area
            estimated_preferred_height += 2

        if self.decorated:
            estimated_preferred_height += 2
        if len(self._content_area.children) > 0:
            for child in self._content_area.children:
                estimated_preferred_height += child.preferred_height

        return estimated_preferred_height

    def draw_widget_in_area(self):
        # Create the subwin
        self.create_or_resize()
        self._update_preferred_sizes()
        self._update_preferred_position()

        #  May be it have no parent or that the first init, then test if subwin creation have work
        if self.subwin:

            # Debug message
            if self.debug:
                logging.debug('Draw {0}'.format(self))
                logging.debug(
                    "In Area -> x: {0}, y: {1}, width: {2}, height:{3}".format(
                        self.x,
                        self.y_offset,
                        self.width,
                        self.preferred_height
                    )
                )

            self._draw_background()

            if self.decorated:
                self._draw_box()

            # Draw the child.
            if self.child is not None:
                # Injection
                self.child.widget.stdscr = GLXCurses.Application().stdscr

                # self.get_child().set_subwin(self.get_subwin())
                self.child.widget.style = GLXCurses.Style()
                self.child.widget.style.attribute_states['text']['STATE_NORMAL'] = 'BLACK'
                self.child.widget.style.attribute_states['bg']['STATE_NORMAL'] = 'WHITE'

                if self.decorated:
                    self.child.widget.x = self.x_offset + 2
                    self.child.widget.y = self.y_offset + 2
                    self.child.widget.width = self.preferred_width - 4
                    self.child.widget.height = self.preferred_height - 6
                else:
                    self.child.widget.x = self.x_offset + 2
                    self.child.widget.y = self.y_offset + 2
                    self.child.widget.width = self.preferred_width - 4
                    self.child.widget.height = self.preferred_height - 6

                # Debug
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

            if len(self._action_area) > 0:
                if self.y_offset + self.preferred_height + 2 - 3 <= self.height:
                    self._draw_action_area()

            if self.title:
                if self.y_offset + 1 >= 0:
                    self._draw_title()

    def _draw_action_area(self):
        # Draw the child.
        if self._action_area:
            total_size = len(self._action_area) - 1
            a_button_have_default = False

            for button in self._action_area:
                total_size += button.widget.preferred_width
                if button.widget.has_default is True:
                    a_button_have_default = True

            if a_button_have_default is False:
                self._action_area[-1].widget.has_default = True

            cursor_position = int(((self.width - 2) / 2) - total_size / 2)
            default_is_display = False

            for button in self._action_area:
                # Injection
                button.widget.stdscr = GLXCurses.Application().stdscr

                # self.get_child().set_subwrcrcin(self.get_subwin())
                # self.style.get_attribute_states()['text']['STATE_NORMAL'] = 'BLACK'
                # self.style.get_attribute_states()['bg']['STATE_NORMAL'] = 'WHITE'

                if button.widget.has_default is True:
                    button.widget.x = cursor_position
                    button.widget.y = self.y_offset + self.preferred_height - 3
                    button.widget.width = button.widget.preferred_width + 3
                    button.widget.height = 2
                    button.widget.bg = 'WHITE'
                    button.widget.fg = 'BLACK'

                    button.widget.can_focus = True
                    button.widget.has_focus = True
                    button.widget.can_default = True
                    GLXCurses.Application().has_default = button.widget
                    GLXCurses.Application().has_focus = button.widget
                    GLXCurses.Application().has_prelight = button.widget
                    cursor_position += button.widget.preferred_width + 3
                    default_is_display = True
                elif button.widget.has_default is False:
                    if not default_is_display:
                        button.widget.x = cursor_position - 1
                    else:
                        button.widget.x = cursor_position
                    button.widget.bg = 'WHITE'
                    button.widget.fg = 'BLACK'
                    button.widget.y = self.y_offset + self.preferred_height - 3
                    button.widget.width = button.widget.preferred_width + 1
                    button.widget.height = 2
                    button.widget.has_focus = False
                    button.widget.can_focus = False
                    button.widget.can_default = False

                    cursor_position += button.widget.preferred_width + 1

                # Debug
                # if self.get_debug():
                logging.debug(
                    "Draw button -> x: {0}, y: {1}, width: {2}, height:{3}".format(
                        button.widget.x,
                        button.widget.y,
                        button.widget.width,
                        button.widget.height
                    )
                )

                button.widget.draw()

            # Check who have default

            for button in self._action_area:
                if isinstance(GLXCurses.Application().has_default, GLXCurses.ChildElement):
                    if GLXCurses.Application().has_default.widget == button.widget:
                        a_button_have_default = True
            if not a_button_have_default:
                self._action_area[-1].widget.can_focus = True
                child_to_add = GLXCurses.ChildElement()
                child_to_add.name = self._action_area[-1].widget.name
                child_to_add.widget = self._action_area[-1].widget
                child_to_add.id = self._action_area[-1].widget.id
                child_to_add.type = self._action_area[-1].widget.glxc_type

                GLXCurses.Application().has_default = child_to_add
                #GLXCurses.Application().set_default(widget=self._action_area[-1].widget)

    def _draw_background(self):
        for y_inc in range(self.y_offset, self.y_offset + self.preferred_height):
            for x_inc in range(self.x_offset, self.x_offset + self.preferred_width):
                try:
                    self.subwin.delch(y_inc, x_inc)
                    self.subwin.insch(
                        y_inc,
                        x_inc,
                        ' ',
                        self.style.color(
                            fg=self.style.get_color_text('dark', 'STATE_NORMAL'),
                            bg=self.style.get_color_text('base', 'STATE_NORMAL')
                        )
                    )
                except curses.error:  # pragma: no cover
                    pass

    def _draw_title(self):
        if self.width > 1:
            title_with_spacing = GLXCurses.resize_text(" {0} ".format(self.title), self.width - 2, '~')
            pos = int(self.width / 2) - int(len(title_with_spacing) / 2)
            for x_inc in range(0, len(title_with_spacing)):
                try:
                    self.subwin.delch(self.y_offset + 1, pos + x_inc)

                    self.subwin.insch(
                        self.y_offset + 1,
                        pos + x_inc,
                        title_with_spacing[x_inc],
                        self.style.color(
                            fg=self.style.get_color_text('text_fg', 'STATE_SELECTED'),
                            bg=self.style.get_color_text('base', 'STATE_NORMAL')
                        )

                    )
                except curses.error:  # pragma: no cover
                    pass

    def _draw_box(self):
        # Create a box and add the name of the windows like a king, who trust that !!!
        if self.decorated:
            if self.subwin:
                self._draw_box_upper_left_corner()
                self._draw_box_top()
                self._draw_box_upper_right_corner()

                self._draw_box_left_side()
                self._draw_box_right_side()

                self._draw_box_bottom_left_corner()
                self._draw_box_bottom()
                self._draw_box_bottom_right_corner()
                if len(self._action_area) > 0:
                    self._draw_box_tee_pointing_right()
                    self._draw_box_tee_pointing_left()
                    self._draw_box_bottom_tee()

    def _draw_box_bottom(self, char=None):
        # Bottom
        if char is None:
            char = curses.ACS_HLINE
        for x_inc in range(self.x_offset + 2, self.x_offset + self.preferred_width - 1):
            try:
                self.subwin.delch(self.y_offset + self.preferred_height - 2, x_inc)
                self.subwin.insch(
                    self.y_offset + self.preferred_height - 2,
                    x_inc,
                    char,
                    self.style.color(
                        fg=self.style.get_color_text('dark', 'STATE_NORMAL'),
                        bg=self.style.get_color_text('base', 'STATE_NORMAL')
                    )
                )

            except curses.error:  # pragma: no cover
                pass

    def _draw_box_top(self, char=None):
        # Top
        if char is None:
            char = curses.ACS_HLINE

        for x_inc in range(self.x_offset + 2, self.x_offset + self.preferred_width - 2):
            try:
                self.subwin.delch(self.y_offset + 1, x_inc)
                self.subwin.insch(
                    self.y_offset + 1,
                    x_inc,
                    char,
                    self.style.color(
                        fg=self.style.get_color_text('dark', 'STATE_NORMAL'),
                        bg=self.style.get_color_text('base', 'STATE_NORMAL')
                    )
                )
            except curses.error:  # pragma: no cover
                pass

    def _draw_box_right_side(self, char=None):
        # Right side
        if char is None:
            char = curses.ACS_VLINE

        for y_inc in range(0 + 2, self.preferred_height - 2):
            try:
                self.subwin.delch(self.y_offset + y_inc, self.x_offset + self.preferred_width - 2)
                self.subwin.insch(
                    self.y_offset + y_inc,
                    self.x_offset + self.preferred_width - 2,
                    char,
                    self.style.color(
                        fg=self.style.get_color_text('dark', 'STATE_NORMAL'),
                        bg=self.style.get_color_text('base', 'STATE_NORMAL')
                    )
                )
            except curses.error:  # pragma: no cover
                pass

    def _draw_box_left_side(self, char=None):
        # Left side
        if char is None:
            char = curses.ACS_VLINE

        for y_inc in range(0 + 2, self.preferred_height - 2):
            try:
                self.subwin.delch(self.y_offset + y_inc, self.x_offset + 1)
                self.subwin.insch(
                    self.y_offset + y_inc,
                    self.x_offset + 1,
                    char,
                    self.style.color(
                        fg=self.style.get_color_text('dark', 'STATE_NORMAL'),
                        bg=self.style.get_color_text('base', 'STATE_NORMAL')
                    )
                )
            except curses.error:  # pragma: no cover
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
            self.subwin.delch(self.y_offset + 1, self.preferred_width + self.x_offset - 2)
            self.subwin.insch(
                self.y_offset + 1,
                self.preferred_width + self.x_offset - 2,
                char,
                self.style.color(
                    fg=self.style.get_color_text('dark', 'STATE_NORMAL'),
                    bg=self.style.get_color_text('base', 'STATE_NORMAL')
                )
            )
        except curses.error:  # pragma: no cover
            pass

    def _draw_box_upper_left_corner(self, char=None):
        # Upper-left corner
        if char is None:
            char = curses.ACS_ULCORNER
        try:
            self.subwin.delch(self.y_offset + 1, self.x_offset + 1)
            self.subwin.insch(
                self.y_offset + 1,
                self.x_offset + 1,
                char,
                self.style.color(
                    fg=self.style.get_color_text('dark', 'STATE_NORMAL'),
                    bg=self.style.get_color_text('base', 'STATE_NORMAL')
                )
            )
        except curses.error:  # pragma: no cover
            pass

    def _draw_box_bottom_right_corner(self, char=None):
        # Bottom-right corner
        if char is None:
            char = curses.ACS_LRCORNER
        try:
            self.subwin.delch(self.y_offset + self.preferred_height - 2, self.x_offset + self.preferred_width - 2)
            self.subwin.insch(
                self.y_offset + self.preferred_height - 2,
                self.x_offset + self.preferred_width - 2,
                char,
                self.style.color(
                    fg=self.style.get_color_text('dark', 'STATE_NORMAL'),
                    bg=self.style.get_color_text('base', 'STATE_NORMAL')
                )
            )
        except curses.error:  # pragma: no cover
            pass

    def _draw_box_bottom_left_corner(self, char=None):
        # Bottom-left corner
        if char is None:
            char = curses.ACS_LLCORNER
        try:
            self.subwin.delch(self.y_offset + self.preferred_height - 2, self.x_offset + 1)
            self.subwin.insch(
                self.y_offset + self.preferred_height - 2,
                self.x_offset + 1,
                char,
                self.style.color(
                    fg=self.style.get_color_text('dark', 'STATE_NORMAL'),
                    bg=self.style.get_color_text('base', 'STATE_NORMAL')
                )
            )
        except curses.error:  # pragma: no cover
            pass

    def _draw_box_tee_pointing_right(self, char=None):
        # Bottom-left tee_pointing_right
        if char is None:
            char = curses.ACS_LTEE
        try:
            self.subwin.delch(self.y_offset + self.preferred_height - 4, self.x_offset + 1)
            self.subwin.insch(
                self.y_offset + self.preferred_height - 4,
                self.x_offset + 1,
                char,
                self.style.color(
                    fg=self.style.get_color_text('dark', 'STATE_NORMAL'),
                    bg=self.style.get_color_text('base', 'STATE_NORMAL')
                )
            )
        except curses.error:  # pragma: no cover
            pass

    def _draw_box_tee_pointing_left(self, char=None):
        # Bottom-right corner
        if char is None:
            char = curses.ACS_RTEE
        try:
            self.subwin.delch(self.y_offset + self.preferred_height - 4, self.x_offset + self.preferred_width - 2)
            self.subwin.insch(
                self.y_offset + self.preferred_height - 4,
                self.x_offset + self.preferred_width - 2,
                char,
                self.style.color(
                    fg=self.style.get_color_text('dark', 'STATE_NORMAL'),
                    bg=self.style.get_color_text('base', 'STATE_NORMAL')
                )
            )
        except curses.error:  # pragma: no cover
            pass

    def _draw_box_bottom_tee(self, char=None):
        # Bottom
        for x_inc in range(self.x_offset + 2, self.x_offset + self.preferred_width - 2):
            try:
                self.subwin.delch(self.y_offset + self.preferred_height - 4, x_inc)
                self.subwin.insch(
                    self.y_offset + self.preferred_height - 4,
                    x_inc,
                    curses.ACS_HLINE,
                    self.style.color(
                        fg=self.style.get_color_text('dark', 'STATE_NORMAL'),
                        bg=self.style.get_color_text('base', 'STATE_NORMAL')
                    )
                )

            except curses.error:  # pragma: no cover
                pass
