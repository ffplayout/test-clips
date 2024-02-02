#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import json
import os
import random
from subprocess import check_output

COLORS = ['AliceBlue', 'AntiqueWhite', 'Aqua', 'Aquamarine', 'Azure', 'Beige',
          'Bisque', 'Black', 'BlanchedAlmond', 'Blue', 'BlueViolet', 'Brown',
          'BurlyWood', 'CadetBlue', 'Chartreuse', 'Chocolate', 'Coral',
          'CornflowerBlue', 'Cornsilk', 'Crimson', 'Cyan', 'DarkBlue',
          'DarkCyan', 'DarkGoldenRod', 'DarkGray', 'DarkGreen', 'DarkKhaki',
          'DarkMagenta', 'DarkOliveGreen', 'Darkorange', 'DarkOrchid',
          'DarkRed', 'DarkSalmon', 'DarkSeaGreen', 'DarkSlateBlue',
          'DarkSlateGray', 'DarkTurquoise', 'DarkViolet', 'DeepPink',
          'DeepSkyBlue', 'DimGray', 'DodgerBlue', 'FireBrick', 'FloralWhite',
          'ForestGreen', 'Fuchsia', 'Gainsboro', 'GhostWhite', 'Gold',
          'GoldenRod', 'Gray', 'Green', 'GreenYellow', 'HoneyDew', 'HotPink',
          'IndianRed', 'Indigo', 'Ivory', 'Khaki', 'Lavender', 'LavenderBlush',
          'LawnGreen', 'LemonChiffon', 'LightBlue', 'LightCoral', 'LightCyan',
          'LightGoldenRodYellow', 'LightGreen', 'LightGrey', 'LightPink',
          'LightSalmon', 'LightSeaGreen', 'LightSkyBlue', 'LightSlateGray',
          'LightSteelBlue', 'LightYellow', 'Lime', 'LimeGreen', 'Linen',
          'Magenta', 'Maroon', 'MediumAquaMarine', 'MediumBlue',
          'MediumOrchid', 'MediumPurple', 'MediumSeaGreen', 'MediumSlateBlue',
          'MediumSpringGreen', 'MediumTurquoise', 'MediumVioletRed',
          'MidnightBlue', 'MintCream', 'MistyRose', 'Moccasin', 'NavajoWhite',
          'Navy', 'OldLace', 'Olive', 'OliveDrab', 'Orange', 'OrangeRed',
          'Orchid', 'PaleGoldenRod', 'PaleGreen', 'PaleTurquoise',
          'PaleVioletRed', 'PapayaWhip', 'PeachPuff', 'Peru', 'Pink', 'Plum',
          'PowderBlue', 'Purple', 'Red', 'RosyBrown', 'RoyalBlue',
          'SaddleBrown', 'Salmon', 'SandyBrown', 'SeaGreen', 'SeaShell',
          'Sienna', 'Silver', 'SkyBlue', 'SlateBlue', 'SlateGray', 'Snow',
          'SpringGreen', 'SteelBlue', 'Tan', 'Teal', 'Thistle', 'Tomato',
          'Turquoise', 'Violet', 'Wheat', 'White', 'WhiteSmoke', 'Yellow',
          'YellowGreen']


DURATIONS = 1500


def main():
    freq = 100
    length = 0
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    path = os.path.dirname(os.path.realpath(__file__))

    playlist = {
        "channel": "Test 1",
        "date": today,
        "program": []
    }

    color = random.choice(COLORS)
    dur = DURATIONS
    freq = random.randint(100, 5000)
    time = str(datetime.timedelta(seconds=dur))

    h, m, s = time.split(':')
    postfix = '{:02d}-{:02d}-{:02d}'.format(int(h), int(m), int(s))

    print(79 * '-',
            (f'\nCreate Clip with: "{color}" color, '
            f'"{freq}hz" and "{time}" length\n'),
            79 * '-')

    cmd = [
        'ffmpeg', '-hide_banner', '-f', 'lavfi', '-i',
        f'color=c={color}:s=640x360:d={dur}:r=25',
        '-f', 'lavfi', '-i',
        f'sine=frequency={freq}:duration={dur}',
        '-vf', (
            "drawtext=fontfile=FreeSerif.ttf:fontcolor=white:text="
            "'%{pts\\:gmtime\\:0\\:%H\\\\\:%M\\\\\:%S}:fontsize=46':"
            "boxborderw=6:x=(main_w/2-text_w/2):y=(main_h/2-text_h/2):"
            "box=1:boxcolor=black,drawtext=fontcolor=white:"
            "text='Length\\: " + time.replace(':', '\\:')
            + ":fontsize=18':boxborderw=6:x=(main_w/2-text_w/2):"
            "y=(h-line_h)*0.855:box=1:boxcolor=black"),
        '-aspect', '16:9', '-pix_fmt', 'yuv420p',
        '-t', f'{dur}', '-c:v', 'libx264',
        '-c:a', 'libfdk_aac', '-profile:a', 'aac_he_v2', '-ac', '2',
        '-ar', '44100', '-b:a', '8k', f'test_list/{color}_{postfix}.mp4']

    check_output(cmd)


if __name__ == '__main__':
    main()
