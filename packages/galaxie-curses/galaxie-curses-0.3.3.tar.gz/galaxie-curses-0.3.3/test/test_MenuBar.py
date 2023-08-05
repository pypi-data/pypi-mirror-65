import unittest
import GLXCurses


class TestMenuBar(unittest.TestCase):
    def test_info_label(self):
        menubar = GLXCurses.MenuBar()
        self.assertIsNone(menubar.info_label)
        menubar.info_label = 'Hello.42'
        self.assertEqual('Hello.42', menubar.info_label)
        menubar.info_label = None
        self.assertIsNone(menubar.info_label)

        self.assertRaises(TypeError, setattr, menubar, 'info_label', 42)

    def test__update_position(self):
        menubar = GLXCurses.MenuBar()
        menu1 = GLXCurses.Menu()
        menu2 = GLXCurses.Menu()
        menu1.title = 'Hello.1'
        menu2.title = 'Hello.2'
        menubar._upgrade_position()

        self.assertEqual([], menubar.list_machin)
        menubar.pack_start(menu1)
        menubar.pack_start(menu2)
        menubar._upgrade_position()
        self.assertEqual([{'start': 1, 'stop': 11}, {'start': 12, 'stop': 22}], menubar.list_machin)

    def test_selected_menu(self):
        menubar = GLXCurses.MenuBar()
        self.assertEqual(0, menubar.selected_menu)
        menubar.selected_menu = 42
        self.assertEqual(42, menubar.selected_menu)
        menubar.selected_menu = None
        self.assertIsNone(menubar.selected_menu)

        self.assertRaises(TypeError, setattr, menubar, 'selected_menu', 'Hello.42')

    def test_selected_menu_item(self):
        menubar = GLXCurses.MenuBar()
        self.assertEqual(0, menubar.selected_menu_item)
        menubar.selected_menu_item = 42
        self.assertEqual(42, menubar.selected_menu_item)
        menubar.selected_menu_item = None
        self.assertEqual(0, menubar.selected_menu_item)
        self.assertRaises(TypeError, setattr, menubar, 'selected_menu_item', 'Hello.42')


if __name__ == '__main__':
    unittest.main()
