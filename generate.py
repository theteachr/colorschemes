from itertools import starmap
from helpers import coolors

from schemes import (
	ayu,
	everforest,
	gruvbox_material,
	nightfly,
	sonokai,
	tokyonight,
)


def to_hsl(color_dict):
	return {
		color: 'hsl({}, {}%, {}%)'.format(*values)
		for color, values in color_dict.items()
	}


def create_root(scheme_name, css_color_data):
	return ':root.{{}} {{{{\n{}\n}}}}\n'.format(
		';\n'.join(starmap('\t--{}: {}'.format, css_color_data.items()))
	).format(scheme_name)


def create_coolors_url(colors):
	return 'https://coolors.co/{}'.format('-'.join(colors))


def create_dict_from_kitty_conf(conf_file):
	with open(conf_file) as f:
		init = dict(map(lambda line: line.rstrip().split(), f.readlines()))

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

SCHEMES = {
	'Ayu Mirage': ayu,
	'Everforest': everforest,
	'Gruvbox Material': gruvbox_material,
	'Sonokai Andromeda': sonokai,
	'Tokyonight': tokyonight,
    'Nightfly': nightfly,
}

def main():
	# define scheme colors
	roots = [
		create_root('-'.join(scheme_name.lower().split()), to_hsl(mod.COLORS))
		for scheme_name, mod in SCHEMES.items()
	]

	# add color classes
	color_classes = '\n'.join(map('.{0} {{\n\tbackground: var(--{0});\n}}'.format, COLORS))

	with open('docs/css/colors.css', 'w') as f:
		f.writelines(roots)
		f.write(color_classes)
		f.write('\n')

if __name__ == '__main__':
	main()
