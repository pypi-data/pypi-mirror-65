#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved

import PIL
import os
import sys
import argparse
from math import sqrt


#                                      ---------------
# Convert to Perceived brightness --> |  HSP Analyse  |
#                                      ---------------
# Pixel value original sequence   --> | 1 | 3 | 2 | 0 |
#                                     |---------------|
# Pixel values converted to 2-bit --> | 01| 11| 10| 00|
# binary pairs                        |---------------|
#              1,2,3,4 -> 4,3,2,1 --> |   Magic Flip  |
#                                     |---------------|
# Re-ordered binary pairs         --> | 00| 10| 11| 01|
#                                     |---------------|
# 1-byte packed hexadecimal value --> |      2D       |
#                                      ---------------


def img_to_cip_data(image, debug_level=0):
    im = image
    data = list()
    hsp_debug = list()

    # HSP Analyse
    # Test if the image is RVB
    if im.mode == 'RGB':
        for y in range(im.size[1]):
            for x in range(0, im.size[0], 1):
                r, g, b = im.getpixel((x, y))

                # DEBUG information's collect
                if debug_level >= 3:
                    debug_infos = ''
                    debug_infos += str('X=' + str(x) + ' ' + 'Y=' + str(y))
                    debug_infos += str(', ')
                    debug_infos += str('RGB=(' + str(r) + ',' + str(g) + ',' + str(b) + ')')

                # HSP  where the P stands for Perceived brightness
                # http://alienryderflex.com/hsp.html
                # Back to double
                r /= 255.0
                g /= 255.0
                b /= 255.0
                perceived_brightness = sqrt(r * r * .299 + r * r * .587 + r * r * .114)

                # DEBUG
                if debug_level >= 3:
                    debug_infos += str(', ')
                    debug_infos += str('Perceived brightness=' + str(perceived_brightness))
                    hsp_debug.append(debug_infos)

                # Short by brightness
                if perceived_brightness < .25:
                    data.append(3)
                elif perceived_brightness < .5:
                    data.append(2)
                elif perceived_brightness < .75:
                    data.append(1)
                else:
                    data.append(0)

    # HSP Analyse
    # Test if mode is Gray
    elif im.mode == "L":
        for y in range(im.size[1]):
            for x in range(0, im.size[0], 1):
                l = im.getpixel((x, y))
                # DEBUG
                debug_infos = ''
                if debug_level >= 3:
                    debug_infos += str('X=' + str(x) + ' ' + 'Y=' + str(y))
                    debug_infos += str(', ')
                    debug_infos += str('L=(' + str(l) + ')')
                # HSP  where the P stands for Perceived brightness
                l /= 255.0
                perceived_brightness = sqrt(l * l * .299 + l * l * .587 + l * l * .114)

                # DEBUG information's collect
                if debug_level >= 3:
                    debug_infos += str(', ')
                    debug_infos += str('Perceived brightness=' + str(perceived_brightness))
                    hsp_debug.append(debug_infos)

                # Short by brightness
                if perceived_brightness < .25:
                    data.append(3)
                elif perceived_brightness < .5:
                    data.append(2)
                elif perceived_brightness < .75:
                    data.append(1)
                else:
                    data.append(0)

    # Convert to 2-bit binary pair
    two_bit_list = list()
    two_bit_conversion_debug = list()
    for i in data:

        # DEBUG information's collect
        if debug_level >= 3:
            debug_infos = ''
            debug_infos += 'Gray value=' + str(i)
            debug_infos += ', '
            debug_infos += '2-bit binary pair=' + str('{0:02b}'.format(i))
            two_bit_conversion_debug.append(debug_infos)

        # Make the job
        two_bit_list.append(str("{0:02b}".format(i)))

    # DEBUG display HSP Analyse result
    if debug_level >= 3:
        sys.stdout.write(str('Perceived brightness Analyse:'))
        sys.stdout.write(str('\n'))
        sys.stdout.flush()
        for i, (hsp_debug_line, two_bit_conversion_debug_info) in enumerate(zip(hsp_debug, two_bit_conversion_debug)):
            sys.stdout.write(str(' '))
            sys.stdout.write(str(hsp_debug_line))
            sys.stdout.write(str(': '))
            sys.stdout.write(str(two_bit_conversion_debug_info))
            sys.stdout.write(str('\n'))
            sys.stdout.flush()
        sys.stdout.write(str('\n'))
        sys.stdout.flush()

    # Re-ordered binary pairs and creat 1-byte packed hexadecimal
    hexa_conversion_debug = list()
    hex_data = list()

    for val1, val2, val3, val4 in (two_bit_list[i:i + 4] for i in range(0, int(len(two_bit_list) / 4) * 4, 4)):

        # DEBUG information's collect
        if debug_level >= 3:
            debug_infos = str('Original=' + val1 + val2 + val3 + val4)
            debug_infos += str(', ')
            debug_infos += str('Hexa=' + str('{0:0>2X}'.format(int(str(val4 + val3 + val2 + val1), 2))))
            hexa_conversion_debug.append(debug_infos)

        # Make the job
        hex_data.append(str("{0:0>2X}".format(int(str(val4 + val3 + val2 + val1), 2))))

    # DEBUG Display magic thing
    if debug_level >= 3:
        sys.stdout.write(str('Re-ordered binary pairs and convert to 1-byte packed hexadecimal value:'))
        sys.stdout.write(str('\n'))
        sys.stdout.flush()
        for i in hexa_conversion_debug:
            sys.stdout.write(str(i))
            sys.stdout.write(str('\n'))
            sys.stdout.flush()
        sys.stdout.write(str('\n'))
        sys.stdout.flush()

    # Prepare cip data string
    cip_data = ''
    for element in hex_data:
        cip_data += element

    # DEBUG Display the cip data
    if debug_level >= 3:
        sys.stdout.write(str('CIP Data:'))
        sys.stdout.write(str('\n'))
        sys.stdout.write(str(cip_data))
        sys.stdout.write(str('\n'))
        sys.stdout.flush()

    # Final Return
    return cip_data


def found_best_output_file_name(file_path='out.cip', overwrite=0, debug_level=0):
    file_ext = os.path.splitext(file_path)[1]
    file_name = os.path.basename(os.path.splitext(file_path)[0])
    working_dir = os.path.realpath(os.path.dirname(file_path))
    output_file = os.path.join(working_dir, file_name + file_ext)

    # DEBUG information's
    if debug_level >= 2:
        sys.stdout.write(str('File:'))
        sys.stdout.write(str(' '))
        sys.stdout.write(str(file_name + file_ext))
        sys.stdout.write(str(' '))

    if os.path.exists(output_file):
        if overwrite:
            if debug_level >= 2:
                # DEBUG information's
                sys.stdout.write(str('will be overwrite'))
                # output_file = os.path.join(working_dir, file_name + file_ext)
        else:
            i = 1
            while os.path.exists(os.path.join(working_dir, file_name) + "-" + str(i) + file_ext):
                i += 1
            output_file = os.path.join(working_dir, file_name) + "-" + str(i) + file_ext

            # DEBUG information's
            if debug_level >= 2:
                sys.stdout.write(str('will be save as'))
                sys.stdout.write(str(' '))
                sys.stdout.write(str(file_name) + "-" + str(i) + file_ext)

    # DEBUG information's
    if debug_level >= 2:
        sys.stdout.write(str('\n'))
        sys.stdout.flush()
    return output_file


def sizeof_fmt(num, suffix='o'):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def save_cip_file(filename_path, width, height, cip_data, overwrite=0, debug_level=0):
    output_file = found_best_output_file_name(
        file_path=filename_path,
        overwrite=overwrite,
        debug_level=debug_level
    )
    cip_file = open(output_file, "w")
    cip_file.write("<CiscoIPPhoneImage>\n")
    cip_file.write("  <Title/>\n")
    cip_file.write("   <LocationX>-1</LocationX>\n")
    cip_file.write("   <LocationY>-1</LocationY>\n")
    cip_file.write("   <Width>" + str(width) + "</Width>\n")
    cip_file.write("   <Height>" + str(height) + "</Height>\n")
    cip_file.write("   <Depth>2</Depth>\n")
    cip_file.write("   <Data>" + str(cip_data) + "</Data>\n")
    cip_file.write("   <Prompt/>\n")
    cip_file.write("</CiscoIPPhoneImage>\n")
    cip_file.close()

    if debug_level >= 2:
        sys.stdout.write(str('File Size: '))
        sys.stdout.write(str(sizeof_fmt(os.path.getsize(output_file))))
        sys.stdout.write(str('\n'))
        sys.stdout.flush()


def open_image(filename, debug_level=0):
    image_file_name = filename
    if os.path.isfile(image_file_name):
        img = PIL.Image.open(image_file_name)
        try:
            img.load()
            if debug_level >= 2:
                sys.stdout.write(str(image_file_name))
                sys.stdout.write(str(' '))
                sys.stdout.write(str('Loaded'))
                sys.stdout.write(str('\n'))
                sys.stdout.flush()
            return img
        except IOError:
            sys.exit(1)
    else:
        if debug_level >= 1:
            sys.stdout.write('It have not image: {0}\n'.format(image_file_name))
            sys.stdout.flush()
        sys.exit(1)


def check_if_file_exists(file):
    if not os.path.exists(file):
        raise argparse.ArgumentTypeError("{0} does not exist".format(file))
    return file


if __name__ == "__main__":
    debug_level = 0
    human_dump = 0
    parser = argparse.ArgumentParser(
        description="Galaxie Image to CIP converter",
        prog='img2cip.py',
        usage='%(prog)s [options] inputfile [outputfile]'
    )
    parser.add_argument("-v", "--verbosity",
                        action="count",
                        default=0,
                        help="increase output verbosity, -v or -vv or -vvv are accepted"
                        )
    parser.add_argument('inputfile',
                        type=check_if_file_exists,
                        action="store",
                        help="Image source file", metavar="inputfile")
    parser.add_argument('outputfile', action="store", nargs='?',
                        help="Output file name, the format will be CIP, if no output file name is given, the inputfile \
                        name will be use, with .cip extention. and store inside the working directory")
    args = parser.parse_args()

    input_file_ext = os.path.splitext(args.inputfile)[1]
    input_file_name = os.path.basename(os.path.splitext(args.inputfile)[0])
    input_file_working_dir = os.path.realpath(os.path.dirname(args.inputfile))
    input_file = os.path.join(input_file_working_dir, input_file_name + input_file_ext)

    output_file_ext = '.cip'
    output_file_name = os.path.basename(os.path.splitext(args.inputfile)[0])
    output_file_working_dir = os.getcwd()
    output_file = os.path.join(output_file_working_dir, output_file_name + output_file_ext)

    if args.verbosity:
        debug_level = args.verbosity

    if args.outputfile:
        output_file_ext = os.path.splitext(args.outputfile)[1]
        output_file_name = os.path.basename(os.path.splitext(args.outputfile)[0])
        output_file_working_dir = os.path.realpath(os.path.dirname(args.outputfile))
        output_file = os.path.join(output_file_working_dir, output_file_name + output_file_ext)

    if debug_level >= 1:
        source_file_text = '{0: <21}: {1:}'.format('Source file', input_file)
        sys.stdout.write(str(source_file_text))
        sys.stdout.write(str('\n'))

        source_destination_text = '{0: <21}: {1:}'.format('Destination file', output_file)
        sys.stdout.write(str(source_destination_text))
        sys.stdout.write(str('\n'))
        sys.stdout.write(str('\n'))
        sys.stdout.flush()

    image = open_image(
        os.path.abspath(input_file),
        debug_level=debug_level
    )
    width, height = image.size

    cip_data = img_to_cip_data(
        image,
        debug_level=debug_level
    )

    save_cip_file(
        filename_path=os.path.abspath(output_file),
        height=height,
        width=width,
        cip_data=cip_data,
        overwrite=1,
        debug_level=debug_level
    )

    # THE END
    sys.exit(0)
