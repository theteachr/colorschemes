from itertools import starmap

from themes import (
	ayu,
	everforest,
	gruvbox_material,
	sonokai,
	tokyonight,
)

def make_root(color_dict):
    css_color_data = {
        color: 'hsl({}, {}%, {}%)'.format(*values)
        for color, values in color_dict.items()
    }

    root = ':root {{\n{}\n}}\n'.format(
            ';\n'.join(starmap('\t--{}: {}'.format, css_color_data.items())))

    return root

def export_colors(color_dict, out_file):
    root = make_root(color_dict)

    with open(out_file, 'w') as f:
        f.write(root)
        f.write('\n')

def main():
    export_colors(gruvbox_material.COLORS, 'colors/css/colors.css')

if __name__ == '__main__':
    main()
