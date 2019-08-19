#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
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


DURATIONS = [10, 5, 15, 20, 30, 60, 3, 25, 45, 50, 120, 100, 1800, 900, 1200,
             2400, 500, 700, 3600]


def main():
    used_color = []
    task = 0
    freq = 100
    length = 68400

    """
    # fixed 1 hour length
    while task < 15:
        color = random.choice(COLORS)

        if color not in used_color:
            used_color.append(color)

            cmd = [
                'ffmpeg', '-f', 'lavfi', '-i',
                'color=c={}:s=1024x576:d=3600:r=25'.format(color),
                '-f', 'lavfi', '-i',
                'sine=frequency={}:duration=3600'.format(freq),
                '-vf', (
                    "drawtext=fontfile=FreeSerif.ttf:fontcolor=white:text="
                    "'%{pts\\:gmtime\\:0\\:%T}:fontsize=46':"
                    "x=(main_w/2-text_w/2):y=(main_h/2-text_h/2):"
                    "box=1:boxcolor=black"), '-aspect', '16:9',
                '-pix_fmt', 'yuv420p', '-preset', 'veryfast',
                '-t', '3600', '-c:v', 'libx265', '-c:a', 'libfdk_aac',
                '-profile:a', 'aac_he_v2', '-ac', '2', '-ar', '44100',
                '-b:a', '16k', '{}_01-00-00.mp4'.format(color)]

            check_output(cmd)

            freq += 100
            length += 3600
            task += 1
    """

    while length < 86400:
        color = random.choice(COLORS)
        freq = random.randint(100, 5000)
        dur = random.choice(DURATIONS)
        time = str(datetime.timedelta(seconds=dur))
        print(time)
        h, m, s = time.split(':')
        postfix = '{:02d}-{:02d}-{:02d}'.format(int(h), int(m), int(s))

        cmd = [
            'ffmpeg', '-f', 'lavfi', '-i',
            'color=c={}:s=1024x576:d={}:r=25'.format(color, dur),
            '-f', 'lavfi', '-i',
            'sine=frequency={}:duration={}'.format(freq, dur),
            '-vf', (
                "drawtext=fontfile=FreeSerif.ttf:fontcolor=white:text="
                "'%{pts\\:gmtime\\:0\\:%T}:fontsize=46':"
                "x=(main_w/2-text_w/2):y=(main_h/2-text_h/2):"
                "box=1:boxcolor=black"), '-aspect', '16:9',
            '-pix_fmt', 'yuv420p',  '-preset', 'veryfast',
            '-t', '{}'.format(dur), '-c:v', 'libx265', '-c:a', 'libfdk_aac',
            '-profile:a', 'aac_he_v2', '-ac', '2', '-ar', '44100',
            '-b:a', '16k', '{}_{}.mp4'.format(color, postfix)]

        check_output(cmd)

        length += dur


if __name__ == '__main__':
    main()
