import os


def remove_tree(path):
    paths = []
    for root, dirs, files in os.walk(path):
        for file in files:
            filename = os.path.join(root, file)
            if os.path.isfile(filename):
                os.unlink(filename)
        paths.append(root)

    for _dir in reversed(paths):
        if os.path.isdir(_dir):
            os.rmdir(_dir)
