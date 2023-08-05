#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import GLXCurses
import curses
import textwrap


def resize_text(text, max_width, separator='~'):
    if max_width < len(text):
        text_to_return = text[:(max_width / 2) - 1] + separator + text[-max_width / 2:]
        if len(text_to_return) == 1:
            text_to_return = text[:1]
        elif len(text_to_return) == 2:
            text_to_return = str(text[:1] + text[-1:])
        elif len(text_to_return) == 3:
            text_to_return = str(text[:1] + separator + text[-1:])
        return text_to_return
    else:
        return text


class Label(GLXCurses.Misc):
    def __init__(self):
        # Load heritage
        GLXCurses.Misc.__init__(self)

        # It's a GLXCurse Type
        self.glxc_type = 'GLXCurses.Label'
        self.name = '{0}{1}'.format(self.__class__.__name__, self.id)

        # Make a Widget Style heritage attribute as local attribute
        # if self.style.attribute_states:
        #     if self.attribute_states != self.style.attribute_states:
        #         self.attribute_states = self.style.attribute_states

        # Label Properties
        # The current position of the insertion cursor in chars. Allowed values: >= 0. Default value: 0
        self.cursor_position = 0

        # justify
        # The alignment of the lines in the text of the label relative to each other.
        # The possible values are:
        # GLXCurses.GLXC.JUSTIFY_LEFT,
        # GLXCurses.GLXC.JUSTIFY_RIGHT,
        # GLXCurses.GLXC.JUSTIFY_CENTER,
        # GLXCurses.GLXC.JUSTIFY_FILL.
        # This does NOT affect the alignment of the label within its allocation.
        # Default value: GLXCurses.GLXC.JUSTIFY_LEFT
        self.justify = GLXCurses.GLXC.JUSTIFY_LEFT

        # The text of the label.
        # Default value: None
        self.__text = None

        # The desired maximum width of the label, in characters.
        # If this property is set to -1, the width will be calculated automatically,
        # otherwise the label will request space for no more than the requested number of characters.
        # If the "width_chars" property is set to a positive value, then the "max_width_chars" property is ignored.
        # Allowed values: >= -1.
        # Default value: -1
        self.max_width_chars = -1

        # The mnemonic accelerator key for this label.
        # Default value: 16777215
        self.mnemonic_keyval = 16777215

        # The widget to be activated when the label's mnemonic key is pressed.
        self.mnemonic_widget = None

        # A string with _ characters in positions used to identify to characters in the text to underline.
        # Default value: None
        self.pattern = '_'

        # If True, the label text can be selected with the mouse.
        # Default value: False
        self.selectable = False

        # The position of the opposite end of the selection from the cursor in chars.
        # Allowed values: >= 0.
        # Default value: 0.
        self.selection_bound = 0

        # If True the label is in single line mode.
        # In single line mode, the height of the label does not depend on the actual text,
        # it is always set to ascent + descent of the font. This can be an advantage
        # in situations where resizing the label because of text changes would be distracting, e.g. in a statusbar.
        # Default value: False
        self.single_line_mode = False

        # If True the label tracks which links have been clicked.
        # It will then apply the "visited-link-color" color, instead of "link-color". False
        self.track_visited_links = False

        # If True, an underscore in the text indicates the next character should be used
        # for the mnemonic accelerator key.
        # Default value: False
        self.use_underline = False

        # The desired width of the label, in characters.
        # If this property is set to -1, the width will be calculated automatically,
        # otherwise the label will request either 3 characters or the property value, whichever is greater.
        # Allowed values: >= -1.
        # Default value: -1.
        self.width_chars = -1

        # If True, wrap lines if the text becomes too wide.
        # Default value: False
        self.wrap = False

        # If line wrapping is on, this controls how the line wrapping is done.
        # The default is GLXCurses.GLXC.WRAP_WORD, which means wrap on word boundaries.
        self.wrap_mode = GLXCurses.GLXC.WRAP_WORD

        self.text_x = 0
        self.text_y = 0

        # Size management
        self.preferred_height = 1
        self.update_preferred_sizes()

    ###########
    # Methods #
    ###########
    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text=None):
        if text is not None and type(text) != str:
            raise TypeError('"text" must be a str type or None')
        if self.text != text:
            self.__text = text
            self.update_preferred_sizes()

    # The set_use_underline() method sets the "use-underline" property to the value of setting.
    # If setting is True,
    # an underscore in the text indicates the next character should be used for the mnemonic accelerator key.
    def set_use_underline(self, setting):
        if bool(setting):
            self.use_underline = True
        else:
            self.use_underline = False

    # The get_use_underline() method returns the value of the "use-underline" property.
    # If True an embedded underscore in the label indicates the next character is a mnemonic. See set_use_underline().
    def get_use_underline(self):
        return bool(self.use_underline)

    # set_markup_with_mnemonic

    # The get_mnemonic_keyval() method returns the value of the "mnemonic-keyval" property that contains the keyval
    # used for the mnemonic accelerator if one has been set on the label.
    # If there is no mnemonic set up it returns the void symbol keyval.
    def get_mnemonic_keyval(self):
        if self.mnemonic_keyval:
            return self.mnemonic_keyval
        else:
            return None

    # The set_mnemonic_widget() method sets the "mnemonic-widget" property using the value of widget.
    # This method associates the label mnemonic with a widget that will be activated
    #   when the mnemonic accelerator is pressed.
    # When the label is inside a widget (like a Button or a Notebook tab) it is automatically associated
    #  with the correct widget, but sometimes (i.e. when the target is a gtk.Entry next to the label)
    #  you need to set it explicitly using this function.
    # The target widget will be activated by emitting "mnemonic_activate" on it.
    def set_mnemonic_widget(self, widget):
        self.mnemonic_widget = widget
        # emitting "mnemonic_activate"

    # The get_mnemonic_widget() method retrieves the value of the "mnemonic-widget" property which is the target
    # of the mnemonic accelerator of this label.
    # See set_mnemonic_widget().
    def get_mnemonic_widget(self):
        return self.mnemonic_widget

    # The set_text_with_mnemonic() method sets the label's text from the string str.
    # If characters in str are preceded by an underscore,
    # they are underlined indicating that they represent a mnemonic accelerator.
    # The mnemonic key can be used to activate another widget, chosen automatically,
    # or explicitly using the set_mnemonic_widget() method.
    def set_text_with_mnemonic(self, string):
        string = str(string)
        if self.pattern in string:
            newstring = str(string).replace(self.pattern, '')
            mnemonic_index = ''
            for i in range(0, len(string)):
                if self.pattern == string[i]:
                    mnemonic_index = i
            self.text = str(newstring) + str(newstring[mnemonic_index])
            self.set_mnemonic_widget(self)
        else:
            self.text = string.index(self.pattern)

    def draw_widget_in_area(self):
        self.create_or_resize()

        if self.subwin is not None:
            if self.text:
                if self.get_single_line_mode():
                    self._draw_single_line_mode()
                else:
                    self._draw_multi_line_mode()

    def update_preferred_sizes(self):
        if self.text:
            preferred_width = 0
            preferred_height = 1

            preferred_width += len(self.text)
            preferred_width += self._get_imposed_spacing() * 2

            self.preferred_height = preferred_height
            self.preferred_width = preferred_width
        else:
            return

    def set_justify(self, justify=GLXCurses.GLXC.JUSTIFY_LEFT):
        """
        Sets the alignment of the lines in the text of the label relative to each other.

        GLXC.JUSTIFY_LEFT is the default value when the widget is first created with
        :func:`Label.new() <GLXCurses.Label.Label.new()>`.

        Allowed Justification:
         The text is placed at the left edge of the label.
          GLXCurses.GLXC.JUSTIFY_LEFT = 'LEFT'

         The text is placed at the right edge of the label.
          GLXC.JUSTIFY_RIGHT = 'RIGHT'

         The text is placed in the center of the label.
          GLXCurses.GLXC.JUSTIFY_CENTER = 'CENTER'

         The text is placed is distributed across the label.
          GLXCurses.GLXC.JUSTIFY_FILL = 'FILL'

        .. seealso:: \
        :func:`Label.get_justify() <GLXCurses.Label.Label.get_justify()>` for get the justification.

        :param justify: a justification
        :type: GLXCurses.GLXC.Justification
        :raise TypeError: when ``justify`` argument is not in GLXCurses.GLXC.Justification list.
        """
        if str(justify).upper() not in GLXCurses.GLXC.Justification:
            raise TypeError("'justify' must in GLXCurses.GLXC.Justification list")

        if self.get_justify() != str(justify).upper():
            self.justify = str(justify).upper()
            self.text_x = 0
            if self.get_justify() == GLXCurses.GLXC.JUSTIFY_CENTER:
                self.xalign = 0.5

            elif self.get_justify() == GLXCurses.GLXC.JUSTIFY_RIGHT:
                self.xalign = 1.0

            elif self.get_justify() == GLXCurses.GLXC.JUSTIFY_LEFT:
                self.xalign = 0.0

            return self.text_x

    def get_justify(self):
        """
        Returns the justification of the label.

        .. seealso:: \
        :func:`Label.set_justify() <GLXCurses.Label.Label.set_justify()>` for set the justification.

        :return: the justification
        :rtype: GLXCurses.GLXC.Justification
        """
        return self.justify

    def set_line_wrap(self, wrap=False):
        """
        The set_wrap() method sets the "wrap" property to the value of wrap.

        If wrap is True the label text will wrap if it is wider than the widget size; otherwise, the text gets
        cut off at the edge of the widget.

        Default, False

        :param wrap: True if wrap is enable
        :type wrap: bool
        :raise TypeError: when ``wrap`` argument is not a bool type.
        """
        # Exit as soon of possible
        if type(wrap) != bool:
            raise TypeError("'wrap' must be a bool type")

        if self.get_line_wrap() != wrap:
            self.wrap = wrap

    def get_line_wrap(self):
        """
        The get_line_wrap() method returns the value of the "wrap" property.

        If "wrap" is True the lines in the label are automatically wrapped. See set_line_wrap().

        :return: True if wrap is enable
        :rtype: bool
        """
        return self.wrap

    def set_width_chars(self, n_chars):
        """
        The set_width_chars() method sets the ``width-chars`` property to the value of n_chars.

        If this property is set to -1, the width will be calculated automatically,

        The ``width_chars`` property specifies the desired width of the label in characters.

         Allowed values: >= -1.
         Default value: -1.

        :param n_chars: number of chars
        :type n_chars: int
        :raise TypeError: when ``n_chars`` argument is not a int type.
        """
        # Exit as soon of possible
        if type(n_chars) != int:
            raise TypeError("'n_chars' must be a int type")

        # write is so slow
        if self.get_width_chars() != n_chars:
            self.width_chars = n_chars

    def get_width_chars(self):
        """
        The get_width_chars() method returns the value of the ``width-chars``

        property that specifies the desired width of the label in characters.

        :return: width of the label in characters
        :rtype: int
        """
        return int(self.width_chars)

    # The set_single_line_mode() method sets the "single-line-mode" property to the value of single_line_mode.
    # If single_line_mode is True the label is in single line mode where the height of the label does not
    # depend on the actual text, it is always set to ascent + descent of the font.
    def set_single_line_mode(self, single_line_mode):
        self.single_line_mode = bool(single_line_mode)

    # The get_single_line_mode() method returns the value of the "single-line-mode" property.
    # See the set_single_line_mode() method for more information
    def get_single_line_mode(self):
        return bool(self.single_line_mode)

    # The set_max_width_chars() method sets the "max-width-chars" property to the value of n_chars.
    def set_max_width_chars(self, n_chars):
        self.max_width_chars = n_chars

    # The get_max_width_chars() method returns the value of the "max-width-chars" property
    # which is the desired maximum width of the label in characters.
    def get_max_width_chars(self):
        return self.max_width_chars

    # The set_line_wrap_mode() method controls how line wrapping is done (if it is enabled, see refetch()).
    # The default is GLXCurses.GLXC.WRAP_WORD which means wrap on word boundaries.

    def set_line_wrap_mode(self, wrap_mode):
        self.wrap_mode = wrap_mode

    def get_line_wrap_mode(self):
        return self.wrap_mode

    # Internal
    def _get_x_offset(self):
        value = 0
        if self.text:
            # must be self.width and not self.width -1
            value += int((self.width - len(self.text)) * self.xalign)
        else:
            value += int(self.width * self.xalign)

        if value <= 0:
            value = self.xpad
            return value
        if 0 < self.xalign <= 0.5:
            value += self.xpad
        elif 0.5 <= self.xalign <= 1.0:
            value -= self.xpad
        return value

    def _get_y_offset(self):
        value = int(self.height * self.yalign)

        if value <= 0:
            value = self.ypad
            return value
        if 0 < self.ypad <= 0.5:
            value += self.ypad
        elif 0.5 <= self.yalign <= 1.0:
            value -= self.ypad
        return value

    def _get_single_line_resided_label_text(self, separator='~'):

        max_width = self.width - (self.xpad * 2)

        dedented_text = textwrap.dedent(self.text).strip()
        filled_text = textwrap.fill(dedented_text)

        border_width = self.width - len(filled_text) + (self.xpad * 2)
        if self.get_max_width_chars() <= -1:
            if border_width <= self.xpad * 2 + 1:
                return filled_text[:int(max_width / 2) - 1] + separator + filled_text[-int(max_width / 2):]
            else:
                return filled_text
        elif self.get_max_width_chars() == 0:
            return ''
        else:
            return filled_text[:self.get_max_width_chars()]

    def _draw_single_line_mode(self):
        try:
            _x_pos = GLXCurses.clamp(value=self._get_x_offset(),
                                     smallest=0,
                                     largest=self.width
                                     )
            _y_pos = GLXCurses.clamp(value=self._get_y_offset(),
                                     smallest=0,
                                     largest=self.height - 1
                                     )
            self.subwin.addstr(
                _y_pos,
                _x_pos,
                self._get_single_line_resided_label_text()[:-1],
                self.style.color(
                    fg=self.style.get_color_text('text', 'STATE_NORMAL'),
                    bg=self.style.get_color_text('bg', 'STATE_NORMAL')
                )
            )
            self.subwin.insch(
                self._get_single_line_resided_label_text()[-1:],
                self.style.color(
                    fg=self.style.get_color_text('text', 'STATE_NORMAL'),
                    bg=self.style.get_color_text('bg', 'STATE_NORMAL')
                )
            )

        except curses.error:  # pragma: no cover
            pass

    def _draw_multi_line_mode(self):

        max_height = self.height - 1 - (self.ypad * 2)
        max_width = self.width - (self.xpad * 2)
        increment = 0
        for line in self._textwrap(text=self.text, height=max_height, width=max_width):
            _x_pos = GLXCurses.clamp(value=self._get_x_offset(),
                                     smallest=0,
                                     largest=self.width
                                     )
            _y_pos = GLXCurses.clamp(value=self._get_y_offset() + increment,
                                     smallest=0,
                                     largest=self.height - 1
                                     )
            try:
                if self.get_max_width_chars() <= -1:
                    self.subwin.addstr(
                        _y_pos,
                        _x_pos,
                        self._check_justification(
                            text=line,
                            width=max_width),
                        self.style.color(
                            fg=self.style.get_color_text('text', 'STATE_NORMAL'),
                            bg=self.style.get_color_text('bg', 'STATE_NORMAL')
                        )
                    )
                    pass
                elif self.get_max_width_chars() == 0:
                    pass
                else:
                    self.subwin.addstr(
                        _y_pos,
                        _x_pos,
                        self._check_justification(
                            text=line,
                            width=self.get_max_width_chars()
                        )[:self.get_max_width_chars()],
                        self.style.color(
                            fg=self.style.get_color_text('text', 'STATE_NORMAL'),
                            bg=self.style.get_color_text('bg', 'STATE_NORMAL')
                        )
                    )
            except curses.error:  # pragma: no cover
                pass
            increment += 1

    def _textwrap(self, text='Hello World!', height=24, width=80):
        if self.get_line_wrap():
            lines = []
            for paragraph in text.split('\n'):
                line = []
                len_line = 0
                if self.get_line_wrap_mode() == GLXCurses.GLXC.WRAP_WORD_CHAR:
                    # Wrap this text.
                    wraped = textwrap.wrap(
                        paragraph,
                        width=width,
                        fix_sentence_endings=True,
                        break_long_words=True,
                        break_on_hyphens=True,
                    )

                    if len(lines) <= height:
                        lines += wraped
                elif self.get_line_wrap_mode() == GLXCurses.GLXC.WRAP_CHAR:
                    if len(paragraph) < width:
                        if len(lines) < height:
                            lines.append(paragraph)
                    else:
                        if len(lines) < height:
                            lines += [paragraph[ind:ind + width] for ind in range(0, len(paragraph), width)]
                else:
                    for word in paragraph.split(' '):
                        len_word = len(word)
                        if len_line + len_word <= width:
                            line.append(word)
                            len_line += len_word + 1
                        else:
                            lines.append(' '.join(line))
                            line = [word]
                            len_line = len_word + 1

                    if len(lines) < height:
                        lines.append(' '.join(line))
            return lines
        else:
            # This is the default display/view
            lines = []
            for paragraph in text.split('\n'):
                if len(paragraph) < width:
                    if len(lines) < height:
                        lines.append(paragraph)
                else:
                    if len(lines) < height:
                        lines.append(paragraph[:width])
            return lines

    def _check_justification(self, text="Hello World!", width=80):
        # Check Justification
        self.text_x = 0
        if self.justify == GLXCurses.GLXC.JUSTIFY_CENTER:
            self.xalign = 0.0
            return text.center(width, ' ')
        elif self.justify == GLXCurses.GLXC.JUSTIFY_LEFT:
            self.xalign = 0.0
            return "{0:<{1}}".format(text, width)
        elif self.justify == GLXCurses.GLXC.JUSTIFY_RIGHT:
            self.xalign = 0.0
            return "{0:>{1}}".format(text, width)
        else:
            self.xalign = self._get_x_offset()
            self.yalign = self._get_y_offset()
        return self.text_x

    def _check_position_type(self):
        self.text_y = self._get_y_offset()
        return self.text_y
