#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

# Inspired by: http://code.activestate.com/recipes/65207-constants-in-python/?in=user-97991


class Constants(object):
    """
    **GLXC.BaselinePosition**

    Whenever a container has some form of natural row it may align children in that row along a common
    typographical baseline. If the amount of vertical space in the row is taller than the total requested
    height of the baseline-aligned children then it can use a GLXC.BaselinePosition to select where
    to put the baseline inside the extra available space.

    Members:
        GLXC.BASELINE_POSITION_TOP: Align the baseline at the top
        GLXC.BASELINE_POSITION_CENTER: Center the baseline
        GLXC.BASELINE_POSITION_BOTTOM: Align the baseline at the bottom
    """

    class ConstError(TypeError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const(%s)" % name)
        self.__dict__[name] = value

    def __getattr__(self, name):
        if name not in self.__dict__:
            raise self.ConstError("No attribute %s exist" % name)
        return self.__dict__[name]


#############################
# Variables
#############################
GLXC = Constants()

#############################
# Internal
#############################
# Inspired by: https://realpython.com/python-rounding/

GLXC.ROUND_UP = 'UP'
GLXC.ROUND_DOWN = 'DOWN'
GLXC.ROUND_HALF_UP = 'HALF_UP'
GLXC.ROUND_HALF_DOWN = 'HALF_DOWN'

GLXC.RoundType = [
    GLXC.ROUND_UP,
    GLXC.ROUND_DOWN,
    GLXC.ROUND_HALF_UP,
    GLXC.ROUND_HALF_DOWN
]
# enum WindowPosition
# Inspired by: https://developer.gnome.org/gtk3/stable/GtkWindow.html#GtkWindowPosition
# Window placement can be influenced using this enumeration.
# Note that using WIN_POS_CENTER_ALWAYS is almost always a bad idea.
# It won’t necessarily work well with all window managers or on all windowing systems.

# No influence is made on placement.
GLXC.WIN_POS_NONE = 'NONE'

# Windows should be placed in the center of the stdscr.
GLXC.WIN_POS_CENTER = 'CENTER'

# Windows should be placed at the current mouse position.
GLXC.WIN_POS_MOUSE = 'MOUSE'

# Keep window centered as it changes size, etc.
GLXC.WIN_POS_CENTER_ALWAYS = 'CENTER_ALWAYS'

# Center the window on its transient parent (see Window.set_transient_for()).
GLXC.WIN_POS_CENTER_ON_PARENT = 'CENTER_ON_PARENT'

# Create WindowPosition
GLXC.WindowPosition = [
    GLXC.WIN_POS_NONE,
    GLXC.WIN_POS_CENTER,
    GLXC.WIN_POS_MOUSE,
    GLXC.WIN_POS_CENTER_ALWAYS,
    GLXC.WIN_POS_CENTER_ON_PARENT
]

# WindowType
# https://developer.gnome.org/gtk3/stable/GtkWindow.html#GtkWindowType

# A GtkWindow can be one of these types. Most things you’d consider a “window” should have type GLXC.WINDOW_TOPLEVEL;
# windows with this type are managed by the window manager and have a frame by default
# (call GLXCurses.Window.set_decorated() to toggle the frame).

# Windows with type GLXC.WINDOW_POPUP are ignored by the window manager; window manager keybindings
# won’t work on them, the window manager won’t decorate the window with a frame, many GLXCurses features that rely
# on the window manager will not work (e.g. resize grips and maximization/minimization).

# GTK_WINDOW_POPUP is used to implement widgets such as GLXCurses.Menu or tooltips that you normally don’t think
# of as windows per se. Nearly all windows should be GLXC.WINDOW_TOPLEVEL.
# In particular, do not use GLXC.WINDOW_POPUP just to turn off the window borders;
# use GLXCurses.Window.set_decorated() for that.

# A regular window, such as a dialog.
GLXC.WINDOW_TOPLEVEL = 'TOPLEVEL'
# A special window such as a tooltip.
GLXC.WINDOW_POPUP = 'POPUP'

# Create WindowType
GLXC.WindowType = [
    GLXC.WINDOW_TOPLEVEL,
    GLXC.WINDOW_POPUP
]

# WindowTypeHint
# http://gtk.php.net/manual/en/html/gdk/gdk.enum.windowtypehint.html
#
# These are hints for the window manager that indicate what type of function the window has. The
# window manager can use this when determining decoration and behaviour of the window. The hint must be set before
# mapping the window.
# Normal toplevel window.
GLXC.WINDOW_TYPE_HINT_NORMAL = 'NORMAL'
# Dialog window.
GLXC.WINDOW_TYPE_HINT_DIALOG = 'DIALOG'
# Window used to implement a menu.
GLXC.WINDOW_TYPE_HINT_MENU = 'MENU'
# Window used to implement toolbars.
GLXC.WINDOW_TYPE_HINT_TOOLBAR = 'TOOLBAR'
# Window used to display a splash screen during application startup.
GLXC.WINDOW_TYPE_HINT_SPLASHSCREEN = 'SPLASHSCREEN'
# Utility windows which are not detached toolbars or dialogs.
GLXC.WINDOW_TYPE_HINT_UTILITY = 'UTILITY'
# Used for creating dock or panel windows.
GLXC.WINDOW_TYPE_HINT_DOCK = 'DOCK'
# Used for creating the desktop background window.
GLXC.WINDOW_TYPE_HINT_DESKTOP = 'DESKTOP'

GLXC.WindowTypeHint = [
    GLXC.WINDOW_TYPE_HINT_NORMAL,
    GLXC.WINDOW_TYPE_HINT_DIALOG,
    GLXC.WINDOW_TYPE_HINT_MENU,
    GLXC.WINDOW_TYPE_HINT_TOOLBAR,
    GLXC.WINDOW_TYPE_HINT_SPLASHSCREEN,
    GLXC.WINDOW_TYPE_HINT_UTILITY,
    GLXC.WINDOW_TYPE_HINT_DOCK,
    GLXC.WINDOW_TYPE_HINT_DESKTOP
]

# DialogType

# Make the constructed dialog modal, see window.set_modal()
GLXC.DIALOG_MODAL = 'MODAL'
# Destroy the dialog when its parent is destroyed, see window.set_destroy_with_parent()
GLXC.DIALOG_DESTROY_WITH_PARENT = 'DESTROY_WITH_PARENT'
# Create dialog with actions in header bar instead of action area.
GLXC.DIALOG_USE_HEADER_BAR = 'USE_HEADER_BAR'

# Create DialogFlags
# https://developer.gnome.org/gtk3/unstable/GtkDialog.html#GtkDialogFlags
GLXC.DialogFlags = [
    GLXC.DIALOG_MODAL,
    GLXC.DIALOG_DESTROY_WITH_PARENT,
    GLXC.DIALOG_USE_HEADER_BAR
]

# ResponseType
# https://developer.gnome.org/gtk3/unstable/GtkDialog.html#GtkResponseType
# Predefined values for use as response ids in gtk_dialog_add_button().
# All predefined values are negative; GTK+ leaves values of 0 or greater for application-defined response ids.
#
# Returned if an action widget has no response id, or if the dialog gets programmatically hidden or destroyed
GLXC.RESPONSE_NONE = 'NONE'
# Generic response id, not used by GTK+ dialogs
GLXC.RESPONSE_REJECT = 'REJECT'
# Generic response id, not used by GTK+ dialogs
GLXC.RESPONSE_ACCEPT = 'ACCEPT'
# Returned if the dialog is deleted
GLXC.RESPONSE_DELETE_EVENT = 'DELETE_EVENT'
# Returned by OK buttons in GTK+ dialogs
GLXC.RESPONSE_OK = 'OK'
# Returned by Cancel buttons in GTK+ dialogs
GLXC.RESPONSE_CANCEL = 'CANCEL'
# Returned by Close buttons in GTK+ dialogs
GLXC.RESPONSE_CLOSE = 'CLOSE'
# Returned by Yes buttons in GTK+ dialogs
GLXC.RESPONSE_YES = 'YES'
# Returned by No buttons in GTK+ dialogs
GLXC.RESPONSE_NO = 'NO'
# Returned by Apply buttons in GTK+ dialogs
GLXC.RESPONSE_APPLY = 'APPLY'
# Returned by Help buttons in GTK+ dialogs
GLXC.RESPONSE_HELP = 'HELP'

# Create GLXC.ResponseType
GLXC.ResponseType = [
    GLXC.RESPONSE_NONE,
    GLXC.RESPONSE_REJECT,
    GLXC.RESPONSE_ACCEPT,
    GLXC.RESPONSE_DELETE_EVENT,
    GLXC.RESPONSE_OK,
    GLXC.RESPONSE_CANCEL,
    GLXC.RESPONSE_CLOSE,
    GLXC.RESPONSE_YES,
    GLXC.RESPONSE_NO,
    GLXC.RESPONSE_APPLY,
    GLXC.RESPONSE_HELP
]

# Gravity
# GRAVITY_NORTH_WEST    The reference point is at the top left corner.
GLXC.GRAVITY_NORTH_WEST = 'NORTH_WEST'
# GRAVITY_NORTH         The reference point is in the middle of the top edge.
GLXC.GRAVITY_NORTH = 'NORTH'
# GRAVITY_NORTH_EAST    The reference point is at the top right corner.
GLXC.GRAVITY_NORTH_EAST = 'NORTH_EAST'
# GRAVITY_WEST          The reference point is at the middle of the left edge.
GLXC.GRAVITY_WEST = 'WEST'
# GRAVITY_CENTER        The reference point is at the center of the window.
GLXC.GRAVITY_CENTER = 'CENTER'
# GRAVITY_EAST          The reference point is at the middle of the right edge.
GLXC.GRAVITY_EAST = 'EAST'
# GRAVITY_SOUTH_WEST    The reference point is at the lower left corner.
GLXC.GRAVITY_SOUTH_WEST = 'SOUTH_WEST'
# GRAVITY_SOUTH         The reference point is at the middle of the lower edge.
GLXC.GRAVITY_SOUTH = 'SOUTH'
# GRAVITY_SOUTH_EAST    The reference point is at the lower right corner.
GLXC.GRAVITY_SOUTH_EAST = 'SOUTH_EAST'
# GRAVITY_STATIC        The reference point is at the top left corner of the window itself,
GLXC.GRAVITY_STATIC = 'STATIC'

GLXC.Gravity = [
    GLXC.GRAVITY_NORTH_WEST,
    GLXC.GRAVITY_NORTH,
    GLXC.GRAVITY_NORTH_EAST,
    GLXC.GRAVITY_WEST,
    GLXC.GRAVITY_CENTER,
    GLXC.GRAVITY_EAST,
    GLXC.GRAVITY_SOUTH_WEST,
    GLXC.GRAVITY_SOUTH,
    GLXC.GRAVITY_SOUTH_EAST,
    GLXC.GRAVITY_STATIC
]

# Inspired by: https://developer.gnome.org/gtk3/stable/gtk3-Standard-Enumerations.html
####################
# BaselinePosition #
####################
# Whenever a container has some form of natural row it may align children in that row along a common
# typographical baseline. If the amount of vertical space in the row is taller than the total requested
# height of the baseline-aligned children then it can use a GLXC.BaselinePosition to select where
# to put the baseline inside the extra available space.

# Align the baseline at the top
GLXC.BASELINE_POSITION_TOP = 'TOP'

# Center the baseline
GLXC.BASELINE_POSITION_CENTER = 'CENTER'

# Align the baseline at the bottom
GLXC.BASELINE_POSITION_BOTTOM = 'BOTTOM'

# Final List
GLXC.BaselinePosition = [
    GLXC.BASELINE_POSITION_TOP,
    GLXC.BASELINE_POSITION_CENTER,
    GLXC.BASELINE_POSITION_BOTTOM
]

#########
# Align #
#########
# Controls how a widget deals with extra space in a single (x or y) dimension.
# Alignment only matters if the widget receives a “too large” allocation, for example if you packed the widget with
# the “expand” flag inside a GLXCurses.Box, then the widget might get extra space.
#
# Note that in horizontal context GLXC.ALIGN_START and GLXC.ALIGN_END are interpreted relative to text direction.
#
# GLXC.ALIGN_BASELINE support for it is optional for containers and widgets,
# and it is only supported for vertical alignment.
# When its not supported by a child or a container it is treated as GLXC.ALIGN_FILL .


# Stretch to fill all space if possible, center if no meaningful way to stretch
GLXC.ALIGN_FILL = 'FILL'

# snap to left or top side, leaving space on right or bottom
GLXC.ALIGN_START = 'START'

# snap to right or bottom side, leaving space on left or top
GLXC.ALIGN_END = 'END'

# center natural width of widget inside the allocation
GLXC.ALIGN_CENTER = 'CENTER'

# align the widget according to the baseline.
GLXC.ALIGN_BASELINE = 'BASELINE'

GLXC.Align = [
    GLXC.ALIGN_FILL,
    GLXC.ALIGN_START,
    GLXC.ALIGN_END,
    GLXC.ALIGN_CENTER,
    GLXC.ALIGN_BASELINE
]

##############
# DeleteType #
##############

# Delete characters.
GLXC.DELETE_CHARS = 'CHARS'

# Delete only the portion of the word to the left/right of cursor if we’re in the middle of a word.
GLXC.DELETE_WORD_ENDS = 'WORD_ENDS'

# Delete words.
GLXC.DELETE_WORDS = 'WORDS'

# Delete display-lines. Display-lines refers to the visible lines, with respect to to the current line breaks.
# As opposed to paragraphs, which are defined by line breaks in the input.
GLXC.DELETE_DISPLAY_LINES = 'DISPLAY_LINES'

# Delete only the portion of the display-line to the left/right of cursor.
GLXC.DELETE_DISPLAY_LINE_ENDS = 'DISPLAY_LINE_ENDS'

# Delete to the end of the paragraph. Like C-k in Emacs (or its reverse).
GLXC.DELETE_PARAGRAPH_ENDS = 'PARAGRAPH_ENDS'

# Delete entire line. Like C-k in pico.
GLXC.DELETE_PARAGRAPHS = 'PARAGRAPHS'

# Delete only whitespace. Like M-\ in Emacs.
GLXC.DELETE_WHITESPACE = 'WHITESPACE'

# Final List
GLXC.DeleteType = [
    GLXC.DELETE_CHARS,
    GLXC.DELETE_WORD_ENDS,
    GLXC.DELETE_WORDS,
    GLXC.DELETE_DISPLAY_LINES,
    GLXC.DELETE_DISPLAY_LINE_ENDS,
    GLXC.DELETE_PARAGRAPH_ENDS,
    GLXC.DELETE_PARAGRAPHS,
    GLXC.DELETE_WHITESPACE
]

#################
# DirectionType #
#################
# Focus movement types.

# Move forward.
GLXC.DIR_TAB_FORWARD = 'TAB_FORWARD'

# Move backward.
GLXC.DIR_TAB_BACKWARD = 'TAB_BACKWARD'

# Move up.
GLXC.DIR_UP = 'UP'

# Move down.
GLXC.DIR_DOWN = 'DOWN'

# Move left.
GLXC.DIR_LEFT = 'LEFT'

# Move right.
GLXC.DIR_RIGHT = 'RIGHT'

# Final List
GLXC.DirectionType = [
    GLXC.DIR_TAB_FORWARD,
    GLXC.DIR_TAB_BACKWARD,
    GLXC.DIR_UP,
    GLXC.DIR_DOWN,
    GLXC.DIR_LEFT,
    GLXC.DIR_RIGHT
]

#################
# Justification #
#################
# The text is placed at the left edge of the label.
GLXC.JUSTIFY_LEFT = 'LEFT'

# The text is placed at the right edge of the label.
GLXC.JUSTIFY_RIGHT = 'RIGHT'

# The text is placed in the center of the label.
GLXC.JUSTIFY_CENTER = 'CENTER'

# The text is placed is distributed across the label.
GLXC.JUSTIFY_FILL = 'FILL'

# Set the final list
GLXC.Justification = [
    GLXC.JUSTIFY_LEFT,
    GLXC.JUSTIFY_CENTER,
    GLXC.JUSTIFY_RIGHT,
    GLXC.JUSTIFY_FILL
]

#################
# MovementStep #
#################

# Move forward or back by graphemes
GLXC.MOVEMENT_LOGICAL_POSITIONS = 'LOGICAL_POSITIONS'

# Move left or right by graphemes
GLXC.MOVEMENT_VISUAL_POSITIONS = 'VISUAL_POSITIONS'

# Move forward or back by words
GLXC.MOVEMENT_WORDS = 'WORDS'

# Move up or down lines (wrapped lines)
GLXC.MOVEMENT_DISPLAY_LINES = 'DISPLAY_LINES'

# Move to either end of a line
GLXC.MOVEMENT_DISPLAY_LINE_ENDS = 'DISPLAY_LINE_ENDS'

# Move up or down paragraphs (newline-ended lines)
GLXC.MOVEMENT_PARAGRAPHS = 'PARAGRAPHS'

# Move to either end of a paragraph
GLXC.MOVEMENT_PARAGRAPH_ENDS = 'PARAGRAPH_ENDS'

# Move by pages
GLXC.MOVEMENT_PAGES = 'PAGES'

# Move to ends of the buffer
GLXC.MOVEMENT_BUFFER_ENDS = 'BUFFER_ENDS'

# Move horizontally by pages
GLXC.MOVEMENT_HORIZONTAL_PAGES = 'HORIZONTAL_PAGES'

# Set Final list
GLXC.MovementStep = [
    GLXC.MOVEMENT_LOGICAL_POSITIONS,
    GLXC.MOVEMENT_VISUAL_POSITIONS,
    GLXC.MOVEMENT_WORDS,
    GLXC.MOVEMENT_DISPLAY_LINES,
    GLXC.MOVEMENT_DISPLAY_LINE_ENDS,
    GLXC.MOVEMENT_PARAGRAPHS,
    GLXC.MOVEMENT_PARAGRAPH_ENDS,
    GLXC.MOVEMENT_PAGES,
    GLXC.MOVEMENT_BUFFER_ENDS,
    GLXC.MOVEMENT_HORIZONTAL_PAGES
]

###################
# Orientation     #
###################
# https://developer.gnome.org/gtk3/stable/gtk3-Standard-Enumerations.html#GtkOrientation
# Represents the orientation of widgets and other objects which can be switched between
# horizontal and vertical orientation on the fly, like ToolBar

# The element is in horizontal orientation.
GLXC.ORIENTATION_HORIZONTAL = 'HORIZONTAL'

# The element is in vertical orientation.
GLXC.ORIENTATION_VERTICAL = 'VERTICAL'

# Set the Final list
GLXC.Orientation = [
    GLXC.ORIENTATION_HORIZONTAL,
    GLXC.ORIENTATION_VERTICAL
]

################
# PackType     #
################
# Represents the packing location Box children. (See: VBox, HBox, and ButtonBox).

# The child is packed into the start of the box
GLXC.PACK_START = 'START'

# The child is packed into the end of the box
GLXC.PACK_END = 'END'

# Set the final list
GLXC.PackType = [
    GLXC.PACK_START,
    GLXC.PACK_END
]

#################
#  PositionType #
#################
# Describes which edge of a widget a certain feature is positioned

# The feature is at the left edge.
GLXC.POS_LEFT = 'LEFT'

# The feature is at the right edge.
GLXC.POS_RIGHT = 'RIGHT'

# The feature is at the center.
GLXC.POS_CENTER = 'CENTER'

# The feature is at the top edge.
GLXC.POS_TOP = 'TOP'

# The feature is at the bottom edge.
GLXC.POS_BOTTOM = 'BOTTOM'

# Set the final list
GLXC.PositionType = [
    GLXC.POS_LEFT,
    GLXC.POS_RIGHT,
    GLXC.POS_CENTER,
    GLXC.POS_TOP,
    GLXC.POS_BOTTOM
]

######################
# Relief ReliefStyle #
######################
# Indicated the relief to be drawn around a Button.

# Draw a normal relief.
GLXC.RELIEF_NORMAL = 'NORMAL'

# A half relief.
GLXC.RELIEF_HALF = 'HALF'

# No relief.
GLXC.RELIEF_NONE = 'NONE'

# Set the final list
GLXC.ReliefStyle = [
    GLXC.RELIEF_NORMAL,
    GLXC.RELIEF_HALF,
    GLXC.RELIEF_NONE
]

##############
# ScrollStep #
##############

# Scroll in steps.
GLXC.SCROLL_STEPS = 'STEPS'

# Scroll by pages.
GLXC.SCROLL_PAGES = 'PAGES'

# Scroll to ends.
GLXC.SCROLL_ENDS = 'ENDS'

# Scroll in horizontal steps.
GLXC.SCROLL_HORIZONTAL_STEPS = 'HORIZONTAL_STEPS'

# Scroll by horizontal pages.
GLXC.SCROLL_HORIZONTAL_PAGES = 'HORIZONTAL_PAGES'

# Scroll to the horizontal ends.
GLXC.SCROLL_HORIZONTAL_ENDS = 'HORIZONTAL_ENDS'

# Set the Final List
GLXC.ScrollStep = [
    GLXC.SCROLL_STEPS,
    GLXC.SCROLL_PAGES,
    GLXC.SCROLL_ENDS,
    GLXC.SCROLL_HORIZONTAL_STEPS,
    GLXC.SCROLL_HORIZONTAL_PAGES,
    GLXC.SCROLL_HORIZONTAL_ENDS
]

##############
# ScrollType #
##############
# Scrolling types.

# No scrolling.
GLXC.SCROLL_NONE = 'NONE'

# Jump to new location.
GLXC.SCROLL_JUMP = 'JUMP'

# Step backward.
GLXC.SCROLL_STEP_BACKWARD = 'STEP_BACKWARD'

# Step forward.
GLXC.SCROLL_STEP_FORWARD = 'STEP_FORWARD'

# Page backward.
GLXC.SCROLL_PAGE_BACKWARD = 'PAGE_BACKWARD'

# Page forward.
GLXC.SCROLL_PAGE_FORWARD = 'PAGE_FORWARD'

# Step up.
GLXC.SCROLL_STEP_UP = 'STEP_UP'

# Step down.
GLXC.SCROLL_STEP_DOWN = 'STEP_DOWN'

# Page up.
GLXC.SCROLL_PAGE_UP = 'PAGE_UP'

# Page down.
GLXC.SCROLL_PAGE_DOWN = 'PAGE_DOWN'

# Step to the left.
GLXC.SCROLL_STEP_LEFT = 'STEP_LEFT'

# Step to the right.
GLXC.SCROLL_STEP_RIGHT = 'STEP_RIGHT'

# Page to the left.
GLXC.SCROLL_PAGE_LEFT = 'PAGE_LEFT'

# Page to the right.
GLXC.SCROLL_PAGE_RIGHT = 'PAGE_RIGHT'

# Scroll to start.
GLXC.SCROLL_START = 'START'

# Scroll to end.
GLXC.SCROLL_END = 'END'

# Set the final list
GLXC.ScrollType = [
    GLXC.SCROLL_NONE,
    GLXC.SCROLL_JUMP,
    GLXC.SCROLL_STEP_BACKWARD,
    GLXC.SCROLL_STEP_FORWARD,
    GLXC.SCROLL_PAGE_BACKWARD,
    GLXC.SCROLL_PAGE_FORWARD,
    GLXC.SCROLL_STEP_UP,
    GLXC.SCROLL_STEP_DOWN,
    GLXC.SCROLL_PAGE_UP,
    GLXC.SCROLL_PAGE_DOWN,
    GLXC.SCROLL_STEP_LEFT,
    GLXC.SCROLL_STEP_RIGHT,
    GLXC.SCROLL_PAGE_LEFT,
    GLXC.SCROLL_PAGE_RIGHT,
    GLXC.SCROLL_START,
    GLXC.SCROLL_END
]

#################
# SelectionMode #
#################
# Used to control what selections users are allowed to make.

# No selection is possible.
GLXC.SELECTION_NONE = 'NONE'

# Zero or one element may be selected.
GLXC.SELECTION_SINGLE = 'SINGLE'

# Exactly one element is selected. In some circumstances,
# such as initially or during a search operation, it’s possible for
# no element to be selected with GLXC.SELECTION_BROWSE.
# What is really enforced is that the user can’t deselect a
# currently selected element except by selecting another element.
GLXC.SELECTION_BROWSE = 'BROWSE'

# Any number of elements may be selected. The Ctrl key may
# be used to enlarge the selection, and Shift key to select
# between the focus and the child pointed to. Some widgets
# may also allow Click-drag to select a range of elements.
GLXC.SELECTION_MULTIPLE = 'MULTIPLE'

# Set the final list
GLXC.SelectionMode = [
    GLXC.SELECTION_NONE,
    GLXC.SELECTION_SINGLE,
    GLXC.SELECTION_BROWSE,
    GLXC.SELECTION_MULTIPLE
]

##############
# ShadowType #
##############
# The Shadow Type constants specify the appearance of an outline typically provided by a Frame.

# No outline
GLXC.SHADOW_NONE = 'NONE'
# The outline is beveled inward.
GLXC.SHADOW_IN = 'IN'
# The outline is beveled outward like a button.
GLXC.SHADOW_OUT = 'OUT'
# The outline itself is an inward bevel, but the frame bevels outward
GLXC.SHADOW_ETCHED_IN = 'ETCHED_IN'
# The outline itself is an outward bevel, but the frame bevels inward
GLXC.SHADOW_ETCHED_OUT = 'ETCHED_OUT'
# Set the final list
GLXC.ShadowType = [
    GLXC.SHADOW_NONE,
    GLXC.SHADOW_IN,
    GLXC.SHADOW_OUT,
    GLXC.SHADOW_ETCHED_IN,
    GLXC.SHADOW_ETCHED_OUT
]

##############
# StateFlags #
##############

# State during normal operation.
GLXC.STATE_FLAG_NORMAL = 'NORMAL'

# Widget is active.
GLXC.STATE_FLAG_ACTIVE = 'ACTIVE'

# Widget has a mouse pointer over it.
GLXC.STATE_FLAG_PRELIGHT = 'PRELIGHT'

# Widget is selected.
GLXC.STATE_FLAG_SELECTED = 'SELECTED'

# Widget is insensitive.
GLXC.STATE_FLAG_INSENSITIVE = 'INSENSITIVE'

# Widget is inconsistent.
GLXC.STATE_FLAG_INCONSISTENT = 'INCONSISTENT'

# Widget has the keyboard focus.
GLXC.STATE_FLAG_FOCUSED = 'FOCUSED'

# Widget is in a background top level window.
GLXC.STATE_FLAG_BACKDROP = 'BACKDROP'

# Widget is in left-to-right text direction.
GLXC.STATE_FLAG_DIR_LTR = 'DIR_LTR'

# Widget is in right-to-left text direction.
GLXC.STATE_FLAG_DIR_RTL = 'DIR_RTL'

# Widget is a link.
GLXC.STATE_FLAG_LINK = 'LINK'

# The location the widget points to has already been visited.
GLXC.STATE_FLAG_VISITED = 'VISITED'

# Widget is checked.
GLXC.STATE_FLAG_CHECKED = 'CHECKED'

# Widget is highlighted as a drop target for DND.
GLXC.STATE_FLAG_DROP_ACTIVE = 'DROP_ACTIVE'

# Set the final list
GLXC.StateFlags = [
    GLXC.STATE_FLAG_NORMAL,
    GLXC.STATE_FLAG_ACTIVE,
    GLXC.STATE_FLAG_PRELIGHT,
    GLXC.STATE_FLAG_SELECTED,
    GLXC.STATE_FLAG_INSENSITIVE,
    GLXC.STATE_FLAG_INCONSISTENT,
    GLXC.STATE_FLAG_FOCUSED,
    GLXC.STATE_FLAG_BACKDROP,
    GLXC.STATE_FLAG_DIR_LTR,
    GLXC.STATE_FLAG_DIR_RTL,
    GLXC.STATE_FLAG_LINK,
    GLXC.STATE_FLAG_VISITED,
    GLXC.STATE_FLAG_CHECKED,
    GLXC.STATE_FLAG_DROP_ACTIVE
]

################
# ToolbarStyle #
################
# Used to customize the appearance of a Toolbar. Note that setting the toolbar style overrides the user’s preferences
# for the default toolbar style. Note that if the button has only a label set and GLXC.TOOLBAR_ICONS is used, the label
# will be visible, and vice versa.

# Buttons display only icons in the toolbar.
GLXC.TOOLBAR_ICONS = 'ICONS'

# Buttons display only text labels in the toolbar.
GLXC.TOOLBAR_TEXT = 'TEXT'

# Buttons display text and icons in the toolbar.
GLXC.TOOLBAR_BOTH = 'BOTH'

# Buttons display icons and text alongside each other, rather than vertically stacked
GLXC.TOOLBAR_BOTH_HORIZ = 'BOTH_HORIZ'

# Set the Final list
GLXC.ToolbarStyle = [
    GLXC.TOOLBAR_ICONS,
    GLXC.TOOLBAR_TEXT,
    GLXC.TOOLBAR_BOTH,
    GLXC.TOOLBAR_BOTH_HORIZ
]

############
# SortType #
############
# Determines the direction of a sort.
# Sorting is in ascending order.
GLXC.SORT_ASCENDING = 'ASCENDING'

# Sorting is in descending order.
GLXC.SORT_DESCENDING = 'DESCENDING'

# Set the final list
GLXC.SortType = [
    GLXC.SORT_ASCENDING,
    GLXC.SORT_DESCENDING
]

###########################
# ResizeMode Constants    #
###########################
# Pass resize request to the parent.
GLXC.RESIZE_PARENT = 'PARENT'
# Queue resize on this widget.
GLXC.RESIZE_QUEUE = 'QUEUE'
# Resize immediately.
GLXC.RESIZE_IMMEDIATE = 'IMMEDIATE'

# Set the final list
GLXC.ResizeMode = [
    GLXC.RESIZE_PARENT,
    GLXC.RESIZE_QUEUE,
    GLXC.RESIZE_IMMEDIATE
]

#####################################
# ProgressBar Orientation Constants #
#####################################
# The ProgressBar Orientation constants specify the orientation and growth direction for a visible progress bar.
# A horizontal progress bar growing from left to right.
GLXC.PROGRESS_LEFT_TO_RIGHT = 'PROGRESS_LEFT_TO_RIGHT'
# A horizontal progress bar growing from right to left.
GLXC.PROGRESS_RIGHT_TO_LEFT = 'PROGRESS_RIGHT_TO_LEFT'
# A vertical progress bar growing from bottom to top.
GLXC.PROGRESS_BOTTOM_TO_TOP = 'PROGRESS_BOTTOM_TO_TOP'
# A vertical progress bar growing from top to bottom.
GLXC.PROGRESS_TOP_TO_BOTTOM = 'PROGRESS_TOP_TO_BOTTOM'

############################
# SizeGroup Mode Constants #
############################
# The SizeGroup Mode constants specify the directions in which the size group affects
# the requested sizes of its component widgets.
# The group has no affect
GLXC.SIZE_GROUP_NONE = 'SIZE_GROUP_NONE'
# The group affects horizontal requisition
GLXC.SIZE_GROUP_HORIZONTAL = 'SIZE_GROUP_HORIZONTAL'
# The group affects vertical requisition
GLXC.SIZE_GROUP_VERTICAL = 'SIZE_GROUP_VERTICAL'
# The group affects both horizontal and vertical requisition
GLXC.SIZE_GROUP_BOTH = 'SIZE_GROUP_BOTH'

#############
# Wrap Mode #
#############
# wrap lines at word boundaries.
GLXC.WRAP_WORD = 'WORD'
# wrap lines at character boundaries.
GLXC.WRAP_CHAR = 'CHAR'
# wrap lines at word boundaries, but fall back to character boundaries if there is not enough space for a full word.
GLXC.WRAP_WORD_CHAR = 'WORD_CHAR'
# NONE
GLXC.WRAP_NONE = 'NONE'

GLXC.WrapMode = [
    GLXC.WRAP_WORD,
    GLXC.WRAP_CHAR,
    GLXC.WRAP_WORD_CHAR,
    GLXC.WRAP_NONE
]
################
# InputPurpose #
################
# Describes primary purpose of the input widget.
# This information is useful for on-stdscr keyboards and similar input methods
# to decide which keys should be presented to the user.

# Allow any character
GLXC.INPUT_PURPOSE_FREE_FORM = 'FREE_FORM'

# Allow only alphabetic characters
GLXC.INPUT_PURPOSE_ALPHA = 'ALPHA'

# Allow only digits
GLXC.INPUT_PURPOSE_DIGITS = 'DIGITS'

# Edited field expects numbers
GLXC.INPUT_PURPOSE_NUMBER = 'NUMBER'

# Edited field expects phone number
GLXC.INPUT_PURPOSE_PHONE = 'PHONE'

# Edited field expects URL
GLXC.INPUT_PURPOSE_URL = 'URL'

# Edited field expects email address
GLXC.INPUT_PURPOSE_EMAIL = 'EMAIL'

# Edited field expects the name of a person
GLXC.INPUT_PURPOSE_NAME = 'NAME'

# Like INPUT_PURPOSE_FREE_FORM , but characters are hidden
GLXC.INPUT_PURPOSE_PASSWORD = 'PASSWORD'

# Like INPUT_PURPOSE_DIGITS , but characters are hidden
GLXC.INPUT_PURPOSE_PIN = 'PIN'

GLXC.InputPurpose = [
    GLXC.INPUT_PURPOSE_FREE_FORM,
    GLXC.INPUT_PURPOSE_ALPHA,
    GLXC.INPUT_PURPOSE_DIGITS,
    GLXC.INPUT_PURPOSE_NUMBER,
    GLXC.INPUT_PURPOSE_PHONE,
    GLXC.INPUT_PURPOSE_URL,
    GLXC.INPUT_PURPOSE_EMAIL,
    GLXC.INPUT_PURPOSE_NAME,
    GLXC.INPUT_PURPOSE_PASSWORD,
    GLXC.INPUT_PURPOSE_PIN
]

##############
# InputHints #
##############
# Describes hints that might be taken into account by input methods or applications.
# Note that input methods may already tailor their behaviour according to the InputPurpose of the entry.

# Some common sense is expected when using these flags -
# mixing GLXC.INPUT_HINTS_LOWERCASE with any of the uppercase hints makes no sense.

# This enumeration may be extended in the future; input methods should ignore unknown values.

# EMOJI - Suggest offering Emoji support.
GLXC.INPUT_HINTS_EMOJI = 'EMOJI'

# INHIBIT_OSK - Suggest to not show an onscreen keyboard (e.
GLXC.INPUT_HINTS_INHIBIT_OSK = 'INHIBIT_OSK'

# LOWERCASE - Suggest to convert all text to lowercase
GLXC.INPUT_HINTS_LOWERCASE = 'LOWERCASE'

# NONE - No special behaviour suggested
GLXC.INPUT_HINTS_NONE = 'NONE'

# NO_EMOJI - Suggest not offering Emoji support.
GLXC.INPUT_HINTS_NO_EMOJI = 'NO_EMOJI'

# NO_SPELLCHECK - Suggest not checking for typos
GLXC.INPUT_HINTS_NO_SPELLCHECK = 'NO_SPELLCHECK'

# SPELLCHECK - Suggest checking for typos
GLXC.INPUT_HINTS_SPELLCHECK = 'SPELLCHECK'

# UPPERCASE_CHARS - Suggest to capitalize all text
GLXC.INPUT_HINTS_UPPERCASE_CHARS = 'UPPERCASE_CHARS'

# UPPERCASE_SENTENCES - Suggest to capitalize the first word of each sentence
GLXC.INPUT_HINTS_UPPERCASE_SENTENCES = 'UPPERCASE_SENTENCES'

# UPPERCASE_WORDS - Suggest to capitalize the first character of each word
GLXC.INPUT_HINTS_UPPERCASE_WORDS = 'UPPERCASE_WORDS'

# VERTICAL_WRITING - The text is vertical.
GLXC.INPUT_HINTS_VERTICAL_WRITING = 'VERTICAL_WRITING'

# WORD_COMPLETION - Suggest word completion
GLXC.INPUT_HINTS_WORD_COMPLETION = 'WORD_COMPLETION'

GLXC.InputHints = [
    GLXC.INPUT_HINTS_EMOJI,
    GLXC.INPUT_HINTS_INHIBIT_OSK,
    GLXC.INPUT_HINTS_LOWERCASE,
    GLXC.INPUT_HINTS_NONE,
    GLXC.INPUT_HINTS_NO_EMOJI,
    GLXC.INPUT_HINTS_NO_SPELLCHECK,
    GLXC.INPUT_HINTS_SPELLCHECK,
    GLXC.INPUT_HINTS_UPPERCASE_CHARS,
    GLXC.INPUT_HINTS_UPPERCASE_SENTENCES,
    GLXC.INPUT_HINTS_UPPERCASE_WORDS,
    GLXC.INPUT_HINTS_VERTICAL_WRITING,
    GLXC.INPUT_HINTS_WORD_COMPLETION
]
################
# Border Style #
################
#    **GLXC.BorderStyle**
#
#    Describes how the border of a UI element should be rendered.
#
#    **Members:**
#       GLXC.BORDER_STYLE_NONE      No visible border
#       GLXC.BORDER_STYLE_SOLID     A single line segment
#       GLXC.BORDER_STYLE_INSET     Looks as if the content is sunken into the canvas
#       GLXC.BORDER_STYLE_OUTSET    Looks as if the content is coming out of the canvas
#       GLXC.BORDER_STYLE_HIDDEN    Same as glxc.BORDER_STYLE_NONE
#       GLXC.BORDER_STYLE_DOTTED    A series of round dots
#       GLXC.BORDER_STYLE_DASHED    A series of square-ended dashes
#       GLXC.BORDER_STYLE_DOUBLE    Two parallel lines with some space between them
#       GLXC.BORDER_STYLE_GROOVE    Looks as if it were carved in the canvas
#       GLXC.BORDER_STYLE_RIDGE     Looks as if it were coming out of the canvas
# No visible border
GLXC.BORDER_STYLE_NONE = 'BORDER_STYLE_NONE'

# A single line segment
GLXC.BORDER_STYLE_SOLID = 'BORDER_STYLE_SOLID'

# Looks as if the content is sunken into the canvas
GLXC.BORDER_STYLE_INSET = 'BORDER_STYLE_INSET'

# Looks as if the content is coming out of the canvas
GLXC.BORDER_STYLE_OUTSET = 'BORDER_STYLE_OUTSET'

# Same as BORDER_STYLE_NONE
GLXC.BORDER_STYLE_HIDDEN = 'BORDER_STYLE_HIDDEN'

# A series of round dots
GLXC.BORDER_STYLE_DOTTED = 'BORDER_STYLE_DOTTED'

# A series of square-ended dashes
GLXC.BORDER_STYLE_DASHED = 'BORDER_STYLE_DASHED'

# Two parallel lines with some space between them
GLXC.BORDER_STYLE_DOUBLE = 'BORDER_STYLE_DOUBLE'

# Looks as if it were carved in the canvas
GLXC.BORDER_STYLE_GROOVE = 'BORDER_STYLE_GROOVE'

# Looks as if it were coming out of the canvas
GLXC.BORDER_STYLE_RIDGE = 'BORDER_STYLE_RIDGE'

GLXC.BorderStyle = [
    'BORDER_STYLE_NONE',
    'BORDER_STYLE_SOLID',
    'BORDER_STYLE_INSET',
    'BORDER_STYLE_OUTSET',
    'BORDER_STYLE_HIDDEN',
    'BORDER_STYLE_DOTTED',
    'BORDER_STYLE_DASHED',
    'BORDER_STYLE_DOUBLE',
    'BORDER_STYLE_GROOVE',
    'BORDER_STYLE_RIDGE'
]

###################
# SensitivityType #
###################
# Determines how Galxie Curses handles the sensitivity of stepper arrows at the end of range widgets.

# The arrow is made insensitive if the thumb is at the end
GLXC.SENSITIVITY_AUTO = 'AUTO'

# The arrow is always sensitive
GLXC.SENSITIVITY_ON = 'ON'

# The arrow is always insensitive
GLXC.SENSITIVITY_OFF = 'OFF'

# Create the Final List
GLXC.SensitivityType = [
    GLXC.SENSITIVITY_AUTO,
    GLXC.SENSITIVITY_ON,
    GLXC.SENSITIVITY_OFF
]

# Container it use children list and not single child list
GLXC.CHILDREN_CONTAINER = [
    'VBox',
    'HBox',
    'Box',
    'Menu',
    'MenuBar'
]

# Container it use children list and not single child list
GLXC.CHILD_CONTAINER = [
    'Bin',
    'Frame',
    'Window',
    'Application'
]

# Widget it is Actionable
GLXC.Actionable = [
    'Button',
    'CheckButton',
    'CheckMenuItem',
    'ColorButton',
    'FontButton',
    'ImageMenuItem',
    'LinkButton',
    'ListBoxRow',
    'LockButton',
    'MenuButton',
    'MenuItem',
    'MenuToolButton',
    'ModelButton',
    'RadioButton',
    'RadioMenuItem',
    'RadioToolButton',
    'ScaleButton',
    'SeparatorMenuItem',
    'Switch',
    'TearoffMenuItem',
    'ToggleButton',
    'ToggleToolButton',
    'ToolButton',
    'VolumeButton'
]

# Widget it is Editable
GLXC.Editable = [
    'Entry',
    'SearchEntry',
    'SpinButton'
]

# Widget it is Editable
GLXC.Buildable = [
    'AboutDialog',
    'AccelLabel',
    'Action',
    'ActionBar',
    'ActionGroup',
    'Alignment',
    'AppChooserButton',
    'AppChooserDialog',
    'AppChooserWidget',
    'ApplicationWindow',
    'Arrow',
    'AspectFrame',
    'Assistant',
    'Bin',
    'Box',
    'Button',
    'ButtonBox',
    'Calendar',
    'CellArea',
    'CellAreaBox',
    'CellView',
    'CheckButton',
    'CheckMenuItem',
    'ColorButton',
    'ColorChooserDialog',
    'ColorChooserWidget',
    'ColorSelection',
    'ColorSelectionDialog',
    'ComboBox',
    'ComboBoxText',
    'Container',
    'Dialog',
    'DrawingArea',
    'Entry',
    'EntryCompletion',
    'EventBox',
    'Expander',
    'FileChooserButton',
    'FileChooserDialog',
    'FileChooserWidget',
    'FileFilter',
    'Fixed',
    'FlowBox',
    'FlowBoxChild',
    'FontButton',
    'FontChooserDialog',
    'FontChooserWidget',
    'FontSelection',
    'FontSelectionDialog',
    'Frame',
    'GLArea',
    'Grid',
    'HBox',
    'HButtonBox',
    'HPaned',
    'HSV',
    'HScale',
    'HScrollbar',
    'HSeparator',
    'HandleBox',
    'HeaderBar',
    'IconFactory',
    'IconView',
    'Image',
    'ImageMenuItem',
    'InfoBar',
    'Invisible',
    'Label',
    'Layout',
    'LevelBar',
    'LinkButton',
    'ListBox',
    'ListBoxRow',
    'ListStore',
    'LockButton',
    'Menu',
    'MenuBar',
    'MenuButton',
    'MenuItem',
    'MenuShell',
    'MenuToolButton',
    'MessageDialog',
    'Misc',
    'ModelButton',
    'Notebook',
    'OffscreenWindow',
    'Overlay',
    'PageSetupUnixDialog',
    'Paned',
    'PlacesSidebar',
    'Plug',
    'Popover',
    'PopoverMenu',
    'PrintUnixDialog',
    'ProgressBar',
    'RadioAction',
    'RadioButton',
    'RadioMenuItem',
    'RadioToolButton',
    'Range',
    'RecentAction',
    'RecentChooserDialog',
    'RecentChooserMenu',
    'RecentChooserWidget',
    'RecentFilter',
    'Revealer',
    'Scale',
    'ScaleButton',
    'Scrollbar',
    'ScrolledWindow',
    'SearchBar',
    'SearchEntry',
    'Separator',
    'SeparatorMenuItem',
    'SeparatorToolItem',
    'ShortcutsGroup',
    'ShortcutsSection',
    'ShortcutsShortcut',
    'ShortcutsWindow',
    'SizeGroup',
    'Socket',
    'SpinButton',
    'Spinner',
    'Stack',
    'StackSidebar',
    'StackSwitcher',
    'Statusbar',
    'Switch',
    'Table',
    'TearoffMenuItem',
    'TextTagTable',
    'TextView',
    'ToggleAction',
    'ToggleButton',
    'ToggleToolButton',
    'ToolButton',
    'ToolItem',
    'ToolItemGroup',
    'ToolPalette',
    'Toolbar',
    'TreeStore',
    'TreeView',
    'TreeViewColumn',
    'UIManager',
    'VBox',
    'VButtonBox',
    'VPaned',
    'VScale',
    'VScrollbar',
    'VSeparator',
    'Viewport',
    'VolumeButton',
    'Widget',
    'Window'
]

#########################
# ctype-style character #
#########################

# whitespace -- a string containing all ASCII whitespace
whitespace = ' \t\n\r\v\f'

# ascii_lowercase -- a string containing all ASCII lowercase letters
ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'

# ascii_uppercase -- a string containing all ASCII uppercase letters
ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# ascii_letters -- a string containing all ASCII letters
ascii_letters = ascii_lowercase + ascii_uppercase

# digits -- a string containing all ASCII decimal digits
digits = '0123456789'

# hexdigits -- a string containing all ASCII hexadecimal digits
hexdigits = digits + 'abcdef' + 'ABCDEF'

# octdigits -- a string containing all ASCII octal digits
octdigits = '01234567'

# punctuation -- a string containing all ASCII punctuation characters
punctuation = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"

# accent
accent = "éèàùô"

# printable -- a string containing all ASCII characters considered printable
# printable = digits + ascii_letters + accent + punctuation + whitespace
printable = digits + ascii_letters + punctuation + whitespace + accent
GLXC.Printable = printable

# ASCII KEYS
GLXC.KEY_NUL = 0x00  # ^@
GLXC.KEY_SOH = 0x01  # ^A
GLXC.KEY_STX = 0x02  # ^B
GLXC.KEY_ETX = 0x03  # ^C
GLXC.KEY_EOT = 0x04  # ^D
GLXC.KEY_ENQ = 0x05  # ^E
GLXC.KEY_ACK = 0x06  # ^F
GLXC.KEY_BEL = 0x07  # ^G
GLXC.KEY_BS = 0x08  # ^H
GLXC.KEY_TAB = 0x09  # ^I
GLXC.KEY_HT = 0x09  # ^I
GLXC.KEY_LF = 0x0a  # ^J enter
GLXC.KEY_NL = 0x0a  # ^J
GLXC.KEY_VT = 0x0b  # ^K
GLXC.KEY_FF = 0x0c  # ^L
GLXC.KEY_CR = 0x0d  # ^M
GLXC.KEY_SO = 0x0e  # ^N
GLXC.KEY_SI = 0x0f  # ^O
GLXC.KEY_DLE = 0x10  # ^P
GLXC.KEY_DC1 = 0x11  # ^Q
GLXC.KEY_DC2 = 0x12  # ^R
GLXC.KEY_DC3 = 0x13  # ^S
GLXC.KEY_DC4 = 0x14  # ^T
GLXC.KEY_NAK = 0x15  # ^U
GLXC.KEY_SYN = 0x16  # ^V
GLXC.KEY_ETB = 0x17  # ^W
GLXC.KEY_CAN = 0x18  # ^X
GLXC.KEY_EM = 0x19  # ^Y
GLXC.KEY_SUB = 0x1a  # ^Z
GLXC.KEY_ESC = 0x1b  # ^[ escape
GLXC.KEY_FS = 0x1c  # ^\
GLXC.KEY_GS = 0x1d  # ^]
GLXC.KEY_RS = 0x1e  # ^^
GLXC.KEY_US = 0x1f  # ^_
GLXC.KEY_SP = 0x20  # space
GLXC.KEY_DEL = 0x7f  # delete

GLXC.ALL_MOUSE_EVENTS = 134217727

GLXC.A_ALTCHARSET = 4194304
GLXC.A_ATTRIBUTES = -256
GLXC.A_BLINK = 524288
GLXC.A_BOLD = 2097152
GLXC.A_CHARTEXT = 255
GLXC.A_COLOR = 65280
GLXC.A_DIM = 1048576
GLXC.A_HORIZONTAL = 33554432
GLXC.A_INVIS = 8388608
GLXC.A_LEFT = 67108864
GLXC.A_LOW = 134217728
GLXC.A_NORMAL = 0
GLXC.A_PROTECT = 16777216
GLXC.A_REVERSE = 262144
GLXC.A_RIGHT = 268435456
GLXC.A_STANDOUT = 65536
GLXC.A_TOP = 536870912
GLXC.A_UNDERLINE = 131072
GLXC.A_VERTICAL = 1073741824

GLXC.BUTTON1_CLICKED = 4
GLXC.BUTTON1_DOUBLE_CLICKED = 8
GLXC.BUTTON1_PRESSED = 2
GLXC.BUTTON1_RELEASED = 1
GLXC.BUTTON1_TRIPLE_CLICKED = 16

GLXC.BUTTON2_CLICKED = 256
GLXC.BUTTON2_DOUBLE_CLICKED = 512
GLXC.BUTTON2_PRESSED = 128
GLXC.BUTTON2_RELEASED = 64
GLXC.BUTTON2_TRIPLE_CLICKED = 1024

GLXC.BUTTON3_CLICKED = 16384
GLXC.BUTTON3_DOUBLE_CLICKED = 32768
GLXC.BUTTON3_PRESSED = 8192
GLXC.BUTTON3_RELEASED = 4096
GLXC.BUTTON3_TRIPLE_CLICKED = 65536

GLXC.BUTTON4_CLICKED = 1048576
GLXC.BUTTON4_DOUBLE_CLICKED = 2097152
GLXC.BUTTON4_PRESSED = 524288
GLXC.BUTTON4_RELEASED = 262144
GLXC.BUTTON4_TRIPLE_CLICKED = 4194304

GLXC.BUTTON_ALT = 67108864
GLXC.BUTTON_CTRL = 16777216
GLXC.BUTTON_SHIFT = 33554432

GLXC.COLOR_BLACK = 0
GLXC.COLOR_RED = 1
GLXC.COLOR_GREEN = 2
GLXC.COLOR_YELLOW = 3
GLXC.COLOR_BLUE = 4
GLXC.COLOR_MAGENTA = 5
GLXC.COLOR_CYAN = 6
GLXC.COLOR_WHITE = 7

GLXC.ERR = -1

# GLXC.KEY_A1 = 348
# GLXC.KEY_A3 = 349
# GLXC.KEY_B2 = 350
# GLXC.KEY_BACKSPACE = 263
# GLXC.KEY_BEG = 354
# GLXC.KEY_BREAK = 257
# GLXC.KEY_BTAB = 353
# GLXC.KEY_C1 = 351
# GLXC.KEY_C3 = 352
# GLXC.KEY_CANCEL = 355
# GLXC.KEY_CATAB = 342
# GLXC.KEY_CLEAR = 333
# GLXC.KEY_CLOSE = 356
# GLXC.KEY_COMMAND = 357
# GLXC.KEY_COPY = 358
# GLXC.KEY_CREATE = 359
# GLXC.KEY_CTAB = 341
# GLXC.KEY_DC = 330
# GLXC.KEY_DL = 328
# GLXC.KEY_DOWN = 258
# GLXC.KEY_EIC = 332
# GLXC.KEY_END = 360
# GLXC.KEY_ENTER = 343
# GLXC.KEY_EOL = 335
# GLXC.KEY_EOS = 334
# GLXC.KEY_EXIT = 361
GLXC.KEY_F0 = 264
GLXC.KEY_F1 = 265
GLXC.KEY_F10 = 274
GLXC.KEY_F11 = 275
GLXC.KEY_F12 = 276
GLXC.KEY_F13 = 277
GLXC.KEY_F14 = 278
GLXC.KEY_F15 = 279
GLXC.KEY_F16 = 280
GLXC.KEY_F17 = 281
GLXC.KEY_F18 = 282
GLXC.KEY_F19 = 283
GLXC.KEY_F2 = 266
GLXC.KEY_F20 = 284
GLXC.KEY_F21 = 285
GLXC.KEY_F22 = 286
GLXC.KEY_F23 = 287
GLXC.KEY_F24 = 288
GLXC.KEY_F25 = 289
GLXC.KEY_F26 = 290
GLXC.KEY_F27 = 291
GLXC.KEY_F28 = 292
GLXC.KEY_F29 = 293
GLXC.KEY_F3 = 267
GLXC.KEY_F30 = 294
GLXC.KEY_F31 = 295
GLXC.KEY_F32 = 296
GLXC.KEY_F33 = 297
GLXC.KEY_F34 = 298
GLXC.KEY_F35 = 299
GLXC.KEY_F36 = 300
GLXC.KEY_F37 = 301
GLXC.KEY_F38 = 302
GLXC.KEY_F39 = 303
GLXC.KEY_F4 = 268
GLXC.KEY_F40 = 304
GLXC.KEY_F41 = 305
GLXC.KEY_F42 = 306
GLXC.KEY_F43 = 307
GLXC.KEY_F44 = 308
GLXC.KEY_F45 = 309
GLXC.KEY_F46 = 310
GLXC.KEY_F47 = 311
GLXC.KEY_F48 = 312
GLXC.KEY_F49 = 313
GLXC.KEY_F5 = 269
GLXC.KEY_F50 = 314
GLXC.KEY_F51 = 315
GLXC.KEY_F52 = 316
GLXC.KEY_F53 = 317
GLXC.KEY_F54 = 318
GLXC.KEY_F55 = 319
GLXC.KEY_F56 = 320
GLXC.KEY_F57 = 321
GLXC.KEY_F58 = 322
GLXC.KEY_F59 = 323
GLXC.KEY_F6 = 270
GLXC.KEY_F60 = 324
GLXC.KEY_F61 = 325
GLXC.KEY_F62 = 326
GLXC.KEY_F63 = 327
GLXC.KEY_F7 = 271
GLXC.KEY_F8 = 272
GLXC.KEY_F9 = 273
# GLXC.KEY_FIND = 362
# GLXC.KEY_HELP = 363
# GLXC.KEY_HOME = 262
# GLXC.KEY_IC = 331
# GLXC.KEY_IL = 329
# GLXC.KEY_LEFT = 260
# GLXC.KEY_LL = 347
# GLXC.KEY_MARK = 364
# GLXC.KEY_MAX = 511
# GLXC.KEY_MESSAGE = 365
# GLXC.KEY_MIN = 257
# GLXC.KEY_MOUSE = 409
# GLXC.KEY_MOVE = 366
# GLXC.KEY_NEXT = 367
# GLXC.KEY_NPAGE = 338
# GLXC.KEY_OPEN = 368
# GLXC.KEY_OPTIONS = 369
# GLXC.KEY_PPAGE = 339
# GLXC.KEY_PREVIOUS = 370
# GLXC.KEY_PRINT = 346
# GLXC.KEY_REDO = 371
# GLXC.KEY_REFERENCE = 372
# GLXC.KEY_REFRESH = 373
# GLXC.KEY_REPLACE = 374
# GLXC.KEY_RESET = 345
# GLXC.KEY_RESIZE = 410
# GLXC.KEY_RESTART = 375
# GLXC.KEY_RESUME = 376
# GLXC.KEY_RIGHT = 261
# GLXC.KEY_SAVE = 377
# GLXC.KEY_SBEG = 378
# GLXC.KEY_SCANCEL = 379
# GLXC.KEY_SCOMMAND = 380
# GLXC.KEY_SCOPY = 381
# GLXC.KEY_SCREATE = 382
# GLXC.KEY_SDC = 383
# GLXC.KEY_SDL = 384
# GLXC.KEY_SELECT = 385
# GLXC.KEY_SEND = 386
# GLXC.KEY_SEOL = 387
# GLXC.KEY_SEXIT = 388
# GLXC.KEY_SF = 336
# GLXC.KEY_SFIND = 389
# GLXC.KEY_SHELP = 390
# GLXC.KEY_SHOME = 391
# GLXC.KEY_SIC = 392
# GLXC.KEY_SLEFT = 393
# GLXC.KEY_SMESSAGE = 394
# GLXC.KEY_SMOVE = 395
# GLXC.KEY_SNEXT = 396
# GLXC.KEY_SOPTIONS = 397
# GLXC.KEY_SPREVIOUS = 398
# GLXC.KEY_SPRINT = 399
# GLXC.KEY_SR = 337
# GLXC.KEY_SREDO = 400
# GLXC.KEY_SREPLACE = 401
# GLXC.KEY_SRESET = 344
# GLXC.KEY_SRIGHT = 402
# GLXC.KEY_SRSUME = 403
# GLXC.KEY_SSAVE = 404
# GLXC.KEY_SSUSPEND = 405
# GLXC.KEY_STAB = 340
# GLXC.KEY_SUNDO = 406
# GLXC.KEY_SUSPEND = 407
# GLXC.KEY_UNDO = 408
# GLXC.KEY_UP = 259
#
# GLXC.OK = 0
#
# GLXC.REPORT_MOUSE_POSITION = 134217728

# Atoms
GLXC.SELECTION_PRIMARY = "PRIMARY"
GLXC.SELECTION_SECONDARY = "SECONDARY"
GLXC.SELECTION_CLIPBOARD = "CLIPBOARD"
GLXC.SELECTION_TYPE_ATOM = "ATOM"
GLXC.SELECTION_TYPE_BITMAP = "BITMAP"
GLXC.SELECTION_TYPE_COLORMAP = "COLORMAP"
GLXC.SELECTION_TYPE_DRAWABLE = "DRAWABLE"
GLXC.SELECTION_TYPE_PIXMAP = "PIXMAP"
GLXC.SELECTION_TYPE_STRING = "STRING"
GLXC.SELECTION_TYPE_WINDOW = "WINDOW"
GLXC.TARGET_BITMAP = "BITMAP"
GLXC.TARGET_COLORMAP = "COLORMAP"
GLXC.TARGET_DRAWABLE = "DRAWABLE"
GLXC.TARGET_PIXMAP = "PIXMAP"
GLXC.TARGET_STRING = "STRING"

GLXC.Atom = [
    GLXC.SELECTION_PRIMARY,
    GLXC.SELECTION_SECONDARY,
    GLXC.SELECTION_CLIPBOARD,
    GLXC.SELECTION_TYPE_ATOM,
    GLXC.TARGET_BITMAP,
    GLXC.SELECTION_TYPE_BITMAP,
    GLXC.TARGET_COLORMAP,
    GLXC.SELECTION_TYPE_COLORMAP,
    GLXC.TARGET_DRAWABLE,
    GLXC.SELECTION_TYPE_DRAWABLE,
    GLXC.TARGET_PIXMAP,
    GLXC.SELECTION_TYPE_PIXMAP,
    GLXC.TARGET_STRING,
    GLXC.SELECTION_TYPE_STRING,
    GLXC.SELECTION_TYPE_WINDOW
]

# GLX.TYPE
# Atoms
GLXC.TYPE_BIN = "BIN"
GLXC.TYPE_BUTTON = "BUTTON"
GLXC.TYPE_CHECKBUTTON = "CHECKBUTTON"
GLXC.TYPE_CONTAINER = "CONTAINER"
GLXC.TYPE_ENTRY = "ENTRY"
GLXC.TYPE_HSEPARATOR = "HSEPARATOR"
GLXC.TYPE_MENUBAR = "MENUBAR"
GLXC.TYPE_MESSAGEBAR = "MESSAGEBAR"
GLXC.TYPE_MISC = "MISC"
GLXC.TYPE_PROGRESSBAR = "PROGRESSBAR"
GLXC.TYPE_RADIOBUTTON = "RADIOBUTTON"
GLXC.TYPE_RANGE = "RANGE"
GLXC.TYPE_STATUSBAR = "STATUSBAR"
GLXC.TYPE_TOOLBAR = "TOOLBAR"
GLXC.TYPE_VSEPARATOR = "VSEPARATOR"
GLXC.TYPE_WIDGET = "WIDGET"

GLXC.Type = [
    GLXC.TYPE_BIN,
    GLXC.TYPE_BUTTON,
    GLXC.TYPE_CHECKBUTTON,
    GLXC.TYPE_CONTAINER,
    GLXC.TYPE_ENTRY,
    GLXC.TYPE_HSEPARATOR,
    GLXC.TYPE_MENUBAR,
    GLXC.TYPE_MESSAGEBAR,
    GLXC.TYPE_MISC,
    GLXC.TYPE_PROGRESSBAR,
    GLXC.TYPE_RADIOBUTTON,
    GLXC.TYPE_RANGE,
    GLXC.TYPE_STATUSBAR,
    GLXC.TYPE_TOOLBAR,
    GLXC.TYPE_VSEPARATOR,
    GLXC.TYPE_WIDGET
]
