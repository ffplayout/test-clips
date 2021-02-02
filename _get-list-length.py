#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sys
from argparse import ArgumentParser
from datetime import timedelta

stdin_parser = ArgumentParser(
    description='calculates the total length of the playlist',
    epilog="")

stdin_parser.add_argument(
    '-p', '--playlist', help='path to playlist'
)

stdin_parser.add_argument(
    '-s', '--shorter', help='get clips shorter then, in timecode format'
)

stdin_parser.add_argument(
    '-l', '--longer', help='get clips longer then, in timecode format'
)

stdin_args = stdin_parser.parse_args()


def str_to_sec(s):
    if s in ['now', '', None, 'none']:
        return None
    else:
        s = s.split(':')
        try:
            return float(s[0]) * 3600 + float(s[1]) * 60 + float(s[2])
        except ValueError:
            print('Wrong time format!')
            sys.exit(1)


def main():
    if not os.path.isfile(stdin_args.playlist):
        print(f'playlist {stdin_args.playlist} does not exist')
        exit()

    with open(stdin_args.playlist, 'r') as f:
        data = json.load(f)

    count = 0
    filter_list = []

    for clip in data['program']:
        duration = clip['out'] - clip['in']
        count += duration

        if stdin_args.shorter and stdin_args.longer:
            shorter = str_to_sec(stdin_args.shorter)
            longer = str_to_sec(stdin_args.longer)

            if shorter > duration > longer:
                filter_list.append([str(timedelta(seconds=round(duration))),
                                    clip['source']])

    print('playlist length:', str(timedelta(seconds=round(count))))
    print('length in seconds:', round(count, 2))

    if filter_list:
        print(79 * '-')
        print(*filter_list, sep="\n")



if __name__ == '__main__':
    main()
