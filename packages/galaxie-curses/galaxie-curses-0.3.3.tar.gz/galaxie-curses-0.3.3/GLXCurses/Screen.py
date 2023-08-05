#!/usr/bin/env python
# -*- coding: utf-8 -*-


# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved
import os
import curses
import threading

lock = threading.Lock()


# class Singleton(type):
#     _instances = {}
#
#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             with lock:
#                 if cls not in cls._instances:
#                     cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
#         return cls._instances[cls]

class Singleton(type):
    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args)
        return cls.instance


# Inspired By: https://linux.die.net/man/3/noecho
class Screen(object, metaclass=Singleton):
    def __init__(self):

        self.__stdscr = None
        self.__cbreak = None
        self.__echo = None
        self.__halfdelay = None
        self.__intrflush = None
        self.__keypad = None
        self.__meta = None
        self.__nodelay = None
        self.__raw = None
        self.__qiflush = None
        self.__timeout = None
        self.__typeahead = None

        self.__curs_set = None
        # During initialization, the ncurses library checks for special cases where VT100 line-drawing
        # (and the corresponding alternate character set capabilities) described in the terminfo are known to be
        # missing. Specifically, when running in a UTF-8 locale, the Linux console emulator and the GNU stdscr
        # program ignore these. Ncurses checks the TERM environment variable for these. For other special cases,
        # you should set this environment variable. Doing this tells ncurses to use Unicode values which correspond
        # to the VT100 line-drawing glyphs. That works for the special cases cited, and is likely to work for terminal
        # emulators.
        #
        # When setting this variable, you should set it to a nonzero value. Setting it to zero (or to a nonnumbe
        # disables the special check for Linux and stdscr.
        os.environ["NCURSES_NO_UTF8_ACS"] = '1'

        # Specifies the total time, in milliseconds, for which ncurses will await a character sequence, e.g.,
        # a function key. The default value, 1000 milliseconds, is enough for most uses. However, it is made a
        # variable to accommodate unusual applications. The most common instance where you may wish to change this
        # value is to work with slow hosts, e.g., running on a network. If the host cannot read characters rapidly
        # enough, it will have the same effect as if the terminal did not send characters rapidly enough. The library
        # will still see a timeout.
        #
        # Note that xterm mouse events are built up from character sequences received from the xterm. If your
        # application makes heavy use of multiple-clicking, you may wish to lengthen this default value because the
        # timeout applies to the composed multi-click event as well as the individual clicks.
        #
        # In addition to the environment variable, this implementation provides a global variable with the same name.
        # Portable applications should not rely upon the presence of ESCDELAY in either form, but setting the
        # environment variable rather than the global variable does not create problems when compiling an application.
        os.environ['ESCDELAY'] = '25'

        self.stdscr = curses.initscr()

        # Turn off echoing of keys, and enter cbreak mode,
        # where no buffering is performed on keyboard input
        self.echo = False
        self.cbreak = True

        # In keypad mode, escape sequences for special keys
        # (like the cursor keys) will be interpreted and
        # a special value like curses.KEY_LEFT will be returned
        self.keypad = True

        # accept mouse events
        # curses.mousemask(0
        #                  | curses.BUTTON1_PRESSED | curses.BUTTON1_RELEASED
        #                  | curses.BUTTON2_PRESSED | curses.BUTTON2_RELEASED
        #                  | curses.BUTTON3_PRESSED | curses.BUTTON3_RELEASED
        #                  | curses.BUTTON4_PRESSED | curses.BUTTON4_RELEASED
        #                  | curses.BUTTON1_DOUBLE_CLICKED | curses.BUTTON1_TRIPLE_CLICKED
        #                  | curses.BUTTON2_DOUBLE_CLICKED | curses.BUTTON2_TRIPLE_CLICKED
        #                  | curses.BUTTON3_DOUBLE_CLICKED | curses.BUTTON3_TRIPLE_CLICKED
        #                  | curses.BUTTON4_DOUBLE_CLICKED | curses.BUTTON4_TRIPLE_CLICKED
        #                  | curses.BUTTON_SHIFT | curses.BUTTON_ALT
        #                  | curses.BUTTON_CTRL)
        curses.mousemask(-1)
        curses.mouseinterval(200)
        self.meta = True
        # Access ^c before shell does.
        # self.raw = True

        # Hide cursor
        curses.curs_set(0)

        # Curses setting
        self.stdscr.clear()

        if curses.has_colors():
            curses.start_color()
            curses.use_default_colors()

    @property
    def stdscr(self):
        return self.__stdscr

    @stdscr.setter
    def stdscr(self, stdscr=None):
        if stdscr != self.stdscr:
            self.__stdscr = stdscr

    @property
    def cbreak(self):
        """
        Normally, the tty driver buffers typed characters until a newline or carriage return is typed.
        If ``cbreak=True`` The cbreak property disables line buffering and erase/kill character-processing
        (interrupt and flow control
        characters are unaffected), making characters typed by the user immediately available to the program.

        The (cbreak is False) returns the terminal to normal (cooked) mode.

        Initially the terminal may or may not be in cbreak mode, as the mode is inherited; therefore, a program
        should call ``cbreak=True`` or ``cbreak=False`` explicitly.

        Most interactive programs using curses set the ``cbreak=True`` mode.

        Note that ``cbreak`` overrides ``raw``.

        The raw=False and cbreak=False calls follow historical practice in that they attempt to restore
        to normal ('cooked') mode from raw and cbreak modes respectively. M

        Mixing (raw is True or False) and (cbreak is True or False) calls leads to tty driver control states
        that are hard to predict or understand; it is not recommended.

        Note that return None if the property have never been set.

        [See curs_getch(3X) for a discussion of how these routines interact with ``echo=True`` and ``echo=False``.]

        :return: The cbreak property value
        :rtype: bool
        """
        return self.__cbreak

    @cbreak.setter
    def cbreak(self, cbreak=None):
        """
        Set the cbreak property.

         * If True: curses.cbreak()
         * If False: curses.nocbreak()
         * If None: curses.nocbreak()

        :param cbreak: accept True, False, None as value
        :type cbreak: bool or None
        """
        if cbreak not in [True, False, None]:
            raise ValueError('"cbreak" must be a bool value or None')

        if cbreak is None:
            cbreak = False

        if self.cbreak != cbreak:
            self.__cbreak = cbreak

        try:
            if self.cbreak is True:
                curses.cbreak()
            if self.cbreak is False:
                curses.nocbreak()
        except curses.error:  # pragma: no cover
            pass

    @property
    def echo(self):
        """
        Control whether characters typed by the user are echoed by getch as they are
        typed. Echoing by the tty driver is always disabled, but initially getch is in echo mode, so characters typed
        are echoed. Authors of most interactive programs prefer to do their own echoing in a controlled area of the
        screen, or not to echo at all, so they disable echoing by calling noecho. [See curs_getch(3X) for a
        discussion of how these routines interact with cbreak and nocbreak.]

        :return the echo property value
        :rtype: bool
        """
        return self.__echo

    @echo.setter
    def echo(self, echo=None):
        """
        Set the echo property.

         * If ``True``: curses.echo()
         * If ``False``: curses.noecho()
         * If ``None``: curses.noecho()

        :param echo: accept ``True``, ``False``, ``None`` as value
        :type echo: bool or None
        :raise ValueError: when ``echo`` is not bool type or None
        """
        if echo is not True and echo is not False and echo is not None:
            raise TypeError('"echo" must be a bool value or None')

        if echo is None:
            echo = False

        if self.echo != echo:
            self.__echo = echo

        try:
            if self.echo is True:
                curses.echo()
            if self.echo is False:
                curses.noecho()
        except curses.error:  # pragma: no cover
            pass

    @property
    def halfdelay(self):
        """
        The ``halfdelay`` property is used for half-delay mode, which is similar to cbreak mode in that characters
        typed by the user are immediately available to the program. However, after blocking for ``tenths`` tenths of
        seconds, ERR is returned if nothing has been typed.



        :return:
        """
        return self.__halfdelay

    @halfdelay.setter
    def halfdelay(self, tenths=None):
        """
        If ``tenths`` is set to ``None``, 0, -1 ``halfdelay`` and ``cbreak`` will be set to ``False``

        Use nocbreak to leave half-delay mode.

        :param tenths: The value of tenths must be a number between 1 and 255.
        :type: int or None
        """
        if tenths is not None and type(tenths) != int:
            raise TypeError('"tenths" must be in int type or None')

        if tenths is not None:
            if self.halfdelay != max(1, min(tenths, 255)):
                self.__halfdelay = max(1, min(tenths, 255))
        else:
            if self.halfdelay is not None:
                self.__halfdelay = None

        if self.halfdelay is None:
            try:
                curses.nocbreak()
            except curses.error:  # pragma: no cover
                pass
            self.cbreak = False
        else:
            curses.halfdelay(self.halfdelay)

    @property
    def intrflush(self):
        """
        If the intrflush property is enabled, (bf is TRUE), when an interrupt key is pressed on the keyboard
        (interrupt, break, quit) all output in the tty driver queue will be flushed, giving the effect of
        faster response to the interrupt, but causing curses to have the wrong idea of what is on the screen.

        Disabling (bf is FALSE), the option prevents the flush.

        The default for the option is inherited from the tty driver settings. The window argument is ignored.

        Note: That return None only if property have never been set

        :return: The ``intrflush`` property value
        :rtype: bool or None
        """
        return self.__intrflush

    @intrflush.setter
    def intrflush(self, bf=None):
        """
        Set the ``intrflush`` property.

         * If ``True``: curses.intrflush(True)
         * If ``False``: curses.intrflush(False)
         * If ``None``: curses.intrflush(False)

        :param bf: accept ``True``, ``False``, ``None`` as value
        :type bf: bool or None
        :raise ValueError: When ``bf`` is not a bool or None type
        """
        if bf not in [True, False, None]:
            raise ValueError('"intrflush" must be a bool value or None')

        if bf is None:
            bf = False

        if bf != self.intrflush:
            self.__intrflush = bf
        try:
            if self.intrflush is True:
                curses.intrflush(True)
            if self.intrflush is False:
                curses.intrflush(False)
        except curses.error:  # pragma: no cover
            pass

    @property
    def keypad(self):
        """
        The ``keypad`` property enables the keypad of the user's terminal.

        If enabled (bf is TRUE), the user can press a function key (such as an arrow key) and wgetch returns a single
        value representing the function key, as in KEY_LEFT. If disabled (bf is FALSE), curses does not treat
        function keys specially and the program has to interpret the escape sequences itself.

        If the keypad in the terminal can be turned on (made to transmit) and off (made to work locally), turning on
        this option causes the terminal keypad to be turned on when wgetch is called.

        The default value for ``keypad`` is ``True``.

        Note: That return ``None`` if ``keypad`` have never been set.

        :return: The ``keypad`` property value
        :rtype: bool or None
        """
        return self.__keypad

    @keypad.setter
    def keypad(self, bf=None):
        """
        Set the ``keypad`` property.

         * If ``True``: self.stdscr.keypad(1)
         * If ``False``: self.stdscr.keypad(0)
         * If ``None``: self.stdscr.keypad(0)

        :param bf: accept ``True``, ``False``, ``None`` as value
        :type bf: bool or None
        """
        if bf not in [True, False, None]:
            raise ValueError('"bf" must be a bool value or None')

        if bf is None:
            bf = False

        if self.keypad != bf:
            self.__keypad = bf

        try:
            if self.stdscr is not None:
                if self.keypad is True:
                    self.stdscr.keypad(1)
                if self.keypad is False:
                    self.stdscr.keypad(0)
        except curses.error:  # pragma: no cover
            pass

    @property
    def meta(self):
        """
        Initially, whether the terminal returns 7 or 8 significant bits on input depends on the control mode of the
        tty driver [see termio(7)].

        To force 8 bits to be returned, invoke ``meta``=``True`` this is equivalent,
        under POSIX, to setting the CS8 flag on the terminal.

        To force 7 bits to be returned, invoke ``meta``=``False`` this is equivalent, under POSIX, to setting the CS7
        flag on the terminal.

        If the terminfo capabilities smm (meta_on) and rmm (meta_off) are defined for the terminal, smm is sent to the
        terminal when ``meta``=``True`` is called and rmm is sent when ``meta``=``False`` is called.

        Note: That return ``None`` when the property have never been set

        :return: The ``meta`` property value
        :rtype: bool or None
        """
        return self.__meta

    @meta.setter
    def meta(self, meta=None):
        """
        Set the ``meta`` property.

         * If ``True``: curses.meta(True)
         * If ``False``: curses.meta(False)
         * If ``None``: curses.meta(False)

        :param meta: accept ``True``, ``False``, ``None`` as value
        :type meta: bool or None
        """
        if meta not in [True, False, None]:
            raise ValueError('"meta" must be a bool value or None')

        if meta is None:
            meta = False

        if self.meta != meta:
            self.__meta = meta

        try:
            if self.meta is True:
                curses.meta(True)
            if self.meta is False:
                curses.meta(False)
        except curses.error:  # pragma: no cover
            pass

    @property
    def nodelay(self):
        """
        The nodelay option causes getch to be a non-blocking call.
        If no input is ready, getch returns ERR. If disabled (bf is FALSE), getch waits until a key is pressed.

        While interpreting an input escape sequence, wgetch sets a timer while waiting for the next character.
        If notimeout(win, TRUE) is called, then wgetch does not set a timer. The purpose of the timeout is to
        differentiate between sequences received from a function key and those typed by a user.

        :return: The ``nodelay`` property value
        :rtype: bool or None
        """
        return self.__nodelay

    @nodelay.setter
    def nodelay(self, bf=None):
        """
        Set the ``nodelay`` property.

         * If ``True``: self.stdscr.nodelay(True)
         * If ``False``: self.stdscr.nodelay(False)
         * If ``None``: self.stdscr.nodelay(False)

        :param bf: accept ``True``, ``False``, ``None`` as value
        :type bf: bool or None
        """
        if bf not in [True, False, None]:
            raise ValueError('"nodelay" must be a bool value or None')

        if bf is None:
            bf = False

        if self.nodelay != bf:
            self.__nodelay = bf

        try:
            if self.stdscr is not None:
                if self.nodelay is True:
                    self.stdscr.nodelay(True)
                if self.nodelay is False:
                    self.stdscr.nodelay(False)
        except curses.error:  # pragma: no cover
            pass

    @property
    def raw(self):
        """
        The ``raw`` property place the terminal into or out of raw mode.

        Raw mode is similar to cbreak mode, in that characters typed are immediately passed through to the user program.
        The differences are that in raw mode, the interrupt, quit, suspend, and flow control characters are all
        passed through uninterpreted, instead of generating a signal.

        The behavior of the BREAK key depends on other bits in the tty driver that are not set by curses.

        :return: The ``property`` value
        :rtype: bool or None
        """
        return self.__raw

    @raw.setter
    def raw(self, raw=None):
        """
        Set the raw property.

         * If ``True``: curses.raw()
         * If ``False``: curses.noraw()
         * If ``None``: curses.noraw()

        :param raw: accept ``True``, ``False``, ``None`` as value
        :type raw: bool or None
        """
        if raw not in [True, False, None]:
            raise ValueError('"raw" must be a bool value or None')

        if raw is None:
            raw = False

        if self.raw != raw:
            self.__raw = raw

        try:
            if self.raw is True:
                curses.raw()
            if self.raw is False:
                curses.noraw()
        except curses.error:  # pragma: no cover
            pass

    @property
    def qiflush(self):
        """
        When (qiflush is False) normal flush of input and output queues associated with the
        INTR, QUIT and SUSP characters will not be done [see termio(7)].

        When (qiflush is True) is called, the queues will be flushed when these control characters are read.

        You may want use (qiflush is False) in a signal handler if you want output to continue as though the interrupt
        had not occurred, after the handler exits.

        :return: The ``qiflush`` property value
        :rtype: bool or None
        """
        return self.__qiflush

    @qiflush.setter
    def qiflush(self, qiflush=None):
        """
        Set the qiflush property.

         * If ``True``: curses.qiflush()
         * If ``False``: curses.noqiflush()
         * If ``None``: curses.noqiflush()

        :param qiflush: accept ``True``, ``False``, ``None`` as value
        :type qiflush: bool or None
        """
        if qiflush not in [True, False, None]:
            raise ValueError('"qiflush" must be a bool value or None')

        if qiflush is None:
            qiflush = False

        if self.qiflush != qiflush:
            self.__qiflush = qiflush

        try:
            if self.qiflush is True:
                curses.qiflush()
            if self.qiflush is False:
                curses.noqiflush()
        except curses.error:  # pragma: no cover
            pass

    @property
    def timeout(self):
        """
        The timeout and wtimeout routines set blocking or non-blocking read for a given window.

        If delay is negative, blocking read is used (i.e., waits indefinitely for input).

        If delay is zero, then non-blocking read is used (i.e., read returns ERR if no input is waiting).

        If delay is positive, then read blocks for delay milliseconds, and returns ERR if there is still no input.

        Hence, these routines provide the same functionality as nodelay, plus the additional capability of
        being able to block for only delay milliseconds (where delay is positive).

        :return:
        """
        return self.__timeout

    @timeout.setter
    def timeout(self, delay=None):
        """
        Set the ``timeout`` property

        If ``delay`` is negative, blocking read is used (i.e., waits indefinitely for input).

        If ``delay`` is zero, then non-blocking read is used (i.e., read returns ERR if no input is waiting).

        If ``delay`` is positive, then read blocks for delay milliseconds, and returns ERR if there is still no input.

        :param delay: negative , zero, positive int
        :type delay: int
        :raise TypeError: When delay is not a int type
        """
        if delay is None:
            delay = 0
        if type(delay) != int:
            raise TypeError('"delay" must be a int type')

        if self.timeout != delay:
            self.__timeout = delay

        try:
            if self.stdscr is not None:
                self.stdscr.timeout(delay)
        except curses.error:  # pragma: no cover
            pass

    # Extra
    @property
    def curs_set(self):
        return self.__curs_set

    # Function
    def close(self):
        """
        A Application must be close properly for permit to Curses to clean up everything and get back the tty \
        in startup condition

        Generally that is follow  by a sys.exit(0) for generate a exit code.
        """
        # Set everything back to normal
        # if 'stdscr' in locals():
        #     self.stdscr.keypad(0)
        #     curses.curs_set(1)
        #     curses.echo()
        #     curses.nocbreak()
        #     curses.endwin()
        self.keypad = False
        curses.curs_set(1)
        self.echo = True
        self.cbreak = False

        try:
            curses.endwin()
        except curses.error:  # pragma: no cover
            pass

    def refresh(self):
        # Curses flush the virtual stdscr in to the real stdscr
        self.stdscr.noutrefresh()
        # After have redraw everything it's time to refresh the stdscr
        # self.stdscr.noutrefresh()
        # curses.doupdate()
        # self.stdscr.noutrefresh()
        self.stdscr.refresh()

    def clear(self):
        # Clean the stdscr
        self.stdscr.erase()

        # self.stdscr.noutrefresh()
        # curses.doupdate()
