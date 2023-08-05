#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import GLXCurses
import curses
import logging


class CheckButton(GLXCurses.Widget, GLXCurses.Movable):
    def __init__(self):
        GLXCurses.Widget.__init__(self)
        GLXCurses.Movable.__init__(self)

        self.name = '{0}{1}'.format(self.__class__.__name__, self.id)

        # Internal Widget Setting
        self.__text = None

        # Sensitive
        self.can_default = True
        self.can_focus = True
        self.sensitive = True
        self.states_list = None

        self.bg = 'BLUE'
        self.fg = 'GRAY'

        self.curses_mouse_states = {
            GLXCurses.GLXC.BUTTON1_PRESSED: 'BUTTON1_PRESS',
            GLXCurses.GLXC.BUTTON1_RELEASED: 'BUTTON1_RELEASED',
            GLXCurses.GLXC.BUTTON1_CLICKED: 'BUTTON1_CLICKED',
            GLXCurses.GLXC.BUTTON1_DOUBLE_CLICKED: 'BUTTON1_DOUBLE_CLICKED',
            GLXCurses.GLXC.BUTTON1_TRIPLE_CLICKED: 'BUTTON1_TRIPLE_CLICKED',

            GLXCurses.GLXC.BUTTON2_PRESSED: 'BUTTON2_PRESSED',
            GLXCurses.GLXC.BUTTON2_RELEASED: 'BUTTON2_RELEASED',
            GLXCurses.GLXC.BUTTON2_CLICKED: 'BUTTON2_CLICKED',
            GLXCurses.GLXC.BUTTON2_DOUBLE_CLICKED: 'BUTTON2_DOUBLE_CLICKED',
            GLXCurses.GLXC.BUTTON2_TRIPLE_CLICKED: 'BUTTON2_TRIPLE_CLICKED',

            GLXCurses.GLXC.BUTTON3_PRESSED: 'BUTTON3_PRESSED',
            GLXCurses.GLXC.BUTTON3_RELEASED: 'BUTTON3_RELEASED',
            GLXCurses.GLXC.BUTTON3_CLICKED: 'BUTTON3_CLICKED',
            GLXCurses.GLXC.BUTTON3_DOUBLE_CLICKED: 'BUTTON3_DOUBLE_CLICKED',
            GLXCurses.GLXC.BUTTON3_TRIPLE_CLICKED: 'BUTTON3_TRIPLE_CLICKED',

            GLXCurses.GLXC.BUTTON4_PRESSED: 'BUTTON4_PRESSED',
            GLXCurses.GLXC.BUTTON4_RELEASED: 'BUTTON4_RELEASED',
            GLXCurses.GLXC.BUTTON4_CLICKED: 'BUTTON4_CLICKED',
            GLXCurses.GLXC.BUTTON4_DOUBLE_CLICKED: 'BUTTON4_DOUBLE_CLICKED',
            GLXCurses.GLXC.BUTTON4_TRIPLE_CLICKED: 'BUTTON4_TRIPLE_CLICKED',

            GLXCurses.GLXC.BUTTON_SHIFT: 'BUTTON_SHIFT',
            GLXCurses.GLXC.BUTTON_CTRL: 'BUTTON_CTRL',
            GLXCurses.GLXC.BUTTON_ALT: 'BUTTON_ALT'
        }

        self.connect('MOUSE_EVENT', CheckButton._handle_mouse_event)
        self.connect('CURSES', CheckButton._handle_key_event)

    @property
    def active(self):
        return self.state['ACTIVE']

    @active.setter
    def active(self, value=None):
        if value is None:
            value = False
        if type(value) != bool:
            raise TypeError('"active" value must be a bool type or None')
        if self.active != value:
            self.state['ACTIVE'] = value

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value=None):
        if value is not None and type(value) != str:
            raise TypeError('"text" value must be a str type or None')
        if self.__text != value:
            self.__text = value
            self.preferred_width = len(self.text) + len(self.interface)

    @property
    def color(self):
        if not self.sensitive:
            return self.style.color(fg=self.fg, bg=self.bg) | curses.A_DIM
        if self.has_prelight:
            return self.style.color(fg='BLACK', bg='CYAN')
        return self.style.color(fg=self.fg, bg=self.bg)

    @property
    def interface(self, active='[x] ', unactivated='[ ] '):
        if self.active:
            return active
        return unactivated

    def draw_widget_in_area(self):
        if self.can_focus:
            if GLXCurses.Application().has_default and GLXCurses.Application().has_default.id == self.id:
                self.has_default = True
            else:
                self.has_default = False
            if GLXCurses.Application().has_focus and GLXCurses.Application().has_focus.id == self.id:
                self.has_focus = True
            else:
                self.has_focus = False
            if GLXCurses.Application().has_prelight and GLXCurses.Application().has_prelight.id == self.id:
                self.has_prelight = True
            else:
                self.has_prelight = False

        self.create_or_resize()
        if self.subwin is not None:
            if self.text:
                self.preferred_width = len(self.text) + len(self.interface)
                self.preferred_height = 1
                self.check_justification()
                self.check_position()
                if len(GLXCurses.resize_text(self.text, self.width - len(self.interface), '~')) > 0:

                    for x_inc in range(0, len(self.interface)):
                        try:
                            self.subwin.delch(self.y_offset,
                                              self.x_offset + x_inc
                                              )
                            self.subwin.insch(self.y_offset,
                                              self.x_offset + x_inc,
                                              self.interface[x_inc],
                                              self.color
                                              )
                        except curses.error:  # pragma: no cover
                            pass

                    message_to_display = GLXCurses.resize_text(self.text, self.width - len(self.interface), '~')
                    for x_inc in range(0, len(message_to_display)):
                        try:
                            self.subwin.delch(self.y_offset,
                                              self.x_offset + int(len(self.interface)) + x_inc
                                              )
                            self.subwin.insch(self.y_offset,
                                              self.x_offset + int(len(self.interface)) + x_inc,
                                              message_to_display[x_inc],
                                              self.color
                                              )
                        except curses.error:  # pragma: no cover
                            pass

    def _handle_mouse_event(self, event_signal, event_args):  # pragma: no cover
        if self.sensitive:
            # Read the mouse event information's
            (mouse_event_id, x, y, z, event) = event_args
            # Be sure we select really the Button
            y -= self.y
            x -= self.x

            x_pos_start = self.x_offset + len(self.interface) + len(self.text) - 1
            x_pos_stop = self.x_offset
            y_pos_start = self.y_offset
            y_pos_stop = self.y_offset - self.preferred_height + 1

            that_for_me = (y_pos_start >= y >= y_pos_stop and x_pos_start >= x >= x_pos_stop)

            if that_for_me:
                if self.can_focus:
                    if isinstance(GLXCurses.Application().has_focus, GLXCurses.ChildElement):
                        if GLXCurses.Application().has_focus.id != self.id:
                            GLXCurses.Application().has_focus = self
                            GLXCurses.Application().has_default = self
                            GLXCurses.Application().has_prelight = self
                            self.has_focus = True
                            self.has_prelight = True
                            self.has_default = True

                # BUTTON1
                if event == curses.BUTTON1_PRESSED:
                    GLXCurses.Application().has_default = self
                    GLXCurses.Application().has_prelight = self
                    self.has_prelight = True
                    self.has_default = True

                elif event == curses.BUTTON1_RELEASED:
                    GLXCurses.Application().has_prelight = None
                    GLXCurses.Application().has_default = self
                    self.has_prelight = True
                    self.has_default = True
                    self.active = not self.active

                if event == curses.BUTTON1_CLICKED:
                    GLXCurses.Application().has_default = self
                    GLXCurses.Application().has_prelight = self
                    self.active = not self.active
                    self.has_prelight = True
                    self.has_default = True

                if event == 134217728 or event == 2097152 or event == 524288 or event == 65536:
                    GLXCurses.Application().has_default = self
                    GLXCurses.Application().has_prelight = self
                    self.active = not self.active
                    self.has_prelight = True
                    self.has_default = True

                if event == curses.BUTTON1_DOUBLE_CLICKED:
                    pass

                if event == curses.BUTTON1_TRIPLE_CLICKED:
                    pass

                if event == 524288 or event == 134217728:
                    self.active = not self.active

                self.emit(self.curses_mouse_states[event], {
                    'class': self.__class__.__name__,
                    'label': self.text,
                    'id': self.id
                })

        else:
            if self.debug:
                logging.debug('{0} -> id:{1}, object:{2}, is not sensitive'.format(
                    self.__class__.__name__,
                    self.id,
                    self
                ))

    def _handle_key_event(self, event_signal, *event_args):  # pragma: no cover
        # Check if we have to care about keyboard event
        if self.sensitive and \
                isinstance(GLXCurses.Application().has_default, GLXCurses.ChildElement) and \
                GLXCurses.Application().has_default.id == self.id:
            # setting
            key = event_args[0]

            # Touch Escape
            if key == GLXCurses.GLXC.KEY_ESC:
                GLXCurses.Application().has_focus = None
                GLXCurses.Application().has_default = None
                GLXCurses.Application().has_prelight = None
                self.has_prelight = False
                self.has_default = False
                self.has_focus = False

            if key == ord(" "):
                self.active = not self.active
