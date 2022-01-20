from itertools import starmap
from helpers import coolors_export_to_color_dict, color_tuple_to_hsl

from schemes import (
	ayu,
	everforest,
	gruvbox_material,
	nightfly,
	sonokai,
	tokyonight,
)

# TODO add scheme name in the `__init__` of the scheme package?
# TODO change js to automatically fetch the new colorschemes
# TODO add cursor colors

def create_root(scheme_name, css_color_data):
	return ':root.{{}} {{{{\n{}\n}}}}\n'.format(
		';\n'.join(starmap('\t--{}: {}'.format, css_color_data.items()))
	).format(scheme_name)


def create_dict_from_kitty_conf(conf_file):
	with open(conf_file) as f:
		return dict(map(str.split, f.read().rstrip().split('\n')))


def create_kitty_conf_from_dict(color_dict):
	pass


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
		create_root(
			'-'.join(scheme_name.lower().split()),
			{component: color_tuple_to_hsl(color) for component, color in mod.COLORS.items()}
		)
		for scheme_name, mod in SCHEMES.items()
	]

	# add color classes
	color_classes = '\n'.join(map('.{0} {{\n\tbackground: var(--{0});\n}}'.format, COLORS))

	with open('docs/css/colors.css', 'w') as f:
		f.writelines(roots)
		f.write(color_classes)
		f.write('\n')

