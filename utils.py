import colorsys
import re

from constants import COLORS

def create_coolors_url(colors):
	return 'https://coolors.co/{}'.format('-'.join(colors))


def coolors_export_to_color_dict(coolors_hsl_export):
	pattern = re.compile('hsla\((\d+), (\d+)%, (\d+)%, 1\)')

	return {
		color: pattern.search(line).groups()
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
	h, s, l = color

	return ''.join(round(v * 255) for v in colorsys.hsv_to_rgb(h/360, s/100, l/100))

def test_coolors():
	export = '''\
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

	print(coolors_export_to_color_dict(export))

def main():
    test_coolors()
    

if __name__ == '__main__':
	main()
