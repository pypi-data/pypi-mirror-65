#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import GLXCurses
import logging
import curses


class Menu(GLXCurses.Window, GLXCurses.Movable, GLXCurses.Box):

    def __init__(self):
        # Load heritage
        GLXCurses.Window.__init__(self)
        GLXCurses.Box.__init__(self)
        GLXCurses.Movable.__init__(self)

        self.glxc_type = 'GLXCurses.{0}'.format(self.__class__.__name__)
        self.name = '{0}{1}'.format(self.__class__.__name__, self.id)
        self.color = self.style.color(fg='WHITE', bg='CYAN')
        #self.selected_menu_item = 0

        # Default Setting
        self.decorated = True

        # Subscription
        self.connect('BUTTON1_CLICKED', Menu._handle_mouse_event)  # Mouse Button
        self.connect('BUTTON1_RELEASED', Menu._handle_mouse_event)
        # Keyboard
        self.connect('CURSES', Menu._handle_key_event)

        self.debug = True

    def _handle_mouse_event(self, event_signal, event_args=None):
        if event_args is None:
            event_args = dict()

    def _handle_key_event(self, event_signal, *event_args):
        # Check if we have to care about keyboard event
        if self.can_focus and self.has_focus:
            # setting
            key = event_args[0]
            # Touch Escape
            if key == GLXCurses.GLXC.KEY_ESC:
                GLXCurses.Application().has_focus = None
                GLXCurses.Application().has_default = None
                GLXCurses.Application().has_prelight = None
                self.has_focus = False
                self.has_prelight = False
                self.has_default = False

    def _update_preferred_sizes(self):
        self.preferred_width = GLXCurses.clamp(self._get_estimated_preferred_width(), 0, self.width)
        self.preferred_height = GLXCurses.clamp(self._get_estimated_preferred_height(), 0, self.height)

    def _update_preferred_position(self):
        pass
        # if self.parent and isinstance(self.parent, GLXCurses.MenuBar):
        #     self.y_offset = 1
        # self.y_offset = self.height
        # self.y_offset -= int(self.height / 2)
        # self.y_offset -= int(self.preferred_height / 2)
        #
        # self.x_offset = self.width
        # self.x_offset -= int(self.width / 2)
        # self.x_offset -= int(self.preferred_width / 2)

    def _get_estimated_preferred_width(self):
        """
        Estimate a preferred width, by consider X Location, allowed width

        :return: a estimated preferred width
        :rtype: int
        """
        estimated_preferred_width = 0
        if self.decorated:
            estimated_preferred_width += 3
        # Spacing
        #estimated_preferred_width += 2

        content_area_width = 0
        if self.children:
            for child in self.children:
                if child.widget.preferred_width > content_area_width:
                    content_area_width = child.widget.preferred_width

        if self.title:
            estimated_preferred_width += max(content_area_width, len(self.title))
        else:
            estimated_preferred_width += max(content_area_width, 0)

        return estimated_preferred_width

    def _get_estimated_preferred_height(self):
        """
        Estimate a preferred height, by consider Y Location

        :return: a estimated preferred height
        :rtype: int
        """
        estimated_preferred_height = 0
        if self.decorated:
            estimated_preferred_height += 2
        if self.children:
            for _ in self.children:
                estimated_preferred_height += 1

        # space_to_add = 0
        # if GLXCurses.Application().messagebar:
        #     estimated_preferred_height -= 1
        # if GLXCurses.Application().statusbar:
        #     estimated_preferred_height -= 1
        # if GLXCurses.Application().toolbar:
        #     estimated_preferred_height -= 1

        return estimated_preferred_height

    def draw_widget_in_area(self):
        # Create the subwin
        self.create_or_resize()
        self._update_preferred_sizes()
        self._update_preferred_position()

        if self.subwin:
            # Draw the child.
            if self.children is not None:
                self._draw_background()

                box_spacing = 0
                if self.decorated:
                    self._draw_box()
                    box_spacing = 2

                count = 0
                for child in self.children:
                    if count < self.preferred_height - box_spacing:
                        # if isinstance(self.parent, GLXCurses.MenuBar):
                            # if child.properties.position == self.selected_menu_item:
                            #     GLXCurses.Application().has_prelight = child.widget
                        child.widget.parent = self
                        child.widget.stdscr = self.stdscr

                        if self.decorated:
                            child.widget.x = self.x_offset + 1
                            if self.parent and isinstance(self.parent, GLXCurses.MenuBar):
                                child.widget.y = self.y_offset + 1 + child.properties.position + 1
                            else:
                                child.widget.y = self.y_offset + 1 + child.properties.position
                            child.widget.width = self.preferred_width - 2
                            child.widget.height = self.preferred_height - 2
                            to_remove = 0

                            # to_remove = 0
                            # while (child.widget.x + child.widget.preferred_width) - to_remove > self.width:
                            #     to_remove += 1
                            # child.widget.x -= to_remove

                            # child.widget.x -= to_remove
                        else:
                            child.widget.x = self.x_offset
                            if self.parent and isinstance(self.parent, GLXCurses.MenuBar):
                                child.widget.y = self.y_offset + child.properties.position + 1
                            else:
                                child.widget.y = self.y_offset + child.properties.position
                            child.widget.width = self.preferred_width - 1
                            child.widget.height = self.preferred_height - 1

                        if self.debug:
                            logging.debug("Set child -> x: {0}, y: {1}, width: {2}, height:{3}".format(
                                child.widget.x,
                                child.widget.y,
                                child.widget.width,
                                child.widget.height))

                        child.widget.draw()
                    count += 1

    def _draw_background(self, fg='BLACK', bg='CYAN'):
        for y_inc in range(self.y_offset, self.y_offset + self.preferred_height):
            for x_inc in range(self.x_offset, self.x_offset + self.preferred_width):
                try:
                    self.subwin.delch(y_inc, x_inc)
                    self.subwin.insch(y_inc, x_inc, ' ', self.style.color(fg=fg, bg=bg))
                except curses.error:  # pragma: no cover
                    pass

    def _draw_title(self):
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

    def _draw_box_bottom(self, char=None):
        # Bottom
        if char is None:
            char = curses.ACS_HLINE
        for x_inc in range(self.x_offset + 1, self.x_offset + self.preferred_width - 1):
            try:
                self.subwin.delch(self.y_offset + self.preferred_height - 1, x_inc)
                self.subwin.insch(
                    self.y_offset + self.preferred_height - 1,
                    x_inc,
                    char,
                    self.color
                )

            except curses.error:  # pragma: no cover
                pass

    def _draw_box_top(self, char=None):
        # Top
        if char is None:
            char = curses.ACS_HLINE

        for x_inc in range(self.x_offset + 1, self.x_offset + self.preferred_width - 1):
            try:
                self.subwin.delch(self.y_offset, x_inc)
                self.subwin.insch(
                    self.y_offset,
                    x_inc,
                    char,
                    self.color
                )
            except curses.error:  # pragma: no cover
                pass

    def _draw_box_right_side(self, char=None):
        # Right side
        if char is None:
            char = curses.ACS_VLINE

        for y_inc in range(0 + 1, self.preferred_height - 1):
            try:
                self.subwin.delch(self.y_offset + y_inc, self.x_offset + self.preferred_width - 1)
                self.subwin.insch(
                    self.y_offset + y_inc,
                    self.x_offset + self.preferred_width - 1,
                    char,
                    self.color
                )
            except curses.error:  # pragma: no cover
                pass

    def _draw_box_left_side(self, char=None):
        # Left side
        if char is None:
            char = curses.ACS_VLINE

        for y_inc in range(0 + 1, self.preferred_height - 1):
            try:
                self.subwin.delch(self.y_offset + y_inc, self.x_offset + 1)
                self.subwin.insch(
                    self.y_offset + y_inc,
                    self.x_offset,
                    char,
                    self.color
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
            self.subwin.delch(self.y_offset, self.preferred_width + self.x_offset - 1)
            self.subwin.insch(
                self.y_offset,
                self.preferred_width + self.x_offset - 1,
                char,
                self.color
            )
        except curses.error:  # pragma: no cover
            pass

    def _draw_box_upper_left_corner(self, char=None):
        # Upper-left corner
        if char is None:
            char = curses.ACS_ULCORNER
        try:
            self.subwin.delch(self.y_offset, self.x_offset)
            self.subwin.insch(
                self.y_offset,
                self.x_offset,
                char,
                self.color
            )
        except curses.error:  # pragma: no cover
            pass

    def _draw_box_bottom_right_corner(self, char=None):
        # Bottom-right corner
        if char is None:
            char = curses.ACS_LRCORNER
        try:
            self.subwin.delch(self.y_offset + self.preferred_height - 1, self.x_offset + self.preferred_width - 1)
            self.subwin.insch(
                self.y_offset + self.preferred_height - 1,
                self.x_offset + self.preferred_width - 1,
                char,
                self.color
            )
        except curses.error:  # pragma: no cover
            pass

    def _draw_box_bottom_left_corner(self, char=None):
        # Bottom-left corner
        if char is None:
            char = curses.ACS_LLCORNER
        try:
            self.subwin.delch(self.y_offset + self.preferred_height - 1, self.x_offset)
            self.subwin.insch(
                self.y_offset + self.preferred_height - 1,
                self.x_offset,
                char,
                self.color
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
                self.color
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
                self.color
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
                    self.color
                )

            except curses.error:  # pragma: no cover
                pass

    @staticmethod
    def remove_accel_group():
        pass

    @staticmethod
    def add_accel_group():
        pass
