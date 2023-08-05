#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import unittest
import GLXCurses

################################################################################
# IT TEST IS REQUIRE FORE CLOSE THE GLXCURSES APPLICATION AFTER UNITTEST TESTS #
################################################################################


# Unittest
class TestZZZ(unittest.TestCase):
    def setUp(self):
        """Get Application Singleton"""
        # Before the test start
        # self.application = GLXCurses.Application()
        GLXCurses.Application().refresh()



    def test_GLXCurses_final_refresh(self):
        """GLXCurses Final refresh"""
        # entry.draw_widget_in_area()
        GLXCurses.Application().refresh()
        GLXCurses.Application().screen.close()
