import unittest

import GLXCurses


class TestApplicationController(unittest.TestCase):
    def test_active_window_id(self):
        monitor = GLXCurses.Spot()
        self.assertIsNone(monitor.active_window_id)
        monitor.active_window_id = 'Hello.40'
        self.assertEqual('Hello.40', monitor.active_window_id)
        self.assertIsNone(monitor.active_window_id_prev)
        monitor.active_window_id = 'Hello.41'
        self.assertEqual('Hello.41', monitor.active_window_id)
        self.assertEqual('Hello.40', monitor.active_window_id_prev)
        monitor.active_window_id = 'Hello.42'
        self.assertEqual('Hello.42', monitor.active_window_id)
        self.assertEqual('Hello.41', monitor.active_window_id_prev)

        self.assertRaises(TypeError, setattr, monitor, 'active_window_id', 42)
        self.assertRaises(TypeError, setattr, monitor, 'active_window_id_prev', 42)

    def test_active_window_id_prev(self):
        monitor = GLXCurses.Spot()
        self.assertIsNone(monitor.active_window_id)
        monitor.active_window_id = 'Hello.40'
        self.assertEqual('Hello.40', monitor.active_window_id)
        self.assertIsNone(monitor.active_window_id_prev)
        monitor.active_window_id = 'Hello.41'
        self.assertEqual('Hello.41', monitor.active_window_id)
        self.assertEqual('Hello.40', monitor.active_window_id_prev)
        monitor.active_window_id = 'Hello.42'
        self.assertEqual('Hello.42', monitor.active_window_id)
        self.assertEqual('Hello.41', monitor.active_window_id_prev)
        monitor.active_window_id_prev = 'Hello.42'
        self.assertEqual('Hello.42', monitor.active_window_id_prev)
        monitor.active_window_id_prev = 'Hello.43'
        self.assertEqual('Hello.43', monitor.active_window_id_prev)

        self.assertRaises(TypeError, setattr, monitor, 'active_window_id', 42)
        self.assertRaises(TypeError, setattr, monitor, 'active_window_id_prev', 42)

    def test_has_default(self):
        monitor = GLXCurses.Spot()
        widget = GLXCurses.Widget()
        self.assertIsNone(monitor.has_default)
        monitor.has_default = widget
        self.assertTrue(isinstance(monitor.has_default, GLXCurses.ChildElement))
        self.assertEqual(widget, monitor.has_default.widget)
        monitor.has_default = None
        self.assertIsNone(monitor.has_default)

        self.assertRaises(TypeError, setattr, monitor, 'has_default', 42)

    def test_has_focus(self):
        monitor = GLXCurses.Spot()
        widget = GLXCurses.Widget()
        self.assertIsNone(monitor.has_focus)
        monitor.has_focus = widget
        self.assertTrue(isinstance(monitor.has_focus, GLXCurses.ChildElement))
        self.assertEqual(widget, monitor.has_focus.widget)
        monitor.has_focus = None
        self.assertIsNone(monitor.has_focus)

        self.assertRaises(TypeError, setattr, monitor, 'has_focus', 42)

    def test_has_prelight(self):
        monitor = GLXCurses.Spot()
        widget = GLXCurses.Widget()
        self.assertIsNone(monitor.has_prelight)
        monitor.has_prelight = widget
        self.assertTrue(isinstance(monitor.has_prelight, GLXCurses.ChildElement))
        self.assertEqual(widget, monitor.has_prelight.widget)
        monitor.has_prelight = None
        self.assertIsNone(monitor.has_prelight)

        self.assertRaises(TypeError, setattr, monitor, 'has_prelight', 42)


if __name__ == '__main__':
    unittest.main()
