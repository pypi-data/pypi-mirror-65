import unittest

import GLXCurses


class TestTextTag(unittest.TestCase):
    def test_accumulative_margin(self):
        text_tag = GLXCurses.TextTag()
        self.assertFalse(text_tag.accumulative_margin)

        text_tag.accumulative_margin = True
        self.assertTrue(text_tag.accumulative_margin)

        text_tag.accumulative_margin = None
        self.assertFalse(text_tag.accumulative_margin)

        self.assertRaises(TypeError, setattr, text_tag, 'accumulative_margin', 42)

    def test_background(self):
        text_tag = GLXCurses.TextTag()
        self.assertEqual('BLUE', text_tag.background)

        text_tag.background = 'WHITE'
        self.assertEqual('WHITE', text_tag.background)

        text_tag.background = None
        self.assertEqual('BLUE', text_tag.background)

        self.assertRaises(TypeError, setattr, text_tag, 'background', 42)

    def test_background_full_height(self):
        text_tag = GLXCurses.TextTag()
        self.assertFalse(text_tag.background_full_height)

        text_tag.background_full_height = True
        self.assertTrue(text_tag.background_full_height)

        text_tag.background_full_height = None
        self.assertFalse(text_tag.background_full_height)

        self.assertRaises(TypeError, setattr, text_tag, 'background_full_height', 42)

    def test_background_full_height_set(self):
        text_tag = GLXCurses.TextTag()
        self.assertFalse(text_tag.background_full_height_set)

        text_tag.background_full_height_set = True
        self.assertTrue(text_tag.background_full_height_set)

        text_tag.background_full_height_set = None
        self.assertFalse(text_tag.background_full_height_set)

        self.assertRaises(TypeError, setattr, text_tag, 'background_full_height_set', 42)


if __name__ == '__main__':
    unittest.main()
