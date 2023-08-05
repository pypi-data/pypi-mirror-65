#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import GLXCurses
import curses


class ProgressBar(GLXCurses.Widget, GLXCurses.Movable):
    def __init__(self):
        # Load heritage
        GLXCurses.Widget.__init__(self)
        GLXCurses.Movable.__init__(self)

        self.name = '{0}{1}'.format(self.__class__.__name__, self.id)

        self.__text = None
        self.__show_text = None
        self.__value = None

        self.text = ''
        self.show_text = True
        self.value = 0
        self.bg = 'BLUE'
        self.fg = 'GRAY'

        # Interface
        self.interface = '[]'



    def color(self, pos=0):
        if int(len(self.interface) / 2) <= pos <= self.preferred_width - int(len(self.interface) / 2) and \
                pos - int(len(self.interface) / 2) < (self.preferred_width - len(self.interface)) * self.value / 100:
            return self.style.color(fg=self.fg, bg=self.bg) | curses.A_REVERSE

        return self.style.color(fg=self.fg, bg=self.bg)

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value=None):
        if value is not None and type(value) != str:
            raise TypeError('"text" value must be a str type or None')
        if self.__text != value:
            self.__text = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value=None):
        if value is None:
            value = 0
        if type(value) != int:
            raise TypeError('"value" must be a int type or None')
        if self.value != GLXCurses.clamp(value, 0, 100):
            self.__value = GLXCurses.clamp(value, 0, 100)
            self.text = '{0}%'.format(GLXCurses.clamp(value, 0, 100))

    @property
    def show_text(self):
        return self.__show_text

    @show_text.setter
    def show_text(self, value=None):
        if value is None:
            value = False
        if type(value) != bool:
            raise TypeError('"show_text" value must be a bool type or None')
        if self.show_text != value:
            self.__show_text = value

    def draw_widget_in_area(self):
        self.create_or_resize()

        if self.subwin:
            self.preferred_height = 1
            self.preferred_width = self.width

            self.check_position()
            # Background
            for x_inc in range(self.x_offset, self.preferred_width):
                try:
                    self.subwin.delch(self.y_offset,
                                      x_inc
                                      )
                    self.subwin.insch(self.y_offset,
                                      x_inc,
                                      ' ',
                                      self.style.color(fg=self.fg, bg=self.bg)
                                      )
                except curses.error:  # pragma: no cover
                    pass
            # Start interface
            for x_inc in range(0, len(self.interface[:int(len(self.interface) / 2)])):
                try:
                    self.subwin.delch(self.y_offset,
                                      self.x_offset + x_inc
                                      )
                    self.subwin.insch(self.y_offset,
                                      self.x_offset + x_inc,
                                      self.interface[:int(len(self.interface) / 2)][x_inc],
                                      self.color(pos=self.x_offset + x_inc)
                                      )
                except curses.error:  # pragma: no cover
                    pass

            # The bar
            x_inc = 0
            progress_text = str(' ' * int(self.preferred_width - len(self.interface)))
            for char in progress_text[:int((self.preferred_width - int(len(self.interface) / 2)) * self.value / 100)]:
                try:
                    self.subwin.delch(self.y_offset,
                                      self.x_offset + int(len(self.interface) / 2) + x_inc
                                      )
                    self.subwin.insch(self.y_offset,
                                      self.x_offset + int(len(self.interface) / 2) + x_inc,
                                      char,
                                      self.color(pos=self.x_offset + int(len(self.interface) / 2) + x_inc)
                                      )
                except curses.error:  # pragma: no cover
                    pass
                x_inc += 1

            # Text to display
            if self.show_text:
                message_to_display = GLXCurses.resize_text(self.text, self.width - len(self.interface), '~')
                for x_inc in range(0, len(message_to_display)):
                    try:
                        self.subwin.delch(self.y_offset,
                                          int(self.preferred_width / 2) - int(len(self.text) / 2) + x_inc
                                          )
                        self.subwin.insch(self.y_offset,
                                          int(self.preferred_width / 2) - int(len(self.text) / 2) + x_inc,
                                          message_to_display[x_inc],
                                          self.color(
                                              pos=int(self.preferred_width / 2) - int(len(self.text) / 2) + x_inc)
                                          )
                    except curses.error:  # pragma: no cover
                        pass

            # End Interface
            for x_inc in range(0, len(self.interface[-int(len(self.interface) / 2):])):
                try:
                    self.subwin.delch(self.y_offset,
                                      self.preferred_width - int(len(self.interface) / 2) + x_inc
                                      )
                    self.subwin.insch(self.y_offset,
                                      self.preferred_width - int(len(self.interface) / 2) + x_inc,
                                      self.interface[-int(len(self.interface) / 2):][x_inc],
                                      self.color(pos=self.preferred_width - int(len(self.interface) / 2) + x_inc)
                                      )
                except curses.error:  # pragma: no cover
                    pass