import unittest

from GLXCurses import GLXC
import GLXCurses


class TestChildProperty(unittest.TestCase):
    def test_expand(self):
        child = GLXCurses.ChildProperty()
        self.assertFalse(child.expand)
        child.expand = True
        self.assertTrue(child.expand)
        child.expand = None
        self.assertFalse(child.expand)

        self.assertRaises(TypeError, setattr, child, 'expand', 'Hello.42')

    def test_fill(self):
        child = GLXCurses.ChildProperty()
        self.assertTrue(child.fill)
        child.fill = False
        self.assertFalse(child.fill)
        child.fill = None
        self.assertTrue(child.fill)

        self.assertRaises(TypeError, setattr, child, 'fill', 'Hello.42')

    def test_pack_type(self):
        child = GLXCurses.ChildProperty()
        self.assertEqual(GLXC.PACK_START, child.pack_type)
        child.pack_type = GLXC.PACK_END
        self.assertEqual(GLXC.PACK_END, child.pack_type)
        child.pack_type = None
        self.assertEqual(GLXC.PACK_START, child.pack_type)

        self.assertRaises(TypeError, setattr, child, 'pack_type', 42)
        self.assertRaises(ValueError, setattr, child, 'pack_type', 'Hello.42')

    def test_padding(self):
        child = GLXCurses.ChildProperty()
        self.assertEqual(0, child.padding)
        child.padding = 42
        self.assertEqual(42, child.padding)
        child.padding = None
        self.assertEqual(0, child.padding)

        self.assertRaises(TypeError, setattr, child, 'padding', 'Hello.42')

    def test_position(self):
        child = GLXCurses.ChildProperty()
        self.assertEqual(0, child.position)
        child.position = 42
        self.assertEqual(42, child.position)
        child.position = None
        self.assertEqual(0, child.position)

        self.assertRaises(TypeError, setattr, child, 'position', 'Hello.42')


if __name__ == '__main__':
    unittest.main()
