from itertools import starmap

from themes import (
	ayu,
	everforest,
	gruvbox_material,
	sonokai,
	tokyonight,
)


def to_hsl(color_dict):
	return {
		color: 'hsl({}, {}%, {}%)'.format(*values)
		for color, values in color_dict.items()
	}


def make_root(css_color_data):
	return ':root {{\n{}\n}}\n'.format(
		';\n'.join(starmap('\t--{}: {}'.format, css_color_data.items()))
	)


def export_colors(color_dict, out_file):
	with open(out_file, 'w') as f:
		f.write(make_root(to_hsl(color_dict)))


def main():
	export_colors(gruvbox_material.COLORS, 'colors/css/colors.css')


if __name__ == '__main__':
	main()
