import unittest
import GLXCurses


class TestGroup(unittest.TestCase):
    def test_members(self):
        group = GLXCurses.Group()
        self.assertEqual([], group.members)
        group.members = ['Hello.42']
        self.assertEqual('Hello.42', group.members[0])
        group.members = None
        self.assertEqual([], group.members)
        self.assertRaises(TypeError, setattr, group, 'members', 42)

    def test_position(self):
        group = GLXCurses.Group()
        self.assertEqual(0, group.position)
        group.position = 42
        self.assertEqual(42, group.position)
        group.position = None
        self.assertEqual(0, group.position)

        self.assertRaises(TypeError, setattr, group, 'position', 'Hello.42')

    def test_is_member(self):
        group = GLXCurses.Group()
        widget_1 = GLXCurses.Widget()
        group_element = GLXCurses.GroupElement(widget_1)
        self.assertEqual([], group.members)
        self.assertFalse(group.is_member(widget_1))
        group.members.append(group_element)
        self.assertTrue(group.is_member(widget_1))
        self.assertFalse(group.is_member(None))

        self.assertRaises(TypeError, group.is_member, 42)

    def test_widget(self):
        group = GLXCurses.Group()
        widget_1 = GLXCurses.Widget()
        widget_2 = GLXCurses.Widget()
        group_element_1 = GLXCurses.GroupElement(widget_1)
        group_element_2 = GLXCurses.GroupElement(widget_2)

        group.members.append(group_element_1)
        group.members.append(group_element_2)

        self.assertTrue(group.is_member(widget_1))
        self.assertTrue(group.is_member(widget_2))

        group.position = 0
        self.assertEqual(widget_1, group.widget)

        group.position = 1
        self.assertEqual(widget_2, group.widget)

        group.members = None
        group.position = 0
        self.assertEqual(None, group.widget)

    def test_add(self):
        group = GLXCurses.Group()
        widget_1 = GLXCurses.Widget()
        widget_2 = GLXCurses.Widget()
        self.assertEqual(0, len(group.members))
        group.add(widget=widget_1)
        self.assertEqual(1, len(group.members))
        self.assertEqual(GLXCurses.GroupElement, type(group.members[0]))
        self.assertEqual(widget_1, group.members[0].widget)
        group.add(widget=widget_2)
        self.assertEqual(2, len(group.members))
        self.assertEqual(GLXCurses.GroupElement, type(group.members[1]))
        self.assertEqual(widget_2, group.members[1].widget)
        # Retry to add the same wigdet it should be ignore
        group.add(widget=widget_2)
        self.assertEqual(2, len(group.members))
        self.assertEqual(GLXCurses.GroupElement, type(group.members[1]))
        self.assertEqual(widget_2, group.members[1].widget)

        group.members = None
        self.assertEqual(0, len(group.members))

        self.assertRaises(TypeError, group.add, 42)

    def test_remove(self):
        group = GLXCurses.Group()
        widget_1 = GLXCurses.Widget()
        widget_2 = GLXCurses.Widget()
        group_element_1 = GLXCurses.GroupElement(widget_1)
        group_element_2 = GLXCurses.GroupElement(widget_2)

        group.members.append(group_element_1)
        group.members.append(group_element_2)

        self.assertTrue(group.is_member(widget_1))
        self.assertTrue(group.is_member(widget_2))

        group.remove(widget_1)
        self.assertFalse(group.is_member(widget_1))
        self.assertTrue(group.is_member(widget_2))

        group.remove(widget_2)
        self.assertFalse(group.is_member(widget_1))
        self.assertFalse(group.is_member(widget_2))

        self.assertRaises(TypeError, group.remove, None)

    def test_up(self):
        group = GLXCurses.Group()
        widget_1 = GLXCurses.Widget()
        widget_2 = GLXCurses.Widget()
        widget_3 = GLXCurses.Widget()
        group_element_1 = GLXCurses.GroupElement(widget_1)
        group_element_2 = GLXCurses.GroupElement(widget_2)
        group_element_3 = GLXCurses.GroupElement(widget_3)

        group.members.append(group_element_1)
        group.members.append(group_element_2)
        group.members.append(group_element_3)

        self.assertTrue(group.is_member(widget_1))
        self.assertTrue(group.is_member(widget_2))
        self.assertTrue(group.is_member(widget_3))

        self.assertEqual(0, group.position)
        self.assertEqual(widget_1, group.widget)

        group.up()
        self.assertEqual(1, group.position)
        self.assertEqual(widget_2, group.widget)

        group.up()
        self.assertEqual(2, group.position)
        self.assertEqual(widget_3, group.widget)

        group.up()
        self.assertEqual(0, group.position)
        self.assertEqual(widget_1, group.widget)

    def test_down(self):
        group = GLXCurses.Group()
        widget_1 = GLXCurses.Widget()
        widget_2 = GLXCurses.Widget()
        widget_3 = GLXCurses.Widget()
        group_element_1 = GLXCurses.GroupElement(widget_1)
        group_element_2 = GLXCurses.GroupElement(widget_2)
        group_element_3 = GLXCurses.GroupElement(widget_3)

        group.members.append(group_element_1)
        group.members.append(group_element_2)
        group.members.append(group_element_3)

        self.assertTrue(group.is_member(widget_1))
        self.assertTrue(group.is_member(widget_2))
        self.assertTrue(group.is_member(widget_3))

        self.assertEqual(0, group.position)
        self.assertEqual(widget_1, group.widget)

        group.down()
        self.assertEqual(2, group.position)
        self.assertEqual(widget_3, group.widget)

        group.down()
        self.assertEqual(1, group.position)
        self.assertEqual(widget_2, group.widget)

        group.down()
        self.assertEqual(0, group.position)
        self.assertEqual(widget_1, group.widget)


if __name__ == '__main__':
    unittest.main()
