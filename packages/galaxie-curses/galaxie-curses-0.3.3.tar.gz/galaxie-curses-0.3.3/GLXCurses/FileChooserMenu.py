#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved
import GLXCurses


class FileChooserMenu(GLXCurses.Container, GLXCurses.Movable):

    def __init__(self, parent=None, y=None, x=None, label=None):
        GLXCurses.Container.__init__(self)
        GLXCurses.Movable.__init__(self)
        self.parent = GLXCurses.Application()
        self.stdscr = GLXCurses.Application().stdscr
        self.y_parent, self.x_parent = self.stdscr.getbegyx()
        # self.y_parent = self.parent.y
        # self.x_parent = self.parent.x
        self.y_max_parent, self.x_max_parent = self.stdscr.getmaxyx()
        self.y = y
        self.x = x
        self.label = str(label)
        self.label = str(" " + label + " ")
        self.Width = len(str(label))

        self.history_dir_list = []
        # Look for history window size it depend of the history list
        if len(parent.history_dir_list) + 2 < self.y_max_parent:
            history_y = len(parent.history_dir_list) + 2

        else:
            history_y = self.y_max_parent - 1

        if len(parent.history_dir_list) > 0:
            history_x = len(max(parent.history_dir_list, key=len)) + 2
            if history_x > self.x_max_parent - 1:
                history_x = self.x_max_parent
        else:
            history_x = len(self.label) + 2

        history_box = self.stdscr.subwin(
            history_y,
            history_x,
            2,
            0
        )

        # Inside the history menu
        history_box.bkgdset(
            ord(' '),
            parent.style.color(
                fg=parent.style.get_color_text('dark', 'STATE_NORMAL'),
                bg=parent.style.get_color_text('base', 'STATE_NORMAL')
            )
        )
        history_box.bkgd(
            ord(' '),
            parent.style.color(
                fg=parent.style.get_color_text('dark', 'STATE_NORMAL'),
                bg=parent.style.get_color_text('base', 'STATE_NORMAL')
            )
        )

        history_box_num_lines, history_box_num_cols = history_box.getmaxyx()
        max_cols_to_display = history_box_num_cols - 2
        max_lines_to_display = 1

        for I in range(0, history_box_num_lines - 2):
            history_box.addstr(I + 1,
                               1,
                               str(" " * int(history_box_num_cols - 2)),
                               parent.style.color(
                                   fg=parent.style.get_color_text('dark', 'STATE_NORMAL'),
                                   bg=parent.style.get_color_text('base', 'STATE_NORMAL')
                               )
                               )
            max_lines_to_display += 1
        parent.history_menu_can_be_display = max_lines_to_display

        for I in range(0 + parent.history_menu_item_list_scroll, parent.history_menu_can_be_display):
            if I < len(parent.history_dir_list):

                if parent.history_menu_selected_item == I:
                    parent.history_menu_selected_item_value = parent.history_dir_list[I]
                    if len(str(parent.history_dir_list[I])) >= max_cols_to_display:
                        history_box.addstr(
                            I + 1,
                            1,
                            str(parent.history_dir_list[I][:max_cols_to_display]),
                            parent.style.color(
                                fg='BLUE',
                                bg=parent.style.get_color_text('bg', 'STATE_SELECTED')
                            )
                        )
                    else:
                        history_box.addstr(
                            I + 1,
                            1,
                            str(parent.history_dir_list[I]),
                            parent.style.color(
                                fg='BLUE',
                                bg=parent.style.get_color_text('bg', 'STATE_SELECTED')
                            )
                        )
                        history_box.addstr(
                            I + 1,
                            len(str(parent.history_dir_list[I])) + 1,
                            str(" " * int(
                                history_box_num_cols - 2 - len(str(parent.history_dir_list[I])))),
                            parent.style.color(
                                fg='BLUE',
                                bg=parent.style.get_color_text('bg', 'STATE_SELECTED')
                            )
                        )
                else:
                    if len(str(parent.history_dir_list[I])) >= max_cols_to_display:
                        history_box.addstr(
                            I + 1,
                            1,
                            str(parent.history_dir_list[I][:max_cols_to_display]),
                            parent.style.color(
                                fg=parent.style.get_color_text('dark', 'STATE_NORMAL'),
                                bg=parent.style.get_color_text('base', 'STATE_NORMAL')
                            )
                        )
                    else:
                        history_box.addstr(
                            I + 1,
                            1,
                            str(parent.history_dir_list[I]),
                            parent.style.color(
                                fg=parent.style.get_color_text('dark', 'STATE_NORMAL'),
                                bg=parent.style.get_color_text('base', 'STATE_NORMAL')
                            )
                        )

        history_box.box()
        # Title
        history_box.addstr(
            0,
            (int(history_box_num_cols / 2)) - int((len(self.label) / 2)),
            self.label,
            parent.style.color(
                fg='BLUE',
                bg=parent.style.get_color_text('base', 'STATE_NORMAL')
            )
        )

    def mouse_clicked(self, mouse_event):
        (event_id, x, y, z, event) = mouse_event
        if self.y_parent <= y <= self.y_parent + 1:
            if self.x + self.x_parent <= x < self.x + self.x_parent + self.Width:
                return 1
        else:
            return 0

