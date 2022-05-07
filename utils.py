import colorsys
import re

from itertools import starmap
from constants import COLORS

# TODO fix module name

def create_coolors_url(colors):
    return 'https://coolors.co/{}'.format('-'.join(colors))


def coolors_export_to_color_dict(coolors_hsl_export):
    pattern = re.compile('hsla\((\d+), (\d+)%, (\d+)%, 1\)')

    return {
        color: tuple(map(int, pattern.search(line).groups()))
        for color, line in zip(['background'] + COLORS, coolors_hsl_export.split('\n'))
    }


def color_tuple_to_hsl(three_tuple):
    """
    Converts a (h, s, l) to a valid CSS value.

    h: hue
    s: saturation (in %)
    l: lightness (in %)
    """

    return 'hsl({}, {}%, {}%)'.format(*three_tuple)


def css_hsl_tuple_to_hex(color):
    # FIXME Colors are washed out and dull
    h, s, l = color

    return ''.join(f'{round(v * 255):02X}' for v in colorsys.hsv_to_rgb(h/360, s/100, l/100))


def create_dict_from_kitty_conf(conf_file):
    with open(conf_file) as f:
        return dict(map(str.split, f.read().rstrip().split('\n')))


def create_kitty_conf_from_coolors_hex_csv_export(line):
    background, *rest = line.split(',')

    color_dict = {f'color{i}': color for i, color in enumerate(rest)}
    color_dict.update(dict(background=background))

    return '\n'.join(starmap('{} #{}'.format, color_dict.items()))


def main():
    coolors_export = '''\
--rich-black-fogra-29: hsla(205, 100%, 7%, 1);
--prussian-blue: hsla(205, 100%, 16%, 1);
--tart-orange: hsla(359, 100%, 65%, 1);
--pistachio: hsla(89, 48%, 62%, 1);
--medium-champagne: hsla(45, 60%, 74%, 1);
--french-sky-blue: hsla(218, 90%, 74%, 1);
--bright-lilac: hsla(280, 60%, 74%, 1);
--middle-blue-green: hsla(170, 58%, 66%, 1);
--alice-blue: hsla(204, 100%, 96%, 1);\
'''

    color_dict = coolors_export_to_color_dict(coolors_export)
    print(color_dict)

    hexed = list(map(css_hsl_tuple_to_hex, color_dict.values()))
    print(hexed)

    print(create_coolors_url(hexed))

    coolors_hex_export_line = '001626,003052,ff4e52,9ecc6e,e4d093,80acf8,c993e4,78dbcb,ebf7ff'
    print(create_kitty_conf_from_coolors_hex_csv_export(coolors_hex_export_line))


if __name__ == '__main__':
    main()
