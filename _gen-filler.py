#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import random
from subprocess import check_output

TEST_SOURCES = ['testsrc=duration=15:size=640x360:rate=25',
                'smptebars=duration=20:size=640x360:rate=25']


DURATIONS = [15, 20]


def main():
    freq = 100

    for i, test_src in enumerate(TEST_SOURCES):
        dur = DURATIONS[i]
        freq = random.randint(100, 5000)
        time = str(datetime.timedelta(seconds=dur))

        h, m, s = time.split(':')
        postfix = '{:02d}-{:02d}-{:02d}'.format(int(h), int(m), int(s))


        cmd = [
            'ffmpeg', '-hide_banner', '-f', 'lavfi', '-i',
            test_src,
            '-f', 'lavfi', '-i',
            f'sine=frequency={freq}:duration={dur}',
            '-vf', (
                "drawtext=fontfile=FreeSerif.ttf:fontcolor=white:text_align=C:text="
                "'Filler\n%{pts\\:gmtime\\:0\\:%H\\\\\:%M\\\\\:%S}:fontsize=46':"
                "boxborderw=6:x=(main_w/2-text_w/2):y=(main_h/2-text_h/2):"
                "box=1:boxcolor=black,drawtext=fontcolor=white:"
                "text='Length\\: " + time.replace(':', '\\:')
                + ":fontsize=18':boxborderw=6:x=(main_w/2-text_w/2):"
                "y=(h-line_h)*0.855:box=1:boxcolor=black"),
            '-aspect', '16:9', '-pix_fmt', 'yuv420p',
            '-t', f'{dur}', '-c:v', 'libx264',
            '-c:a', 'libfdk_aac', '-profile:a', 'aac_he_v2', '-ac', '2',
            '-ar', '44100', '-b:a', '8k', '-y', f'filler/filler_{i}.mp4']

        check_output(cmd)


if __name__ == '__main__':
    main()
