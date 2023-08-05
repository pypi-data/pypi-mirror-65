import unittest
import GLXCurses


class TestProgressBar(unittest.TestCase):
    def tearDown(self):
        GLXCurses.Application().refresh()

    def setUp(self):
        self.win = GLXCurses.Window()
        self.progress_bar = GLXCurses.ProgressBar()
        GLXCurses.Application().add_window(self.win)
        self.win.add(self.progress_bar)

    def test_text(self):
        self.progress_bar.text = None
        self.assertIsNone(self.progress_bar.text)
        self.progress_bar.text = 'Hello.42'
        self.assertEqual('Hello.42', self.progress_bar.text)

        self.assertRaises(TypeError, setattr, self.progress_bar, 'text', 42)

    def test_show_text(self):
        self.progress_bar.show_text = True
        self.assertTrue(self.progress_bar.show_text)
        self.progress_bar.show_text = False
        self.assertFalse(self.progress_bar.show_text)
        self.progress_bar.show_text = None
        self.assertFalse(self.progress_bar.show_text)

        self.assertRaises(TypeError, setattr, self.progress_bar, 'show_text', 'Hello.42')

    def test_value(self):
        self.assertEqual(0, self.progress_bar.value)
        self.progress_bar.value = 42
        self.assertEqual(42, self.progress_bar.value)

        self.progress_bar.value = None
        self.assertEqual(0, self.progress_bar.value)

        self.progress_bar.value = 4242
        self.assertEqual(100, self.progress_bar.value)

        self.progress_bar.value = -4242
        self.assertEqual(0, self.progress_bar.value)

        self.assertRaises(TypeError, setattr, self.progress_bar, 'value', 'Hello.42')

    def test_draw_widget_in_area(self):
        for i in range(0, 101):
            self.progress_bar.value = i


if __name__ == '__main__':
    unittest.main()
