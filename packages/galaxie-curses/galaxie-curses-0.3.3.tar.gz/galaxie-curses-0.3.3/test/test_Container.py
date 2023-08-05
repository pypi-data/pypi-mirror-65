#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import unittest
from GLXCurses import Container
from GLXCurses import Adjustment
from GLXCurses import Box
from GLXCurses import Object
from GLXCurses import GLXC
from GLXCurses.Utils import glxc_type
from GLXCurses.Utils import is_valid_id

import GLXCurses

# Unittest
class TestContainer(unittest.TestCase):
    # Test
    def test_Container_type(self):
        """Test Container type"""
        self.assertTrue(glxc_type(Container()))

    def test_Container_add(self):
        """Test Container.add()"""
        container = Container()
        # Test add method for None parameter
        # Create a child
        child1 = Container()
        child2 = Container()
        # Add the child
        container.add(child1)
        # We must have the child inside the child list
        self.assertEqual(container.child.widget, child1)
        # Add the child
        container.add(child2)
        # We must have the child inside the child list
        self.assertEqual(container.child.widget, child2)
        # Test type error
        self.assertRaises(TypeError, container.add, int())
        self.assertRaises(TypeError, container.add, Object())
        self.assertRaises(TypeError, container.add)

    def test_Container_remove(self):
        """Test Container.remove()"""
        # create our tested container
        container = Container()

        # Create a child
        child1 = Container()
        child2 = Box()

        # Add the child and test
        container.add(child1)
        self.assertEqual(container.child.widget, child1)

        # remove and test
        container.remove(child1)
        self.assertEqual(container.child, None)

        # Add the child and test
        container.add(child2)
        self.assertEqual(container.child.widget, child2)

        child2.pack_start(child1)
        self.assertEqual(child2.children[0].widget, child1)

        # remove and test
        child2.remove(child1)
        self.assertEqual(len(child2.children), 0)

        # we still have the child 2
        self.assertEqual(container.child.widget, child2)

        # we remove child 2
        container.remove(child2)
        self.assertEqual(container.child, None)

        # Test type error
        self.assertRaises(TypeError, container.remove, int())
        self.assertRaises(TypeError, container.remove)
        self.assertRaises(TypeError, container.remove, child2, int())
        self.assertRaises(TypeError, container.remove, Object())

    def test_Container_add_with_properties(self):
        """Test Container.add_with_property()"""
        container = Container()
        # Create a child
        child1 = Container()
        # prepare a property
        child_properties = GLXCurses.ChildProperty()
        child_properties.padding = 42
        # Add the child
        container.add_with_properties(child1, properties=child_properties)
        # We must have the child inside the child list
        self.assertEqual(container.child.widget, child1)
        self.assertEqual(container.child.properties.padding, 42)
        # Test type error
        self.assertRaises(TypeError, container.add_with_properties, int())
        self.assertRaises(TypeError, container.add_with_properties, child1, int())
        self.assertRaises(TypeError, container.add_with_properties, Object())

    def test_Container_get_resize_mode(self):
        """Test container.get_resize_mode()"""
        container = Container()
        container.resize_mode = 42
        self.assertEqual(container.get_resize_mode(), 42)

    def test_Container_set_resize_mode(self):
        """Test container.set_resize_mode()"""
        container = Container()

        container.set_resize_mode(GLXC.RESIZE_PARENT)
        self.assertEqual(container.resize_mode, GLXC.RESIZE_PARENT)

        container.set_resize_mode(GLXC.RESIZE_QUEUE)
        self.assertEqual(container.resize_mode, GLXC.RESIZE_QUEUE)

        container.set_resize_mode(GLXC.RESIZE_IMMEDIATE)
        self.assertEqual(container.resize_mode, GLXC.RESIZE_IMMEDIATE)

        # check error
        self.assertRaises(TypeError, container.set_resize_mode, 'Hello')

    def test_Container_check_resize(self):
        """Test Container.check_resize()"""
        container = Container()
        container.check_resize()

    def test_Container_foreachs(self):
        """Test Container.foreachs()"""

        # CHILD_CONTAINER
        container1 = Container()
        container2 = Container()
        container3 = Container()

        container4 = Container()
        container5 = Container()

        # CHILDREN_CONTAINER
        container_box = Box()

        def say_hello1(widget):
            widget.name = 'Hello say_hello1'
            # print("say_hello1 have been touch")

        def say_hello2(widget):
            widget.name = 'Hello say_hello2'
            # print("say_hello2 have been touch")

        def say_hello3(widget):
            widget.name = 'Hello say_hello3'
            # print("say_hello3 have been touch")

        # set children
        container_box.pack_start(container3)
        container_box.pack_start(container2)
        container_box.pack_start(container1)

        # set child
        container4.add(container5)

        # check if container_box1 have a list of children via children properties
        self.assertEquals(container_box.children[0].widget, container1)
        self.assertEquals(container_box.children[1].widget, container2)
        self.assertEquals(container_box.children[2].widget, container3)
        # check if child property stay empty
        self.assertEquals(container_box.child, None)

        # check if container4 have a child
        self.assertEquals(container4.child.widget, container5)
        # check if children property stay empty
        self.assertEquals(len(container4.children), 0)

        container_box.children[2].widget.connect('say_hello1', say_hello1)
        container_box.children[2].widget.connect('say_hello2', say_hello2)
        container_box.children[2].widget.connect('say_hello3', say_hello3)
        container_box.children[1].widget.connect('say_hello1', say_hello1)
        container_box.children[1].widget.connect('say_hello2', say_hello2)
        container_box.children[1].widget.connect('say_hello3', say_hello3)
        container_box.children[0].widget.connect('say_hello1', say_hello1)
        container_box.children[0].widget.connect('say_hello2', say_hello2)
        container_box.children[0].widget.connect('say_hello3', say_hello3)

        # check if we have store handler and callbacks
        self.assertEquals(container_box.children[2].widget.events_list['say_hello1'][0], say_hello1)
        self.assertEquals(container_box.children[2].widget.events_list['say_hello2'][0], say_hello2)
        self.assertEquals(container_box.children[2].widget.events_list['say_hello3'][0], say_hello3)

        self.assertEquals(container_box.children[1].widget.events_list['say_hello1'][0], say_hello1)
        self.assertEquals(container_box.children[1].widget.events_list['say_hello2'][0], say_hello2)
        self.assertEquals(container_box.children[1].widget.events_list['say_hello3'][0], say_hello3)

        self.assertEquals(container_box.children[0].widget.events_list['say_hello1'][0], say_hello1)
        self.assertEquals(container_box.children[0].widget.events_list['say_hello2'][0], say_hello2)
        self.assertEquals(container_box.children[0].widget.events_list['say_hello3'][0], say_hello3)

        # Call foreachs
        container_box.foreachs(say_hello1, container1)
        container_box.foreachs(say_hello2, container2)
        container_box.foreachs(say_hello3, container3)

        # Check if it work for children
        self.assertEquals(container1.name, 'Hello say_hello1')
        self.assertEquals(container2.name, 'Hello say_hello2')
        self.assertEquals(container3.name, 'Hello say_hello3')

        # check for child
        container4.child.widget.connect('say_hello1', say_hello1)
        container4.child.widget.connect('say_hello2', say_hello2)
        container4.child.widget.connect('say_hello3', say_hello3)

        container4.foreachs(say_hello1, container5)

        # Check if it work for child
        container4.foreachs(say_hello1, container5)
        self.assertEquals(container5.name, 'Hello say_hello1')
        container4.foreachs(say_hello2, container5)
        self.assertEquals(container5.name, 'Hello say_hello2')
        container4.foreachs(say_hello3, container5)
        self.assertEquals(container5.name, 'Hello say_hello3')

    def test_Container_get_children(self):
        """Test Container.children"""
        # prepare container
        container = Container()
        # it's a list
        self.assertEqual(type(container.children), type(list()))
        # prepare a children
        box1 = Box()
        box2 = Box()

        box1.pack_start(box2)
        self.assertEqual(box1.children[0].widget, box2)

    def test_Container_get_path_for_child(self):
        """Test Container.get_path_for_child """
        container = Container()

    def test_Container_set_get_focus_vadjustment(self):
        """Test Container.set_focus_vadjustment() and Container.get_focus_vadjustment()"""
        # prepare container
        container = Container()
        # prepare children
        adjustment = Adjustment()
        box = Box()
        # set
        container.set_focus_vadjustment(adjustment=adjustment)
        # get
        self.assertEqual(container.get_focus_vadjustment().widget, adjustment)
        self.assertTrue(is_valid_id(container.get_focus_vadjustment().id))
        self.assertEqual(type(container.get_focus_vadjustment().properties), GLXCurses.ChildProperty)
        # set None
        container.set_focus_vadjustment(adjustment=None)
        # get None
        self.assertEqual(container.get_focus_vadjustment(), None)
        # test raise
        self.assertRaises(TypeError, container.set_focus_vadjustment, int())
        self.assertRaises(TypeError, container.set_focus_vadjustment, box)

    def test_Container_set_get_focus_hadjustment(self):
        """Test Container.set_focus_hadjustment() and Container.get_focus_hadjustment()"""
        # prepare container
        container = Container()
        # prepare children
        adjustment = Adjustment()
        box = Box()
        # set
        container.set_focus_hadjustment(adjustment=adjustment)
        # get
        self.assertEqual(container.get_focus_hadjustment().widget, adjustment)
        self.assertTrue(is_valid_id(container.get_focus_hadjustment().id))
        self.assertTrue(isinstance(container.get_focus_hadjustment().properties, GLXCurses.ChildProperty))
        # set None
        container.set_focus_hadjustment(adjustment=None)
        # get None
        self.assertEqual(container.get_focus_hadjustment(), None)
        # test raise
        self.assertRaises(TypeError, container.set_focus_hadjustment, int())
        self.assertRaises(TypeError, container.set_focus_hadjustment, box)

    def test_Container_child_type(self):
        """Test Container.child-type"""
        # create our tested container
        container = Container()

        # child
        box1 = Box()
        box2 = Box()

        cont1 = Container()
        cont2 = Container()

        # The container haven't it self as child then waiting -1
        self.assertEqual(container.child_type(container), -1)

        container.add(box1)
        # when it work normally
        self.assertEqual(container.child_type(box1), 'GLXCurses.Box')

        box1.pack_start(cont1)
        # when it work normally
        self.assertEqual(box1.child_type(cont1), 'GLXCurses.Container')

        cont1.add(box2)
        # cont1 have no more child space
        self.assertEqual(box1.child_type(cont1), None)

        # yes it work
        box2.pack_start(cont2)
        self.assertEqual(box2.child_type(cont2), 'GLXCurses.Container')
        self.assertEqual(box2.child_type(cont1), -1)
        # change for a single child
        ###########################
        # create our tested container
        container = Container()

        # child
        box1 = Box()
        box2 = Box()

        cont1 = Container()
        cont2 = Container()

        # The container haven't it self as child then waiting -1
        self.assertEqual(container.child_type(container), -1)

        container.add(cont1)
        # when it work normally
        self.assertEqual(container.child_type(cont1), 'GLXCurses.Container')
        self.assertEqual(container.child_type(cont2), -1)

        cont1.add(box1)
        # Should have no space
        self.assertEqual(container.child_type(cont1), None)

        box1.pack_start(box2)
        self.assertEqual(cont1.child_type(box1), 'GLXCurses.Box')

    def test_Container_child_get(self):
        """Test Container.child_get()"""
        # Use Container as main container (single child)
        # create our tested container
        container = Container()

        # Create a child
        child1 = Container()
        child2 = Container()

        # Add the child and test
        container.add(child1)
        self.assertEqual(container.child.widget, child1)

        # check if we receive a dict type

        self.assertTrue(isinstance(container.child_get(child1), GLXCurses.ChildProperty))

        self.assertEqual(container.child_get(child1), container.child.properties)

        # return None if child is not found
        self.assertEqual(None, container.child_get(child2))

        # Use Box as main container (multiple child)
        # create our tested container
        container_to_test = Box()

        # Create a child
        child_to_test1 = Container()
        child_to_test2 = Container()
        child_to_test3 = Container()

        # Add the child and test
        container_to_test.pack_start(child_to_test2)
        container_to_test.pack_start(child_to_test1)
        self.assertEqual(container_to_test.children[0].widget, child_to_test1)
        self.assertEqual(
            container_to_test.children[0].properties,
            container_to_test.child_get(child_to_test1)
        )
        # return None if child is not found
        self.assertEqual(None, container_to_test.child_get(child_to_test3))

        # check if we receive a dict type
        self.assertTrue(isinstance(container_to_test.child_get(child_to_test1), GLXCurses.ChildProperty))

        # Test type error
        self.assertRaises(TypeError, container.child_get, int())
        self.assertRaises(TypeError, container.child_get)

    def test_Container_child_set(self):
        """Test Container.child_set()"""
        # Use Container as main container (single child)
        # create our tested container
        container = Container()

        # Create a child
        child1 = Container()
        child2 = Container()

        # Add the child and test
        container.add(child1)
        added_properties = GLXCurses.ChildProperty()
        added_properties.padding = 42

        # use child set
        old_properties = container.child.properties.padding
        container.child_set(child1, added_properties)
        new_properties = container.child.properties.padding

        # check result
        self.assertGreater(new_properties, old_properties)
        self.assertEqual(
            42,
            container.child.properties.padding
        )


        # raise error
        self.assertRaises(TypeError, container.child_set, int())
        self.assertRaises(TypeError, container.child_set)
        self.assertRaises(TypeError, container.child_set, child2, int())
        self.assertRaises(TypeError, container.child_set, child2)

    def test_Container_child_set_property(self):
        """Test Container.child_set_property()"""
        # Use Container as main container (single child)
        # create our tested container
        container = Container()

        # Create a child
        child1 = Container()
        child2 = Container()

        # Add the child and test
        container.add(child1)

        # use child set
        old_properties = container.child.properties
        container.child_set_property(child1, property_name='padding', value=42)
        new_properties = container.child.properties

        # check result
        self.assertEqual(42, container.child.properties.padding)

        # Use Box as main container (multiple child)
        # create our tested container
        container_to_test = Box()

        # Create a child
        child_to_test1 = Container()

        # Add the child and test
        container_to_test.pack_start(child_to_test1)

        old_properties = container_to_test.children[0].properties.padding
        container_to_test.child_set_property(child_to_test1, property_name='padding', value=42)
        new_properties = container_to_test.children[0].properties.padding

        # check result
        self.assertNotEqual(old_properties, new_properties)

        # check raise
        self.assertRaises(TypeError, container.child_set_property, int())
        self.assertRaises(TypeError, container.child_set_property)
        self.assertRaises(TypeError, container.child_set_property, child2, int())
        self.assertRaises(TypeError, container.child_set_property, child2)
        self.assertRaises(TypeError, container.child_set_property, child2, 'Galaxie', None)
        self.assertRaises(TypeError, container.child_set_property, child2, 'Galaxie')

    def test_Container_child_get_property(self):
        """Test Container.child_get_property()"""
        # Use Container as main container (single child)
        # create our tested container
        container = Container()

        # Create a child
        child1 = Container()

        # Add the child and test
        container.add(child1)

        # use child set
        container.child_set_property(child1, property_name='Galaxie', value=42.00)
        old_properties = container.child_get_property(child1, 'Galaxie')
        container.child_set_property(child1, property_name='Galaxie', value=42.42)
        new_properties = container.child_get_property(child1, 'Galaxie')

        # check result
        self.assertGreater(new_properties, old_properties)
        self.assertEqual(
            type(float()),
            type(container.child_get_property(child1, 'Galaxie'))
        )

        # Use Box as main container (multiple child)
        # create our tested container
        container_to_test = Box()

        # Create a child
        child_to_test1 = Container()

        # Add the child and test
        container_to_test.pack_start(child_to_test1)

        container_to_test.child_set_property(child_to_test1, property_name='Galaxie', value=42.00)
        old_properties = container_to_test.child_get_property(child_to_test1, 'Galaxie')
        container_to_test.child_set_property(child_to_test1, property_name='Galaxie', value=42.42)
        new_properties = container_to_test.child_get_property(child_to_test1, 'Galaxie')

        # check result
        self.assertGreater(new_properties, old_properties)
        self.assertEqual(
            type(float()),
            type(container_to_test.child_get_property(child_to_test1, 'Galaxie'))
        )

        # check raise
        self.assertRaises(TypeError, container.child_get_property, int())
        self.assertRaises(TypeError, container.child_get_property)

    def test_Container_set_border_width(self):
        """Test Container.set_border_width()"""
        container = Container()
        # check default value
        self.assertEqual(
            container.border_width,
            0
        )
        # test normal
        container.set_border_width(border_width=42)
        self.assertEqual(
            container.border_width,
            42
        )
        # test negative
        container.set_border_width(border_width=-42)
        self.assertEqual(
            container.border_width,
            0
        )
        # test over the limit
        container.set_border_width(border_width=65542)
        self.assertEqual(
            container.border_width,
            65535
        )
        # check raise
        self.assertRaises(TypeError, container.set_border_width, str('Hello'))

    def test_Container_get_border_width(self):
        """Test Container.get_border_width()"""
        container = Container()
        # check default value
        self.assertEqual(
            container.get_border_width(),
            0
        )
        # test
        container.border_width = 65542  # yes that is over the limit :) verify that is not clamp
        self.assertEqual(
            container.get_border_width(),
            65542
        )


if __name__ == '__main__':
    unittest.main()
