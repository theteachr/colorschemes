from itertools import starmap
from typing import List, Tuple
from constants import COLORS
from utils import color_tuple_to_hsl

from schemes import (
    ayu,
    everforest,
    gruvbox_material,
    nightfly,
    catppuccin,
    sonokai,
    tokyonight,
)

# TODO add scheme name in the `__init__` of the scheme package?
# TODO change js to automatically fetch the new colorschemes
# TODO add cursor colors

def create_root(scheme_name: str, css_color_data: dict) -> str:
    return ':root.{} {{\n{}\n}}\n'.format(scheme_name,
        ';\n'.join(starmap('\t--{}: {}'.format, css_color_data.items())))


SCHEMES = [
    ('Ayu Mirage', ayu),
    ('Everforest', everforest),
    ('Gruvbox Material', gruvbox_material),
    ('Catppuccin', catppuccin),
    ('Sonokai Andromeda', sonokai),
    ('Tokyonight', tokyonight),
    ('Nightfly', nightfly),
]

def hyphenate(text: str) -> str:
    return text.lower().replace(' ', '-')


def generate_css(schemes: Tuple, css_out_file: str):
    roots = [
        create_root(
            '-'.join(scheme_name.lower().split()),
            {component: color_tuple_to_hsl(color) for component, color in mod.COLORS.items()})
        for scheme_name, mod in schemes
    ]

    color_classes = '\n'.join(map('.{0} {{\n\tbackground: var(--{0});\n}}'.format, COLORS))

    with open(css_out_file, 'w') as f:
        f.writelines(roots)
        f.write(color_classes)
        f.write('\n')


def generate_js(schemes: List, js_out_file: str):
    with open('template.tjs') as f:
        js_template = f.read()

    class_name_pairs = [[hyphenate(scheme), scheme] for scheme in schemes]
    num_schemes = len(class_name_pairs)

    js = js_template.format(num_schemes=num_schemes, class_name_pairs=class_name_pairs)

    with open(js_out_file, 'w') as f:
        f.write(js)


def generate_docs():
    generate_css(SCHEMES, 'docs/css/colors.css')
    generate_js(map(lambda pair: pair[0], SCHEMES), 'docs/main.js')


if __name__ == '__main__':
    generate_docs()
