import os


def list_dirs(path):
    _, dirs, _ = next(os.walk(path))
    return dirs
