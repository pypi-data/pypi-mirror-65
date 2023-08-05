#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import GLXCurses
import curses
import logging


class ToolBar(GLXCurses.Widget, GLXCurses.Dividable):
    def __init__(self):
        # Load heritage
        GLXCurses.Widget.__init__(self)
        GLXCurses.Dividable.__init__(self)

        # It's a GLXCurse Type
        self.glxc_type = 'GLXCurses.ToolBar'
        self.name = '{0}{1}'.format(self.__class__.__name__, self.id)

        # Make a Widget Style heritage attribute as local attribute
        # if self.style.attribute_states:
        #     if self.attribute_states != self.style.attribute_states:
        #         self.attribute_states = self.style.attribute_states

        self.button_list = [
            'Help'
        ]

        # States
        self.curses_mouse_states = {
            curses.BUTTON1_PRESSED: 'BUTTON1_PRESS',
            curses.BUTTON1_RELEASED: 'BUTTON1_RELEASED',
            curses.BUTTON1_CLICKED: 'BUTTON1_CLICKED',
            curses.BUTTON1_DOUBLE_CLICKED: 'BUTTON1_DOUBLE_CLICKED',
            curses.BUTTON1_TRIPLE_CLICKED: 'BUTTON1_TRIPLE_CLICKED',

            curses.BUTTON2_PRESSED: 'BUTTON2_PRESSED',
            curses.BUTTON2_RELEASED: 'BUTTON2_RELEASED',
            curses.BUTTON2_CLICKED: 'BUTTON2_CLICKED',
            curses.BUTTON2_DOUBLE_CLICKED: 'BUTTON2_DOUBLE_CLICKED',
            curses.BUTTON2_TRIPLE_CLICKED: 'BUTTON2_TRIPLE_CLICKED',

            curses.BUTTON3_PRESSED: 'BUTTON3_PRESSED',
            curses.BUTTON3_RELEASED: 'BUTTON3_RELEASED',
            curses.BUTTON3_CLICKED: 'BUTTON3_CLICKED',
            curses.BUTTON3_DOUBLE_CLICKED: 'BUTTON3_DOUBLE_CLICKED',
            curses.BUTTON3_TRIPLE_CLICKED: 'BUTTON3_TRIPLE_CLICKED',

            # curses.BUTTON4_PRESSED: 'BUTTON4_PRESSED',
            # curses.BUTTON4_RELEASED: 'BUTTON4_RELEASED',
            # curses.BUTTON4_CLICKED: 'BUTTON4_CLICKED',
            # curses.BUTTON4_DOUBLE_CLICKED: 'BUTTON4_DOUBLE_CLICKED',
            # curses.BUTTON4_TRIPLE_CLICKED: 'BUTTON4_TRIPLE_CLICKED',

            curses.REPORT_MOUSE_POSITION: 'MOUSE_WHEEL_DOWN',
            curses.BUTTON4_PRESSED: 'MOUSE_WHEEL_UP',

            curses.BUTTON_SHIFT: 'BUTTON_SHIFT',
            curses.BUTTON_CTRL: 'BUTTON_CTRL',
            curses.BUTTON_ALT: 'BUTTON_ALT'
        }

        self.can_default = True
        self.can_focus = True
        self.sensitive = True
        self.states_list = None
        self._focus_without_selecting = False

        # Subscription
        # Mouse
        self.connect('MOUSE_EVENT', ToolBar._handle_mouse_event)
        # Keyboard
        self.connect('CURSES', ToolBar._handle_key_event)

    def draw(self):
        # That is not a normal widget, then the ToolBar create the subwin by it self
        self.create_or_resize()
        self._update_preferred_sizes()
        self._check_sizes()
        self._check_selected()
        if self.subwin:
            self._draw_background()

            count = 0
            for _ in self.get_button_list():
                self._draw_button(count)

                count += 1

    def set_button_list(self, button_list):
        """
        Set the button list

        :param button_list: the button list
        :type button_list: list
        :raise TypeError: if button list is not a list
        :return:
        """
        # Exit as soon of possible
        if type(button_list) != list:
            raise TypeError("'button_list' must be a list type")

        if self.get_button_list() != button_list:
            self.button_list = button_list

    def get_button_list(self):
        """
        Return the list of button to display

        :return: list of button
        :rtype: list
        """
        return self.button_list

    def _update_preferred_sizes(self):
        self.preferred_height = 1
        self.preferred_width = self.width

    def _check_sizes(self):
        # dividable = GLXCurses.Dividable()
        self.start = 0
        self.stop = self.width - 1
        self.num = len(self.get_button_list())
        self.round_type = GLXCurses.GLXC.ROUND_DOWN

    def _draw_button(self, item_number):

        try:
            self.round_type = GLXCurses.GLXC.ROUND_HALF_UP
            start, stop = self.split_positions[str(item_number)]
        except IndexError :
            self.round_type = GLXCurses.GLXC.ROUND_DOWN
            start, stop = self.split_positions[str(item_number)]

        if stop - start <= 1:
            item_number_size = 1
            item_number_text = str('{}'.format(item_number + 1))
            text_max_width = stop - start
        else:
            item_number_size = 2
            item_number_text = str('{0: >2}'.format(item_number + 1))
            text_max_width = stop - start - 1

        text = GLXCurses.resize_text(
            text=str(self.get_button_list()[item_number]),
            max_width=text_max_width

        )

        if len(text) > 0:
            for x_inc in range(start, stop + 1):
                # Background
                try:
                    self.subwin.delch(0, x_inc)
                    self.subwin.insch(
                        0,
                        x_inc,
                        ' ',
                        self.style.color(
                            fg=self.style.get_color_text('dark', 'STATE_NORMAL'),
                            bg=self.style.get_color_text('bg', 'STATE_PRELIGHT')
                        )
                    )
                except curses.error:  # pragma: no cover
                    pass

            # Num Label
            for x_inc in range(0, len(item_number_text)):
                try:
                    self.subwin.delch(0, start + x_inc)
                    self.subwin.insch(
                        0,
                        start + x_inc,
                        item_number_text[x_inc],
                        self.style.color(
                            fg=self.style.get_color_text('dark', 'STATE_NORMAL'),
                            bg=self.style.get_color_text('white', 'STATE_NORMAL')
                        ) | curses.A_REVERSE

                    )
                except curses.error:  # pragma: no cover
                    pass

            # text
            for x_inc in range(0, len(text)):
                try:
                    self.subwin.delch(0, start + item_number_size + x_inc)
                    self.subwin.insch(
                        0,
                        start + item_number_size + x_inc,
                        text[x_inc],
                        self.style.color(
                            fg=self.style.get_color_text('dark', 'STATE_NORMAL'),
                            bg=self.style.get_color_text('bg', 'STATE_PRELIGHT')
                        )

                    )
                except curses.error:  # pragma: no cover
                    pass

    def _draw_background(self):
        self.subwin.bkgd(
            ord(' '),
            self.style.color(fg='GRAY', bg='BLACK')
        )
        self.subwin.bkgdset(
            ord(' '),
            self.style.color(fg='GRAY', bg='BLACK')
        )

    def _handle_mouse_event(self, event_signal, event_args):
        if self.sensitive:
            (mouse_event_id, x, y, z, event) = event_args
            # convert mouse point of view to Area point of view
            y -= self.y
            x -= self.x
            if 0 <= y <= self.height - 1:
                if 0 <= x <= self.preferred_width - 1:
                    # We are sure about the ToolBar have been clicked
                    self._grab_focus()
                    for count in range(0, self.num):
                        if self.split_positions['{0}'.format(count)][0] <= x <= self.split_positions['{0}'.format(count)][1]:
                            if event == GLXCurses.GLXC.BUTTON1_CLICKED or event == curses.BUTTON1_RELEASED:
                                self.emit('F{0}_CLICKED'.format(count + 1), {
                                          'class': self.__class__.__name__,
                                          'id': self.id,
                                          'event_signal': 'F{0}_CLICKED'.format(count + 1)})

    def _handle_key_event(self, event_signal, *event_args):
        # Check if we have to care about keyboard event
        if isinstance(GLXCurses.Application().has_focus, GLXCurses.ChildElement) and \
                GLXCurses.Application().has_focus.id == self.id:
            # setting
            key = event_args[0]
            instance = None
            # Touch Escape
            if key == GLXCurses.GLXC.KEY_ESC:
                GLXCurses.Application().has_focus = None

                self.is_focus = False
                self.has_focus = False

            if key == GLXCurses.GLXC.KEY_F1:
                instance = {
                    'class': self.__class__.__name__,
                    'id': self.id,
                    'event_signal': 'F1_PRESSED'
                }
                self.emit(str(instance['event_signal']), instance)
            elif key == GLXCurses.GLXC.KEY_F2:
                instance = {
                    'class': self.__class__.__name__,
                    'id': self.id,
                    'event_signal': 'F2_PRESSED'
                }
                self.emit(str(instance['event_signal']), instance)
            elif key == GLXCurses.GLXC.KEY_F3:
                instance = {
                    'class': self.__class__.__name__,
                    'id': self.id,
                    'event_signal': 'F3_PRESSED'
                }
                self.emit(str(instance['event_signal']), instance)

            elif key == GLXCurses.GLXC.KEY_F4:
                instance = {
                    'class': self.__class__.__name__,
                    'id': self.id,
                    'event_signal': 'F4_PRESSED'
                }
                self.emit(str(instance['event_signal']), instance)

            elif key == GLXCurses.GLXC.KEY_F5:
                instance = {
                    'class': self.__class__.__name__,
                    'id': self.id,
                    'event_signal': 'F5_PRESSED'
                }
                self.emit(str(instance['event_signal']), instance)

            elif key == GLXCurses.GLXC.KEY_F6:
                instance = {
                    'class': self.__class__.__name__,
                    'id': self.id,
                    'event_signal': 'F6_PRESSED'
                }
                self.emit(str(instance['event_signal']), instance)

            elif key == GLXCurses.GLXC.KEY_F7:
                instance = {
                    'class': self.__class__.__name__,
                    'id': self.id,
                    'event_signal': 'F7_PRESSED'
                }
                self.emit(str(instance['event_signal']), instance)

            elif key == GLXCurses.GLXC.KEY_F8:
                instance = {
                    'class': self.__class__.__name__,
                    'id': self.id,
                    'event_signal': 'F8_PRESSED'
                }
                self.emit(str(instance['event_signal']), instance)

            elif key == GLXCurses.GLXC.KEY_F9:
                instance = {
                    'class': self.__class__.__name__,
                    'id': self.id,
                    'event_signal': 'F9_PRESSED'
                }
                self.emit(str(instance['event_signal']), instance)

            elif key == GLXCurses.GLXC.KEY_F10:
                instance = {
                    'class': self.__class__.__name__,
                    'id': self.id,
                    'event_signal': 'F10_PRESSED'
                }
                self.emit(str(instance['event_signal']), instance)

            # Create a Dict with everything
            # if instance is None:
            #     instance = {
            #         'class': self.__class__.__name__,
            #         'id': self.id,
            #         'event_signal': event_signal
            #     }
            # EVENT EMIT
            # Application().emit(self.curses_mouse_states[event], instance)

    def _grab_focus(self):
        """
        Internal method, for Select the contents of the Entry it take focus.

        See: grab_focus_without_selecting ()
        """
        if self.can_focus:
            if isinstance(GLXCurses.Application().has_focus, GLXCurses.ChildElement):
                if GLXCurses.Application().has_focus.id != self.id:
                    GLXCurses.Application().has_focus = self
                    GLXCurses.Application().has_default = self
                    GLXCurses.Application().has_prelight = self
                    self.has_focus = True
                    self.has_prelight = True
                    self.has_default = True

    def _check_selected(self):
        if self.can_focus:
            if isinstance(GLXCurses.Application().has_default, GLXCurses.ChildElement):
                if GLXCurses.Application().has_default.widget.id == self.id:
                    self.has_default = True
                else:
                    self.has_default = False
            if isinstance(GLXCurses.Application().has_focus, GLXCurses.ChildElement):
                if GLXCurses.Application().has_focus.widget.id == self.id:
                    self.has_focus = True
                else:
                    self.has_focus = False
            if isinstance(GLXCurses.Application().has_prelight, GLXCurses.ChildElement):
                if GLXCurses.Application().has_prelight.widget.id == self.id:
                    self.has_prelight = True
                else:
                    self.has_prelight = False


