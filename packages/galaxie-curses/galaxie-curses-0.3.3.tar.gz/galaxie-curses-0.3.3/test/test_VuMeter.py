#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

# Require when you haven't GLXCurses as default Package
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(current_dir))
import unittest
import GLXCurses


# Unittest
# class TestVuMeter(unittest.TestCase):
#
#     # Test
#     def test_glxc_type(self):
#         """Test VuMeter Type"""
#         vumeter = GLXCurses.VuMeter()
#         self.assertTrue(GLXCurses.glxc_type(vumeter))
#
#     def test_draw_widget_in_area(self):
#         """Test VSeparator.draw_widget_in_area()"""
#
#         win = GLXCurses.Window()
#         vumeter = GLXCurses.VuMeter()
#         vumeter.set_value(50)
#         vumeter.set_text('dBFS')
#         vumeter.set_display_text(True)
#         vumeter.set_justify('right')
#         vumeter.set_border(True)
#
#         win.add(vumeter)
#
#         GLXCurses.Application().add_window(win)
#         # Main loop
#         # entry.draw_widget_in_area()
#         GLXCurses.Application().refresh()
#         vumeter.set_border(False)
#         GLXCurses.Application().refresh()
#         vumeter.set_border(True)
#         GLXCurses.Application().refresh()
#         vumeter.set_display_text(True)
#         GLXCurses.Application().refresh()
#         vumeter.set_display_text(False)
#         GLXCurses.Application().refresh()
#         vumeter.set_justify('left')
#         GLXCurses.Application().refresh()
#         vumeter.set_justify('center')
#         GLXCurses.Application().refresh()
#         vumeter.set_justify('right')
#         GLXCurses.Application().refresh()
#         vumeter.draw_widget_in_area()
#
#         # impossible to test the curse error
#
#     def test_VuMeter_set_text(self):
#         """Test VuMeter.set_text()"""
#
#         vumeter = GLXCurses.VuMeter()
#
#         self.assertEqual('dBFS', vumeter.text)
#
#         vumeter.set_text('LBU')
#         self.assertEqual('LBU', vumeter.text)
#
#         self.assertRaises(TypeError, vumeter.set_text, 42)
#
#     def test_VuMeter_get_text(self):
#         """Test VuMeter.get_text()"""
#         vumeter = GLXCurses.VuMeter()
#
#         self.assertEqual('dBFS', vumeter.get_text())
#
#         vumeter.text = '42'
#         self.assertEqual('42', vumeter.get_text())
#
#     def test_VuMeter_set_display_text(self):
#         """Test VuMeter.set_display_text()"""
#
#         vumeter = GLXCurses.VuMeter()
#
#         self.assertEqual(True, vumeter.display_text)
#
#         vumeter.set_display_text(False)
#         self.assertEqual(False, vumeter.display_text)
#
#         self.assertRaises(TypeError, vumeter.set_display_text, 42)
#
#     def test_VuMeter_get_display_text(self):
#         """Test VuMeter.get_display_text()"""
#         vumeter = GLXCurses.VuMeter()
#
#         self.assertEqual(True, vumeter.get_display_text())
#
#         vumeter.display_text = False
#         self.assertEqual(False, vumeter.get_display_text())
#
#     def test_VuMeter_set_display_scale(self):
#         """Test VuMeter.set_display_text()"""
#
#         vumeter = GLXCurses.VuMeter()
#
#         self.assertEqual(True, vumeter.display_scale)
#
#         vumeter.set_display_scale(False)
#         self.assertEqual(False, vumeter.display_scale)
#
#         self.assertRaises(TypeError, vumeter.set_display_scale, 42)
#
#     def test_VuMeter_get_display_scale(self):
#         """Test VuMeter.get_display_scale()"""
#         vumeter = GLXCurses.VuMeter()
#
#         self.assertEqual(True, vumeter.get_display_scale())
#
#         vumeter.display_scale = False
#         self.assertEqual(False, vumeter.get_display_scale())
#
#     def test_VuMeter_get_scale_min(self):
#         """Test VuMeter.get_scale_min()"""
#         vumeter = GLXCurses.VuMeter()
#
#         self.assertEqual(0, vumeter.get_scale_min())
#
#         vumeter.scale_min = 42
#         self.assertEqual(42, vumeter.get_scale_min())
#
#     def test_VuMeter_set_scale_min(self):
#         """Test VuMeter.set_scale_min()"""
#         vumeter = GLXCurses.VuMeter()
#
#         self.assertEqual(0, vumeter.scale_min)
#
#         vumeter.set_scale_min(42)
#         self.assertEqual(42, vumeter.scale_min)
#
#         self.assertRaises(TypeError, vumeter.set_scale_min, None)
#
#     def test_VuMeter_get_scale_max(self):
#         """Test VuMeter.get_scale_max()"""
#         vumeter = GLXCurses.VuMeter()
#
#         self.assertEqual(32767, vumeter.get_scale_max())
#
#         vumeter.scale_max = 42
#         self.assertEqual(42, vumeter.get_scale_max())
#
#     def test_VuMeter_set_scale_max(self):
#         """Test VuMeter.set_scale_max()"""
#         vumeter = GLXCurses.VuMeter()
#
#         self.assertEqual(32767, vumeter.scale_max)
#
#         vumeter.set_scale_max(42)
#         self.assertEqual(42, vumeter.scale_max)
#
#         self.assertRaises(TypeError, vumeter.set_scale_max, None)
#
#     def test_VuMeter_set_value(self):
#         """Test VuMeter.set_value"""
#
#         vumeter = GLXCurses.VuMeter()
#
#         self.assertEqual(0, vumeter.value)
#
#         vumeter.set_value(42)
#         self.assertEqual(42, vumeter.value)
#
#         # Do it clamp ?
#         vumeter.set_scale_min(10)
#         vumeter.set_scale_max(42)
#         vumeter.set_value(50)
#         self.assertEqual(42, vumeter.value)
#
#         self.assertRaises(TypeError, vumeter.set_value, '42')
#
#     def test_VuMeter_get_value(self):
#         """Test VuMeter.get_value()"""
#         vumeter = GLXCurses.VuMeter()
#
#         self.assertEqual(0, vumeter.get_value())
#
#         vumeter.value = 42
#         self.assertEqual(42, vumeter.get_value())
#
#     def test_VuMeter_set_get_justify(self):
#         """Test VuMeter.set_justify() and VuMeter.get_justify()"""
#         vumeter = GLXCurses.VuMeter()
#
#         vumeter.set_justify(GLXCurses.GLXC.JUSTIFY_CENTER)
#         self.assertEqual(vumeter.get_justify(), GLXCurses.GLXC.JUSTIFY_CENTER)
#
#         vumeter.set_justify(GLXCurses.GLXC.JUSTIFY_LEFT)
#         self.assertEqual(vumeter.get_justify(), GLXCurses.GLXC.JUSTIFY_LEFT)
#
#         vumeter.set_justify(GLXCurses.GLXC.JUSTIFY_RIGHT)
#         self.assertEqual(vumeter.get_justify(), GLXCurses.GLXC.JUSTIFY_RIGHT)
#
#         vumeter.set_justify(GLXCurses.GLXC.JUSTIFY_FILL)
#         self.assertEqual(vumeter.get_justify(), GLXCurses.GLXC.JUSTIFY_FILL)
#
#         self.assertRaises(TypeError, vumeter.set_justify, 'HELLO')
#
#     def test_VuMeter_set_border(self):
#         """Test VuMeter.set_border()"""
#
#         vumeter = GLXCurses.VuMeter()
#
#         self.assertEqual(False, vumeter.border)
#
#         vumeter.set_border(True)
#         self.assertEqual(True, vumeter.border)
#
#         self.assertRaises(TypeError, vumeter.set_border, 42)
#
#     def test_VuMeter_get_border(self):
#         """Test VuMeter.get_border()"""
#         vumeter = GLXCurses.VuMeter()
#
#         self.assertEqual(False, vumeter.get_border())
#
#         vumeter.border = True
#         self.assertEqual(True, vumeter.get_border())
#
#     def test_VuMeter__get_estimated_preferred_width(self):
#         """Test VSeparator._get_estimated_preferred_width()"""
#         vumeter = GLXCurses.VuMeter()
#         self.assertGreater(vumeter._get_estimated_preferred_width(), 1)
#
#     def test_VuMeter__get_estimated_preferred_height(self):
#         """Test VuMeter._get_estimated_preferred_height()"""
#         vumeter = GLXCurses.VuMeter()
#         vumeter.y = 20
#         vumeter.height = 20
#         self.assertEqual(vumeter._get_estimated_preferred_height(), 20)
#
#     # def test_VuMeter__set__get_vseperator_x(self):
#     #     """Test VuMeter._set_vseperator_x() and VuMeter._get_vseperator_x()"""
#     #     vumeter = VuMeter()
#     #     # call set_decorated() with 0 as argument
#     #     vumeter._set_x_offset(0)
#     #     # verify we go back 0
#     #     self.assertEqual(vumeter._get_x_offset(), 0)
#     #     # call set_decorated() with 0 as argument
#     #     vumeter._set_x_offset(42)
#     #     # verify we go back 0
#     #     self.assertEqual(vumeter._get_x_offset(), 0)
#     #     # test raise TypeError
#     #     self.assertRaises(TypeError, vumeter._set_x_offset, 'Galaxie')
#
#     # def test_VuMeter__set__get_vseperator_y(self):
#     #     """Test VuMeter._set_vseperator_y() and VuMeter._get_vseperator_y()"""
#     #     vumeter = VuMeter()
#     #     # call set_decorated() with 0 as argument
#     #     vumeter._set_y_offset(0)
#     #     # verify we go back 0
#     #     self.assertEqual(vumeter._get_y_offset(), 0)
#     #     # call set_decorated() with 0 as argument
#     #     vumeter._set_y_offset(42)
#     #     # verify we go back 0
#     #     self.assertEqual(vumeter._get_y_offset(), 0)
#     #     # test raise TypeError
#     #     self.assertRaises(TypeError, vumeter._set_y_offset, 'Galaxie')
#
#
# if __name__ == '__main__':
#     unittest.main()
