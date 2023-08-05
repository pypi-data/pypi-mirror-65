import unittest
import GLXCurses


class TestGroupElement(unittest.TestCase):
    def test_widget(self):
        widget = GLXCurses.Widget()
        group_element = GLXCurses.GroupElement()
        self.assertEqual(None, group_element.widget)
        group_element.widget = widget
        self.assertEqual(widget, group_element.widget)
        group_element.widget = None
        self.assertEqual(None, group_element.widget)
        self.assertRaises(TypeError, setattr, group_element, 'widget', 42)


if __name__ == '__main__':
    unittest.main()
