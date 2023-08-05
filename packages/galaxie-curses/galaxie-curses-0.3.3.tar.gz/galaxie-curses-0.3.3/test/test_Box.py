#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from GLXCurses import GLXC
import GLXCurses


# Unittest
class TestBox(unittest.TestCase):

    # Test
    def test_glxc_type(self):
        """Test StatusBar type"""
        box = GLXCurses.Box()
        self.assertTrue(GLXCurses.glxc_type(box))

    def test_baseline_position(self):
        box = GLXCurses.Box()
        self.assertEqual(GLXC.BASELINE_POSITION_CENTER, box.baseline_position)
        box.baseline_position = GLXC.BASELINE_POSITION_TOP
        self.assertEqual(GLXC.BASELINE_POSITION_TOP, box.baseline_position)
        box.baseline_position = None
        self.assertEqual(GLXC.BASELINE_POSITION_CENTER, box.baseline_position)

        self.assertRaises(TypeError, setattr, box, 'baseline_position', 42)
        self.assertRaises(ValueError, setattr, box, 'baseline_position', 'Hello.42')

    def test_new(self):
        """Test Box.new()"""
        # check default value
        box1 = GLXCurses.Box().new()
        self.assertEqual(GLXC.ORIENTATION_HORIZONTAL, box1.orientation)
        self.assertEqual(0, box1.spacing)

        # check with value
        box1 = GLXCurses.Box().new(orientation=GLXC.ORIENTATION_VERTICAL, spacing=4)
        self.assertEqual(GLXC.ORIENTATION_VERTICAL, box1.orientation)
        self.assertEqual(4, box1.spacing)

        # check error Type
        self.assertRaises(TypeError, box1.new, orientation='Galaxie', spacing=4)
        self.assertRaises(TypeError, box1.new, orientation=GLXC.ORIENTATION_HORIZONTAL, spacing='Galaxie')

    def test_pack_start(self):
        """Test Box type"""
        box1 = GLXCurses.Box()
        box2 = GLXCurses.Box()
        box3 = GLXCurses.Box()

        # If child is worng
        self.assertRaises(TypeError, box1.pack_start, child=None, expand=True, fill=True, padding=0)
        self.assertRaises(TypeError, box1.pack_start, child=box2, expand='Galaxie', fill=True, padding=0)
        self.assertRaises(TypeError, box1.pack_start, child=box2, expand=True, fill='Galaxie', padding=0)
        self.assertRaises(TypeError, box1.pack_start, child=box2, expand=True, fill=True, padding='Galaxie')

        # Can i get children list ?
        self.assertEqual(type(list()), type(box1.children))

        # pack the child
        box1.pack_start(child=box2, expand=False, fill=False, padding=4)
        box1.pack_start(child=box3, expand=False, fill=False, padding=2)

        self.assertTrue(isinstance(box1.children[0], GLXCurses.ChildElement))

        self.assertEqual(box3, box1.children[0].widget)
        self.assertEqual(False, box1.children[0].properties.expand)
        self.assertEqual(False, box1.children[0].properties.fill)
        self.assertEqual(2, box1.children[0].properties.padding)
        self.assertEqual(GLXC.PACK_START, box1.children[-1].properties.pack_type)

    def test_pack_end(self):
        """Test Box.pack_end()"""
        box1 = GLXCurses.Box()
        box2 = GLXCurses.Box()
        box3 = GLXCurses.Box()

        # If child is worng
        self.assertRaises(TypeError, box1.pack_end, child=None, expand=True, fill=True, padding=0)
        self.assertRaises(TypeError, box1.pack_end, child=box2, expand='Galaxie', fill=True, padding=0)
        self.assertRaises(TypeError, box1.pack_end, child=box2, expand=True, fill='Galaxie', padding=0)
        self.assertRaises(TypeError, box1.pack_end, child=box2, expand=True, fill=True, padding='Galaxie')

        # Can i get children list ?
        self.assertEqual(type(list()), type(box1.children))

        # pack the child
        box1.pack_end(child=box2, expand=True, fill=True, padding=4)
        box1.pack_end(child=box3, expand=False, fill=False, padding=2)

        self.assertTrue(isinstance(box1.children[-1], GLXCurses.ChildElement))

        self.assertEqual(box3, box1.children[-1].widget)
        self.assertEqual(False, box1.children[-1].properties.expand)
        self.assertEqual(False, box1.children[-1].properties.fill)
        self.assertEqual(2, box1.children[-1].properties.padding)
        self.assertEqual(GLXC.PACK_END, box1.children[-1].properties.pack_type)

    def test_set_get_homogeneous(self):
        """Test Box.set_homogeneous() and Box.get_homogeneous()"""
        box1 = GLXCurses.Box().new()

        box1.homogeneous = False
        self.assertFalse(box1.homogeneous)
        box1.homogeneous = True
        self.assertTrue(box1.homogeneous)

        self.assertRaises(TypeError, setattr, box1, 'homogeneous', 'Galaxie')

    def test_spacing(self):
        """Test Box.set_spacing() and Box.get_spacing()"""
        box1 = GLXCurses.Box().new()
        self.assertEqual(0, box1.spacing)
        box1.spacing = 2
        self.assertEqual(2, box1.spacing)
        box1.spacing = None
        self.assertEqual(0, box1.spacing)

        self.assertRaises(TypeError, setattr, box1, 'spacing', 'Galaxie')

    def test_reorder_child(self):
        """Test Box.reorder_child()"""
        # create box
        box1 = GLXCurses.Box().new()

        # create child box
        box2 = GLXCurses.Box().new()
        box3 = GLXCurses.Box().new()
        box4 = GLXCurses.Box().new()
        box5 = GLXCurses.Box().new()

        # add 3 children
        box1.pack_end(box2)
        box1.pack_end(box3)
        box1.pack_end(box4)

        # check if we have our 3 children in the good order
        self.assertEqual(3, len(box1.children))
        self.assertEqual(box2, box1.children[0].widget)
        self.assertEqual(box3, box1.children[1].widget)
        self.assertEqual(box4, box1.children[2].widget)

        # try to reorder
        box1.reorder_child(child=box2, position=2)
        box1.reorder_child(child=box5, position=2)

        # check if we have our 3 children in the good order
        self.assertEqual(3, len(box1.children))
        self.assertEqual(box3, box1.children[0].widget)
        self.assertEqual(box4, box1.children[1].widget)
        self.assertEqual(box2, box1.children[2].widget)

        # try to reorder
        box1.reorder_child(child=box2, position=-1)
        self.assertEqual(3, len(box1.children))
        # self.assertEqual(box4, box1.children[0].widget)
        # self.assertEqual(box2, box1.children[1].widget)
        # self.assertEqual(box3, box1.children[2].widget)

        # check raises
        self.assertRaises(TypeError, box1.reorder_child, child=int(42), position=2)
        self.assertRaises(TypeError, box1.reorder_child, child=box2, position="Galaxie")

    def test_query_child_packing(self):
        """Test Box.query_child_packing()"""
        # create box
        box1 = GLXCurses.Box().new()

        # create child box
        box2 = GLXCurses.Box().new()
        box3 = GLXCurses.Box().new()
        box4 = GLXCurses.Box().new()

        # add children
        box1.pack_end(box2)
        box1.pack_start(box3)

        # query
        child1_packing = box1.query_child_packing(child=box2)
        child2_packing = box1.query_child_packing(child=box3)

        # return None the widget is not a child
        child3_packing = box1.query_child_packing(child=box4)
        self.assertEqual(type(None), type(child3_packing))

        # check if we have a dict as return
        self.assertEqual('END', child1_packing)
        self.assertEqual('START', child2_packing)

        # check pack
        self.assertEqual(GLXC.PACK_END, child1_packing)
        self.assertEqual(GLXC.PACK_START, child2_packing)

        self.assertRaises(TypeError, box1.query_child_packing, child=int(42))

    def test_set_child_packing(self):
        """Test Box.set_child_packing()"""
        # create box
        box1 = GLXCurses.Box().new()

        # create child box
        box2 = GLXCurses.Box().new()

        # add children
        box1.pack_end(child=box2, expand=False, fill=False, padding=4)

        # query
        child1_packing = box1.query_child_packing(child=box2)

        # check if we have a dict as return
        self.assertEqual(str, type(child1_packing))

        # check pack
        self.assertEqual('END', child1_packing)

        # set child_packing
        box1.set_child_packing(child=box2, expand=True, fill=True, padding=2, pack_type=GLXC.PACK_START)

        # query
        child1_packing = box1.query_child_packing(child=box2)

        # check if we have a dict as return
        self.assertEqual(str, type(child1_packing))

        # check pack
        self.assertEqual('START', child1_packing)

        # check raise
        # bad child
        self.assertRaises(
            TypeError,
            box1.set_child_packing,
            child=None,
            expand=True,
            fill=True,
            padding=2,
            pack_type=GLXC.PACK_START
        )
        # bad expand
        self.assertRaises(
            TypeError,
            box1.set_child_packing,
            child=box2,
            expand="Galaxie",
            fill=True,
            padding=2,
            pack_type=GLXC.PACK_START
        )
        # bad fill
        self.assertRaises(
            TypeError,
            box1.set_child_packing,
            child=box2,
            expand=True,
            fill="Galaxie",
            padding=2,
            pack_type=GLXC.PACK_START
        )
        # bad padding
        self.assertRaises(
            TypeError,
            box1.set_child_packing,
            child=box2,
            expand=True,
            fill=True,
            padding="Galaxie",
            pack_type=GLXC.PACK_START
        )
        # bad pack_type
        self.assertRaises(
            TypeError,
            box1.set_child_packing,
            child=box2,
            expand=True,
            fill=True,
            padding=2,
            pack_type="Galaxie"
        )

    def test_set_get_center_widget(self):
        """Test Box.set_center_widget() and Box.get_center_widget()"""
        box1 = GLXCurses.Box().new()
        box2 = GLXCurses.Box().new()

        box1.set_center_widget(box2)
        self.assertEqual(box1.get_center_widget(), box2)

        box1.set_center_widget(None)
        self.assertEqual(box1.get_center_widget(), None)

        box1.set_center_widget(box2)
        self.assertEqual(box1.get_center_widget(), box2)

        box1.set_center_widget()
        self.assertEqual(box1.get_center_widget(), None)

        self.assertRaises(TypeError, box1.set_center_widget, 42)

    def test__emit_reorder_child(self):
        """Test Box._emit_reorder_child()"""
        box1 = GLXCurses.Box().new()

        child_properties = {
            'expand': True,
            'fill': True,
            'padding': 0,
            'pack_type': GLXC.PACK_END
        }

        child_info = {
            'widget': box1,
            'properties': child_properties
        }

        box1._emit_reorder_child(data=child_info)

        # test raise
        self.assertRaises(TypeError, box1._emit_reorder_child, data=None)
        child_info = {}
        self.assertRaises(KeyError, box1._emit_reorder_child, data=child_info)
        child_info = {'widget': box1}
        self.assertRaises(KeyError, box1._emit_reorder_child, data=child_info)

    def test__emit_pack_end(self):
        """Test Box._emit_pack_end()"""
        box1 = GLXCurses.Box().new()

        child_properties = {
            'expand': True,
            'fill': True,
            'padding': 0,
            'pack_type': GLXC.PACK_END
        }

        child_info = {
            'widget': box1,
            'properties': child_properties
        }

        box1._emit_pack_end(data=child_info)

        # test raise
        self.assertRaises(TypeError, box1._emit_pack_end, data=None)
        child_info = {}
        self.assertRaises(KeyError, box1._emit_pack_end, data=child_info)
        child_info = {'widget': box1}
        self.assertRaises(KeyError, box1._emit_pack_end, data=child_info)

    def test__emit_pack_start(self):
        """Test Box._emit_pack_start()"""
        box1 = GLXCurses.Box().new()

        child_properties = {
            'expand': True,
            'fill': True,
            'padding': 0,
            'pack_type': GLXC.PACK_END
        }

        child_info = {
            'widget': box1,
            'properties': child_properties
        }

        box1._emit_pack_start(data=child_info)

        # test raise
        self.assertRaises(TypeError, box1._emit_pack_start, data=None)
        child_info = {}
        self.assertRaises(KeyError, box1._emit_pack_start, data=child_info)
        child_info = {'widget': box1}
        self.assertRaises(KeyError, box1._emit_pack_start, data=child_info)
