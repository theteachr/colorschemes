from itertools import starmap
import gruvbox_material

css_color_data = {
    color: 'hsl({}, {}%, {}%)'.format(*values)
    for color, values in gruvbox_material.COLORS.items()
}

root = ':root {{\n{}\n}}\n'.format(';\n'.join(starmap('\t--{}: {}'.format, css_color_data.items())))

with open('colors.css', 'w') as f:
    f.write(root)
    f.write('\n')
