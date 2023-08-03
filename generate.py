import json

from dataclasses import dataclass
from itertools import starmap
from typing import Dict, List, Self, Tuple

from constants import COLORS
from shell_utils import list_dirs

COLORSCHEME_JSON_FILES = sorted(
    ["schemes/{}/colors.json".format(dirr) for dirr in list_dirs("schemes")]
)

CSS_PROPERTY_DELIMITER = ";\n"

ENTRYPOINT_TEMPLATE = "templates/index.html"
SITE_ENTRYPOINT = "docs/index.html"
COLORS_CSS = "docs/css/colors.css"

# NOTE: This has to sync with the `id` given to the root div in Elm.
ROOT_DIV_ID = "main"


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
            color_rules = f"""#{ROOT_DIV_ID}.{self.hyphenated_name}-{variant} {{
{CSS_PROPERTY_DELIMITER.join(color_properties)}
}}
"""
            root_nodes.append(color_rules)

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
# TODO classify every variant into either dark / light


def generate_css(colorschemes: List[Colorscheme], css_out_file: str):
    roots = [colorscheme.to_css_root() for colorscheme in colorschemes]
    color_classes = "\n".join(
        map(".{0} {{\n\tbackground: var(--{0});\n}}".format, COLORS)
    )

    with open(css_out_file, "w") as f:
        f.writelines(roots)
        f.write(color_classes)
        f.write("\n")


def generate_html(schemes: List[Colorscheme], out_file: str):
    with open(ENTRYPOINT_TEMPLATE) as f:
        content = f.read()

    schemes_data = [(scheme.name, scheme.variant_names) for scheme in schemes]
    data = dict(schemes_data=json.dumps(schemes_data), root_div_id=ROOT_DIV_ID)

    with open(out_file, "w") as f:
        f.write(content % data)


def generate_docs():
    colorschemes = [Colorscheme.from_json(m) for m in COLORSCHEME_JSON_FILES]

    generate_css(colorschemes, COLORS_CSS)
    generate_html(colorschemes, SITE_ENTRYPOINT)


if __name__ == "__main__":
    generate_docs()
