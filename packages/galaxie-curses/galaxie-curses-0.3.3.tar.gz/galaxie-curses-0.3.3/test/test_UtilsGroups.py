import unittest
import GLXCurses


class TestGroup(unittest.TestCase):
    def test_members(self):
        groups = GLXCurses.Groups()
        self.assertEqual([], groups.groups)
        groups.groups = ['Hello.42']
        self.assertEqual('Hello.42', groups.groups[0])
        groups.groups = None
        self.assertEqual([], groups.groups)
        self.assertRaises(TypeError, setattr, groups, 'groups', 42)

    def test_position(self):
        groups = GLXCurses.Groups()
        self.assertEqual(0, groups.position)
        groups.position = 42
        self.assertEqual(42, groups.position)
        groups.position = None
        self.assertEqual(0, groups.position)

        self.assertRaises(TypeError, setattr, groups, 'position', 'Hello.42')

    def test_is_group(self):
        groups = GLXCurses.Groups()
        group_1 = GLXCurses.Group()
        group_2 = GLXCurses.Group()

        groups.groups.append(group_1)
        groups.groups.append(group_2)

        self.assertTrue(groups.is_group(group_1))
        self.assertTrue(groups.is_group(group_2))
        self.assertFalse(groups.is_group(None))

        self.assertRaises(TypeError, groups.is_group, 42)

    def test_group(self):
        groups = GLXCurses.Groups()
        group_1 = GLXCurses.Group()
        group_2 = GLXCurses.Group()

        self.assertEqual([], groups.groups)
        groups.groups.append(group_1)
        groups.groups.append(group_2)

        self.assertTrue(groups.is_group(group_1))
        self.assertTrue(groups.is_group(group_2))

        groups.position = 0
        self.assertEqual(group_1, groups.group)

        groups.position = 1
        self.assertEqual(group_2, groups.group)

        groups.groups = None
        self.assertEqual(None, groups.group)

    def test_add_group(self):
        groups = GLXCurses.Groups()
        group_1 = GLXCurses.Group()
        group_2 = GLXCurses.Group()
        self.assertEqual(0, len(groups.groups))
        groups.add_group(group_1)
        self.assertEqual(1, len(groups.groups))
        self.assertEqual(GLXCurses.Group, type(groups.groups[0]))
        groups.add_group(group_2)
        self.assertEqual(2, len(groups.groups))
        self.assertEqual(GLXCurses.Group, type(groups.groups[1]))
        # Retry to add the same wigdet it should be ignore
        groups.add_group(group_2)
        self.assertEqual(2, len(groups.groups))
        self.assertEqual(GLXCurses.Group, type(groups.groups[1]))

        groups.groups = None
        self.assertEqual(0, len(groups.groups))

        self.assertRaises(TypeError, groups.add_group, 42)

    def test_remove_group(self):
        groups = GLXCurses.Groups()
        group_1 = GLXCurses.Group()
        group_2 = GLXCurses.Group()

        groups.groups.append(group_1)
        groups.groups.append(group_2)

        self.assertTrue(groups.is_group(group_1))
        self.assertTrue(groups.is_group(group_2))

        groups.remove_group(group_1)
        self.assertFalse(groups.is_group(group_1))
        self.assertTrue(groups.is_group(group_2))

        groups.remove_group(group_2)
        self.assertFalse(groups.is_group(group_1))
        self.assertFalse(groups.is_group(group_2))

        self.assertRaises(TypeError, groups.remove_group, None)

    def test_up(self):
        groups = GLXCurses.Groups()
        group_element_1 = GLXCurses.Group()
        group_element_2 = GLXCurses.Group()
        group_element_3 = GLXCurses.Group()

        groups.groups.append(group_element_1)
        groups.groups.append(group_element_2)
        groups.groups.append(group_element_3)

        self.assertTrue(groups.is_group(group_element_1))
        self.assertTrue(groups.is_group(group_element_2))
        self.assertTrue(groups.is_group(group_element_3))

        self.assertEqual(0, groups.position)
        self.assertEqual(group_element_1, groups.group)

        groups.up()
        self.assertEqual(1, groups.position)
        self.assertEqual(group_element_2, groups.group)

        groups.up()
        self.assertEqual(2, groups.position)
        self.assertEqual(group_element_3, groups.group)

        groups.up()
        self.assertEqual(0, groups.position)
        self.assertEqual(group_element_1, groups.group)

    def test_down(self):
        groups = GLXCurses.Groups()
        group_element_1 = GLXCurses.Group()
        group_element_2 = GLXCurses.Group()
        group_element_3 = GLXCurses.Group()

        groups.groups.append(group_element_1)
        groups.groups.append(group_element_2)
        groups.groups.append(group_element_3)

        self.assertTrue(groups.is_group(group_element_1))
        self.assertTrue(groups.is_group(group_element_2))
        self.assertTrue(groups.is_group(group_element_3))

        self.assertEqual(0, groups.position)
        self.assertEqual(group_element_1, groups.group)

        groups.down()
        self.assertEqual(2, groups.position)
        self.assertEqual(group_element_3, groups.group)

        groups.down()
        self.assertEqual(1, groups.position)
        self.assertEqual(group_element_2, groups.group)

        groups.down()
        self.assertEqual(0, groups.position)
        self.assertEqual(group_element_1, groups.group)


if __name__ == '__main__':
    unittest.main()
