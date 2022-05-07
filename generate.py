from itertools import starmap
from constants import COLORS
from utils import color_tuple_to_hsl

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

def create_root(scheme_name: str, css_color_data: dict) -> str:
    return ':root.{{}} {{{{\n{}\n}}}}\n'.format(
        ';\n'.join(starmap('\t--{}: {}'.format, css_color_data.items()))
    ).format(scheme_name)



SCHEMES = {
    'Ayu Mirage': ayu,
    'Everforest': everforest,
    'Gruvbox Material': gruvbox_material,
    'Sonokai Andromeda': sonokai,
    'Tokyonight': tokyonight,
    'Nightfly': nightfly,
}

def hyphenate(text: str) -> str:
    return text.lower().replace(' ', '-')

def generate_docs():
    # define scheme colors
    roots = [
        create_root(
            '-'.join(scheme_name.lower().split()),
            {component: color_tuple_to_hsl(color) for component, color in mod.COLORS.items()})
        for scheme_name, mod in SCHEMES.items()
    ]

    # add color classes
    color_classes = '\n'.join(map('.{0} {{\n\tbackground: var(--{0});\n}}'.format, COLORS))

    with open('docs/css/colors.css', 'w') as f:
        f.writelines(roots)
        f.write(color_classes)
        f.write('\n')


def generate_js():
    with open('template.tjs') as f:
        js_template = f.read()

    num_schemes = len(SCHEMES)
    schemes = [[hyphenate(scheme_name), scheme_name] for scheme_name in SCHEMES.keys()]

    js = js_template.format(num_schemes=num_schemes, schemes=schemes)

    with open('docs/main.js', 'w') as f:
        f.write(js)

if __name__ == '__main__':
    generate_js()