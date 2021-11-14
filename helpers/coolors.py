import re
from generate import COLORS

def create_coolors_url(colors):
	return 'https://coolors.co/{}'.format('-'.join(colors))


def to_colors_dict(coolors_hsl_export):
    pattern = re.compile('hsla\((\d+), (\d+)%, (\d+)%, 1\)')

    return {
        color: pattern.search(line).groups()
        for color, line in zip(['background'] + COLORS, coolors_hsl_export.split('\n'))
    }

def main():
    to_colors_dict(export)

if __name__ == '__main__':
    main()
