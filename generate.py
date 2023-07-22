import json
import os
import random

from dataclasses import dataclass
from itertools import starmap
from typing import Dict, List, Self, Tuple
from constants import COLORS

COLORSCHEME_JSON_FILES = [
    "schemes/{}/colors.json".format(d) for d in next(os.walk("schemes"))[1]
]

CSS_PROPERTY_DELIMITER = ";\n"

ENTRYPOINT_TEMPLATE = "templates/index.html"
SITE_ENTRYPOINT = "docs/index.html"

# def to_json(module):
#     try:
#         scheme_name, variant = module.NAME.split()
#     except:
#         scheme_name = module.NAME
#         variant = "default"

#     config = dict(name=module.NAME, colors={variant.lower(): module.COLORS})
#     colors_json_file = os.path.join(module.__path__[0], "colors.json")

#     with open(colors_json_file, "w") as f:
#         json.dump(config, f, indent=2, sort_keys=True)


# for m in COLORSCHEME_JSON_FILES:
#     to_json(m)


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
    variants: Dict[str, Dict[str, HSLColor]]
    # TODO: Enforce at least one variant, by adding an explicit instance variable.

    @property
    def default_variant(self) -> Tuple[str, Dict[str, HSLColor]]:
        name, colors = self.variants.popitem()
        self.variants[name] = colors
        return name, colors

    @property
    def variant_names(self) -> List[str]:
        return list(self.variants.keys())

    def to_css_root(self) -> str:
        root_nodes = []

        for variant, colors in self.variants.items():
            color_properties = starmap("\t--{}: {!r}".format, colors.items())
            root_node = f""":root.{self.hyphenated_name}-{variant} {{
{CSS_PROPERTY_DELIMITER.join(color_properties)}
}}
"""
            root_nodes.append(root_node)

        return "\n".join(root_nodes)

    @property
    def hyphenated_name(self) -> str:
        return self.name.lower().replace(" ", "-")

    @classmethod
    def from_json(cls, filepath):
        with open(filepath) as f:
            data = json.load(f)
        scheme_name = data["name"]
        variants_data = data["colors"]

        variants = {}

        for variant, colors in variants_data.items():
            variants[variant] = {
                color_name: HSLColor.from_tuple(t) for color_name, t in colors.items()
            }

        return cls(scheme_name, variants)


# TODO add cursor colors


def generate_css(colorschemes: List[Colorscheme], css_out_file: str):
    roots = [colorscheme.to_css_root() for colorscheme in colorschemes]
    color_classes = "\n".join(
        map(".{0} {{\n\tbackground: var(--{0});\n}}".format, COLORS)
    )

    with open(css_out_file, "w") as f:
        f.writelines(roots)
        f.write(color_classes)
        f.write("\n")


def generate_js(schemes: List[Colorscheme], out_file: str):
    with open("templates/main.js") as f:
        content = f.read()

    schemes_data = [
        (scheme.name, scheme.hyphenated_name, scheme.variant_names)
        for scheme in schemes
    ]

    content = content.replace("'<schemes>'", json.dumps(schemes_data, indent=2))

    with open(out_file, "w") as f:
        f.write(content)


def update_default_scheme(scheme: Colorscheme):
    variant, _ = scheme.default_variant
    scheme_class = f"{scheme.name.lower()}-{variant}"

    with open(ENTRYPOINT_TEMPLATE) as f:
        html = f.read()

    with open(SITE_ENTRYPOINT, "w") as f:
        f.write(
            html.format(
                scheme_name=scheme.name,
                scheme_class=scheme_class,
                scheme_variant=variant,
            )
        )


def generate_docs():
    colorschemes = [Colorscheme.from_json(m) for m in COLORSCHEME_JSON_FILES]
    entry_scheme = random.choice(colorschemes)

    update_default_scheme(entry_scheme)
    generate_css(colorschemes, "docs/css/colors.css")
    generate_js(colorschemes, "docs/main.js")


if __name__ == "__main__":
    generate_docs()
