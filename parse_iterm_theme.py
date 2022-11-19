import xml.etree.ElementTree as ET


def main():
    tree = ET.parse("schemes/kanagawa/iterm/Kanagawa.itermcolors")
    root = tree.getroot()

    main_dict = next(iter(root))
    kvs = list(iter(main_dict))

    for (color,) in zip(kvs[::2], kvs[1::2]):
        print(e.tag)


if __name__ == "__main__":
    main()
