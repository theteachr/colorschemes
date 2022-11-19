from dataclasses import dataclass
from itertools import starmap
from typing import Dict, List, Tuple
from typing_extensions import Self
from constants import COLORS

from schemes import (
    ayu,
    everforest,
    gruvbox_material,
    nightfly,
    catppuccin,
    sonokai,
    tokyonight,
)

COLORSCHEME_MODS = [
    ayu,
    everforest,
    gruvbox_material,
    nightfly,
    catppuccin,
    sonokai,
    tokyonight,
]
CSS_PROPERTY_DELIMITER = ";\n"


@dataclass(frozen=True)
class HSLColor:
    hue: int
    saturation: int
    lightness: int

    @classmethod
    def from_tuple(cls, hsl: Tuple) -> Self:
        return cls(*hsl)

    def __repr__(self) -> str:
        return f"hsl({self.hue}, {self.saturation}%, {self.lightness}%)"


@dataclass(frozen=True)
class Colorscheme:
    name: str
    colors: Dict[str, HSLColor]

    def to_css_root(self) -> str:
        color_properties = starmap("\t--{}: {!r}".format, self.colors.items())
        return f""":root.{hyphenate(self.name.lower())} {{
{CSS_PROPERTY_DELIMITER.join(color_properties)}
}}
"""

    @classmethod
    def from_module(cls, m) -> Self:
        colors = {name: HSLColor.from_tuple(hsl) for name, hsl in m.COLORS.items()}
        return cls(m.NAME, colors)


# TODO add cursor colors
# TODO add switchable schemes with variants (light/dark/solarized)


def hyphenate(text: str) -> str:
    return text.lower().replace(" ", "-")


def generate_css(colorschemes: List[Colorscheme], css_out_file: str):
    roots = [colorscheme.to_css_root() for colorscheme in colorschemes]
    color_classes = "\n".join(
        map(".{0} {{\n\tbackground: var(--{0});\n}}".format, COLORS)
    )

    with open(css_out_file, "w") as f:
        f.writelines(roots)
        f.write(color_classes)
        f.write("\n")


def generate_js(schemes: List, js_out_file: str):
    with open("template.tjs") as f:
        js_template = f.read()

    class_name_pairs = [[hyphenate(scheme), scheme] for scheme in schemes]
    num_schemes = len(class_name_pairs)

    js = js_template.format(num_schemes=num_schemes, class_name_pairs=class_name_pairs)

    with open(js_out_file, "w") as f:
        f.write(js)


def generate_docs():
    generate_css(
        [Colorscheme.from_module(m) for m in COLORSCHEME_MODS], "docs/css/colors.css"
    )
    generate_js([m.NAME for m in COLORSCHEME_MODS], "docs/main.js")


if __name__ == "__main__":
    generate_docs()
