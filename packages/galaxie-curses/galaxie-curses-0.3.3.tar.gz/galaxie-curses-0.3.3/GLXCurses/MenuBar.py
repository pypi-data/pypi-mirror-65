#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import GLXCurses
import logging
from curses import error as curses_error
from curses import A_BOLD, KEY_DOWN, KEY_UP
from curses import A_REVERSE
from curses import KEY_LEFT
from curses import KEY_RIGHT
from curses import BUTTON1_RELEASED
import curses

class MenuBar(GLXCurses.Box, GLXCurses.Dividable):
    def __init__(self):
        # Load heritage
        GLXCurses.Box.__init__(self)
        GLXCurses.Dividable.__init__(self)

        self.glxc_type = 'GLXCurses.{0}'.format(self.__class__.__name__)
        self.name = '{0}{1}'.format(self.__class__.__name__, self.id)

        self.__info_label = None
        self.__selected_menu = None
        self.__selected_menu_item = None

        # Internal Widget Setting
        self.can_focus = True
        self.can_default = True
        self.can_prelight = True
        self.spacing = 4

        self.info_label = None
        self.selected_menu = 0
        self.selected_menu_item = 0
        self.list_machin = []

        # Cab be remove
        self.debug = True

        # Subscription
        # Mouse
        self.connect('MOUSE_EVENT', MenuBar._handle_mouse_event)
        # Keyboard
        self.connect('CURSES', MenuBar._handle_key_event)

    @property
    def info_label(self):
        return self.__info_label

    @info_label.setter
    def info_label(self, text=None):
        if text is not None and type(text) != str:
            raise TypeError('"text" must be a str type or None')
        if self.info_label != text:
            self.__info_label = text

    @property
    def selected_menu(self):
        return self.__selected_menu

    @selected_menu.setter
    def selected_menu(self, selected_menu=None):
        if selected_menu is not None and type(selected_menu) != int:
            raise TypeError('"selected_menu" must be a int type or None')
        if self.selected_menu != selected_menu:
            self.__selected_menu = selected_menu

    @property
    def selected_menu_item(self):
        return self.__selected_menu_item

    @selected_menu_item.setter
    def selected_menu_item(self, selected_menu_item=None):
        if selected_menu_item is None:
            selected_menu_item = 0
        if selected_menu_item is not None and type(selected_menu_item) != int:
            raise TypeError('"selected_menu_item" must be a int type or None')
        if self.selected_menu_item != selected_menu_item:
            self.__selected_menu_item = selected_menu_item

    def draw_widget_in_area(self):
        """
        White the menubar to the stdscr, the location is imposed to top left corner
        """
        self.create_or_resize()
        self._check_selected()
        self._update_sizes()
        self._update_preferred_sizes()
        if self.subwin:
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
            self._draw_background()
            self._draw_menu_bar()
            self._draw_info_label()

    def _update_preferred_sizes(self):
        self.preferred_height = self.height
        self.preferred_width = self.width

    def _update_sizes(self):
        self.start = self.x
        self.stop = self.width - 1
        self.num = len(self.children)
        self.round_type = GLXCurses.GLXC.ROUND_DOWN

        self._upgrade_position()

    def _upgrade_position(self):

        pos = 0
        for child in self.children:
            if child.widget.title is not None:
                self.list_machin.append({'start': pos + 1, 'stop': pos + len(child.widget.title) + self.spacing})
                pos += len(child.widget.title) + self.spacing

    def _check_selected(self):
        if self.can_default:
            if GLXCurses.Application().has_default:
                if GLXCurses.Application().has_default.id == self.id:
                    self.has_default = True
                else:
                    self.has_default = False
        if self.can_focus:
            if GLXCurses.Application().has_focus:
                if GLXCurses.Application().has_focus.id == self.id:
                    self.has_focus = True
                else:
                    self.has_focus = False
        if self.can_prelight:
            if GLXCurses.Application().has_prelight:
                if GLXCurses.Application().has_prelight.id == self.id:
                    self.has_prelight = True
                    try:
                        GLXCurses.Application().has_prelight = self.children[self.selected_menu].widget.children[0].widget
                    except IndexError:
                        pass
                else:
                    self.has_prelight = False

    def _grab_focus(self):
        """
        Internal method, for Select the contents of the Entry it take focus.

        See: grab_focus_without_selecting ()
        """
        if self.can_focus:
            if GLXCurses.Application().has_focus is None or \
                    GLXCurses.Application().has_focus and \
                    GLXCurses.Application().has_focus.id != self.id:
                self.selected_menu = 0
                self.selected_menu_item = 0

            GLXCurses.Application().has_focus = self
        if self.can_default:
            GLXCurses.Application().has_default = self
        if self.can_prelight:
            GLXCurses.Application().has_prelight = self

        self._check_selected()

    def _draw_info_label(self):
        if self.info_label:
            text = GLXCurses.resize_text(self.info_label, self.width, '~')
            for x_inc in range(0, len(text)):
                try:
                    self.subwin.delch(0, self.width - len(text) + x_inc)
                    self.subwin.insstr(0,
                                       self.width - len(text) + x_inc,
                                       text[x_inc],
                                       self.style.color(fg='BLACK', bg='CYAN') | A_BOLD)
                except curses.error:  # pragma: no cover
                    pass

    def _draw_background(self):
        self.subwin.bkgd(ord(' '), self.style.color(fg='BLACK', bg='CYAN'))
        self.subwin.bkgdset(ord(' '), self.style.color(fg='BLACK', bg='CYAN'))

    def _draw_menu_bar(self):
        if self.children:
            self.start = self.x
            self.stop = self.width
            self.num = len(self.children)
            self.round_type = GLXCurses.GLXC.ROUND_DOWN

            count = 0
            shortcut_to_display = False

            if not self.children:
                return

            for child in self.children:
                box_spacing = 0
                if child.widget.decorated:
                    box_spacing = 2
                if self.can_focus and self.has_focus:
                    if self.selected_menu is not None and self.selected_menu == count:
                        color_shortcut = self.style.color(fg='YELLOW', bg='BLACK')
                        color_base = self.style.color(fg='BLACK', bg='WHITE') | A_REVERSE
                        if len(child.widget.children) > 0:
                            child.widget.parent = self
                            child.widget.x = GLXCurses.Application().x
                            child.widget.y = GLXCurses.Application().y
                            child.widget.x_offset = self.list_machin[count]['start'] - 1
                            child.widget.width = self.width
                            child.widget.height = GLXCurses.clamp(len(child.widget.children) + box_spacing,
                                                                  0,
                                                                  GLXCurses.Application().height)
                            child.widget.x_offset = GLXCurses.clamp(
                                child.widget.x_offset,
                                0,
                                self.width - child.widget.preferred_width
                            )
                            for sub_child in child.widget.children:
                                sub_child.widget.x = child.widget.x_offset

                            child.widget.stdscr = self.stdscr
                            child.widget.draw()
                    else:
                        color_shortcut = self.style.color(fg='YELLOW', bg='CYAN')
                        color_base = self.style.color(fg='GRAY', bg='CYAN')
                else:
                    color_shortcut = self.style.color(fg='BLACK', bg='CYAN')
                    color_base = self.style.color(fg='BLACK', bg='CYAN')

                if child.widget.title is not None:
                    # Draw one dark before
                    try:
                        self.subwin.delch(0, self.list_machin[count]['start'])
                        self.subwin.insch(0,
                                          self.list_machin[count]['start'],
                                          ' ',
                                          color_shortcut)
                    except curses.error:  # pragma: no cover
                        pass
                    for x_inc in range(0, len(child.widget.title)):
                        if child.widget.title[x_inc] == '_':
                            shortcut_to_display = True
                            continue
                        if shortcut_to_display:
                            try:
                                self.subwin.delch(0, self.list_machin[count]['start'] + x_inc)
                                self.subwin.insch(0,
                                                  self.list_machin[count]['start'] + x_inc,
                                                  child.widget.title[x_inc],
                                                  color_shortcut)
                            except curses.error:  # pragma: no cover
                                pass
                            shortcut_to_display = False
                        else:
                            try:
                                self.subwin.delch(0, self.list_machin[count]['start'] + x_inc)
                                self.subwin.insch(0,
                                                  self.list_machin[count]['start'] + x_inc,
                                                  child.widget.title[x_inc],
                                                  color_base)
                            except curses.error:  # pragma: no cover
                                pass

                    # Draw one dark after
                    try:
                        self.subwin.delch(0,
                                          self.list_machin[count]['start'] + len(child.widget.title))
                        self.subwin.insch(0,
                                          self.list_machin[count]['start'] + len(child.widget.title),
                                          ' ',
                                          color_shortcut)
                    except curses.error:  # pragma: no cover
                        pass
                count += 1

    def _handle_mouse_event(self, event_signal, event_args):
        if self.sensitive:
            (mouse_event_id, x, y, z, event) = event_args
            # Be sure we select really the Button
            y -= self.y
            x -= self.x
            if 0 <= y <= self.height - 1:
                if 0 <= x <= self.preferred_width - 1:
                    # We are sure about the ToolBar have been clicked
                    self._grab_focus()

                    if self.children is not None:
                        count = 0
                        for child in self.children:
                            if self.list_machin[count]['start'] <= x <= self.list_machin[count]['start'] + len(
                                    child.widget.title):
                                self.selected_menu = count
                                GLXCurses.Application().has_prelight = child.widget.children[0].widget

                                if event == GLXCurses.GLXC.BUTTON1_CLICKED or event == BUTTON1_RELEASED:
                                    self.emit('BUTTON1_CLICKED', {'class': self.__class__.__name__,
                                                                  'id': self.id,
                                                                  'event_signal': 'F1_CLICKED'
                                                                  })
                            count += 1

    def _handle_key_event(self, event_signal, *event_args):
        # Check if we have to care about keyboard event
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

            if key == KEY_RIGHT:
                if self.selected_menu + 1 > len(self.children) - 1:
                    self.selected_menu = 0
                    self.selected_menu_item = 0
                else:
                    self.selected_menu += 1
                    self.selected_menu_item = 0
                # count = 0
                # for child in self.children:
                #     if self.selected_menu = count:
                GLXCurses.Application().has_prelight = self.children[self.selected_menu].widget.children[0].widget

            if key == KEY_LEFT:
                if self.selected_menu - 1 < 0:
                    self.selected_menu = len(self.children) - 1
                    self.selected_menu_item = 0
                else:
                    self.selected_menu -= 1
                    self.selected_menu_item = 0
                GLXCurses.Application().has_prelight = self.children[self.selected_menu].widget.children[0].widget

            if key == KEY_UP:
                if self.children:
                    for child in self.children:
                        if child.properties.position == self.selected_menu:
                            if child.widget.children:
                                if self.selected_menu_item - 1 < 0:
                                    self.selected_menu_item = len(child.widget.children) - 1
                                else:
                                    self.selected_menu_item -= 1
                                GLXCurses.Application().has_prelight = child.widget.children[
                                    self.selected_menu_item].widget

            if key == KEY_DOWN:
                if self.children:
                    for child in self.children:
                        if child.properties.position == self.selected_menu:
                            if child.widget.children:
                                if self.selected_menu_item + 1 > len(child.widget.children) - 1:
                                    self.selected_menu_item = 0
                                else:
                                    self.selected_menu_item += 1
                                GLXCurses.Application().has_prelight = child.widget.children[
                                    self.selected_menu_item].widget
