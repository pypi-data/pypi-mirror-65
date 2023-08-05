import unittest
import GLXCurses


class TestTextBuffer(unittest.TestCase):
    def test_cursor_position(self):
        text_buffer = GLXCurses.TextBuffer()
        self.assertEqual(0, text_buffer.cursor_position)
        text_buffer.cursor_position = 42
        self.assertEqual(42, text_buffer.cursor_position)
        text_buffer.cursor_position = -42
        self.assertEqual(0, text_buffer.cursor_position)

        self.assertRaises(TypeError, setattr, text_buffer, 'cursor_position', 'Hello.42')

    def test_has_selection(self):
        text_buffer = GLXCurses.TextBuffer()
        self.assertFalse(text_buffer.has_selection)
        text_buffer.has_selection = True
        self.assertTrue(text_buffer.has_selection)
        text_buffer.has_selection = None
        self.assertFalse(text_buffer.has_selection)

        self.assertRaises(TypeError, setattr, text_buffer, 'has_selection', 'hello.42')

    def test_text(self):
        text_buffer = GLXCurses.TextBuffer()
        text_buffer.text = None
        self.assertIsNone(text_buffer.text)
        text_buffer.text = 'Hello.42'
        self.assertEqual('Hello.42', text_buffer.text)

        self.assertRaises(TypeError, setattr, text_buffer, 'text', 42)


if __name__ == '__main__':
    unittest.main()
