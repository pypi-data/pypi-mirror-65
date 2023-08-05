#!/usr/bin/env python
# -*- coding: utf-8 -*-
# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

# I DON'T RESPECT PEP8 ABOUT IMPORT ...
# BECAUSE PYTHON DEVELOPER HAVE RESPONSIBILITY TO HAVE MAINTAIN 2 PYTHON VERSION DURING MORE OF 10 YEARS
# THEY HAVE DO THAT , JUST FOR A CONCEPTUAL THING, WITHOUT ANY GAIN.
#
# NOW , I HAVE TO TEST PYTHON2 ...

import sys

if not sys.version_info > (2, 7, 17):
    raise SystemExit('You need Python 3 or later to run this script')

import locale

lang, enc = locale.getdefaultlocale()
lang = lang or 'C'
enc = enc or 'UTF-8'
try:
    oldlocale = locale.getlocale(locale.LC_TIME)
    try:
        locale.setlocale(locale.LC_TIME, (lang, enc))
    finally:
        locale.setlocale(locale.LC_TIME, oldlocale)
except (locale.Error, ValueError):
    # raise ImportError('cannot set the system default locale')
    pass
# locale.setlocale(locale.getdefaultlocale())
# code = locale.getpreferredencoding(do_setlocale=True)
# print(code)
# print(locale.getdefaultlocale())
# sys.exit()
__all__ = [
    'GLXC',
    'Clipboard',
    'Screen',
    'Style',
    'EventBusClient',
    'Area',
    'Object',
    'Dividable',
    'Movable',
    'ChildElement',
    'ChildProperty',
    'GroupElement',
    'Group',
    'Groups',
    'Widget',
    'Container',
    'TextTag',
    'TextTagTable',
    'TextBuffer',
    'TextView',
    'Bin',
    'Box',
    'VBox',
    'HBox',
    'Window',
    'RadioButton',
    'CheckButton',
    'Adjustment',
    'Dialog',
    'MainLoop',
    'Application',
    'Frame',
    'MenuBar',
    'Menu',
    'MenuItem',
    'StatusBar',
    'MessageBar',
    'ToolBar',
    'Misc',
    'Label',
    'ProgressBar',
    'VuMeter',
    'HSeparator',
    'VSeparator',
    'EntryBuffer',
    'Editable',
    'Entry',
    'EntryCompletion',
    'Range',
    'Actionable',
    'FileSelect'
]

from GLXCurses.Utils import *
from GLXCurses.Constants import GLXC
from GLXCurses.UtilsMovable import Movable
from GLXCurses.UtilsDividable import Dividable
from GLXCurses.Clipboards import Clipboard
from GLXCurses.Screen import Screen
from GLXCurses.EventBusClient import EventBusClient
from GLXCurses.Aera import Area
from GLXCurses.Style import Style
from GLXCurses.UtilsGroupElement import GroupElement
from GLXCurses.UtilsGroup import Group
from GLXCurses.UtilsGroups import Groups
from GLXCurses.UtilsSpot import Spot
from GLXCurses.Application import Application
from GLXCurses.Object import Object
from GLXCurses.UtilsChildElement import ChildElement
from GLXCurses.UtilsChildProperty import ChildProperty
from GLXCurses.Widget import Widget
from GLXCurses.Container import Container
from GLXCurses.Bin import Bin
from GLXCurses.Box import Box
from GLXCurses.VBox import VBox
from GLXCurses.HBox import HBox
from GLXCurses.Window import Window
from GLXCurses.Frame import Frame
from GLXCurses.Button import Button
from GLXCurses.RadioButton import RadioButton
from GLXCurses.CheckButton import CheckButton
from GLXCurses.Adjustment import Adjustment
from GLXCurses.Dialog import Dialog
from GLXCurses.MainLoop import MainLoop
from GLXCurses.FileChooserMenu import FileChooserMenu
from GLXCurses.MenuBar import MenuBar
from GLXCurses.Menu import Menu
from GLXCurses.MenuItem import MenuItem
from GLXCurses.StatusBar import StatusBar
from GLXCurses.MessageBar import MessageBar
from GLXCurses.ToolBar import ToolBar
from GLXCurses.Misc import Misc
from GLXCurses.TextTag import TextTag
from GLXCurses.TextTagTable import TextTagTable
from GLXCurses.TextBuffer import TextBuffer
from GLXCurses.TextView import TextView

from GLXCurses.Label import Label
from GLXCurses.ProgressBar import ProgressBar
from GLXCurses.HSeparator import HSeparator
from GLXCurses.VSeparator import VSeparator
from GLXCurses.EntryBuffer import EntryBuffer
from GLXCurses.Editable import Editable
from GLXCurses.Entry import Entry
from GLXCurses.EntryCompletion import EntryCompletion
from GLXCurses.Range import Range
from GLXCurses.Actionable import Actionable
# from GLXCurses.VuMeter import VuMeter
from GLXCurses.FileChooser import FileSelect

application = Application()
mainloop = MainLoop()
