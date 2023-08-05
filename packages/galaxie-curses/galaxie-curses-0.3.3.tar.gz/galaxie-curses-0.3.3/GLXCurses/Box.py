#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved


import GLXCurses


# https://developer.gnome.org/gtk3/stable/GtkBox.html
class Box(GLXCurses.Container):
    """
    :Description:

    The :class:`Box <GLXCurses.Box.Box>` widget organizes child widgets into a rectangular area.
    """

    def __init__(self):
        """
        **Attributes Details**

        .. py:attribute:: base_position

           The position of the baseline aligned widgets if extra space is available.

              :Type: :py:const:`BaselinePosition`
              :Flags: Read / Write
              :Default value: :py:const:`BASELINE_POSITION_CENTER`

        .. py:attribute:: base_position

           Whether the children should all be the same size.

              :Type: :py:obj:`bool`
              :Flags: Read / Write
              :Default value: :py:obj:`False`

        .. py:attribute:: spacing

           The amount of space between children.

              :Type: :py:obj:`int`
              :Flags: Read / Write
              :Allowed values: >= 0
              :Default value: 0

        :Child Attributes Details:

        .. py:attribute:: expand

           Whether the child should receive extra space when the parent grows.

           Note that the default value for this property is :py:obj:`False` for :class:`Box <GLXCurses.Box.Box>`,
           but :class:`HBox <GLXCurses.HBox.HBox>`, :class:`VBox <GLXCurses.VBox.VBox>` and other subclasses use the
           old default of :py:obj:`True`.

           Note that the **halign**, **valign**, **hexpand** and **vexpand** attribute are the preferred way to
           influence child size allocation in containers

           In contrast to **hexpand**, the expand child attribute does not cause the box to expand itself.

              :Type: :py:obj:`bool`
              :Flags: Read / Write
              :Default value: :py:obj:`False`

        .. py:attribute:: fill

           Whether the child should receive extra space when the parent grows.

           Note that the **halign**, **valign**, **hexpand** and **vexpand** properties are the preferred way to
           influence child size allocation in containers.

              :Type: :py:obj:`bool`
              :Flags: Read / Write
              :Default value: :py:obj:`True`

        .. py:attribute:: pack_type

           A PackType indicating whether the child is packed with reference to the start or end of the parent.

              :Type: :py:const:`PackType`
              :Flags: Read / Write
              :Default value: :py:const:`PACK_START`

        .. py:attribute:: padding

           Extra space to put between the child and its neighbors, in chars.

              :Type: :py:obj:`int`
              :Flags: Read / Write
              :Allowed values: <= G_MAXINT
              :Default value: 0

        .. py:attribute:: position

           The index of the child in the parent.

              :Type: :py:obj:`int`
              :Flags: Read / Write
              :Allowed values: >= -1
              :Default value: 0
        """
        # Load heritage
        GLXCurses.Container.__init__(self)

        # It's a GLXCurse Type
        self.glxc_type = 'GLXCurses.Box'

        # Widgets can be named, which allows you to refer to them from a GLXCStyle
        self.name = '{0}{1}'.format(self.__class__.__name__, self.id)

        # Make a Widget Style heritage attribute as local attribute
        # if self.style.attribute_states:
        #     if self.attribute_states != self.style.attribute_states:
        #         self.attribute_states = self.style.attribute_states

        self.__baseline_position = None
        self.__homogeneous = None
        self.__spacing = None

        # Attributes
        self.baseline_position = GLXCurses.GLXC.BASELINE_POSITION_CENTER
        self.homogeneous = False
        self.spacing = 0

        self.orientation = GLXCurses.GLXC.ORIENTATION_HORIZONTAL
        self.center_widget = None

    @property
    def baseline_position(self):
        """
        Gets the ``baseline_position`` value.

        :return: a BaselinePosition
        :rtype: BaselinePosition
        """
        return self.__baseline_position

    @baseline_position.setter
    def baseline_position(self, position=None):
        """
        Sets the baseline position of a box.

        This affects only horizontal boxes with at least one baseline aligned child.
        If there is more vertical space available than requested, and the baseline is not allocated by
        the parent then position is used to allocate the baseline wrt the extra space available.

        :param position: a GLXC.BaselinePosition
        :type position: GLXC.BaselinePosition or None
        :raise Type: if ``position`` is not a str type or None
        :raise ValueError: if ``position`` is not GLXC.BaselinePosition list
        """
        if position is None:
            position = GLXCurses.GLXC.BASELINE_POSITION_CENTER
        if type(position) != str:
            raise TypeError('"position" must be a str type or None')
        if position not in GLXCurses.GLXC.BaselinePosition:
            raise ValueError('"position" must be in GLXC.BaselinePosition list')

        if self.baseline_position != position:
            self.__baseline_position = position

    @property
    def homogeneous(self):
        """
        Returns whether the :class:`Box <GLXCurses.Box.Box>` is homogeneous (all children's have the same size).

        .. seealso:: :func:`Box.set_homogeneous() <GLXCurses.Box.Box.set_homogeneous>`

        :return: ``True`` if the :class:`Box <GLXCurses.Box.Box>` is homogeneous.
        :rtype: bool
        """
        return self.__homogeneous

    @homogeneous.setter
    def homogeneous(self, homogeneous=None):
        """
        Sets the :py:attr:`homogeneous` attribute of :class:`Box <GLXCurses.Box.Box>`, controlling whether or not all
        children of :class:`Box <GLXCurses.Box.Box>` are given equal space in the box.

        Default Value: False
        Note: None restore default value.

        :param homogeneous: ``True`` to create equal allotments, ``False`` for variable allotments
        :type homogeneous: bool or None
        :raise TypeError: if ``homogeneous`` is not bool type
        """
        if homogeneous is None:
            homogeneous = False
        if type(homogeneous) != bool:
            raise TypeError('"homogeneous" argument must be a bool type')
        if self.homogeneous != homogeneous:
            self.__homogeneous = homogeneous

    @property
    def spacing(self):
        return self.__spacing

    @spacing.setter
    def spacing(self, spacing=None):
        if spacing is None:
            spacing = 0
        if type(spacing) != int:
            raise TypeError('"spacing" must be a int type or None')
        if self.spacing != GLXCurses.clamp_to_zero(spacing):
            self.__spacing = GLXCurses.clamp_to_zero(spacing)

    def new(self, orientation=GLXCurses.GLXC.ORIENTATION_HORIZONTAL, spacing=None):
        """
        Creates a new :class:`Box <GLXCurses.Box.Box>`.
        
        :param orientation: the box’s orientation. Default: ORIENTATION_HORIZONTAL
        :type orientation: Orientation
        :param spacing: the number of characters to place by default between children. Default: 0
        :type spacing: int or None
        :return: a new :class:`Box <GLXCurses.Box.Box>`.
        :raise TypeError: if ``orientation`` is not glxc.ORIENTATION_HORIZONTAL or glxc.ORIENTATION_VERTICAL
        :raise TypeError: if ``spacing`` is not int type or None
        """
        if orientation not in [GLXCurses.GLXC.ORIENTATION_HORIZONTAL, GLXCurses.GLXC.ORIENTATION_VERTICAL]:
            raise TypeError('"orientation" must be GLX.ORIENTATION_HORIZONTAL or glxc.ORIENTATION_VERTICAL')
        if spacing is not None:
            if type(spacing) != int:
                raise TypeError('"spacing" must be int type or None')
        if spacing is None:
            spacing = 0

        self.__init__()
        self.spacing = GLXCurses.clamp_to_zero(spacing)
        self.orientation = orientation
        return self

    def pack_start(self, child=None, expand=True, fill=True, padding=None):
        """
        Adds child to :class:`Box <GLXCurses.Box.Box>` , packed with reference to the start of
        :class:`Box <GLXCurses.Box.Box>`.

        :param child: the widget to be added to :class:`Box <GLXCurses.Box.Box>`
        :type child: a GLXCures Object
        :param expand: ``True`` if the new child is to be given extra space allocated to \
        `Box <GLXCurses.Box.Box>`. The extra space will be divided evenly between all children that use this option
        :type expand: bool
        :param fill: ``True`` if space given to :py:obj:`child` by the :py:attr:`expend` option is actually \
        allocated to :py:obj:`child`, rather than just padding it. This parameter has no effect if :py:attr:`expend` \
        is set to :py:obj:`False`. A child is always allocated the full height of a horizontal \
        :class:`Box <GLXCurses.Box.Box>` and the full width of a vertical :class:`Box <GLXCurses.Box.Box>`. \
        This option affects the other dimension.
        :type fill: bool
        :param padding: extra space in characters to put between this child and its neighbors, over and above \
        the global amount specified by :py:attr:`spacing` attribute. If child is a widget at one of the reference \
        ends of box , then padding pixels are also put between child and the reference edge of box
        :type padding: int or None
        :raise TypeError: if ``child`` is not a GLXCurses type as tested by \
        :func:`glxc_type() <GLXCurses.Utils.glxc_type>`
        :raise TypeError: if ``expand`` is not bool type
        :raise TypeError: if ``fill`` is not bool type
        :raise TypeError: if ``padding`` is not int or None
        """
        # Try to exit as soon of possible
        if not GLXCurses.glxc_type(child):
            raise TypeError('"child" argument must be a GLXCurses object type')
        if type(expand) != bool:
            raise TypeError('"expand" argument must be a bool')
        if type(fill) != bool:
            raise TypeError('"fill" argument must be a bool')
        if padding is not None:
            if type(padding) != int:
                raise TypeError('"spacing" must be int type or None')

        child_to_add = GLXCurses.ChildElement()
        child_to_add.widget = child
        child_to_add.type = child.glxc_type
        child_to_add.id = child.id
        child_to_add.name = '{0}{1}'.format(child.name, child.id)
        child_to_add.properties.expand = expand
        child_to_add.properties.fill = fill
        child_to_add.properties.padding = GLXCurses.clamp_to_zero(padding)
        child_to_add.properties.pack_type = GLXCurses.GLXC.PACK_START
        child_to_add.position = 0

        self.children.insert(0, child_to_add)

        self._upgrade_child_position()

        self._emit_pack_start(data={'widget': child,
                                    'type': child.glxc_type,
                                    'id': child.id,
                                    'properties': {
                                        'expand': expand,
                                        'fill': fill,
                                        'padding': GLXCurses.clamp_to_zero(padding),
                                        'pack_type': GLXCurses.GLXC.PACK_START,
                                        'position': 0}
                                    })

    def pack_end(self, child=None, expand=True, fill=True, padding=None):
        """
        Adds child to :class:`Box <GLXCurses.Box.Box>` , packed with reference to the end of
        :class:`Box <GLXCurses.Box.Box>`.

        :param child: the widget to be added to :class:`Box <GLXCurses.Box.Box>`
        :type child: Widget
        :param expand: ``True`` if the new child is to be given extra space allocated to \
        `Box <GLXCurses.Box.Box>`. The extra space will be divided evenly between all children that use this option
        :type expand: bool
        :param fill: ``True`` if space given to :py:obj:`child` by the :py:attr:`expend` option is actually \
        allocated to :py:obj:`child`, rather than just padding it. This parameter has no effect if :py:attr:`expend` \
        is set to :py:obj:`False`. A child is always allocated the full height of a horizontal \
        :class:`Box <GLXCurses.Box.Box>` and the full width of a vertical :class:`Box <GLXCurses.Box.Box>`. \
        This option affects the other dimension.
        :type fill: bool
        :param padding: extra space in characters to put between this child and its neighbors, over and above \
        the global amount specified by :py:attr:`spacing` attribute. If child is a widget at one of the reference ends \
        of box , then padding pixels are also put between child and the reference edge of box
        :type padding: int or None
        :raise TypeError: if ``child`` is not a instance of :class:`Widget <GLXCurses.Widget.Widget>`
        :raise TypeError: if ``expand`` is not bool type
        :raise TypeError: if ``fill`` is not bool type
        :raise TypeError: if ``padding`` is not int or None
        """
        # Try to exit as soon of possible
        if not isinstance(child, GLXCurses.Widget):
            raise TypeError("'child' must be an instance of GLXCurses.Widget")
        if type(expand) != bool:
            raise TypeError('"expand" argument must be a bool type')
        if type(fill) != bool:
            raise TypeError('"fill" argument must be a bool type')
        if padding is not None:
            if type(padding) != int:
                raise TypeError('"spacing" must be int type or None')

        child_to_add = GLXCurses.ChildElement()
        child_to_add.widget = child
        child_to_add.type = child.glxc_type
        child_to_add.id = child.id
        child_to_add.name = "{0}{1}.fomat(child.name, child.id)"
        child_to_add.properties.expand = expand
        child_to_add.properties.fill = fill
        child_to_add.properties.padding = GLXCurses.clamp_to_zero(padding)
        child_to_add.properties.pack_type = GLXCurses.GLXC.PACK_END
        child_to_add.position = len(self.children)

        self.children.append(child_to_add)
        self._upgrade_child_position()

        self._emit_pack_end(data={'widget': child,
                                  'type': child.glxc_type,
                                  'id': child.id,
                                  'properties': {
                                      'expand': expand,
                                      'fill': fill,
                                      'padding': GLXCurses.clamp_to_zero(padding),
                                      'pack_type': GLXCurses.GLXC.PACK_END,
                                      'position': len(self.children)}
                                  })

    def reorder_child(self, child, position):
        """
        Moves :py:obj:`child` to a new :py:obj:`position` in the list of :class:`Box <GLXCurses.Box.Box>` children.
        The list contains widgets packed :py:const:`PACK_START` as well as widgets packed :py:const:`PACK_END`,
        in the order that these widgets were added to :class:`Box <GLXCurses.Box.Box>`.

        A widget’s position in the :class:`Box <GLXCurses.Box.Box>` children list determines where the widget is
        packed into :class:`Box <GLXCurses.Box.Box>`. A child widget at some position in the list will be packed
        just after all other widgets of the same packing type that appear earlier in the list.

        :param child: the widget to move
        :type child: :class:`Widget <GLXCurses.Widget.Widget>`
        :param position: the new position for :py:obj:`child` in the list of children of \
        :class:`Box <GLXCurses.Box.Box>`, starting from 0. If negative, indicates the end of the list.
        :type position: int
        :raise TypeError: if ``child`` is not a GLXCurses type as tested by \
        :func:`glxc_type() <GLXCurses.Utils.glxc_type>`
        :raise TypeError: if ``position`` is not int type
        :raise TypeError: if ``child`` is not a GLXCurses type as tested by \
        :func:`glxc_type() <GLXCurses.Utils.glxc_type>`
        """
        # Try to exit as soon of possible
        if not GLXCurses.glxc_type(child):
            raise TypeError('"child" argument must be a GLXCurses object type')
        if type(position) != int:
            raise TypeError('"position" must be int type')

        # If we are here everything look ok
        count = 0
        last_found = None
        last_element = None
        for children in self.children:
            if child == children.widget:
                last_found = count
                last_element = children
            count += 1

        if last_found is not None:
            self.children.pop(last_found)
            if position < 0:
                self.children.append(last_element)
            else:
                self.children.insert(position, last_element)
            self._upgrade_child_position()
            self._emit_reorder_child(data={'widget': last_element.widget,
                                           'type': last_element.widget.glxc_type,
                                           'id': last_element.widget.id,
                                           'properties': {
                                               'expand': last_element.properties.expand,
                                               'fill': last_element.properties.fill,
                                               'padding': last_element.properties.padding,
                                               'pack_type': last_element.properties.pack_type,
                                               'position': position}
                                           }
                                     )

    def query_child_packing(self, child):
        """
        Obtains information about how child is packed into box or None if child is not found

        **Return Key's:**
         widget: the Widget of the child to query
         expand: expand child property.
         fill: fill child property
         padding: padding child property.
         pack_type: pack-type child property

        :param child: the Widget of to query
        :type child: a Galaxie Widget
        :return: information about how child is packed into box
        :rtype: dict or None
        :raise TypeError: if ``child`` is not a GLXCurses type as tested by \
        :func:`glxc_type() <GLXCurses.Utils.glxc_type>`
        """
        # Try to exit as soon of possible
        if not GLXCurses.glxc_type(child):
            raise TypeError('"child" argument must be a GLXCurses object type')

        # If we are here everything look ok
        count = 0
        last_found = None
        last_element = None
        for children in self.children:
            if child == children.widget:
                last_found = count
                last_element = children
            count += 1

        if last_found is None:
            return None
        else:
            return last_element.properties.pack_type

    def set_child_packing(self, child, expand, fill, padding, pack_type):
        """
        Sets the way child is packed into box .

        :param child: the :class:`Widget <GLXCurses.Widget.Widget>` of the child to set
        :type child: :class:`Widget <GLXCurses.Widget.Widget>`
        :param expand: the new value of the expand child property
        :type expand: bool
        :param fill: the new value of the fill child property
        :type fill: bool
        :param padding: the new value of the padding child property
        :type padding: int
        :param pack_type: the new value of the pack-type child property
        :type pack_type: :py:const:`PackType`
        :raise TypeError: if ``child`` is not bool type
        :raise TypeError: if ``expand`` is not bool type
        :raise TypeError: if ``padding`` is not int or None
        :raise TypeError: if ``pack_type`` is not glxc.PACK_START or glxc.PACK_END
        """
        # Try to exit as soon of possible
        if not GLXCurses.glxc_type(child):
            raise TypeError('"child" argument must be a GLXCurses object type')
        if type(expand) != bool:
            raise TypeError('"expand" argument must be a bool type')
        if type(fill) != bool:
            raise TypeError('"fill" argument must be a bool type')
        if padding is not None:
            if type(padding) != int:
                raise TypeError('"padding" must be int type or None')
        if pack_type not in [GLXCurses.GLXC.PACK_START, GLXCurses.GLXC.PACK_END]:
            raise TypeError('"pack_type" must be glxc.PACK_START or glxc.PACK_END type')

        # If we are here everything look ok
        last_element = None
        for children in self.children:
            if child == children.widget:
                last_element = children

        if last_element is not None:
            last_element.widget = child
            last_element.properties.expand = expand
            last_element.properties.fill = fill
            last_element.properties.padding = padding
            last_element.properties.pack_type = pack_type

    def set_center_widget(self, widget=None):
        """
        Sets a center widget; that is a child widget that will be centered with respect to the full width of the box,
        even if the children at either side take up different amounts of space.

        :param widget: the :class:`Widget <GLXCurses.Widget.Widget>` of the child to set
        :type widget: :class:`Widget <GLXCurses.Widget.Widget>` or None
        :raise TypeError: if ``widget`` is not a GLXCurses type as tested by \
        :func:`glxc_type() <GLXCurses.Utils.glxc_type>` or None
        """
        if widget is not None:
            if not GLXCurses.glxc_type(widget):
                raise TypeError('"widget" argument must be a GLXCurses object type')

        if self.get_center_widget() != widget:
            self.center_widget = widget

    def get_center_widget(self):
        """
        Retrieves the center widget of the box.

        :return: the center widget or None in case no center widget is set.
        """
        return self.center_widget

    # Internal
    def _emit_reorder_child(self, data=None):
        """
        Is emitted whenever a new child is pack_end on the Box.

        :param data: user __area_data, what you want store
        :type data: dict
        :raise TypeError: When __area_data is not a dictionary
        :raise KeyError: When __area_data do not contain a "widget" key
        :raise KeyError: When __area_data do not contain a "properties" key
        """
        if type(data) != dict:
            raise TypeError('"__area_data" must be a dictionary')
        if 'widget' not in data:
            raise KeyError('"widget" key name is do not exist int __area_data dictionary')
        if 'properties' not in data:
            raise KeyError('"properties" key name is do not exist int __area_data dictionary')

        self.emit('reorder_child'.upper(), {
            'widget': ' '.join([self.__class__.__name__, self.id]),
            'child': ' '.join([data['widget'].__class__.__name__, data['widget'].id]),
            'child_properties': data['properties']
        })

    def _emit_pack_end(self, data=None):
        """
        Is emitted whenever a new child is pack_end on the Box.

        :param data: user __area_data, what you want store
        :type data: dict
        :raise TypeError: When __area_data is not a dictionary
        :raise KeyError: When __area_data do not contain a "widget" key
        :raise KeyError: When __area_data do not contain a "properties" key
        """
        if type(data) != dict:
            raise TypeError('"__area_data" must be a dictionary')
        if 'widget' not in data:
            raise KeyError('"widget" key name is do not exist int __area_data dictionary')
        if 'properties' not in data:
            raise KeyError('"properties" key name is do not exist int __area_data dictionary')
        self.emit('PACK_END', {'widget': ' '.join([self.__class__.__name__, self.id]),
                               'child': ' '.join([data['widget'].__class__.__name__, data['widget'].id]),
                               'child_properties': data['properties']
                               }
                  )

    def _emit_pack_start(self, data=None):
        """
        Is emitted whenever a new child is pack_start on the Box.

        :param data: user __area_data, what you want store
        :type data: dict
        :raise TypeError: When __area_data is not a dictionary
        :raise KeyError: When __area_data do not contain a "widget" key
        :raise KeyError: When __area_data do not contain a "properties" key
        """
        if type(data) != dict:
            raise TypeError('"__area_data" must be a dictionary')
        if 'widget' not in data:
            raise KeyError('"widget" key name is do not exist int __area_data dictionary')
        if 'properties' not in data:
            raise KeyError('"properties" key name is do not exist int __area_data dictionary')
        self.emit('PACK_START', {'widget': ' '.join([self.__class__.__name__, self.id]),
                                 'child': ' '.join([data['widget'].__class__.__name__, data['widget'].id]),
                                 'child_properties': data['properties']
                                 }
                  )

    def _upgrade_child_position(self):
        """After have reorder widget position update position property of all children"""
        if bool(self.children):
            count = 0
            for child in self.children:
                if child.properties.position != count:
                    self.emit('UPDATE_POSITION', {
                        'widget': ' '.join([self.__class__.__name__, self.id]),
                        'child': ' '.join([child.name, child.id]),
                        'before': child.properties.position,
                        'after': count
                    })
                    child.properties.position = count
                count += 1
