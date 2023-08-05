#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import random
import re
import os
import io
import math
import time
import curses
import logging
from array import array

import GLXCurses
from GLXCurses.Constants import GLXC
from datetime import date


# json
def serialize(obj):
    if isinstance(obj, date):
        serial = obj.isoformat()
        return serial

    return obj.__dict__


def glxc_type(thing_to_test=None):
    """
    Internal method for check if object pass as argument is GLXCurses Type Object

    :param thing_to_test = A object to test
    :type thing_to_test: object
    :return: True or False
    :rtype: bool
    """
    if hasattr(thing_to_test, 'glxc_type') and (thing_to_test.glxc_type == str(
            'GLXCurses.' + thing_to_test.__class__.__name__)):
        return True
    else:
        return False


def resize_text_wrap_char(text='', max_width=0):
    """
    Resize the text , and return a new text

    example: return '123' for '123456789' where max_width = 3

    :param text: the original text to resize
    :type text: str
    :param max_width: the size of the text
    :type max_width: int
    :return: a resize text
    :rtype: str
    """
    # Try to quit as soon of possible
    if type(text) != str:
        raise TypeError('"text" must be a str type')
    if type(max_width) != int:
        raise TypeError('"max_width" must be a int type')

    # just if it have something to resize
    if max_width < len(text):
        return text[:max_width]
    else:
        return text


def sizeof(value=None):
    """
    Convert a num to a human readable thing it use metric prefix.

    Metric prefixes in everyday use:
        yotta	Y	1000000000000000000000000	10 power 24
        zetta	Z	1000000000000000000000	10 power 21
        exa	    E	1000000000000000000	10 power 18
        peta	P	1000000000000000	10 power 15
        tera	T	1000000000000	10 power 12
        giga	G	1000000000	10 power 9
        mega	M	1000000	10 power 6
        kilo	k	1000	10 power 3
        (none)	(none)	1	10 power 0

    :param value: a value to translate for a future display
    :type value: int or float
    :return: str
    :raise TypeError: when "value" argument is not a :py:__area_data:`int` or :py:__area_data:`float`
    """
    # Exit a soon of possible
    if type(value) != int and type(value) != float and type(value) != int:
        raise TypeError("'value' must be a int or float type")

    suffix = ['', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']
    i = 0 if value < 1 else int(math.log(value, 1024)) + 1
    v = value / math.pow(1024, i)
    v, i = (v, i) if v > 0.5 else (v * 1024, (i - 1 if i else 0))

    return str(str(int(round(v, 0))) + suffix[i])


#     """
#     For split a area homogeneously a area, it use by HBox and VBox for create children area
#
#     Console:
#      get_split_area_positions(start=0, stop=99, num=3)
#      {'0': (0.0, 32.0), '1': (33.0, 65.0), '2': (66.0, 99)}
#
#     :param start: The starting value of the sequence.
#     :type start: int
#     :param stop: The end value of the sequence
#     :type stop: int
#     :param num: Number of samples to generate.
#     :type num: int
#     :param roundtype: GLXC.RoundType
#     :type roundtype: str
#     :return: a dictionary with position
#     :rtype : dict
#     :raise TypeError: when ``start`` argument is not a :py:data:`int`
#     :raise TypeError: when ``stop`` argument is not a :py:data:`int`
#     :raise TypeError: when ``num`` argument is not a :py:data:`int`
#     :raise TypeError: when ``roundtype`` argument is not in GLXC.RoundType :py:data:`list`
#     """
# def get_split_area_positions(start=0, stop=0, num=0, roundtype=GLXC.ROUND_UP):
#     # Exit a soon of possible
#     if type(start) != int:
#         raise TypeError("'start' must be a int type")
#
#     if type(stop) != int:
#         raise TypeError("'stop' must be a int type")
#
#     if type(num) != int:
#         raise TypeError("'num' must be a int type")
#
#     if roundtype not in GLXC.RoundType:
#         raise TypeError("'roundtype' must be in GLXC.RoundType list")
#
#     # We make the job
#     position_list = numpy.linspace(start, stop, num + 1)
#     thing_to_return = dict()
#     count = 0
#     for i in range(num):
#         if count + 1 >= num:
#             item_start = position_list[int(count)]
#             item_stop = stop
#         else:
#             item_start = position_list[int(count)]
#             item_stop = position_list[int(count + 1)] - 1
#
#         # We have to round the Value because that is that it balance the fact our first
#         # and last element have min and max position.
#         # That is clearly require for human smooth thing
#         if roundtype == GLXC.ROUND_UP:
#             item_start = int(round_up(item_start, decimals=0))
#             item_stop = int(round_up(item_stop, decimals=0))
#
#         elif roundtype == GLXC.ROUND_DOWN:
#             item_start = int(round_down(item_start, decimals=0))
#             item_stop = int(round_down(item_stop, decimals=0))
#
#         elif roundtype == GLXC.ROUND_HALF_UP:
#             item_start = int(round_half_up(item_start, decimals=0))
#             item_stop = int(round_half_up(item_stop, decimals=0))
#
#         elif roundtype == GLXC.ROUND_HALF_DOWN:
#             item_start = int(round_half_down(item_start, decimals=0))
#             item_stop = int(round_half_down(item_stop, decimals=0))
#
#         thing_to_return[str(count)] = (item_start, item_stop)
#         count += 1
#
#     # Return something
#     return thing_to_return
#

def disk_usage(path):
    """
    Return something like: 94G/458G (20%).

    It use teh File system it self and just request it about the drive space where is store teh file pass in argument.

    :param path:
    :type:
    :return: something like 94G/458G (20%) with '.' as ``path`` argument
    """
    st = os.statvfs(path)
    total = (st.f_blocks * st.f_frsize)
    used = (st.f_bsize * st.f_bavail)

    try:
        percent = (float(used) / total) * 100
    except ZeroDivisionError:
        percent = 0
    line = str(sizeof(used) + "/" + sizeof(total) + " (" + str(int(percent)) + "%)")
    line = " " + line + " "
    return line


def round_up(n, decimals=0):
    """
    https://realpython.com/python-rounding/

    :param n:
    :param decimals:
    :return:
    """
    multiplier = 10 ** decimals
    if decimals == 0:
        return int(math.ceil(n * multiplier) / multiplier)

    return math.ceil(n * multiplier) / multiplier


def round_down(n, decimals=0):
    """
    https://realpython.com/python-rounding/

    :param n: the number
    :type n: int or float
    :param decimals: number of decimal
    :type decimals: int
    :return:
    """
    multiplier = 10 ** decimals
    if decimals == 0:
        return int(math.floor(n * multiplier) / multiplier)
    return math.floor(n * multiplier) / multiplier


def round_half_up(n, decimals=0):
    """
    https://realpython.com/python-rounding/

    :param n:
    :param decimals:
    :return:
    """

    multiplier = 10 ** decimals
    if decimals == 0:
        return int(math.floor(n * multiplier + 0.5) / multiplier)
    return math.floor(n * multiplier + 0.5) / multiplier


def round_half_down(n, decimals=0):
    """
    https://realpython.com/python-rounding/

    :param n:
    :param decimals:
    :return:
    """
    multiplier = 10 ** decimals
    if decimals == 0:
        return int(math.ceil(n * multiplier - 0.5) / multiplier)
    return math.ceil(n * multiplier - 0.5) / multiplier


def resize_text(text='', max_width=0, separator='~'):
    """
    Resize the text , and return a new text

    example: return '123~789' for '123456789' where max_width = 7 or 8

    :param text: the original text to resize
    :type text: str
    :param max_width: the size of the text
    :type max_width: int
    :param separator: a separator a in middle of the resize text
    :type separator: str
    :return: a resize text
    :rtype: str
    """
    # Try to quit as soon of possible
    if type(text) != str:
        raise TypeError('"text" must be a str type')
    if type(max_width) != int:
        raise TypeError('"max_width" must be a int type')
    if type(separator) != str:
        raise TypeError('"separator" must be a str type')

    # If we are here we haven't quit
    if max_width < len(text):
        if max_width <= 0:
            return str('')
        elif max_width == 1:
            return str(text[:1])
        elif max_width == 2:
            return str(text[:1] + text[-1:])
        elif max_width == 3:
            return str(text[:1] + separator[:1] + text[-1:])
        elif max_width == 4:
            return str(text[:2] + separator[:1] + text[-1:])
        elif max_width == 5:
            return str(text[:2] + separator[:1] + text[-2:])
        elif max_width == 6:
            return str(text[:3] + separator[:1] + text[-2:])
        elif max_width == 7:
            return str(text[:3] + separator[:1] + text[-3:])
        elif max_width == 8:
            return str(text[:4] + separator[:1] + text[-3:])
        elif max_width == 9:
            return str(text[:4] + separator[:1] + text[-4:])
        elif max_width == 10:
            return str(text[:5] + separator[:1] + text[-4:])
        elif max_width == 11:
            return str(text[:5] + separator[:1] + text[-5:])
        elif max_width == 12:
            return str(text[:6] + separator[:1] + text[-5:])
        elif max_width == 13:
            return str(text[:6] + separator[:1] + text[-6:])
        elif max_width == 14:
            return str(text[:7] + separator[:1] + text[-6:])
        elif max_width == 15:
            return str(text[:7] + separator[:1] + text[-7:])
        else:
            max_width -= len(separator[:1])
            max_div = int(max_width / 2)
            return str(text[:max_div] + separator[:1] + text[-max_div:])
    return str(text)


def clamp_to_zero(value=None):
    """
    Convert any int value to positive int

    :param value: a integer
    :type value: int or None
    :return: a integer
    :rtype: int
    """
    if type(value) != int and value is not None:
        raise TypeError('"value" must be a int type or None')
    if value is None or value <= 0:
        return 0
    return value


def clamp(value=None, smallest=None, largest=None):
    """
    Back ``value`` inside ``smallest`` and ``largest`` value range.

    :param value: The value it have to be clamped
    :param smallest: The lower value
    :param largest: The upper value
    :type value: int or float
    :type value: int or float
    :return: The clamped value it depend of parameters value type, int or float will be preserve.
    :rtype: int or float
    """
    # Try to exit as soon of possible
    if type(value) != int and type(value) != float:
        raise TypeError('>value< must be a int or float type')

    if type(smallest) != int and type(smallest) != float:
        raise TypeError('>smallest< must be a int or float type')

    if type(largest) != int and type(largest) != float:
        raise TypeError('>largest< must be a int or float type')

    # make the job
    if type(value) == int:
        if value < smallest:
            value = smallest
        elif value > largest:
            value = largest
        return int(value)
    elif type(value) == float:
        if value < smallest:
            value = smallest
        elif value > largest:
            value = largest
        return float(value)


def new_id():
    """
    Generate a GLXCurses ID like 'E59E8457', two chars by two chars it's a random HEX

    **Default size:** 8
    **Default chars:** 'ABCDEF0123456789'

    **Benchmark**
       +----------------+---------------+----------------------------------------------+
       | **Iteration**  | **Duration**  | **CPU Information**                          |
       +----------------+---------------+----------------------------------------------+
       | 10000000       | 99.114s       | Intel(R) Core(TM) i7-2860QM CPU @ 2.50GHz    |
       +----------------+---------------+----------------------------------------------+
       | 1000000        | 9.920s        | Intel(R) Core(TM) i7-2860QM CPU @ 2.50GHz    |
       +----------------+---------------+----------------------------------------------+
       | 100000         | 0.998s        | Intel(R) Core(TM) i7-2860QM CPU @ 2.50GHz    |
       +----------------+---------------+----------------------------------------------+
       | 10000          | 0.108s        | Intel(R) Core(TM) i7-2860QM CPU @ 2.50GHz    |
       +----------------+---------------+----------------------------------------------+

    :return: a string it represent a unique ID
    :rtype: str
    """
    return '%02x%02x%02x%02x'.upper() % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )


def is_valid_id(value):
    """
    Check if it's a valid id

    :param value: a id to verify
    :return: bool
    """
    allowed = re.compile(r"""
                         (
                             ^([0-9A-F]{8})$
                         )
                         """,
                         re.VERBOSE | re.IGNORECASE)
    try:
        if allowed.match(value) is None:
            return False
        else:
            return True
    except TypeError:
        return False


def merge_dicts(*dict_args):
    """
    A merge dict fully compatible Python 2 and 3

    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def get_os_temporary_dir():
    """
    Get the OS default dir , the better as it can.

    It suppose to be cross platform

    :return: A tmp dir path
    """
    text_flags = os.O_RDWR | os.O_CREAT | os.O_EXCL
    if hasattr(os, 'O_NOFOLLOW'):
        text_flags |= os.O_NOFOLLOW

    bin_flags = text_flags
    if hasattr(os, 'O_BINARY'):
        bin_flags |= os.O_BINARY

    directory_list = list()

    # First, try the environment.
    for envname in 'TMPDIR', 'TEMP', 'TMP':
        dirname = os.getenv(envname)
        if dirname:
            directory_list.append(os.path.abspath(dirname))

    # Failing that, try OS-specific locations.
    if os.name == 'nt':
        directory_list.extend([r'c:\temp', r'c:\tmp', r'\temp', r'\tmp'])
    else:
        directory_list.extend(['/tmp', '/var/tmp', '/usr/tmp'])

    for directory in directory_list:
        if directory != os.path.curdir:
            directory = os.path.abspath(directory)

        name = str('GLXCurses-')
        name += str(new_id())
        name += str('.cp')
        filename = os.path.join(directory, name)
        try:
            fd = os.open(filename, bin_flags, 0o600)
            try:
                try:
                    with io.open(fd, 'wb', closefd=False) as fp:
                        fp.write(b'Test')
                finally:
                    os.close(fd)
            finally:
                os.unlink(filename)
            return directory

        except PermissionError:
            # This exception is thrown when a directory with the chosen name
            # already exists on windows.
            if (os.name == 'nt' and os.path.isdir(directory) and
                    os.access(directory, os.W_OK)):
                return directory
            break  # no point trying more names in this directory
        except OSError:
            break  # no point trying more names in this directory
    raise FileNotFoundError("No usable temporary directory found in %s" % directory_list)


def linspace(start=None, stop=None, num=None, round_type=None):
    """
    np.linspace(3, 9, 10)
        array([ 3.,  3.66666667,  4.33333333,  5. ,  5.66666667, 6.33333333,  7. ,  7.66666667,  8.33333333,  9. ])

    :param start:
    :param stop:
    :param num:
    :param roundtype:
    :return:
    """
    if stop is None:
        raise ValueError("start property must be int value")
    if stop is None:
        raise ValueError("stop property must be int value")
    if num is None:
        raise ValueError("num property must be int value")


    position_list = array('l')
    value = start
    while value <= stop:
        position_list.append(int(value))
        if round_type == GLXCurses.GLXC.ROUND_UP:
            value += GLXCurses.round_up((stop - start) / num, decimals=0)

        elif round_type == GLXCurses.GLXC.ROUND_DOWN:
            value += GLXCurses.round_down((stop - start) / num, decimals=0)

        elif round_type == GLXCurses.GLXC.ROUND_HALF_UP:
            value += GLXCurses.round_half_up((stop - start) / num, decimals=0)

        elif round_type == GLXCurses.GLXC.ROUND_HALF_DOWN:
            value += int(GLXCurses.round_half_down((stop - start) / num, decimals=0))
        else:
            value += int((stop - start) / num)

    return position_list
