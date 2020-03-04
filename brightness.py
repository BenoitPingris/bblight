#!/usr/bin/env python3.8

import sys
import argparse
from typing import List

FILE_MAX_BRIGHTNESS = '/sys/class/backlight/intel_backlight/max_brightness'
FILE_BRIGHTNESS = '/sys/class/backlight/intel_backlight/brightness'


def read_file(path: str) -> List[str]:
    with open(path, 'r') as fd:
        return fd.readlines()


def write_in_file(path: str, content: str):
    with open(path, 'w') as fd:
        fd.write(content)


def get_max_brightness() -> int:
    return int(read_file(FILE_MAX_BRIGHTNESS)[0])


def get_current_brightness() -> int:
    return int(read_file(FILE_BRIGHTNESS)[0])


def get_current_brightness_as_perc() -> float:
    return get_current_brightness() / get_max_brightness() * 100


def set_brightness_as_perc(perc: int) -> bool:
    max_brightness = get_max_brightness()
    write_in_file(FILE_BRIGHTNESS, str(int(max_brightness * (perc/100))))


def decrease_brightness(dec: int):
    current_brightness = get_current_brightness_as_perc()
    if current_brightness - dec <= 0:
        print('Error: brightness level can\' be negative or equal to 0.')
        return 1
    set_brightness_as_perc(current_brightness - dec)
    return 0


def increase_brightness(inc: int):
    current_brightness = get_current_brightness_as_perc()
    if current_brightness + inc > 100:
        print('Error: brightness level can\' be above 100%.')
        return 1
    set_brightness_as_perc(current_brightness + inc)
    return 0


def handle_args(args):
    parser = argparse.ArgumentParser(
        description="Program to manage brightness level by editing a file (don't know if it's good)")
    parser.add_argument('-i', '--increase', type=int,
                        help="Level of brightness to increase (in %%)")
    parser.add_argument('-d', '--decrease', type=int,
                        help="Level of brightness to decrease (in %%)")
    parser.add_argument('-s', '--set', type=int,
                        help="Level of brightness to set (in %%)")
    parser.add_argument('-g', '--get', help="Get level of brightness", action="store_true")
    return parser.parse_args(args), parser


def main():
    options, parser = handle_args(sys.argv[1:])
    if options.increase:
        return increase_brightness(int(options.increase))
    elif options.decrease:
        return decrease_brightness(int(options.decrease))
    elif options.set:
        return set_brightness_as_perc(int(options.set))
    elif options.get:
        try:
            print(get_current_brightness_as_perc())
            return 0
        except:
            return 1
    parser.print_help(sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
