#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved
import GLXCurses
import curses
from curses import A_BOLD, A_REVERSE, KEY_ENTER, BUTTON1_RELEASED, BUTTON1_CLICKED, BUTTON1_PRESSED


class MenuItem(GLXCurses.Widget):
    def __init__(self):
        GLXCurses.Widget.__init__(self)
        self.__text = None
        self.__spacing = None
        self.__text_short_cut = None
        self.__is_accel = None
        self.__have_cross_a_accel = None

        self.spacing = 1
        self.can_focus = True
        self.can_prelight = True
        self.can_default = True
        self.debug = True

        # Subscription
        # Mouse
        self.connect('MOUSE_EVENT', MenuItem._handle_mouse_event)
        # Keyboard
        self.connect('CURSES', MenuItem._handle_key_event)

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text=None):
        if text is not None and type(text) != str:
            raise TypeError('"text" must be a str type or None')
        if self.text != text:
            self.__text = text
            self._update_sizes()

    @property
    def text_short_cut(self):
        return self.__text_short_cut

    @text_short_cut.setter
    def text_short_cut(self, text=None):
        if text is not None and type(text) != str:
            raise TypeError('"text" must be a str type or None')
        if self.text_short_cut != text:
            self.__text_short_cut = text
            self._update_sizes()

    @property
    def spacing(self):
        return self.__spacing

    @spacing.setter
    def spacing(self, spacing=None):
        if spacing is not None and type(spacing) != int:
            raise TypeError('"spacing" must be a int type or None')
        if self.spacing != GLXCurses.clamp_to_zero(spacing):
            self.__spacing = GLXCurses.clamp_to_zero(spacing)
            self._update_sizes()

    @property
    def resized_text(self):
        return GLXCurses.resize_text(self.text, self.width - (self.spacing * 2), '~')

    @property
    def resized_text_short_cut(self):
        return GLXCurses.resize_text(
            self.text_short_cut,
            self.width - 1 - len(self.resized_text) + self.accelerator_size - (self.spacing * 2),
            '~'
        )

    @property
    def is_accel(self):
        return self.__is_accel

    @is_accel.setter
    def is_accel(self, value=None):
        if value is None:
            value = False
        if type(value) != bool:
            raise TypeError('"value" must be a bool type or None')
        if self.is_accel != value:
            self.__is_accel = value

    @property
    def accelerator_size(self):
        return self.__have_cross_a_accel

    @accelerator_size.setter
    def accelerator_size(self, value=None):
        if value is None:
            value = 0
        if type(value) != int:
            raise TypeError('"value" must be a int type or None')
        if self.accelerator_size != value:
            self.__have_cross_a_accel = value

    @property
    def color(self):
        if self.is_accel:
            if self.has_prelight or self.has_default:
                self.__is_accel = False
                return self.style.color(fg='YELLOW', bg='BLACK')
            else:
                self.__is_accel = False
                return self.style.color(fg='YELLOW', bg='CYAN')
        else:
            if GLXCurses.Application().has_prelight:
                if GLXCurses.Application().has_prelight.id == self.id:
                    return self.style.color(fg='BLACK', bg='WHITE') | A_REVERSE
                else:
                    return self.style.color(fg='GRAY', bg='CYAN')
            else:
                return self.style.color(fg='GRAY', bg='CYAN')

    def draw(self):
        self.create_or_resize()
        self._update_sizes()
        if self.subwin:
            self._draw_background()
            pos = 0
            if self.spacing:
                self._draw_spacing(pos)
                pos += 1
            if self.text:
                self._draw_text(pos)
                pos += len(self.resized_text)
            # if self.spacing:
            #     self._draw_spacing(pos)
            #     pos += 1
            if self.text_short_cut:
                self._draw_text_short_cut()
                # if self.spacing:
                #     self._draw_spacing(self.width - 1)
                #     pos += 1

    def _draw_text_short_cut(self):
        for x_inc in range(0, len(self.resized_text_short_cut)):
            try:
                self.subwin.delch(0, self.width - self.spacing - len(self.resized_text_short_cut) + x_inc)
                self.subwin.insch(0,
                                  self.width - self.spacing - len(self.resized_text_short_cut) + x_inc,
                                  self.resized_text_short_cut[x_inc],
                                  self.color
                                  )
            except curses.error:  # pragma: no cover
                pass

    def _draw_text(self, pos):
        self.accelerator_size = 0
        for x_inc in range(0, len(self.resized_text)):
            try:
                if self.resized_text[x_inc] == '_':
                    self.is_accel = True
                    self.accelerator_size += 1
                    continue

                self.subwin.delch(0, pos + x_inc - self.accelerator_size)
                self.subwin.insch(0,
                                  pos + x_inc - self.accelerator_size,
                                  self.resized_text[x_inc],
                                  self.color
                                  )

            except curses.error:  # pragma: no cover
                pass

    def _draw_spacing(self, pos):
        try:
            self.subwin.delch(0, pos)
            self.subwin.insch(0,
                              pos,
                              ' ',
                              self.color
                              )

        except curses.error:  # pragma: no cover
            pass

    def _draw_background(self):
        for y_inc in range(0, self.height):
            for x_inc in range(0, self.width):
                try:
                    self.subwin.delch(y_inc, x_inc)
                    self.subwin.insch(
                        y_inc,
                        x_inc,
                        ' ',
                        self.color
                    )
                except curses.error:  # pragma: no cover
                    pass

    def _update_sizes(self):
        self.height = 1
        self.preferred_height = 1

        self.preferred_width = 0
        if self.spacing and self.text_short_cut:
            self.preferred_width += self.spacing
        if self.text:
            self.preferred_width += len(self.text)
        if self.text_short_cut:
            if self.spacing:
                self.preferred_width += self.spacing * 3
            self.preferred_width += len(self.text_short_cut)
        if self.spacing and self.text_short_cut:
            self.preferred_width += self.spacing

    def _check_selected(self):
        if self.can_default:
            if GLXCurses.Application().has_default and GLXCurses.Application().has_default.widget.id == self.id:
                self.has_default = True
            else:
                self.has_default = False

        if self.can_focus:
            if GLXCurses.Application().has_focus and GLXCurses.Application().has_focus.widget.id == self.id:
                self.has_focus = True
            else:
                self.has_focus = False

        if self.can_prelight:
            if GLXCurses.Application().has_prelight and GLXCurses.Application().has_prelight.widget.id == self.id:
                self.has_prelight = True
            else:
                self.has_prelight = False

    def _grab_focus(self):
        """
        Internal method, for Select the contents of the Entry it take focus.

        See: grab_focus_without_selecting ()
        """
        if self.can_focus:
            GLXCurses.Application().has_focus = self
        if self.can_default:
            GLXCurses.Application().has_default = self
        if self.can_prelight:
            GLXCurses.Application().has_prelight = self

        self._check_selected()

    def _handle_mouse_event(self, event_signal, event_args):
        if self.sensitive:
            (mouse_event_id, x, y, z, event) = event_args
            # Be sure we select really the Button
            y -= self.y
            x -= self.x
            if 0 <= y <= self.height - 1:
                if 0 <= x <= self.x + self.width - 1:
                    # We are sure about the ToolBar have been clicked
                    self._grab_focus()
                    if event == BUTTON1_PRESSED:
                        self._grab_focus()

                    if event == BUTTON1_CLICKED or event == BUTTON1_RELEASED:
                        self.selected_menu = 0
                        self.selected_menu_item = 0
                        GLXCurses.Application().has_focus = None
                        GLXCurses.Application().has_default = None
                        GLXCurses.Application().has_prelight = None
                        self._check_selected()
                        instance = {
                            'class': self.__class__.__name__,
                            'id': self.id,
                            'event_signal': 'CLICKED'
                        }
                        self.emit(instance['event_signal'], instance)

    def _handle_key_event(self, event_signal, *event_args):
        # Check if we have to care about keyboard event
        import curses
        if self.can_focus and self.has_focus:
            # setting
            key = event_args[0]
            # Touch Escape
            if key == GLXCurses.GLXC.KEY_ESC:
                self.selected_menu = 0
                self.selected_menu_item = 0
                GLXCurses.Application().has_focus = None
                GLXCurses.Application().has_default = None
                GLXCurses.Application().has_prelight = None
                self.has_focus = False
                self.has_prelight = False
                self.has_default = False

            if key == KEY_ENTER or ord('\n'):
                self.selected_menu = 0
                self.selected_menu_item = 0
                GLXCurses.Application().has_focus = None
                GLXCurses.Application().has_default = None
                GLXCurses.Application().has_prelight = None
                self.has_focus = False
                self.has_prelight = False
                self.has_default = False
                instance = {
                    'class': self.__class__.__name__,
                    'id': self.id,
                    'event_signal': 'CLICKED'
                }
                self.emit(instance['event_signal'], instance)
