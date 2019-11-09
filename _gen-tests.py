#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import glob
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


DURATIONS = [10, 5, 15, 20, 30, 60, 3, 25, 45, 50, 120, 100, 1800, 900, 1200,
             2400, 500, 700, 3600, 5400, 7200]


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

    while length < 86400:
        color = random.choice(COLORS)
        freq = random.randint(100, 5000)
        dur = random.choice(DURATIONS)
        time = str(datetime.timedelta(seconds=dur))

        h, m, s = time.split(':')
        postfix = '{:02d}-{:02d}-{:02d}'.format(int(h), int(m), int(s))

        if os.path.isfile(os.path.join(path, '{}_{}.mp4'.format(color,
                                                                postfix))):
            continue

        print(79 * '-',
              ('\nCreate Clip with: "{}" color, '
               '"{}hz" and "{}" length\n').format(color, freq, time),
              79 * '-')

        cmd = [
            'ffmpeg', '-hide_banner', '-f', 'lavfi', '-i',
            'color=c={}:s=1024x576:d={}:r=25'.format(color, dur),
            '-f', 'lavfi', '-i',
            'sine=frequency={}:duration={}'.format(freq, dur),
            '-vf', (
                "drawtext=fontfile=FreeSerif.ttf:fontcolor=white:text="
                "'%{pts\\:gmtime\\:0\\:%H\\\\\:%M\\\\\:%S}:fontsize=46':"
                "boxborderw=6:x=(main_w/2-text_w/2):y=(main_h/2-text_h/2):"
                "box=1:boxcolor=black,drawtext=fontcolor=white:"
                "text='Length\\: " + time.replace(':', '\\:')
                + ":fontsize=18':boxborderw=6:x=(main_w/2-text_w/2):"
                "y=(h-line_h)*0.855:box=1:boxcolor=black,"
                "drawtext=fontcolor=white:text='Position in time\\: "
                + str(datetime.timedelta(seconds=length)).replace(':', '\\:')
                + ":fontsize=18':boxborderw=6:x=(main_w/2-text_w/2):"
                "y=(h-line_h)*0.9:box=1:boxcolor=black"),
            '-aspect', '16:9', '-pix_fmt', 'yuv420p',
            '-t', '{}'.format(dur), '-c:v', 'libx265',  '-preset', 'veryfast',
            '-tag:v', 'hvc1', '-c:a', 'libfdk_aac',
            '-profile:a', 'aac_he_v2', '-ac', '2', '-ar', '44100',
            '-b:a', '16k', '{}_{}.mp4'.format(color, postfix)]

        check_output(cmd)

        dur_cmd = [
                'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                '{}_{}.mp4'.format(color, postfix)]

        duration = float(check_output(dur_cmd).decode('utf-8'))

        playlist['program'].append({
                "in": 0,
                "out": duration,
                "duration": duration,
                "source": os.path.join(
                    path, '{}_{}.mp4'.format(color, postfix))
            })
        length += duration

        print(playlist)
        exit()

    with open(os.path.join(path, 'playlist.json'),
              'w', encoding='utf-8') as f:
        json.dump(playlist, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
