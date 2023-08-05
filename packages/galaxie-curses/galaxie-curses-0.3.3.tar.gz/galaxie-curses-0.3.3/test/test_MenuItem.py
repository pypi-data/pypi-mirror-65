import unittest
import GLXCurses


class TestMenuItem(unittest.TestCase):
    def test_text(self):
        menuitem = GLXCurses.MenuItem()
        self.assertIsNone(menuitem.text)
        menuitem.text = 'Hello.42'
        self.assertEqual('Hello.42', menuitem.text)
        menuitem.text = None
        self.assertIsNone(menuitem.text)

        self.assertRaises(TypeError, setattr, menuitem, 'text', 42)

    def test_text_short_cut(self):
        menuitem = GLXCurses.MenuItem()
        self.assertIsNone(menuitem.text_short_cut)
        menuitem.text_short_cut = 'Hello.42'
        self.assertEqual('Hello.42', menuitem.text_short_cut)
        menuitem.text_short_cut = None
        self.assertIsNone(menuitem.text_short_cut)

        self.assertRaises(TypeError, setattr, menuitem, 'text_short_cut', 42)

    def test_spacing(self):
        menuitem = GLXCurses.MenuItem()
        self.assertEqual(1, menuitem.spacing)

        menuitem.text = None
        self.assertEqual(1, menuitem.spacing)

        menuitem.spacing = 42
        self.assertEqual(42, menuitem.spacing)

        menuitem.spacing = -42
        self.assertEqual(0, menuitem.spacing)

        self.assertRaises(TypeError, setattr, menuitem, 'spacing', 'Hello.42')

    def test__update_preferred_sizes(self):
        menuitem = GLXCurses.MenuItem()
        self.assertEqual(0, menuitem.preferred_width)
        self.assertEqual(1, menuitem.preferred_height)

        menuitem._update_sizes()
        self.assertEqual(0, menuitem.preferred_width)
        self.assertEqual(1, menuitem.preferred_height)

        menuitem.text = 'Hello'
        menuitem._update_sizes()
        self.assertEqual(5, menuitem.preferred_width)

        menuitem.spacing = 1
        menuitem._update_sizes()
        self.assertEqual(5, menuitem.preferred_width)

        menuitem.text_short_cut = '42'
        menuitem._update_sizes()
        self.assertEqual(12, menuitem.preferred_width)

    def test_draw(self):
        app = GLXCurses.Application()
        win = GLXCurses.Window()
        menuitem = GLXCurses.MenuItem()
        win.add(menuitem)
        app.add_window(win)
        app.refresh()

if __name__ == '__main__':
    unittest.main()
