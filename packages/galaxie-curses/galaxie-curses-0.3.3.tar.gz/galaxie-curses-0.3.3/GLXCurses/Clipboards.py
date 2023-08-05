#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

# Inspired by: http://code.activestate.com/recipes/576887-shared-clipboard/
# Inspired by: https://developer.gnome.org/gtk3/stable/gtk3-Clipboards.html

import os
import getpass
import codecs

try:
    import pyperclip
except ImportError:
    pass
import json
# try:
#     from yaml import load, dump, FullLoader
# except ImportError:
#     pass

import GLXCurses


class Clipboard(object):
    def __init__(self):
        """

        """
        # It's a GLXCurse Type
        self.glxc_type = 'GLXCurses.Clipboard'

        # Unique ID it permit to individually identify a widget by example for get_focus get_default
        self.id = GLXCurses.new_id()

        self.name = '{0}{1}'.format(self.__class__.__name__, self.id)

        # pyperclip special attention
        self._use_pyperclip = True
        self._test_pyperclip()

        # Public Property
        self.can_store = True
        self.text = ''
        self.owner = getpass.getuser()

        # Internal
        self.directory = GLXCurses.get_os_temporary_dir()

        self.filename = str('')
        self.filename += str('GLXCurses-')
        self.filename += str(getpass.getuser())
        self.filename += str('.cb')

        self.file = os.path.normpath(os.path.join(self.directory, self.filename))

    def get(self):
        """
        Returns the clipboard object for the given selection.

        :return: The appropriate clipboard object.
        :rtype: Clipboard
        """
        return self

    def set_text(self, clipboard=None, text=None, length=-1):
        """
        Sets the contents of the clipboard to the given UTF-8 string.
        GLXCurses will make a copy of the text and take responsibility for responding for requests for the text,
        and for converting the text into the requested format.

        :param clipboard: a GLXCurses.Clipboard object or None for self
        :type clipboard: Clipboard or None
        :param text: a UTF-8 string.
        :type text: str or None
        :param length: length of text , in bytes, or -1, in which case the length will be determined with strlen().

        """
        # permit better unit test
        if clipboard is None:
            clipboard = self

        # Try to exit as soon of possible
        if not GLXCurses.glxc_type(clipboard):
            raise TypeError("'clipboard' must be a GLXCurses type")

        if not isinstance(clipboard, Clipboard):
            raise TypeError("'clipboard' must be an instance of GLXCurses.Clipboard")

        if not isinstance(text, (str, int, float, bool)):
            raise TypeError(
                'only str, int, float, and bool values can be copied to the clipboard, not %s' % (
                    text.__class__.__name__))

        # convert text as a str
        text = str(text)

        # make the job
        if length < 0:
            text = text
        if length == 0:
            text = ''
        if length > 0:
            length = GLXCurses.clamp(
                value=length,
                smallest=0,
                largest=len(text)
            )
            text = text[:length]

        # in case value have change
        if clipboard.text != text:
            clipboard.text = text

    def wait_for_text(self, clipboard=None):
        """
        Requests the contents of the clipboard as text and converts the result to UTF-8 if necessary.
        This function waits for the __area_data to be received using the main loop, so events, timeouts, etc,
        may be dispatched during the wait.

        :param clipboard: a GLXCurses.Clipboard
        :type clipboard: Clipboard
        :return: a newly-allocated UTF-8 string or NULL if retrieving the selection __area_data failed. \
        (This could happen for various reasons, in particular if the clipboard was empty or if the contents \
        of the clipboard could not be converted into text form.).
        :rtype: str
        """
        # permit better unit test
        if clipboard is None:
            clipboard = self

        # Try to exit as soon of possible
        if not GLXCurses.glxc_type(clipboard):
            raise TypeError("'clipboard' must be a GLXCurses type")

        if not isinstance(clipboard, Clipboard):
            raise TypeError("'clipboard' must be an instance of GLXCurses.Clipboard")

        # We make the job
        # Check if pyperclip can be use
        if clipboard._use_pyperclip:

            # Get the content of the pyperclip clipboard
            clipboard_contents = clipboard._pyperclip_paste(clipboard=clipboard)

            # If it have content we inform the GLXCurses clipboard
            if clipboard_contents:
                # First we set the text in the GLXCurses clipboard
                clipboard.set_text(clipboard=clipboard, text=clipboard_contents)

                # YES !!! we save on the GLXCurses clipboard exchange file the content of pyperclip clipboard
                clipboard.store(clipboard=clipboard)

        # In any case pyperclip or not we read the GLXCurses clipboard exchange file
        with codecs.open(clipboard.file, mode='r', encoding='utf-8-sig') as f:
            clipboard_contents = json.load(f)

        # Return GLXCurses clipboard exchange file content
        return clipboard_contents[self.__class__.__name__]['__area_data']

    def set_can_store(self, clipboard=None, targets=None, n_targets=None):
        """
        Hints that the clipboard __area_data should be stored somewhere when the application exits or when
        store() is called.

        This value is reset when the clipboard owner changes.

        :param clipboard: a GLXCurses.Clipboard object or None for self
        :type clipboard: Clipboard or None
        :param targets: array containing information about which forms should be stored or None to indicate that all \
        forms should be stored.
        :type targets: TYPE Constant or None
        :param n_targets: number of elements in targets
        :type n_targets: int or None
        """
        # permit better unit test
        if clipboard is None:
            clipboard = self

        # Try to exit as soon of possible
        if not GLXCurses.glxc_type(clipboard):
            raise TypeError("'clipboard' must be a GLXCurses type")

        if not isinstance(clipboard, Clipboard):
            raise TypeError("'clipboard' must be an instance of GLXCurses.Clipboard")

        # Make the job
        clipboard.can_store = True

    def store(self, clipboard=None):
        """
        Stores the current clipboard __area_data somewhere so that it will stay around after the application has quit.

        :param clipboard: a GLXCurses.Clipboard object or None for self
        :type clipboard: Clipboard or None
        """
        # permit better unit test
        if clipboard is None:
            clipboard = self

        # Try to exit as soon of possible
        if not GLXCurses.glxc_type(clipboard):
            raise TypeError("'clipboard' must be a GLXCurses type")

        if not isinstance(clipboard, Clipboard):
            raise TypeError("'clipboard' must be an instance of GLXCurses.Clipboard")

        # Make the job
        if self.can_store:
            data = {self.__class__.__name__: {'owner': clipboard.owner,
                                              'atom': 'CLIPBOARD',
                                              'id': clipboard.id,
                                              'type': GLXCurses.GLXC.TARGET_STRING,
                                              '__area_data': clipboard.text
                                              }
                    }

            with codecs.open(clipboard.file, mode='w', encoding='utf-8-sig') as fd:
                json.dump(data, fd)
                fd.close()
                # value have change then in case inform pyperclip
                if clipboard._use_pyperclip:
                    clipboard._pyperclip_copy(clipboard=clipboard)

    def _test_pyperclip(self, clipboard=None):
        """
        Determine if pyperclip can be use or not.

        That estimation is done one time during the initialisation of the GLXCurses.Clipboard class.

        :param clipboard: a GLXCurses.Clipboard object or None for self
        :type clipboard: Clipboard or None
        :return: True if we use pyperclip, False if not
        ;:rtype: bool
        """
        # permit better unit test
        if clipboard is None:
            clipboard = self

        # Try to exit as soon of possible
        if not GLXCurses.glxc_type(clipboard):
            raise TypeError("'clipboard' must be a GLXCurses type")

        if not isinstance(clipboard, Clipboard):
            raise TypeError("'clipboard' must be an instance of GLXCurses.Clipboard")

        # We Make the job
        try:
            pyperclip.paste()
            return True
        except pyperclip.PyperclipException:
            self._use_pyperclip = False
            return False

    def _pyperclip_copy(self, clipboard=None):
        """
        Just in case inform pyperclip better it can .

        :param clipboard: a GLXCurses.Clipboard object or None for self
        :type clipboard: Clipboard or None
        """
        # permit better unit test
        if clipboard is None:
            clipboard = self

        # Try to exit as soon of possible
        if not GLXCurses.glxc_type(clipboard):
            raise TypeError("'clipboard' must be a GLXCurses type")

        if not isinstance(clipboard, Clipboard):
            raise TypeError("'clipboard' must be an instance of GLXCurses.Clipboard")

        pyperclip.copy(clipboard.text)

    def _pyperclip_paste(self, clipboard=None):
        """
        Just in case inform pyperclip better it can .

        :param clipboard: a GLXCurses.Clipboard object or None for self
        :type clipboard: Clipboard or None
        :return: The Clipboard pyperclip content
        :rtype: str
        """
        # permit better unit test
        if clipboard is None:
            clipboard = self

        # Try to exit as soon of possible
        if not GLXCurses.glxc_type(clipboard):
            raise TypeError("'clipboard' must be a GLXCurses type")

        if not isinstance(clipboard, Clipboard):
            raise TypeError("'clipboard' must be an instance of GLXCurses.Clipboard")

        return str(pyperclip.paste())

    def _get_file(self, clipboard=None):
        """
        Get the file cross platform full path

        :param clipboard: a GLXCurses.Clipboard object or None for self
        :type clipboard: Clipboard or None
        :return: Normalized Cross plathform path
        :rtype: str
        """
        # permit better unit test
        if clipboard is None:
            clipboard = self

        # Try to exit as soon of possible
        if not GLXCurses.glxc_type(clipboard):
            raise TypeError("'clipboard' must be a GLXCurses type")

        if not isinstance(clipboard, Clipboard):
            raise TypeError("'clipboard' must be an instance of GLXCurses.Clipboard")

        # We Make the job
        return clipboard.file
