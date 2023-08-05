import unittest
import GLXCurses


class TestTextView(unittest.TestCase):

    def tearDown(self):
        GLXCurses.Application().refresh()

    def setUp(self):
        self.win = GLXCurses.Window()
        self.text_view = GLXCurses.TextView()
        GLXCurses.Application().add_window(self.win)
        self.win.add(self.text_view)

    def test_accept_tab(self):
        self.assertTrue(self.text_view.accept_tab)
        self.text_view.accept_tab = False
        self.assertFalse(self.text_view.accept_tab)
        self.text_view.accept_tab = None
        self.assertTrue(self.text_view.accept_tab)

        self.assertRaises(TypeError, setattr, self.text_view, 'accept_tab', 'Hello.42')

    def test_bottom_margin(self):
        self.assertEqual(0, self.text_view.bottom_margin)

        self.text_view.bottom_margin = 42
        self.assertEqual(42, self.text_view.bottom_margin)

        self.text_view.bottom_margin = None
        self.assertEqual(0, self.text_view.bottom_margin)

        self.text_view.bottom_margin = -42
        self.assertEqual(0, self.text_view.bottom_margin)

        self.assertRaises(TypeError, setattr, self.text_view, 'bottom_margin', 'Hello.42')

    def test_buffer(self):
        self.assertIsNotNone(self.text_view.buffer)
        self.text_view.buffer = GLXCurses.TextBuffer()
        self.assertTrue(isinstance(self.text_view.buffer, GLXCurses.TextBuffer))

        self.text_view.buffer = None
        self.assertIsNone(self.text_view.buffer)

        self.assertRaises(TypeError, setattr, self.text_view, 'buffer', 'Hello.42')

    def test_editable(self):
        self.assertTrue(self.text_view.editable)
        self.text_view.editable = False
        self.assertFalse(self.text_view.editable)
        self.text_view.editable = None
        self.assertTrue(self.text_view.editable)

        self.assertRaises(TypeError, setattr, self.text_view, 'editable', 'Hello.42')

    def test_cursor_visible(self):
        self.assertTrue(self.text_view.cursor_visible)
        self.text_view.cursor_visible = False
        self.assertFalse(self.text_view.cursor_visible)
        self.text_view.cursor_visible = None
        self.assertTrue(self.text_view.cursor_visible)

        self.assertRaises(TypeError, setattr, self.text_view, 'cursor_visible', 'Hello.42')

    def test_indent(self):
        self.assertEqual(0, self.text_view.indent)

        self.text_view.indent = 42
        self.assertEqual(42, self.text_view.indent)

        self.text_view.indent = None
        self.assertEqual(0, self.text_view.indent)

        self.text_view.indent = -42
        self.assertEqual(0, self.text_view.indent)

        self.assertRaises(TypeError, setattr, self.text_view, 'indent', 'Hello.42')

    def test_input_hints(self):
        self.assertEqual(GLXCurses.GLXC.INPUT_HINTS_NONE, self.text_view.input_hints)

        for input_hints in GLXCurses.GLXC.InputHints:
            self.text_view.input_hints = input_hints
            self.assertEqual(input_hints, self.text_view.input_hints)

        self.text_view.input_hints = None
        self.assertRaises(TypeError, setattr, self.text_view, 'input_hints', 42)
        self.assertRaises(ValueError, setattr, self.text_view, 'input_hints', 'Hello.42')

    def test_input_purpose(self):
        self.assertEqual(GLXCurses.GLXC.INPUT_PURPOSE_FREE_FORM, self.text_view.input_purpose)
        for input_purpose in GLXCurses.GLXC.InputPurpose:
            self.text_view.input_purpose = input_purpose
            self.assertEqual(input_purpose, self.text_view.input_purpose)

        self.text_view.input_purpose = None
        self.assertEqual(GLXCurses.GLXC.INPUT_PURPOSE_FREE_FORM, self.text_view.input_purpose)
        self.assertRaises(TypeError, setattr, self.text_view, 'input_purpose', 42)
        self.assertRaises(ValueError, setattr, self.text_view, 'input_purpose', 'Hello.42')

    def test_justification(self):
        for justification in GLXCurses.GLXC.Justification:
            self.text_view.justification = justification
            self.assertEqual(justification, self.text_view.justification)

        self.text_view.justification = None
        self.assertEqual(GLXCurses.GLXC.JUSTIFY_CENTER, self.text_view.justification)

        self.assertRaises(TypeError, setattr, self.text_view, 'justification', 42)
        self.assertRaises(ValueError, setattr, self.text_view, 'justification', 'Hello.42')

    def test_left_margin(self):
        self.assertEqual(0, self.text_view.left_margin)

        self.text_view.left_margin = 42
        self.assertEqual(42, self.text_view.left_margin)

        self.text_view.left_margin = None
        self.assertEqual(0, self.text_view.left_margin)

        self.text_view.left_margin = -42
        self.assertEqual(0, self.text_view.left_margin)

        self.assertRaises(TypeError, setattr, self.text_view, 'left_margin', 'Hello.42')

    def test_overwrite(self):
        self.assertFalse(self.text_view.overwrite)
        self.text_view.overwrite = None
        self.assertFalse(self.text_view.overwrite)
        self.text_view.overwrite = True
        self.assertTrue(self.text_view.overwrite)

        self.assertRaises(TypeError, setattr, self.text_view, 'overwrite', 'Hello.42')

    def test_populate_all(self):
        self.assertTrue(self.text_view.populate_all)
        self.text_view.populate_all = None
        self.assertTrue(self.text_view.populate_all)
        self.text_view.populate_all = False
        self.assertFalse(self.text_view.populate_all)

        self.assertRaises(TypeError, setattr, self.text_view, 'populate_all', 'Hello.42')

    def test_right_margin(self):
        self.assertEqual(0, self.text_view.right_margin)

        self.text_view.right_margin = 42
        self.assertEqual(42, self.text_view.right_margin)

        self.text_view.right_margin = None
        self.assertEqual(0, self.text_view.right_margin)

        self.text_view.right_margin = -42
        self.assertEqual(0, self.text_view.right_margin)

        self.assertRaises(TypeError, setattr, self.text_view, 'right_margin', 'Hello.42')

    def test_top_margin(self):
        self.assertEqual(0, self.text_view.top_margin)

        self.text_view.top_margin = 42
        self.assertEqual(42, self.text_view.top_margin)

        self.text_view.top_margin = None
        self.assertEqual(0, self.text_view.top_margin)

        self.text_view.top_margin = -42
        self.assertEqual(0, self.text_view.top_margin)

        self.assertRaises(TypeError, setattr, self.text_view, 'top_margin', 'Hello.42')

    def test_wrap_mode(self):
        for wrap_mode in GLXCurses.GLXC.WrapMode:
            self.text_view.wrap_mode = wrap_mode
            self.assertEqual(wrap_mode, self.text_view.wrap_mode)

        self.text_view.wrap_mode = None
        self.assertEqual(GLXCurses.GLXC.WRAP_NONE, self.text_view.wrap_mode)

        self.assertRaises(TypeError, setattr, self.text_view, 'wrap_mode', 42)
        self.assertRaises(ValueError, setattr, self.text_view, 'wrap_mode', 'Hello.42')


if __name__ == '__main__':
    unittest.main()
