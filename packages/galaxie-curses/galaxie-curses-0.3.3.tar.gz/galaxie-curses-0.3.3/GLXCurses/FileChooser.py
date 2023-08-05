#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

"""
Created on 4 avr. 2015

@author: Tuuux
"""

import curses
import os
from operator import itemgetter
import time
import logging

import GLXCurses


class FileSelect(GLXCurses.Widget):

    def __init__(self):
        # Load heritage
        GLXCurses.Widget.__init__(self)

        # It's a GLXCurse Type
        self.glxc_type = 'GLXCurses.FileSelect'
        self.name = '{0}{1}'.format(self.__class__.__name__, self.id)

        # Make a Widget Style heritage attribute as local attribute
        # if self.style.attribute_states:
        #     if self.attribute_states != self.style.attribute_states:
        #         self.attribute_states = self.style.attribute_states

        # Variables:
        self.__sort_by_name = None
        self.__sort_name_order = None
        self.__sort_by_size = None
        self.__sort_size_order = None
        self.__sort_by_mtime = None
        self.__sort_mtime_order = None
        self.__item_list = None
        self.__item_info_list = None
        self.__item_it_can_be_display = None
        self.__item_scroll_pos = None
        self.__selected_item_pos = None
        self.__selected_item_info_list = None
        self.app_file_extensions = None

        # Object use for clickable Text
        self.name_text_object = None
        self.size_text_object = None
        self.mtime_text_object = None

        self.display_history_menu = 0
        self.display_history_text = 'History'
        self.history_dir_list_object = None
        self.history_dir_list_prev_object = None
        self.history_dir_list_next_object = None
        self.history_dir_list = list()
        self.history_menu_selected_item = 0
        self.history_menu_selected_item_value = "."
        self.history_menu_item_list_scroll = 0
        self.history_menu_can_be_display = 0
        self.history_menu_item_number = 0

        # Scroll

        # Set thing for the first time, yes like a boss ...
        self.sort_by_name = True
        self.sort_name_order = True
        self.sort_by_size = False
        self.sort_size_order = True
        self.sort_by_mtime = False
        self.sort_mtime_order = True

        self.item_it_can_be_display = 0
        self.item_scroll_pos = 0
        self.selected_item_pos = 0
        self.selected_item_info_list = list()

        # Size management
        self.border_len = 2

        # Mouse speed
        self.time_last_scroll_up = time.time()
        self.time_last_scroll_down = time.time()

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

        # self.model = model
        self.rep_sup_text = "UP--DIR"
        self.name_text = "Name"
        self.size_text = "Size"
        self.mtime_text = "Modify time"
        self.sort_name_letter = self.name_text[0].lower()
        self.sort_size_letter = self.size_text[0].lower()
        self.sort_mtime_letter = self.mtime_text[0].lower()
        self.history_button_text_prev = '<'
        self.history_button_text_list = '.[^]'
        self.history_button_text_next = '<'

        self._update_directory_list()

        # Sensitive
        self.can_default = True
        self.can_focus = True
        self.can_prelight = True
        self.sensitive = True
        self.states_list = None
        self._focus_without_selecting = False

        # Subscription
        # Mouse
        self.connect('MOUSE_EVENT', FileSelect._handle_mouse_event)
        # Keyboard
        self.connect('CURSES', FileSelect._handle_key_event)

    @property
    def sort_by_name(self):
        """
        Return sort_by_name attribute.

        :return: True if enable, False if disable
        :rtype: bool
        """
        return self.__sort_by_name

    @sort_by_name.setter
    def sort_by_name(self, boolean=True):
        """
        Set the sort_name_order attribute . It use for display files and directory sorted by name in order.

        Order are:
            True for A to Z
            False for Z to A

        :param boolean: True for A to Z, False for Z to A
        :type boolean: bool
        :raise TypeError: when ``boolean`` argument is not a bool type or None
        """
        if boolean is None:
            boolean = False
        if boolean is not None and type(boolean) != bool:
            raise TypeError("'boolean' must be a bool type")
        if self.sort_by_name != boolean:
            self.__sort_by_name = boolean

    @property
    def sort_name_order(self):
        """
        Return sort_name_order attribute.

        :return: True if ordering A to Z, False if ordering Z to A
        :rtype: bool
        """
        return self.__sort_name_order

    @sort_name_order.setter
    def sort_name_order(self, boolean=True):
        """
        Set the sort_name_order attribute . It use for display files and directory sorted by name in order.

        Order are:
            True for A to Z
            False for Z to A

        :param boolean: True for A to Z, False for Z to A
        :type boolean: bool
        :raise TypeError: when ``boolean`` argument is not a bool type
        """
        if boolean is None:
            boolean = False
        if type(boolean) != bool:
            raise TypeError("'boolean' must be a bool type or None")
        if self.sort_name_order != boolean:
            self.__sort_name_order = boolean

    @property
    def sort_by_size(self):
        """
        Return sort_by_size attribute.

        :return: True if enable, False if disable
        :rtype: bool
        """
        return self.__sort_by_size

    @sort_by_size.setter
    def sort_by_size(self, boolean=None):
        """
        Set the sort_by_size attribute . It use for display files and directory sorted by size.

        :param boolean: True for enable, False for disable
        :type boolean: bool
        :raise TypeError: when ``boolean`` argument is not a bool type
        """
        if boolean is None:
            boolean = False
        if type(boolean) != bool:
            raise TypeError("'boolean' must be a bool type")

        # just in case we make the job
        if self.sort_by_size != boolean:
            self.__sort_by_size = boolean

    @property
    def sort_size_order(self):
        """
        Return sort_by_size attribute. as set by set_sort_size_order()

        :return: True if enable, False if disable
        :rtype: bool
        """
        return self.__sort_size_order

    @sort_size_order.setter
    def sort_size_order(self, boolean=None):
        """
        Set the sort_size_order attribute . It use for display files and directory sorted by size in order.

        Order are:
            True: Min to Max
            False: Max to Min

        :param boolean: True if ordering Min to Max, False if ordering Max to Min.
        :type boolean: bool
        :raise TypeError: when ``boolean`` argument is not a bool type
        """
        if boolean is None:
            boolean = False
        if type(boolean) != bool:
            raise TypeError("'boolean' must be a bool type")
        if self.sort_size_order != boolean:
            self.__sort_size_order = boolean

    @property
    def sort_by_mtime(self):
        """
        Return sort_by_mtime attribute.

        :return: True if enable, False if disable
        :rtype: bool
        """
        return self.__sort_by_mtime

    @sort_by_mtime.setter
    def sort_by_mtime(self, boolean=None):
        """
        Set the sort_by_mtime attribute . It use for display files and directory sorted by mtime.

        :param boolean: True for enable, False for disable
        :type boolean: bool
        :raise TypeError: when ``boolean`` argument is not a bool type
        """
        if boolean is None:
            boolean = False
        if type(boolean) != bool:
            raise TypeError("'boolean' must be a bool type or None")
        if self.sort_by_mtime != boolean:
            self.__sort_by_mtime = boolean

    @property
    def sort_mtime_order(self):
        """
        Return sort_mtime_order attribute. as set by set_sort_mtime_order()

        :return: True if ordering Now to Ago, False if ordering Ago to Now.
        :rtype: bool
        """
        return self.__sort_mtime_order

    @sort_mtime_order.setter
    def sort_mtime_order(self, boolean=True):
        """
        Set the sort_size_order attribute . It use for display files and directory sorted by mtime in order.

        Order are:
            True: Now to Ago
            False: Ago to Now

        :param boolean: True if ordering Now to Ago, False if ordering Ago to Now.
        :type boolean: bool
        :raise TypeError: when ``boolean`` argument is not a bool type or None
        """
        if boolean is None:
            boolean = False
        if type(boolean) != bool:
            raise TypeError("'boolean' must be a bool type or None")
        if self.sort_mtime_order != boolean:
            self.__sort_mtime_order = boolean

    @property
    def item_list(self):
        """
        Set the files list.

        Note tha can't be None, that because _set_file_list() set a empty list.

        :return: the file list, internally use for list directory
        :rtype: list
        """
        return self.__item_list

    @item_list.setter
    def item_list(self, file_list=None):
        """
        Set the files list, internally use for list directory.

        Note that item_list=None will reset the list

        :param file_list: a file list
        :type file_list: list
        :raise TypeError: when ``item_list`` argument is not a list or None
        """
        if file_list is None:
            file_list = list()
        if type(file_list) != list:
            raise TypeError("'item_list' must be a list type")
        if self.item_list != file_list:
            self.__item_list = file_list

    @property
    def item_info_list(self):
        """
        Set the files list.

        Note tha can't be None, that because _set_file_list() set a empty list.

        :return: the file list, internally use for list directory
        :rtype: list
        """
        return self.__item_info_list

    @item_info_list.setter
    def item_info_list(self, list_item_info=None):
        """
        Set a item info list, internally use for store information about each item in a directory.

        Note that item_info_list=None will reset the list

        :param list_item_info: a file list
        :type list_item_info: list
        :raise TypeError: when ``item_info_list`` argument is not a list or None
        """
        # Reset the list in case that None
        if list_item_info is None:
            list_item_info = list()

        # Exit as soon of possible
        if type(list_item_info) != list:
            raise TypeError("'item_info_list' must be a list type")

        # just in case it make teh job
        if self.item_info_list != list_item_info:
            self.__item_info_list = list_item_info

    @property
    def item_it_can_be_display(self):
        """
        Get the number of item it can be display, as set by _set_item_it_can_be_display().

        :return: The number of item it can be display
        :rtype: int
        """
        return self.__item_it_can_be_display

    @item_it_can_be_display.setter
    def item_it_can_be_display(self, value=None):
        """
        Get the number of item it can be display

        :param value: the number of item it can be display
        :type value: int
        :raise TypeError: when ``value`` argument is not a int
        """
        if value is None:
            value = 0
        if type(value) != int:
            raise TypeError("'value' must be a int type or None")
        if self.item_it_can_be_display != value:
            self.__item_it_can_be_display = value

    @property
    def item_scroll_pos(self):
        """
        Get the number of item it can be display, as set by _set_item_it_can_be_display().

        :return: The Position on the scroll list
        :rtype: int
        """
        return self.__item_scroll_pos

    @item_scroll_pos.setter
    def item_scroll_pos(self, value=None):
        """
        Position on the scroll list. value=None for reset to 0.

        Default 0

        :param value: the position
        :type value: int or None
        :raise TypeError: when ``value`` argument is not a int or None
        """
        if value is None:
            value = 0

        # Exit as soon of possible
        if type(value) != int:
            raise TypeError("'value' must be a int type")

        # just in case it make teh job
        if self.item_scroll_pos != value:
            self.__item_scroll_pos = value

    @property
    def selected_item_pos(self):
        """
        Position of the selected item.

        :return: The Position on the scroll list
        :rtype: int
        """
        return self.__selected_item_pos

    @selected_item_pos.setter
    def selected_item_pos(self, value=None):
        """
        Position of the selected item in parallel of the scroll list.

        value=None for reset to 0.

        Default: 0

        :param value: the position
        :type value: int or None
        :raise TypeError: when ``value`` argument is not a int or None
        """
        if value is None:
            value = 0
        if type(value) != int:
            raise TypeError("'value' must be a int type")
        if self.selected_item_pos != value:
            self.__selected_item_pos = value

    @property
    def selected_item_info_list(self):
        """
        Get the selected file information's list.

        The file_info_list information's store position:
            item_name_text in position [0]
            item_path_sys in position [1]
            item_size_text in position [2]
            item_time_text in position [3]

        :return: information's about selected item.
        :rtype: list
        """
        return self.__selected_item_info_list

    @selected_item_info_list.setter
    def selected_item_info_list(self, file_info_list=None):
        """
        Set the files list, internally use for list directory.

        The file_info_list information's store position:
            item_name_text in position [0]
            item_path_sys in position [1])
            item_size_text in position [2]
            item_time_text in position [3]

        :param file_info_list: a file list
        :type file_info_list: list
        :raise TypeError: when ``file_info_list`` argument is not a list or None
        """
        if file_info_list is None:
            file_info_list = list()
        if type(file_info_list) != list:
            raise TypeError("'file_info_list' must be a list type")
        if self.selected_item_info_list != file_info_list:
            self.__selected_item_info_list = file_info_list

    @property
    def x_pos_history_next_label(self):
        if self.get_decorated():
            return GLXCurses.round_down(self.preferred_width - 1 - self.border_len / 2)
        else:
            return self.preferred_width - 1

    @property
    def x_pos_history_list_label(self):
        return self.x_pos_history_next_label - len(self.history_button_text_list)

    @property
    def x_pos_history_prev_label(self):
        if self.get_decorated():
            return GLXCurses.round_down(self.border_len / 2)
        else:
            return 0

    @property
    def x_pos_history_actual_path(self):
        return self.x_pos_history_prev_label + len(self.history_button_text_prev) + 1

    @property
    def x_pos_history_actual_path_allowed_size(self):
        return self.x_pos_history_next_label - self.x_pos_history_actual_path

    @property
    def x_pos_title_mtime(self):
        return GLXCurses.round_down(self.mtime_column_width + 1 + (len(str(self.mtime_text)) - 1 / 2) - 4)

    @property
    def x_pos_title_size(self):
        return GLXCurses.round_down(
            self.mtime_column_width - self.size_column_width + 1 + (len(str(self.size_text)) - 1 / 2))

    @property
    def x_pos_title_name(self):
        return GLXCurses.round_down(((self.mtime_column_width - self.size_column_width) / 2) - (
                len(self.name_text) / 2) + 1)

    @property
    def x_pos_line_start(self):
        if self.get_decorated():
            return GLXCurses.round_down(self.border_len / 2)
        else:
            return 0

    @property
    def x_pos_line_stop(self):
        if self.get_decorated():
            return GLXCurses.round_down(self.preferred_width - 1 - (self.border_len / 2) - 1)
        else:
            return self.preferred_width - 1 - 1

    @property
    def y_pos_history(self):
        return 0

    @property
    def y_pos_titles(self):
        return self.y_pos_history + 1

    @property
    def y_pos_items(self):
        return self.y_pos_titles + 1

    @property
    def name_column_width(self):
        if self.get_decorated():
            name_collumn_width = self.preferred_width
            name_collumn_width -= 16
            name_collumn_width -= self.size_column_width
            name_collumn_width -= 2
            name_collumn_width -= self.border_len
        else:
            name_collumn_width = self.preferred_width
            name_collumn_width -= 16
            name_collumn_width -= self.size_column_width
            name_collumn_width -= 2
        return name_collumn_width

    @property
    def mtime_column_width(self):
        if self.get_decorated():
            mtime_collumn_width = self.preferred_width - 1 - GLXCurses.round_down(self.border_len / 2)
            mtime_collumn_width -= len(time.strftime("%d/%m/%Y  %H:%M", time.localtime(time.time())))
        else:
            mtime_collumn_width = self.preferred_width - 1
            mtime_collumn_width -= len(time.strftime("%d/%m/%Y  %H:%M", time.localtime(time.time())))
        return GLXCurses.round_down(mtime_collumn_width)

    @property
    def size_column_width(self):
        return 8

    # Internal function
    def _scroll_up(self):
        if not self.selected_item_pos == 0:
            self.selected_item_pos -= 1
        elif not self.item_scroll_pos == 0:
            self.item_scroll_pos -= 1

    def _scroll_down(self):
        if not (self.item_it_can_be_display - 1) == self.selected_item_pos:
            if not self.__selected_item_pos == len(self.item_list) - 1:
                self.selected_item_pos += 1
        else:
            if self.item_scroll_pos + self.item_it_can_be_display < len(self.item_list):
                self.item_scroll_pos += 1

    def _history_scroll_up(self):
        if not self.history_menu_selected_item == 0:
            self.history_menu_selected_item -= 1
        else:
            if not self.history_menu_item_list_scroll == 0:
                self.history_menu_item_list_scroll -= 1

    def _history_scroll_down(self):
        if not self.history_menu_can_be_display == self.history_menu_selected_item \
                and not self.history_menu_selected_item + 1 == len(self.history_dir_list) \
                and not len(self.history_dir_list) == 0:
            self.history_menu_selected_item += 1
        else:
            if self.history_menu_item_list_scroll + self.history_menu_can_be_display < self.history_menu_item_number + 1:
                self.history_menu_item_list_scroll += 1

    def _get_item_info(self, file_path):
        """
        Return information list about a file pass as argument

        Index position and description:
            0 - Name to Display
            1 - Full Path
            2 - Size to Display
            3 - Time to Display
            4 - Size value used by the shorted process
            5 - Mtime value used by the shorted process
            6 - Small symbol
            7 - Color
            8 - Color_add

        :param file_path: a filename path
        :type file_path: str
        :return: a list with information's
        :raise TypeError: when ``file_path`` argument is not a :py:__area_data:`string`
        :raise IOError: when ``file_path`` does not exist
        """
        # Exit as soon of possible
        if type(file_path) != str:
            raise TypeError("'file_path' must be a str type")

        # if not os.path.exists(os.path.realpath(file_path)):
        #     raise FileNotFoundError("'%s' do not exist" % file_path)

        # 0 Name to Display
        if os.path.islink(file_path):
            name_to_display = os.path.basename(file_path) + ' -> ' + os.readlink(file_path)
        else:
            name_to_display = os.path.basename(file_path)

        # 1 Full Path
        full_path = os.path.abspath(file_path)

        # 2 Size to Display
        if os.path.basename(file_path) == "..":
            size_to_display = "UP--DIR"
        elif os.path.islink(file_path):
            st = os.lstat(file_path)
            size = GLXCurses.sizeof(st.st_size)
            size_to_display = size
        else:
            if os.path.isfile(file_path):
                st = os.lstat(file_path)
                size = GLXCurses.sizeof(st.st_size)
                size_to_display = size
            else:
                try:
                    x = os.statvfs(file_path)
                    size_to_display = x.f_bsize
                except OSError:
                    size_to_display = "ERROR"

        # 3 Time to Display
        try:
            st = os.lstat(file_path)
            time_to_display = time.strftime("%d/%m/%Y  %H:%M", time.localtime(st.st_mtime))
        except OSError:
            time_to_display = 'ERROR'

        # 4 Size value used by the shorted process
        try:
            st = os.lstat(file_path)
            size_value_to_order = st.st_size
        except OSError:
            size_value_to_order = 'ERROR'

        # 5 Mtime value used by the shorted process
        try:
            st = os.lstat(file_path)
            mtime_value_to_order = st.st_mtime
        except OSError:
            mtime_value_to_order = "ERROR"

        # 6 - Small symbol
        # 7 - Color
        # 8 - Color_add
        small_symbol = ' '
        color = 'GRAY'
        color_add = curses.A_NORMAL
        if os.path.islink(file_path):
            if not os.path.exists(file_path):
                small_symbol = '!'
                color = 'RED'
                color_add = curses.A_BOLD
                if self.get_app_file_extensions() is not None:
                    if file_path.endswith(self.get_app_file_extensions()):
                        color = 'RED'
                        color_add = curses.A_BOLD
                    else:
                        color = 'GRAY'
                        color_add = curses.A_BOLD | curses.A_DIM
            else:
                small_symbol = '@'
                if self.get_app_file_extensions() is not None:
                    if file_path.endswith(self.get_app_file_extensions()):
                        color_add = curses.A_NORMAL
                    else:
                        color_add = curses.A_DIM
        elif os.path.isfile(file_path):
            if os.access(file_path, os.X_OK):
                small_symbol = '*'
                color = 'GREEN'
                color_add = curses.A_BOLD
                if self.get_app_file_extensions() is not None:
                    if file_path.endswith(self.get_app_file_extensions()):
                        color = 'GREEN'
                        color_add = curses.A_BOLD
                    else:
                        color = 'GRAY'
                        color_add = curses.A_BOLD | curses.A_DIM
            else:
                small_symbol = ' '
                if self.get_app_file_extensions() is not None:
                    if file_path.endswith(self.get_app_file_extensions()):
                        color_add = curses.A_NORMAL
                    else:
                        color_add = curses.A_DIM

        elif os.path.isdir(file_path):
            small_symbol = os.path.sep
            color = 'GRAY'
            color_add = curses.A_NORMAL

        # Yes it return something, it's a live !
        file_info_list = list()
        file_info_list.append(name_to_display)
        file_info_list.append(full_path)
        file_info_list.append(size_to_display)
        file_info_list.append(time_to_display)
        file_info_list.append(size_value_to_order)
        file_info_list.append(mtime_value_to_order)
        file_info_list.append(small_symbol)
        file_info_list.append(color)
        file_info_list.append(color_add)
        return file_info_list

    def _update_directory_list(self):
        # We consider to be on the local directory
        self.item_list = os.listdir(os.getcwd())
        self.item_list.sort()

        # Prepare the super list with all information's to display
        self.item_info_list = None
        for item in self.item_list:
            self.item_info_list.append(self._get_item_info(item))

        # Prepare list by sort
        # Sort by name
        if self.sort_by_name:
            list_file = list()
            list_dir = list()
            if self.sort_name_order:
                for tmp in self.item_list:
                    if os.path.isfile(tmp):
                        list_file.append(tmp)
                    else:
                        list_dir.append(tmp)
                list_file.sort()
                list_dir.sort()
            else:
                for tmp in reversed(self.item_list):
                    if os.path.isfile(tmp):
                        list_file.append(tmp)
                    else:
                        list_dir.append(tmp)
            self.item_list = list_dir + list_file

        # # Sort by size
        elif self.sort_by_size:
            self.item_info_list.sort(key=itemgetter(4))
            tmp_file = list()
            if self.sort_size_order:
                for tmp in self.item_info_list:
                    tmp_file.append(tmp[0])
            else:
                for tmp in reversed(self.item_info_list):
                    tmp_file.append(tmp[0])

            self.item_list = tmp_file

        # # Sort by Time
        elif self.sort_by_mtime:
            self.__item_info_list.sort(key=itemgetter(5))
            tmp_file = list()
            if self.sort_mtime_order == 0:
                for tmp in self.item_info_list:
                    tmp_file.append(tmp[0])
            else:
                for tmp in reversed(self.item_info_list):
                    tmp_file.append(tmp[0])

            self.item_list = tmp_file

        # At end insert .. for permit to back to the parent directory
        self.item_list.insert(0, '..')

    def set_app_file_extensions(self, file_extensions=None):
        """
        A tuple of file extension to colorize, it's consider as file type you searching for.

        The FileChooser will colorize they file's, in orange.

        Note the function automatically deal with case sensitive.

        Example: .mkv -> ('.mkv','.Mkv','MKV')

        :param file_extensions: a tuple of file extension to colorize or None for disable the colorize.
        :type file_extensions: tuple or None
        :raise TypeError: when ``file_extensions`` argument is not a tuple type or None
        """
        if file_extensions is None:
            if self.get_app_file_extensions() is not None:
                self.app_file_extensions = None
                return

        # Exit as soon of possible
        if type(file_extensions) != tuple:
            raise TypeError("'file_extensions' must be a tuple type")

        # Create a Tuple with Upper Lower and Title extension
        # Example: .mkv -> ('.mkv','.Mkv','MKV')
        file_extensions_temp = list()
        # Lower -> .mkv
        for I in list(file_extensions):
            file_extensions_temp.append(I.lower())
        # Title -> Mkv
        for I in list(file_extensions):
            file_extensions_temp.append(I.title())
        # Upper -> .MKV
        for I in list(file_extensions):
            file_extensions_temp.append(I.upper())
        video_file_extensions = tuple(file_extensions_temp)

        if self.get_app_file_extensions() != video_file_extensions:
            self.app_file_extensions = video_file_extensions

    def get_app_file_extensions(self):
        """
        Return the list of file extension to colorize.

        See . Filechooser.set_app_file_extensions() for more details.

        :return: a tuple of file extension to colorize or None if disable.
        :rtype: tuple or None
        """
        return self.app_file_extensions

    # Curses Display
    def draw_widget_in_area(self):
        self.create_or_resize()
        self._check_selected()
        self._update_preferred_sizes()
        self._update_directory_list()

        if self.subwin:
            # self._draw_background()
            if self.get_decorated():
                self._draw_box_top()
                self._draw_box_bottom()

            self._draw_filechooser()

            if self.get_decorated():
                self._draw_box_left_side()
                self._draw_box_right_side()
                self._draw_box_upper_left_corner()
                self._draw_box_upper_right_corner()
                self._draw_box_bottom_right_corner()
                self._draw_box_bottom_left_corner()

    def _draw_filechooser(self):
        # History Line
        # History arrow for navigate inside history directory list
        self._draw_history_hline()
        self._draw_history_prev()
        self._draw_history_actual_path()
        self._draw_history_button()
        self._draw_history_next()

        # Titles Column
        self._draw_column_title_sorted_order()

        # Create 3 clickable elements for "Name", "Size", "Modify Time"
        self._draw_column_title_name()
        self._draw_column_title_size()
        self._draw_column_title_mtime()

        # Create 2 Vertical Lines for create columns for Name, Size and Modify Time
        self._draw_column_vline_mtime()
        self._draw_column_vline_size()

        # FOR qui occupe toute la fenetre avec des listes de fichiers
        count = 0
        for line_number in range(self.y_pos_items, self.preferred_height - 2):

            if count < len(self.item_list):

                # Force the selected high color line to stay on the aviable box size
                if self.selected_item_pos + 1 > self.item_it_can_be_display:
                    self.selected_item_pos -= 1

                try:
                    # We know how is the selected line
                    file_info_list = self._get_item_info(
                        os.path.join(
                            os.getcwd(),
                            self.item_list[count + self.item_scroll_pos],
                        )
                    )
                    # Draw normal line
                    self._draw_line_normal(line_number, file_info_list)

                    # Draw the selected Line
                    # That is the selected line enjoy, cher !!!!
                    if self.selected_item_pos == count:
                        self.selected_item_info_list = file_info_list
                        self._draw_line_selected(line_number, file_info_list)
                        self._draw_information_text(file_info_list[1])
                except IndexError:
                    continue

            count += 1

        # Information part
        self._draw_information_hline()

        # If the item value is '..' it use Directory setting
        # if self.get_has_focus():
        #     self._draw_information_text(file_info_list)

        # Disk Usage
        self._draw_information_disk_usage()

        # Test if the history widget should be display
        if self.display_history_menu:
            self.history_dialog_box = GLXCurses.FileChooserMenu(
                parent=self,
                y=self.y_pos_history - 1,
                x=self.x_pos_history_list_label,
                label=self.display_history_text,
            )

    def _draw_line_normal(self, line_number, file_info_list):
        try:
            name_to_display = GLXCurses.resize_text(file_info_list[6] + file_info_list[0], self.name_column_width)
            try:
                for x_inc in range(0, len(name_to_display)):
                    self.subwin.delch(line_number, self.x_pos_line_start + x_inc)
                    self.subwin.insch(line_number,
                                      self.x_pos_line_start + x_inc,
                                      str(name_to_display[x_inc]),
                                      self.style.color(fg=file_info_list[7], bg='BLUE') | file_info_list[8]
                                      )
            except curses.error:  # pragma: no cover
                pass
            except OverflowError:
                pass
        except TypeError:
            pass

        try:
            name_to_display = GLXCurses.resize_text(str(file_info_list[2]), self.size_column_width)
            try:
                for x_inc in range(0, len(name_to_display)):
                    self.subwin.delch(line_number,
                                      self.mtime_column_width - len(name_to_display) + x_inc
                                      )
                    self.subwin.insch(line_number,
                                      self.mtime_column_width - len(name_to_display) + x_inc,
                                      name_to_display[x_inc],
                                      self.style.color(fg=file_info_list[7],
                                                       bg='BLUE'
                                                       ) | file_info_list[8]
                                      )
            except curses.error:  # pragma: no cover
                pass
        except TypeError:
            pass

        for x_inc in range(0, len(file_info_list[3])):
            try:
                self.subwin.delch(line_number, self.mtime_column_width + 1 + x_inc)
                self.subwin.insch(
                    line_number,
                    self.mtime_column_width + 1 + x_inc,
                    file_info_list[3][x_inc],
                    self.style.color(
                        fg=file_info_list[7],
                        bg='BLUE'
                    ) | file_info_list[8]
                )
            except curses.error:  # pragma: no cover
                pass

    def _draw_line_selected(self, line_number, file_info_list):
        if self.has_prelight:
            # Line Background
            try:
                for x_inc in range(self.x_pos_line_start, self.x_pos_line_stop):
                    self.subwin.delch(line_number, x_inc)
                    self.subwin.insch(line_number,
                                      x_inc,
                                      ' ',
                                      self.style.color(fg='BLACK', bg='CYAN')
                                      )
            except curses.error:  # pragma: no cover
                pass

            # Name_Column
            try:
                name_to_display = GLXCurses.resize_text(str(file_info_list[6]) + str(file_info_list[0]),
                                                        self.name_column_width
                                                        )
                try:
                    for x_inc in range(0, len(name_to_display)):
                        self.subwin.delch(line_number, self.x_pos_line_start + x_inc)
                        self.subwin.insch(line_number,
                                          self.x_pos_line_start + x_inc,
                                          str(name_to_display[x_inc]),
                                          self.style.color(fg='BLACK', bg='CYAN')
                                          )
                except curses.error:  # pragma: no cover
                    pass
                except OverflowError:
                    pass
            except TypeError:
                pass

            try:
                self.subwin.delch(line_number, self.mtime_column_width - self.size_column_width)
                self.subwin.insch(line_number,
                                  self.mtime_column_width - self.size_column_width,
                                  curses.ACS_VLINE,
                                  self.style.color(fg='BLACK', bg='CYAN')
                                  )
            except curses.error:  # pragma: no cover
                pass

            # Draw the Size
            for x_inc in range(0, len(str(file_info_list[2]))):
                try:
                    self.subwin.delch(line_number, self.mtime_column_width - len(str(file_info_list[2])) + x_inc)
                    self.subwin.insch(
                        line_number,
                        self.mtime_column_width - len(str(file_info_list[2])) + x_inc,
                        str(file_info_list[2])[x_inc],
                        self.style.color(fg='BLACK', bg='CYAN')
                    )
                except curses.error:  # pragma: no cover
                    pass
            # Draw the Date
            for x_inc in range(0, len(str(file_info_list[3]))):
                try:
                    self.subwin.delch(line_number, self.mtime_column_width + 1 + x_inc)
                    self.subwin.insch(
                        line_number,
                        self.mtime_column_width + 1 + x_inc,
                        str(file_info_list[3])[x_inc],
                        self.style.color(fg='BLACK', bg='CYAN')
                    )
                except curses.error:  # pragma: no cover
                    pass

            # Draw the 2 vertical lines with high light color
            try:
                self.subwin.delch(line_number, self.mtime_column_width)
                self.subwin.insch(line_number,
                                  self.mtime_column_width,
                                  curses.ACS_VLINE,
                                  self.style.color(fg='BLACK', bg='CYAN')
                                  )
            except curses.error:  # pragma: no cover
                pass

    def _draw_information_hline(self):
        if self.get_decorated():
            for x_inc in range(self.x_pos_line_start, self.x_pos_line_stop + 2):
                try:
                    self.subwin.delch(self.preferred_height - 3, x_inc)
                    self.subwin.insch(
                        self.preferred_height - 3,
                        x_inc,
                        curses.ACS_HLINE,
                        self.style.color(fg='GRAY', bg='BLUE')
                    )
                except curses.error:  # pragma: no cover
                    pass
        else:
            for x_inc in range(self.x_pos_line_start, self.preferred_width):
                try:
                    self.subwin.delch(self.preferred_height - 3, x_inc)
                    self.subwin.insch(
                        self.preferred_height - 3,
                        x_inc,
                        curses.ACS_HLINE,
                        self.style.color(fg='GRAY', bg='BLUE')
                    )
                except curses.error:  # pragma: no cover
                    pass

    def _draw_information_text(self, text):
        for x_inc in range(0, len(GLXCurses.resize_text(text, self.preferred_width - 2))):
            try:
                self.subwin.delch(self.preferred_height - 2, self.x_pos_line_start + x_inc)
                self.subwin.insch(
                    self.preferred_height - 2,
                    self.x_pos_line_start + x_inc,
                    str(GLXCurses.resize_text(text, self.preferred_width - 2)[x_inc]),
                    self.style.color(fg='GRAY', bg='BLUE')
                )
            except curses.error:  # pragma: no cover
                pass
            except OverflowError:
                pass

    def _draw_information_disk_usage(self):
        # Add Disk usage
        disk_space_line = GLXCurses.disk_usage(os.getcwd())
        if self.get_decorated():
            for x_inc in range(0, len(disk_space_line)):
                try:
                    self.subwin.delch(self.preferred_height - 1,
                                      self.preferred_width - 1 - int(self.border_len / 2) - len(disk_space_line) + x_inc
                                      )
                    self.subwin.insch(
                        self.preferred_height - 1,
                        self.preferred_width - 1 -int(self.border_len / 2) - len(disk_space_line) + x_inc,
                        disk_space_line[x_inc],
                        self.style.color(fg='GRAY', bg='BLUE')
                    )
                except curses.error:  # pragma: no cover
                    pass
        else:
            for x_inc in range(0, len(disk_space_line)):
                try:
                    self.subwin.delch(self.preferred_height - 1,
                                      self.preferred_width - len(disk_space_line) + x_inc
                                      )
                    self.subwin.insch(
                        self.preferred_height - 1,
                        self.preferred_width - len(disk_space_line) + x_inc,
                        disk_space_line[x_inc],
                        self.style.color(fg='GRAY', bg='BLUE')
                    )
                except curses.error:  # pragma: no cover
                    pass

    def _draw_history_hline(self):
        for x_inc in range(self.x_pos_line_start, self.x_pos_line_stop):
            try:
                self.subwin.delch(self.y_pos_history,
                                  x_inc)
                self.subwin.insch(self.y_pos_history,
                                  x_inc,
                                  curses.ACS_HLINE,
                                  self.style.color(fg='GRAY', bg='BLUE') | curses.A_NORMAL
                                  )
            except curses.error:  # pragma: no cover
                pass

    def _draw_history_prev(self):
        # History arrow for navigate inside history directory list
        try:
            self.subwin.delch(self.y_pos_history,
                              self.x_pos_history_prev_label
                              )
            self.subwin.insch(
                self.y_pos_history,
                self.x_pos_history_prev_label,
                "<",
                self.style.color(fg='GRAY', bg='BLUE')
            )
        except curses.error:  # pragma: no cover
            pass

    def _draw_history_actual_path(self):
        spacing = 2
        internal_spacing = 2
        prepend_text = '...'

        label_dir = os.getcwd()
        label_dir = label_dir.replace(os.path.expanduser("~"), "~")
        ce_que_je_retire = self.x_pos_history_actual_path_allowed_size
        ce_que_je_retire -= self.x_pos_history_actual_path
        ce_que_je_retire -= spacing

        if internal_spacing >= 2:
            space_to_add = ' ' * int(internal_spacing / 2)
            label_dir = space_to_add + label_dir + space_to_add

        label_dir = label_dir[-ce_que_je_retire:]

        if self.has_focus:
            color = self.style.color(fg='BLACK', bg='WHITE')
        else:
            color = self.style.color(fg='GRAY', bg='BLUE')

        if ce_que_je_retire > 1:
            for x_inc in range(0, len(str(label_dir))):
                try:
                    self.subwin.delch(self.y_pos_history,
                                      self.x_pos_history_actual_path + x_inc
                                      )
                    self.subwin.insch(self.y_pos_history,
                                      self.x_pos_history_actual_path + x_inc,
                                      str(label_dir[x_inc]),
                                      color
                                      )
                except curses.error:  # pragma: no cover
                    pass
                except OverflowError:
                    pass
            if ce_que_je_retire <= len(label_dir):
                for x_inc in range(0, len(str(prepend_text))):
                    try:
                        self.subwin.delch(self.y_pos_history,
                                          self.x_pos_history_actual_path + x_inc
                                          )
                        self.subwin.insch(self.y_pos_history,
                                          self.x_pos_history_actual_path + x_inc,
                                          prepend_text[x_inc],
                                          color
                                          )
                    except curses.error:  # pragma: no cover
                        pass

    def _draw_history_button(self):
        # History button for display the history dialog window
        for x_inc in range(0, len(str(".[^]"))):
            try:
                self.subwin.delch(self.y_pos_history,
                                  self.x_pos_history_list_label + x_inc
                                  )

                self.subwin.insch(self.y_pos_history,
                                  self.x_pos_history_list_label + x_inc,
                                  ".[^]"[x_inc],
                                  self.style.color(fg='GRAY', bg='BLUE')
                                  )

            except curses.error:  # pragma: no cover
                pass

    def _draw_history_next(self):
        # History next arrow for navigate inside history directory list
        try:
            self.subwin.delch(self.y_pos_history, self.x_pos_history_next_label)
            self.subwin.insch(self.y_pos_history,
                              self.x_pos_history_next_label,
                              ">",
                              self.style.color(fg='GRAY', bg='BLUE')
                              )

        except curses.error:  # pragma: no cover
            pass

    def _draw_column_vline_size(self):
        try:
            for y_inc in range(self.y_pos_titles, self.preferred_height - 2):
                self.subwin.delch(y_inc,
                                  self.mtime_column_width - self.size_column_width
                                  )
                self.subwin.insch(y_inc,
                                  self.mtime_column_width - self.size_column_width,
                                  curses.ACS_VLINE,
                                  self.style.color(fg='GRAY', bg='BLUE')
                                  )

        except curses.error:  # pragma: no cover
            pass

    def _draw_column_vline_mtime(self):
        try:
            for y_inc in range(self.y_pos_titles, self.preferred_height - 2):
                self.subwin.delch(y_inc, self.mtime_column_width)
                self.subwin.insch(y_inc,
                                  self.mtime_column_width,
                                  curses.ACS_VLINE,
                                  self.style.color(fg='GRAY', bg='BLUE')
                                  )

        except curses.error:  # pragma: no cover
            pass

    def _draw_column_title_mtime(self):
        for x_inc in range(0, len(self.mtime_text)):
            try:
                self.subwin.delch(self.y_pos_titles, self.x_pos_title_mtime + x_inc)
                self.subwin.insch(self.y_pos_titles,
                                  self.x_pos_title_mtime + x_inc,
                                  self.mtime_text[x_inc],
                                  self.style.color(fg='YELLOW', bg='BLUE')
                                  )
            except curses.error:  # pragma: no cover
                pass

    def _draw_column_title_size(self):
        for x_inc in range(0, len(self.size_text)):
            try:
                self.subwin.delch(self.y_pos_titles,
                                  self.x_pos_title_size + x_inc
                                  )
                self.subwin.insch(self.y_pos_titles,
                                  self.x_pos_title_size + x_inc,
                                  self.size_text[x_inc],
                                  self.style.color(fg='YELLOW', bg='BLUE')
                                  )
            except curses.error:  # pragma: no cover
                pass

    def _draw_column_title_name(self):
        for x_inc in range(0, len(self.name_text)):
            try:
                self.subwin.delch(self.y_pos_titles,
                                  self.x_pos_title_name + x_inc
                                  )
                self.subwin.insch(self.y_pos_titles,
                                  self.x_pos_title_name + x_inc,
                                  self.name_text[x_inc],
                                  self.style.color(fg='YELLOW', bg='BLUE')
                                  )
            except curses.error:  # pragma: no cover
                pass

    def _draw_column_title_sorted_order(self):
        # Verify which short type is selected and display ('n) (.n) ('s) (.s) ('m) (.m)
        if self.sort_by_name:
            if self.sort_name_order:
                symbol = "'n"
            else:
                symbol = ".n"
        elif self.sort_by_size:
            if self.sort_size_order:
                symbol = "'s"
            else:
                symbol = ".s"
        elif self.sort_by_mtime:
            if self.sort_mtime_order:
                symbol = "'t"
            else:
                symbol = ".t"
        else:
            symbol = ""
        for x_inc in range(0, len(symbol)):
            try:
                self.subwin.delch(self.y_pos_titles, self.x_pos_line_start + x_inc)
                self.subwin.insch(
                    self.y_pos_titles,
                    self.x_pos_line_start + x_inc,
                    symbol[x_inc],
                    self.style.color(fg='YELLOW', bg='BLUE')
                )
            except curses.error:  # pragma: no cover
                pass

    def _update_preferred_sizes(self):
        self.preferred_width = self.width
        self.preferred_height = self.height

        # it_can_be_display
        # what is 5 or 4 ????
        self.item_it_can_be_display = self.preferred_height - 5

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
                else:
                    self.has_prelight = False

    def _grab_focus(self):
        """
        Internal method, for Select the contents of the Entry it take focus.

        See: grab_focus_without_selecting ()
        """
        if self.can_focus:
            GLXCurses.Application().has_focus = self
            GLXCurses.Application().has_default = self
            GLXCurses.Application().has_prelight = self
            self._check_selected()

    def _handle_key_event(self, event_signal, *event_args):
        # Check if we have to care about keyboard event
        if self.sensitive and \
                isinstance(GLXCurses.Application().has_focus, GLXCurses.ChildElement) and \
                GLXCurses.Application().has_focus.id == self.id:
            # setting
            key = event_args[0]

            if not self.display_history_menu == 1:
                # Touch Escape
                if key == GLXCurses.GLXC.KEY_ESC:
                    GLXCurses.Application().has_focus = None
                    GLXCurses.Application().has_default = None
                    GLXCurses.Application().has_prelight = None
                    # self.has_focus = False
                    # self.has_default = False
                    # self.has_prelight = False
                    self._check_selected()

                if key == curses.KEY_UP:
                    logging.debug(str(time.time() - self.time_last_scroll_up))
                    if time.time() - self.time_last_scroll_up > 0.10:
                        self._scroll_up()
                    elif 0.06 >= time.time() - self.time_last_scroll_up > 0.0:
                        self._scroll_up()
                        self._scroll_up()

                    self.time_last_scroll_up = time.time()

                if key == curses.KEY_DOWN:
                    logging.debug(str(time.time() - self.time_last_scroll_down))
                    if time.time() - self.time_last_scroll_down > 0.06:
                        self._scroll_down()
                    elif 0.06 >= time.time() - self.time_last_scroll_down > 0.0:
                        self._scroll_down()
                        self._scroll_down()

                    self.time_last_scroll_down = time.time()

                if key == curses.KEY_HOME:
                    self.selected_item_pos = 0
                    self.item_scroll_pos = 0

                # END Touch
                if key == curses.KEY_END:
                    # Scroll to down like curses.KEY_DOWN via a loop it have the len of item in directory,
                    for line_number in range(0, len(self.item_list)):
                        self._scroll_down()

                if key == curses.KEY_NPAGE:
                    for line_number in range(0, self.item_it_can_be_display - 1):
                        self._scroll_down()

                if key == curses.KEY_PPAGE:
                    for line_number in range(0, self.item_it_can_be_display - 1):
                        self._scroll_up()

                if key == ord("n"):
                    self.sort_by_name = True
                    self.sort_by_size = False
                    self.sort_by_mtime = False
                    self.sort_name_order = not self.sort_name_order

                if key == ord("s"):
                    self.sort_by_name = False
                    self.sort_by_size = True
                    self.sort_by_mtime = False
                    self.sort_size_order = not self.sort_size_order

                if key == ord("t"):
                    self.sort_by_name = False
                    self.sort_by_size = False
                    self.sort_by_mtime = True
                    self.sort_mtime_order = not self.sort_mtime_order

                if key == ord("h"):
                    self.display_history_menu = not self.display_history_menu

                if key == curses.KEY_ENTER or key == ord("\n"):

                    # We gat the line go do something
                    if os.path.isdir(self.selected_item_info_list[1]):
                        os.chdir(os.path.join(os.getcwd(), self.selected_item_info_list[1]))

                        self.selected_item_pos = 0
                        self.item_scroll_pos = 0

                        found = 0
                        for item in self.history_dir_list:
                            if item == os.getcwd():
                                found = 1
                        if not found == 1:
                            self.history_dir_list.append(os.getcwd())

                    else:
                        pass

            # When history i display enable special shortcut
            elif self.display_history_menu == 1:
                if key == GLXCurses.GLXC.KEY_ESC:
                    # Escape was pressed
                    self.display_history_menu = not self.display_history_menu

                elif key == curses.KEY_UP:
                    self._history_scroll_up()

                elif key == curses.KEY_DOWN:
                    self._history_scroll_down()

                elif key == curses.KEY_ENTER or key == ord("\n"):
                    self.display_history_menu = not self.display_history_menu
                    if os.path.isdir(self.history_menu_selected_item_value):
                        os.chdir(self.history_menu_selected_item_value)
                        # self.window_source_pwd = os.getcwd()
                        self.selected_item = 0
                        self.item_list_scroll = 0

                elif key == ord("h"):
                    self.display_history_menu = not self.display_history_menu

            # Create a Dict with everything
            instance = {
                'class': self.__class__.__name__,
                'id': self.id,
                'event_signal': event_signal
            }
            # EVENT EMIT
            # Application().emit(self.curses_mouse_states[event], instance)
            self.emit(str(key), instance)

    def _handle_mouse_event(self, event_signal, event_args):

        if self.sensitive:
            (mouse_event_id, x, y, z, event) = event_args

            # Be sure we select really the Button
            y -= self.y
            x -= self.x
            that_for_me = (0 <= y <= self.preferred_height - 1 and 0 <= x <= self.preferred_width - 1)

            if that_for_me:
                self._grab_focus()
                # First line Prev / Next / History
                if y == 0:
                    if self.x_pos_history_prev_label <= x <= self.x_pos_history_prev_label:
                        # logging.debug('x:' + str(x) + " y:" + str(y))
                        if not self.history_menu_selected_item == 0:
                            self.history_menu_selected_item -= 1

                        if os.path.isdir(self.history_dir_list[self.history_menu_selected_item]):
                            os.chdir(self.history_dir_list[self.history_menu_selected_item])

                            self.selected_item_pos = 0
                            self.item_scroll_pos = 0

                    if self.x_pos_history_list_label <= x <= self.x_pos_history_list_label - 1 + len(
                            self.history_button_text_list):
                        self.display_history_menu = not self.display_history_menu

                    if self.x_pos_history_next_label <= x <= self.x_pos_history_next_label:

                        if len(self.history_dir_list) > self.history_menu_selected_item + 1:
                            self.history_menu_selected_item += 1

                            if os.path.isdir(self.history_dir_list[self.history_menu_selected_item]):
                                os.chdir(self.history_dir_list[self.history_menu_selected_item])
                                self.selected_item_pos = 0
                                self.item_scroll_pos = 0
                # Titles
                if y == self.y_pos_titles:
                    x_pos_name_start = self.x_pos_title_name - self.x - 1
                    if x_pos_name_start <= x <= self.x_pos_title_name + len(self.name_text) - 1:
                        self.sort_by_name = True
                        self.sort_by_size = False
                        self.sort_by_mtime = False
                        self.sort_name_order = not self.sort_name_order
                    if self.x_pos_title_size <= x <= self.x_pos_title_size + len(self.size_text) - 1:
                        self.sort_by_name = False
                        self.sort_by_size = True
                        self.sort_by_mtime = False
                        self.sort_size_order = not self.sort_size_order
                    if self.x_pos_title_mtime <= x <= self.x_pos_title_mtime + len(self.mtime_text) - 1:
                        self.sort_by_name = False
                        self.sort_by_size = False
                        self.sort_by_mtime = True
                        self.sort_mtime_order = not self.sort_mtime_order

                # Mouse weel
                if self.y_pos_titles + 1 <= y <= self.preferred_height - 3 \
                        and event != 524288 and event != 134217728 and event != curses.BUTTON4_PRESSED:
                    clicked_line = y - self.y_pos_titles - 1
                    if 0 <= x <= self.preferred_width - 1:

                        if event == curses.BUTTON1_DOUBLE_CLICKED:
                            # Selected the line
                            if clicked_line <= len(self.item_list):
                                value = clicked_line
                            else:
                                value = len(self.item_list) - 1

                            self.selected_item_pos = value
                            self.item_scroll_pos = value
                            self.selected_item_info_list = self._get_item_info(
                                self.__item_list[self.item_scroll_pos],
                            )

                            # We got the line and do something
                            if os.path.isdir(self.selected_item_info_list[1]):
                                os.chdir(os.path.join(os.getcwd(), self.selected_item_info_list[0]))

                                self.selected_item_pos = 0
                                self.item_scroll_pos = 0

                                # Update history List
                                found = 0
                                for item in self.history_dir_list:
                                    if item == os.getcwd():
                                        found = 1
                                if not found == 1:
                                    self.history_dir_list.append(os.getcwd())

                            else:
                                pass

                        if event == curses.BUTTON1_CLICKED or event == curses.BUTTON1_PRESSED:
                            if clicked_line <= len(self.item_list):
                                self.selected_item_pos = clicked_line
                            else:
                                # Scroll to down like curses.KEY_DOWN via a loop
                                # it have the len of item in directory,
                                for line_number in range(0, len(self.item_list)):
                                    self._scroll_down()

                if event == 524288 or event == 65536:
                    if not self.display_history_menu == 1:
                        if not self.display_history_menu == 1:
                            # logging.debug(str(time.time() - self.time_last_scroll_up))
                            if time.time() - self.time_last_scroll_up > 0.10:
                                self._scroll_up()
                            elif 0.10 >= time.time() - self.time_last_scroll_up > 0.05:
                                self._scroll_up()
                                self._scroll_up()
                            elif 0.05 >= time.time() - self.time_last_scroll_up > 0.025:
                                self._scroll_up()
                                self._scroll_up()
                                self._scroll_up()
                                self._scroll_up()
                            elif 0.025 >= time.time() - self.time_last_scroll_up > 0.0:
                                self._scroll_up()
                                self._scroll_up()
                                self._scroll_up()
                                self._scroll_up()
                                self._scroll_up()
                                self._scroll_up()
                                self._scroll_up()
                                self._scroll_up()

                            self.time_last_scroll_up = time.time()
                    else:
                        self._history_scroll_up()

                if event == 134217728 or event == 2097152:
                    if not self.display_history_menu == 1:
                        # logging.debug(str(time.time() - self.time_last_scroll_down))
                        if time.time() - self.time_last_scroll_down > 0.10:
                            self._scroll_down()
                        elif 0.10 >= time.time() - self.time_last_scroll_down > 0.05:
                            self._scroll_down()
                            self._scroll_down()
                        elif 0.05 >= time.time() - self.time_last_scroll_down > 0.025:
                            self._scroll_down()
                            self._scroll_down()
                            self._scroll_down()
                            self._scroll_down()
                        elif 0.025 >= time.time() - self.time_last_scroll_down > 0.0:
                            self._scroll_down()
                            self._scroll_down()
                            self._scroll_down()
                            self._scroll_down()
                            self._scroll_down()
                            self._scroll_down()
                            self._scroll_down()
                            self._scroll_down()

                        self.time_last_scroll_down = time.time()
                    else:
                        self._history_scroll_down()

                # INTERNAL METHOD
                if event == curses.BUTTON1_PRESSED:
                    pass

                elif event == curses.BUTTON1_RELEASED:
                    pass

                if event == curses.BUTTON1_CLICKED:
                    pass

                if event == curses.BUTTON1_DOUBLE_CLICKED:
                    pass

                if event == curses.BUTTON1_TRIPLE_CLICKED:
                    pass

                # BUTTON2
                if event == curses.BUTTON2_PRESSED:
                    pass

                elif event == curses.BUTTON2_RELEASED:
                    pass

                if event == curses.BUTTON2_CLICKED:
                    pass

                if event == curses.BUTTON2_DOUBLE_CLICKED:
                    pass

                if event == curses.BUTTON2_TRIPLE_CLICKED:
                    pass

                # BUTTON3
                if event == curses.BUTTON3_PRESSED:
                    pass

                elif event == curses.BUTTON3_RELEASED:
                    pass

                if event == curses.BUTTON3_CLICKED:
                    pass

                if event == curses.BUTTON3_DOUBLE_CLICKED:
                    pass

                if event == curses.BUTTON3_TRIPLE_CLICKED:
                    pass

                # BUTTON4
                if event == curses.BUTTON4_PRESSED:
                    pass

                elif event == curses.BUTTON4_RELEASED:
                    pass

                if event == curses.BUTTON4_CLICKED:
                    pass

                if event == curses.BUTTON4_DOUBLE_CLICKED:
                    pass

                if event == curses.BUTTON4_TRIPLE_CLICKED:
                    pass

                if event == curses.BUTTON_SHIFT | curses.BUTTON1_CLICKED:
                    pass
                if event == curses.BUTTON_CTRL:
                    pass
                if event == curses.BUTTON_ALT:
                    pass

                # Create a Dict with everything
                instance = {
                    'class': self.__class__.__name__,
                    'id': self.id,
                    'event_signal': event_signal
                }
                # EVENT EMIT
                # Application().emit(self.curses_mouse_states[event], instance)
                self.emit(self.curses_mouse_states[event], instance)
            else:
                # The widget is not selected
                self.has_focus = False
                self._check_selected()
        else:
            if self.debug:
                logging.debug('{0} -> id:{1}, object:{2}, is not sensitive'.format(
                    self.__class__.__name__,
                    self.id,
                    self
                ))
