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


def create_root(css_color_data):
	return ':root {{\n{}\n}}\n'.format(
		';\n'.join(starmap('\t--{}: {}'.format, css_color_data.items()))
	)


def export_colors(color_dict, out_file):
	with open(out_file, 'w') as f:
		f.write(create_root(to_hsl(color_dict)))


def create_coolors_url(colors):
	return 'https://coolors.co/{}'.format('-'.join(colors))


def create_dict_from_kitty_conf(conf_file):
	with open(conf_file) as f:
		init = dict(map(lambda line: line.rstrip().split(),
				f.readlines()))
	
	res = dict(background=init['background'][1:])
	res.update({COLORS[i]: init[f'color{i}'][1:] for i in range(8)})

	return res


COLORS = [
	'black',
	'red',
	'green',
	'yellow',
	'blue',
	'magenta',
	'cyan',
	'white',
]

def main():
	export_colors(gruvbox_material.COLORS, 'colors/css/colors.css')


if __name__ == '__main__':
	main()
