#!/usr/bin/env python
# -*- coding: utf-8 -*-
import GLXCurses
import curses
import logging


# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved


class HBox(GLXCurses.Box, GLXCurses.Dividable):
    """
    :Description:

    The :class:`HBox <GLXCurses.HBox.HBox>` is a container that organizes child widgets into a single row.

    Use the :class:`Box <GLXCurses.Box.Box>`  packing interface to determine the arrangement, spacing, width,
    and alignment of :class:`HBox <GLXCurses.HBox.HBox>` children.

    All children are allocated the same height.
    """

    def check_resize(self):
        pass

    def __init__(self):
        """
        :Attributes Details:

        .. py:attribute:: homogeneous

           TRUE if all children are to be given equal space allotments.

              +---------------+-------------------------------+
              | Type          | :py:__area_data:`bool`               |
              +---------------+-------------------------------+
              | Flags         | Read / Write                  |
              +---------------+-------------------------------+
              | Default value | TRUE                          |
              +---------------+-------------------------------+

        .. py:attribute:: spacing

           The number of char to place by default between children.

              +---------------+-------------------------------+
              | Type          | :py:__area_data:`int`                |
              +---------------+-------------------------------+
              | Flags         | Read / Write                  |
              +---------------+-------------------------------+
              | Default value | 0                             |
              +---------------+-------------------------------+
        """
        # Load heritage
        GLXCurses.Box.__init__(self)
        GLXCurses.Dividable.__init__(self)

        # It's a GLXCurse Type
        self.glxc_type = 'GLXCurses.HBox'
        self.name = '{0}{1}'.format(self.__class__.__name__, self.id)

        # Make a Widget Style heritage attribute as local attribute
        if self.style.attribute_states:
            if self.attribute_states != self.style.attribute_states:
                self.attribute_states = self.style.attribute_states

        self.preferred_height = 2
        self.preferred_width = 2

        # Default Value
        self.spacing = GLXCurses.clamp_to_zero(0)
        self.homogeneous = False

        self.children_area_end_coord = None

    def new(self, homogeneous=True, spacing=None):
        """
        Creates a new GLXCurses :class:`HBox <GLXCurses.HBox.HBox>`

        :param homogeneous: True if all children are to be given equal space allotments.
        :type homogeneous: bool
        :param spacing: The number of characters to place by default between children.
        :type spacing: int
        :return: a new :class:`HBox <GLXCurses.HBox.HBox>`.
        :raise TypeError: if ``homogeneous`` is not bool type
        :raise TypeError: if ``spacing`` is not int type or None
        """
        if type(homogeneous) != bool:
            raise TypeError('"homogeneous" argument must be a bool type')
        if spacing is not None:
            if type(spacing) != int:
                raise TypeError('"spacing" must be int type or None')

        self.__init__()
        self.spacing = GLXCurses.clamp_to_zero(spacing)
        self.homogeneous = homogeneous
        return self

    def draw_widget_in_area(self):
        self.create_or_resize()

        if self.subwin is not None:

            # Debug message
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

            if self.homogeneous:
                self._draw_homogeneous()
            else:
                self._draw_not_homogeneous()

    def _draw_not_homogeneous(self):
        # Check widgets to display

        # in case it have children attach to the widget.
        if self.children:

            # Get position dictionary like: {'0': (0, 32), '1': (33, 65), '2': (66, 99)}
            # dividable = GLXCurses.Dividable()
            self.start = self.x
            self.stop = self.width
            self.num = len(self.children)
            self.round_type = GLXCurses.GLXC.ROUND_DOWN
            # position = dividable.split_positions

            # position = GLXCurses.get_split_area_positions(
            #     start=self.x,
            #     stop=self.width,
            #     num=len(self.children),
            #     roundtype=GLXCurses.GLXC.ROUND_DOWN
            # )

            # for each children
            for child in self.children:
                # child.widget.style = self.style
                child.widget.stdscr = self.stdscr

                start, stop = self.split_positions['{0}'.format(child.properties.position)]

                child.widget.y = self.y
                child.widget.x = start
                child.widget.height = self.height
                #child.widget.width = (stop - start) + 1

                if child.properties.position == len(self.children) - 1:
                    if self.get_decorated():
                        child.widget.width = (self.width - child.widget.x + 1)
                    else:
                        child.widget.width = (self.width - child.widget.x)
                else:
                    child.widget.width = (stop - start + 1)

                if self.debug:
                    logging.debug(
                        "Set child -> x: {0}, y: {1}, width: {2}, height:{3}".format(
                            child.widget.x,
                            child.widget.y,
                            child.widget.width,
                            child.widget.height
                        )
                    )

                child.widget.draw_widget_in_area()

    def _draw_homogeneous(self):
        devised_box_size = int(self.width - 1 / len(self.children))
        total_horizontal_spacing = 0
        for child in self.children:

            # Check if that the first element
            if child.properties.position == 0:
                # position compute
                pos_y = self.y + self.spacing
                pos_x = self.x + self.spacing

                child.widget.x = pos_x
                child.widget.y = pos_y
                child.widget.width = devised_box_size - self.spacing + 1
                child.widget.height = self.height - self.spacing * 2
                child.widget.stdscr = self.stdscr
                total_horizontal_spacing += self.spacing

            # Check if that the last element
            elif child.properties.position == len(self.children) - 1:

                last_element_horizontal_size = self.width
                last_element_horizontal_size -= int(devised_box_size * child.properties.position)
                last_element_horizontal_size -= total_horizontal_spacing
                last_element_horizontal_size -= self.spacing

                pos_y = self.y + self.spacing
                pos_x = self.x
                pos_x += int(devised_box_size * child.properties.position)
                pos_x += int(self.spacing / 2)

                child.widget.x = int(pos_x)
                child.widget.y = int(pos_y)
                child.widget.width = int(last_element_horizontal_size)
                child.widget.height = int(self.height - self.spacing * 2)
                child.widget.stdscr = self.stdscr

            else:
                # position compute
                pos_y = self.y + self.spacing
                pos_x = self.x
                pos_x += int(devised_box_size * child.properties.position)
                pos_x += int(self.spacing / 2)

                child.widget.x = int(pos_x)
                child.widget.y = int(pos_y)
                child.widget.width = int(devised_box_size - int(self.spacing / 2))
                child.widget.height = int(self.height - self.spacing * 2)
                child.widget.stdscr = self.stdscr

                total_horizontal_spacing += int(self.spacing / 2)

            # Drawing
            child.widget.draw_widget_in_area()
