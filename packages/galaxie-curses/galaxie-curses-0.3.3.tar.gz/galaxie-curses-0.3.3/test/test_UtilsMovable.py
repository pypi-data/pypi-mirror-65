import unittest
import GLXCurses


class TestGLXCMovable(unittest.TestCase):
    def test_x_offset(self):
        movable = GLXCurses.Movable()
        self.assertEqual(0, movable.x_offset)
        movable.x_offset = 42
        self.assertEqual(42, movable.x_offset)
        movable.x_offset = None
        self.assertEqual(0, movable.x_offset)

        self.assertRaises(TypeError, setattr, movable, 'x_offset', 'Hello.42')

    def test_y_offset(self):
        movable = GLXCurses.Movable()
        self.assertEqual(0, movable.y_offset)
        movable.y_offset = 24
        self.assertEqual(24, movable.y_offset)
        movable.y_offset = None
        self.assertEqual(0, movable.y_offset)

        self.assertRaises(TypeError, setattr, movable, 'y_offset', 'Hello.42')

    def test_justify(self):
        movable = GLXCurses.Movable()
        movable.justify = 'LEFT'
        self.assertEqual('LEFT', movable.justify)
        movable.justify = 'CENTER'
        self.assertEqual('CENTER', movable.justify)
        movable.justify = 'RIGHT'
        self.assertEqual('RIGHT', movable.justify)
        movable.justify = None
        self.assertEqual('CENTER', movable.justify)

        self.assertRaises(TypeError, setattr, movable, 'justify', 42)
        self.assertRaises(ValueError, setattr, movable, 'justify', 'Hello.42')

    def test_position_type(self):
        movable = GLXCurses.Movable()

        movable.position_type = 'CENTER'
        for position in GLXCurses.GLXC.PositionType:
            movable.position_type = position
            self.assertEqual(movable.position_type, position)

        movable.position_type = None
        self.assertEqual('CENTER', movable.position_type)

        self.assertRaises(TypeError, setattr, movable, 'position_type', 42)
        self.assertRaises(ValueError, setattr, movable, 'position_type', 'HELLO')


if __name__ == '__main__':
    unittest.main()
