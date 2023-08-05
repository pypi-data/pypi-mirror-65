#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import GLXCurses


class Bin(GLXCurses.Container):

    def __init__(self):
        """
        A container with just one child

        **Properties**

        **Description**

        The :class:`Bin <GLXCurses.Bin.Bin>` widget is a container with just one child. It is not very useful itself,
        but it is useful for deriving subclasses, since it provides common code needed for handling a single child widget.

        Many GLXCurses widgets are subclasses of :class:`Bin <GLXCurses.Bin.Bin>`, including
         * :class:`Window <GLXCurses.Window.Window>`
         * :class:`Button <GLXCurses.Button.Button>`
         * :class:`Frame <GLXCurses.Frame.Frame>`
         * :class:`HandleBox <GLXCurses.HandleBox.HandleBox>`
         * :class:`ScrolledWindow <GLXCurses.ScrolledWindow.ScrolledWindow>`
        """
        GLXCurses.Container.__init__(self)
        self.glxc_type = 'GLXCurses.Bin'
        self.name = '{0}{1}'.format(self.__class__.__name__, self.id)
        # if self.style.attribute_states:
        #     if self.attribute_states != self.style.attribute_states:
        #         self.attribute_states = self.style.attribute_states

    def check_resize(self):
        pass
