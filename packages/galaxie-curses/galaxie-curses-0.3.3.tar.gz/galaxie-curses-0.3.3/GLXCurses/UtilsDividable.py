#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved
from array import array

import GLXCurses


class Dividable(object):
    def __init__(self):
        self.__start = None
        self.__stop = None
        self.__num = None
        self.__round_type = None

        self.start = None
        self.stop = None
        self.num = None
        self.round_type = None

    @property
    def start(self):
        return self.__start

    @start.setter
    def start(self, start=None):
        if start is not None and type(start) != int:
            raise TypeError('"start" must be int type or None')
        if self.start != GLXCurses.clamp_to_zero(start):
            self.__start = GLXCurses.clamp_to_zero(start)

    @property
    def stop(self):
        return self.__stop

    @stop.setter
    def stop(self, stop=None):
        if stop is not None and type(stop) != int:
            raise TypeError('"stop" must be int type or None')
        if self.stop != GLXCurses.clamp_to_zero(stop):
            self.__stop = GLXCurses.clamp_to_zero(stop)

    @property
    def num(self):
        return self.__num

    @num.setter
    def num(self, num=None):
        if num is not None and type(num) != int:
            raise TypeError('"num" must be int type or None')
        if self.num != GLXCurses.clamp_to_zero(num):
            self.__num = GLXCurses.clamp_to_zero(num)

    @property
    def round_type(self):
        return self.__round_type

    @round_type.setter
    def round_type(self, round_type=None):
        if round_type is not None and type(round_type) != str:
            raise TypeError('"round_type" must be str type or None')
        if round_type is not None and round_type not in [GLXCurses.GLXC.ROUND_UP,
                                                         GLXCurses.GLXC.ROUND_DOWN,
                                                         GLXCurses.GLXC.ROUND_HALF_UP,
                                                         GLXCurses.GLXC.ROUND_HALF_DOWN]:
            raise ValueError('"round_type" must be Valid round Type or None')

        if self.round_type != round_type:
            self.__round_type = round_type

    @property
    def split_positions(self):
        """
        np.linspace(3, 9, 10)
            array([ 3.,  3.66666667,  4.33333333,  5. ,  5.66666667, 6.33333333,  7. ,  7.66666667,  8.33333333,  9. ])

        :param start:
        :param stop:
        :param num:
        :param roundtype:
        :return:
        """
        # ###############################################################
        # TODO: Fix infinity loop with a better method
        # MUST BE HERE FOR THE MOMENT
        # ###############################################################
        if self.start >= self.stop or self.stop - self.start < self.num:
            thing_to_return = dict()
            count = 0
            for i in range(self.num):

                item_start = 0
                item_stop = 0
                thing_to_return[str(count)] = (item_start, item_stop)
                count += 1
            return thing_to_return
        # ###############################################################
        # MUST BE HERE FOR THE MOMENT
        # ###############################################################

        position_list = array('l')
        value = self.start
        while value <= self.stop:
            position_list.append(int(value))
            if self.round_type == GLXCurses.GLXC.ROUND_UP:
                value += GLXCurses.round_up((self.stop - self.start) / self.num, decimals=0)

            elif self.round_type == GLXCurses.GLXC.ROUND_DOWN:
                value += GLXCurses.round_down((self.stop - self.start) / self.num, decimals=0)

            elif self.round_type == GLXCurses.GLXC.ROUND_HALF_UP:
                value += GLXCurses.round_half_up((self.stop - self.start) / self.num, decimals=0)

            elif self.round_type == GLXCurses.GLXC.ROUND_HALF_DOWN:
                value += int(GLXCurses.round_half_down((self.stop - self.start) / self.num, decimals=0))
            else:
                value += int((self.stop - self.start) / self.num)

        thing_to_return = dict()
        count = 0
        for i in range(self.num):
            if count + 1 >= self.num:
                item_start = position_list[int(count)]
                item_stop = self.stop
            else:
                item_start = position_list[int(count)]
                item_stop = position_list[int(count + 1)] - 1

            thing_to_return[str(count)] = (item_start, item_stop)
            count += 1
        return thing_to_return
