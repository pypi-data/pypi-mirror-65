#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import GLXCurses
import curses
import logging


class MessageBar(GLXCurses.Widget):
    """
    A MessageBar is usually placed along the bottom of an Application. It may provide a regular
    commentary of the application's status (as is usually the case in a web browser, for example), or may be used to
    simply output a message when the status changes, (when an upload is complete in an FTP client, for example).

    Status bars in GLXCurses maintain a stack of messages.
    The message at the top of the each bar’s stack is the one that will currently be displayed.

    Any messages added to a StatusBar’s stack must specify a context id that is used to uniquely identify
    the source of a message. This context id can be generated by
    :func:`GLXCurses.StatusBar.get_context_id() <GLXCurses.StatusBar.StatusBar.get_context_id>`, given a message
    and the StatusBar that it will be added to. Note that messages are stored in a stack,
    and when choosing which message to display, the stack structure is adhered to, regardless of the context
    identifier of a message.

    One could say that a StatusBar maintains one stack of messages for display purposes, but allows multiple message
    producers to maintain sub-stacks of the messages they produced (via context ids).

    Status bars are created using
    :func:`GLXCurses.MessageBar.new() <GLXCurses.MessageBar.MessageBar.new>`.

    Messages are added to the bar’s stack with
    :func:`GLXCurses.MessageBar.push() <GLXCurses.MessageBar.MessageBar.push>`.

    The message at the top of the stack can be removed using
    :func:`GLXCurses.MessageBar.pop() <GLXCurses.MessageBar.MessageBar.pop>`.

    A message can be removed from anywhere in the stack if its message id was recorded at the time it was added.
    This is done using :func:`GLXCurses.MessageBar.remove() <GLXCurses.MessageBar.StatusBar.remove>`.
    """

    def __init__(self):
        # Load heritage
        GLXCurses.Widget.__init__(self)

        # It's a GLXCurse Type
        self.glxc_type = 'GLXCurses.MessageBar'
        self.name = '{0}{1}'.format(self.__class__.__name__, self.id)

        # Make a Widget Style heritage attribute as local attribute
        if self.style.attribute_states:
            if self.attribute_states != self.style.attribute_states:
                self.attribute_states = self.style.attribute_states

        # Widget Setting
        self.messagebar_stack = list()
        self.context_id_dict = dict()

    def new(self):
        """
        Creates a new :func:`GLXCurses.MessageBar <GLXCurses.MessageBar.MessageBar>` ready for messages.

        :return: the new MessageBar
        :rtype: GLXCurses.MessageBar
        """
        self.__init__()
        return self

    def get_context_id(self, context_description='Default'):
        """
        Returns a new context identifier, given a description of the actual context.

        .. note: the description is not shown in the UI.

        :param context_description: textual description of what context the new message is being used in
        :type context_description: str
        :return: an context_id generate by Utils.new_id()
        :rtype: str
        :raises TypeError: When context_description is not a str
        """
        # Try to exit as soon of possible
        if type(context_description) != str:
            raise TypeError('"context_description" must be a str or unicode type')

        # If we are here everything look ok
        if context_description not in self._get_context_id_list():
            self._get_context_id_list()[context_description] = GLXCurses.new_id()
            logging.debug(
                "MessageBar CONTEXT CREATION: context_id={0} context_description={1}".format(
                    self._get_context_id_list()[context_description],
                    str(context_description)
                )
            )

        return self._get_context_id_list()[context_description]

    def push(self, context_id, text):
        """
        Push a new message onto the MessageBar's stack.

        :param context_id: a context identifier, as returned by MessageBar.get_context_id()
        :type context_id: str
        :param text: the message to add to the MessageBar
        :type text: str
        :return: a message identifier that can be used with MessageBar.remove().
        :rtype: str
        """
        # Try to exit as soon of possible
        if not GLXCurses.is_valid_id(context_id):
            raise TypeError('"context_id" must be a str type as returned by MessageBar.get_context_id()')
        if type(text) != str:
            raise TypeError('"text" must be a str type')

        # If we are here everything look ok
        message_id = GLXCurses.new_id()

        message_info = dict()
        message_info['context_id'] = context_id
        message_info['message_id'] = message_id
        message_info['text'] = text

        self._get_messagebar_stack().append(message_info)
        self._emit_text_pushed(context_id, text)
        return message_id

    def pop(self, context_id):
        """
        Removes the first message in the MessageBar’s stack with the given context id.

        Note that this may not change the displayed message, if the message at the top of the stack has a different
        context id.

        :param context_id: a context identifier, as returned by MessageBar.get_context_id()
        :type context_id: str
        """
        # Try to exit as soon of possible
        if not GLXCurses.is_valid_id(context_id):
            raise TypeError('"context_id" must be a unicode type see MessageBar.get_context_id()')

        # If we are here everything look ok
        count = 0
        last_found = None
        last_element = None
        for element in self._get_messagebar_stack():
            if context_id == element['context_id']:
                last_found = count
                last_element = element
            count += 1

        if last_found is not None:
            self._get_messagebar_stack().pop(last_found)
            self._emit_text_popped(last_element['context_id'], last_element['text'])

    def remove(self, context_id, message_id):
        """
        Forces the removal of a message from a MessageBar’s stack.
        The exact **context_id** and **message_id** must be specified.

        :param context_id: a context identifier, as returned by MessageBar.get_context_id()
        :type context_id: str
        :param message_id: a message identifier, as returned by MessageBar.push()
        :type message_id: str
        """
        # Try to exit as soon of possible
        if not GLXCurses.is_valid_id(context_id):
            raise TypeError('"context_id" arguments must be unicode type as returned by MessageBar.get_context_id()')
        if not GLXCurses.is_valid_id(message_id):
            raise TypeError('"message_id" arguments must be unicode type as returned by MessageBar.push()')

        # If we are here everything look ok
        count = 0
        last_found = None
        last_element = None
        for element in self._get_messagebar_stack():
            if context_id == element['context_id'] and message_id == element['message_id']:
                last_found = count
                last_element = element
            count += 1
        if last_found is not None:
            logging.debug(
                "MessageBar REMOVE: index={0} context_id={1} message_id={2} text={3}".format(
                    str(last_found),
                    str(last_element['context_id']),
                    str(last_element['message_id']),
                    str(last_element['text'])
                )
            )
            self._get_messagebar_stack().pop(last_found)

    def remove_all(self, context_id):
        """
        Forces the removal of all messages from a MessageBar's stack with the exact context_id .

        :param context_id: a context identifier, as returned by MessageBar.get_context_id()
        :type context_id: str
        """
        # Try to exit as soon of possible
        if not GLXCurses.is_valid_id(context_id):
            raise TypeError('"context_id" arguments must be unicode type as returned by MessageBar.get_context_id()')

        # If we are here everything look ok
        for element in self._get_messagebar_stack():
            if context_id == element['context_id']:
                self.remove(element['context_id'], element['message_id'])

    def _check_sizes(self):
        self.preferred_width = self.width
        self.preferred_height = 1

    def _draw_background(self):
        self.subwin.bkgd(
            ord(' '),
            self.style.color(fg='GRAY', bg='BLACK')
        )
        self.subwin.bkgdset(
            ord(' '),
            self.style.color(fg='GRAY', bg='BLACK')
        )

    # def _draw_background(self):
    #
    #     self.subwin.addstr(
    #         0,
    #         0,
    #         str(' ' * (self.width - 1)),
    #         self.style.get_color_pair(
    #             foreground=self.style.get_color_text('text', 'STATE_NORMAL'),
    #             background=self.style.get_color_text('dark', 'STATE_NORMAL')
    #         )
    #     )
    #     self.subwin.insstr(
    #         0,
    #         self.width - 1,
    #         str(' '),
    #         self.style.get_color_pair(
    #             foreground=self.style.get_color_text('text', 'STATE_NORMAL'),
    #             background=self.style.get_color_text('dark', 'STATE_NORMAL')
    #         )
    #     )

    def draw(self):
        """
        Place the status bar from the end of the stdscr by look if it have a tool bar before
        """
        self.create_or_resize()

        if self.subwin is not None:
            self._check_sizes()
            self._draw_background()

            # If it have something inside the StatusBar stack they display it but care about the display size
            if len(self._get_messagebar_stack()):
                for x_inc in range(0, len(str(self._get_messagebar_stack()[-1]['text']))):
                    try:
                        self.subwin.delch(0, 0 + x_inc)
                        self.subwin.insch(
                            0,
                            x_inc,
                            str(self._get_messagebar_stack()[-1]['text'][x_inc]),
                            self.style.color(
                                fg=self.style.get_color_text('text', 'STATE_NORMAL'),
                                bg=self.style.get_color_text('dark', 'STATE_NORMAL')
                            )
                        )
                    except curses.error:  # pragma: no cover
                        pass

    # Siganles
    def _emit_text_popped(self, context_id, text, user_data=None):
        """
        Is emitted whenever a new message is popped off a StatusBar's stack.

        :param context_id: the context id of the relevant message/StatusBar
        :type context_id: str
        :param text: the message that was just popped
        :type text: str
        :param user_data: user __area_data set when the signal handler was connected.
        :type user_data: list
        """
        if user_data is None:
            user_data = list()
        # Create a Dict with everything
        instance = {
            'class': self.__class__.__name__,
            'type': 'text-popped',
            'id': self.id,
            'context_id': context_id,
            'text': text,
            'user_data': user_data
        }
        # EVENT EMIT
        self.emit('SIGNALS', instance)

    def _emit_text_pushed(self, context_id, text, user_data=None):
        """
        Is emitted whenever a new message is popped off a StatusBar's stack.

        :param context_id: the context id of the relevant message/StatusBar
        :type context_id: str
        :param text: the message that was just popped
        :type text: str
        :param user_data: user __area_data set when the signal handler was connected.
        :type user_data: list
        """
        if user_data is None:
            user_data = list()

        # Create a Dict with everything
        instance = {
            'class': self.__class__.__name__,
            'type': 'text-pushed',
            'id': self.id,
            'context_id': context_id,
            'text': text,
            'user_data': user_data
        }
        # EVENT EMIT
        self.emit('SIGNALS', instance)

    # Internal Method's
    def _get_context_id_list(self):
        """
        Return context_id_dict attribute

        :return: context_id_dict attribute
        :rtype: dict
        """
        return self.context_id_dict

    def _get_messagebar_stack(self):
        """
        Return messagebar_stack attribute

        :return: messagebar_stack attribute
        :rtype: list
        """
        return self.messagebar_stack
