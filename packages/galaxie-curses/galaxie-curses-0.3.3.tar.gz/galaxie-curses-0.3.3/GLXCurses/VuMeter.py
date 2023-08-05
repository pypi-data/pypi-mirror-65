#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved
from array import array

import GLXCurses
import curses
#import numpy as np
import math


# class VuMeter(GLXCurses.Widget, GLXCurses.Movable):
#     def __init__(self):
#         # Load heritage
#         GLXCurses.Movable.__init__(self)
#         GLXCurses.Widget.__init__(self)
#
#         # It's a GLXCurse Type
#         self.glxc_type = 'GLXCurses.VuMeter'
#         self.name = '{0}{1}'.format(self.__class__.__name__, self.id)
#
#         # Make a Widget Style heritage attribute as local attribute
#         if self.style.attribute_states:
#             if self.attribute_states != self.style.attribute_states:
#                 self.attribute_states = self.style.attribute_states
#
#         # Internal Widget Setting
#         # Label
#         self.char = None
#
#         # Interface
#         self.char = '_'
#         self.display_scale = True
#         self.display_text = True
#         self.display_meter = True
#         self.can_display_meter = True
#         self.can_display_scale = True
#         self.can_display_scale_title = True
#         self.space_reserved_for_scale = 3
#         self.space_reserved_for_meter = 2
#         self.preferred_width = self.space_reserved_for_scale + self.space_reserved_for_meter
#         self.preferred_height = 0
#         self.scale_max = None
#         self.scale_min = None
#         # Audio section
#         self.channels = None
#         self.base_ten_signed_max_value = None
#         self.border = None
#
#         # Internal Widget Setting
#         self.value = None
#         self.text = None
#         self._justify = None
#
#
#         # init for the first time
#         # The Percent value
#         self.set_scale_min(0)
#         self.set_scale_max(32767)
#         self.set_value(0)
#         self.set_text('dBFS')
#         self.preferred_width = self._get_estimated_preferred_width()
#         self.preferred_height = self._get_estimated_preferred_height()
#
#         # Justification: LEFT, RIGHT, CENTER
#         self.set_border(False)
#         self.border_len = 2
#         self.set_justify(GLXCurses.GLXC.JUSTIFY_CENTER)
#
#
#         self.vumeter_curses_subwin = None
#
#     def draw_widget_in_area(self):
#         self.create_or_resize()
#         if self.subwin is not None:
#             # Check x offset
#             self._check_justify_and_sizes()
#
#             if self.get_border():
#                 self.border_len = 2
#             else:
#                 self.border_len = 0
#
#             self.draw_vumeter()
#
#     def draw_vumeter(self):
#
#         max_log = 20 * math.log10(self.get_scale_max())
#
#         allowed_height = int(self.preferred_height - int(self.border_len / 2))
#
#         scale_list_reverse = GLXCurses.linspace(max_log, self.get_scale_min(), allowed_height)
#         scale_list = GLXCurses.linspace(self.get_scale_min(), max_log, allowed_height)
#
#         if self.get_border():
#             height_de_merde = 0
#         else:
#             height_de_merde = 1
#
#         # Offset for text
#         if self.get_display_text():
#             offset_text = 1
#         else:
#             offset_text = 0
#
#         if self.get_display_scale():
#             space_for_scale = self.space_reserved_for_scale
#         else:
#             space_for_scale = 0
#
#         # Draw
#         try:
#             # Create the subwin for vumeter
#             # self.vumeter_curses_subwin = self.subwin.subwin(
#             #     self.preferred_height,
#             #     self.preferred_width,
#             #     self.get_y(),
#             #     self._get_x_offset()
#             # )
#             self.vumeter_curses_subwin = self.subwin
#             # Apply the Background color
#             self.vumeter_curses_subwin.bkgdset(
#                 ord(' '),
#                 self.style.get_color_pair(
#                     foreground=self.style.get_color_text('text', 'STATE_NORMAL'),
#                     background=self.style.get_color_text('dark', 'STATE_NORMAL')
#                 )
#             )
#             self.vumeter_curses_subwin.bkgd(
#                 ord(' '),
#                 self.style.get_color_pair(
#                     foreground=self.style.get_color_text('white', 'STATE_NORMAL'),
#                     background=self.style.get_color_text('dark', 'STATE_NORMAL')
#                 )
#             )
#
#             # The scale
#             if self.get_display_scale():
#                 # Small dot
#                 for i in range(0, allowed_height, 1):
#                     self.vumeter_curses_subwin.addstr(
#                         allowed_height - i - height_de_merde,
#                         int(self.border_len / 2),
#                         "{:>{}}".format('.', space_for_scale),
#                         self.style.get_color_pair(
#                             foreground=self.style.get_color_text('text', 'STATE_NORMAL'),
#                             background=self.style.get_color_text('dark', 'STATE_NORMAL')
#                         )
#                     )
#
#                 # Display Value
#                 for i in range(0, allowed_height, 3):
#                     # estimate the decibel dB
#                     value = (20 * math.log10(scale_list[i]))
#                     if math.isinf(value):
#                         value = self.get_scale_min()
#
#                 #     self.vumeter_curses_subwin.addstr(
#                 #         allowed_height - i - height_de_merde,
#                 #         int(self.border_len / 2),
#                 #         str("{:>{}.0f}".format(value, space_for_scale)),
#                 #         self.style.get_color_pair(
#                 #             foreground=self.style.get_color_text('text', 'STATE_NORMAL'),
#                 #             background=self.style.get_color_text('dark', 'STATE_NORMAL')
#                 #         )
#                 #     )
#
#                 # Force to display ZERO at TOP
#                 self.vumeter_curses_subwin.addstr(
#                     0 + int(self.border_len / 2),
#                     int(self.border_len / 2),
#                     str("{:>{}.0f}".format(0, space_for_scale)),
#                     self.style.get_color_pair(
#                         foreground=self.style.get_color_text('text', 'STATE_NORMAL'),
#                         background=self.style.get_color_text('dark', 'STATE_NORMAL')
#                     )
#                 )
#
#             # Draw LED
#             # value = 20 * np.log10(self.get_value())
#             # if np.isinf(value):
#             #     value = 0
#             for i in range(0, allowed_height, 1):
#                 self.vumeter_curses_subwin.addstr(
#                     allowed_height - i - height_de_merde,
#                     GLXCurses.clamp_to_zero(int(self.border_len / 2) + space_for_scale),
#                     ' ' * int(self.space_reserved_for_meter - 1),
#                     self.style.get_color_pair(
#                         foreground=self.style.get_color_text('text', 'STATE_NORMAL'),
#                         background=self.style.get_color_text('dark', 'STATE_NORMAL')
#                     )
#                 )
#                 color = 'GREEN'
#                 clamped_value = 0.0001
#                 if self.get_value() > clamped_value:
#                     clamped_value = self.get_value()
#                 if scale_list[i] <= 20 * math.log10(clamped_value):
#
#                     if max_log == scale_list[i]:
#                         color = 'RED'
#                     if max_log > scale_list[i] > max_log * 0.8:
#                         color = 'YELLOW'
#                     if max_log * 0.8 >= scale_list[i] > self.get_scale_min():
#                         color = 'GREEN'
#
#                     self.vumeter_curses_subwin.insstr(
#                         allowed_height - i - height_de_merde,
#                         GLXCurses.clamp_to_zero(int(self.border_len / 2) + space_for_scale),
#                         '_' * int(self.space_reserved_for_meter),
#                         self.style.get_color_pair(
#                             foreground=self.style.get_color_text('dark', 'STATE_NORMAL'),
#                             background=color
#                         )
#                     )
#
#             if self.get_border():
#                 self.vumeter_curses_subwin.box()
#
#             if self.get_display_text():
#                 # Text
#                 self.vumeter_curses_subwin.addstr(
#                     allowed_height - offset_text,
#                     int(self.border_len / 2),
#                     self.get_text() + ' ' * int(self.preferred_width - len(self.get_text()) - self.border_len),
#                     self.style.get_color_pair(
#                         foreground=self.style.get_color_text('white', 'STATE_NORMAL'),
#                         background=self.style.get_color_text('dark', 'STATE_NORMAL')
#                     )
#                 )
#         except curses.error:
#             pass
#
#     # Internal curses_subwin functions
#     def set_text(self, text='dBFS'):
#         """
#         Set the text on buttom of teh scale, here for inform about unit use like dBFS, LBU , % , etc ...
#
#         :param text: a text
#         :type text: str
#         :raise TypeError: when ``text`` argument is not a str
#         """
#         # Exit as soon of possible
#         if type(text) != str:
#             raise TypeError("'text' must be a str type")
#
#         # just in case it make teh job
#         if self.get_text() != text or self.get_text() is None:
#             self.text = text
#             # In case who know , it can require a resize somewhere
#
#     def get_text(self):
#         """
#         Return the scale title text as set by VuMeter().set_text().
#
#         :return: a text
#         :rtype: str
#         """
#         return self.text
#
#     def set_display_text(self, boolean=True):
#         """
#         Set if the text have to be display.
#
#         True for have the text display on buttom of VuMeter
#
#         :param boolean: True for display, False for not
#         :type boolean: bool or None for True
#         """
#         # Exit a soon of possible
#         if type(boolean) != bool:
#             raise TypeError("'boolean' must be a bool type")
#
#         if self.get_display_text() != bool(boolean):
#             self.display_text = bool(boolean)
#
#     def get_display_text(self):
#         """
#         Get the display_text value for know if the text have to be display.
#
#         :return: True for display the text , False for not
#         :rtype: bool
#         """
#         return self.display_text
#
#     def set_display_scale(self, boolean=True):
#         """
#         Set if the scale have to be display.
#
#         True for have the scale to display with VuMeter
#
#         :param boolean: True for display, False for not
#         :type boolean: bool or None for True
#         """
#         # Exit a soon of possible
#         if type(boolean) != bool:
#             raise TypeError("'boolean' must be a bool type")
#
#         if self.get_display_scale() != bool(boolean):
#             self.display_scale = bool(boolean)
#
#     def get_display_scale(self):
#         """
#         Get the display_text value for know if the text have to be display.
#
#         :return: True for display the text , False for not
#         :rtype: bool
#         """
#         return self.display_scale
#
#     def set_scale_min(self, value=0):
#         """
#         Set the Minimal value of the scale
#
#         :param value: a value
#         :type value: int or float
#         """
#         # Exit a soon of possible
#         if type(value) != int and type(value) != float:
#             raise TypeError("'value' must be a int or float type")
#
#         if self.get_scale_min() != value:
#             self.scale_min = value
#
#     def get_scale_min(self):
#         """
#         Return the Sclan min value, as set by set_scale_min()
#
#         :return: the scale value
#         :rtype: int or float
#         """
#         return self.scale_min
#
#     def set_scale_max(self, value=0):
#         """
#         Set the Maximal value of the scale
#
#         :param value: a value
#         :type value: int or float
#         """
#         # Exit a soon of possible
#         if type(value) != int and type(value) != float:
#             raise TypeError("'value' must be a int or float type")
#
#         if self.get_scale_max() != value:
#             self.scale_max = value
#
#     def get_scale_max(self):
#         """
#         Return the scale max value, as set by set_scale_max()
#
#         :return: the scale value
#         :rtype: int or float
#         """
#         return self.scale_max
#
#     def set_value(self, samples=0):
#         """
#         Set the value of the
#
#         :param samples: a value
#         :type samples: int or float
#         """
#         self.value = GLXCurses.clamp(value=samples, smallest=self.get_scale_min(), largest=self.get_scale_max())
#
#     def get_value(self):
#         """
#
#         :return: the value set by set_value()
#         :rtype: float or int
#         """
#         return self.value
#
#     # Justification: LEFT, RIGHT, CENTER
#     def set_justify(self, justify):
#         """
#         Set the Justify of the Vertical separator
#
#          Justify:
#             GLXCurses.GLXC.JUSTIFY_LEFT
#
#             GLXCurses.GLXC.JUSTIFY_CENTER
#
#             GLXCurses.GLXC.JUSTIFY_RIGHT
#
#             GLXCurses.GLXC.JUSTIFY_FILL
#
#         :param justify: a GLXCurses.GLXC.Justification
#         :type justify: str
#         :raise TypeError: if ``justify`` is not a valid GLXCurses.GLXC.Justification.
#         """
#         # Exit a soon of possible
#         if str(justify).upper() not in GLXCurses.GLXC.Justification:
#             raise TypeError("'justify' must be a valid GLXCurses.GLXC.Justification")
#
#         if self.get_justify() != str(justify).upper():
#             self._justify = str(justify).upper()
#
#     def get_justify(self):
#         return self._justify
#
#     def set_border(self, border=True):
#         """
#         By default, vumeter are decorated with a borderline.
#
#         :param border: True to decorate the vumeter with a borderline
#         :type border: bool
#         :raise TypeError: if ``border`` is not bool type
#         """
#         # Todo : Integration from https://developer.gnome.org/gtk3/stable/GtkWindow.html#gtk-window-set-decorated
#         # Exit as soon of possible
#         if not isinstance(border, bool):
#             raise TypeError("'setting' must be a bool type")
#
#         # We make the job in case that require
#         if self.get_border() != bool(border):
#             self.border = bool(border)
#
#     def get_border(self):
#         """
#         Returns whether the window has been set to have decorations such as borderline.
#
#         .. seealso:: :func:`Window.set_decorated() <GLXCurses.Window.Window.set_decorated>`.
#
#         :return: True if the window has been set to have decorations
#         :rtype: bool
#         """
#         return self.border
#
#     # Internal
#     def _check_justify_and_sizes(self):
#         """Check the justification of the X axe"""
#         width = self.width - 1
#         preferred_width = self.preferred_width
#
#         if self.get_justify() == GLXCurses.GLXC.JUSTIFY_CENTER:
#             # Clamp value et impose the center
#             if width <= 0:
#                 estimated_width = 0
#             elif width == 1:
#                 estimated_width = 0
#             else:
#                 estimated_width = int(width / 2)
#
#             # Clamp value et impose the center
#             if preferred_width is None:
#                 estimated_preferred_width = 0
#             elif preferred_width <= 0:
#                 estimated_preferred_width = 0
#             elif preferred_width == 1:
#                 estimated_preferred_width = 0
#             else:
#                 estimated_preferred_width = int(preferred_width / 2)
#
#             # Make the compute
#             final_value = int(estimated_width - estimated_preferred_width)
#
#             # clamp the result
#             if final_value <= 0:
#                 final_value = 0
#
#             # Finally set the value
#             self.__x_offset = final_value
#
#         elif self.get_justify() == GLXCurses.GLXC.JUSTIFY_LEFT:
#
#             # Finally set the value
#             self.__x_offset = 0
#
#         elif self.get_justify() == GLXCurses.GLXC.JUSTIFY_RIGHT:
#
#             # Clamp estimated_width
#             estimated_width = GLXCurses.clamp_to_zero(width)
#
#             # Clamp preferred_width
#             estimated_preferred_width = GLXCurses.clamp_to_zero(preferred_width)
#
#             # Make the compute
#             final_value = int(estimated_width - estimated_preferred_width)
#
#             # clamp the result
#             if final_value <= 0:
#                 final_value = 0
#
#             # Finally set the value
#             self.__x_offset = final_value
#
#         self.preferred_width = self._get_estimated_preferred_width()
#         self.preferred_height = self._get_estimated_preferred_height()
#         # Check y offset
#         self.__y_offset = 0
#
#     def _get_estimated_preferred_width(self):
#         """
#         Estimate a preferred width, by consider X Location, allowed width
#
#         :return: a estimated preferred width
#         :rtype: int
#         """
#         if self.get_border():
#             if self.get_display_scale():
#                 return self.space_reserved_for_scale + self.space_reserved_for_meter + self.border_len
#             else:
#                 return self.space_reserved_for_meter + self.border_len
#         else:
#             if self.get_display_scale():
#                 return self.space_reserved_for_scale + self.space_reserved_for_meter
#             else:
#                 return self.space_reserved_for_meter
#
#     def _get_estimated_preferred_height(self):
#         """
#         Estimate a preferred height, by consider Y Location
#
#         :return: a estimated preferred height
#         :rtype: int
#         """
#         return self.height

