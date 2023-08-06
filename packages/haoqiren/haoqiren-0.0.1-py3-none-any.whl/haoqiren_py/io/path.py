import os
import sys

print(__file__)
print(sys.path)

print(os.path.abspath('.'))

print(os.getcwd())
print(os.path.relpath(__file__))
print(os.path.abspath(__file__))
print(os.path.realpath(__file__))
print(os.path.commonpath([__file__, __file__]))
print(os.path.normpath(__file__))

print(os.path.split("C:/cd"))
print(os.path.split(os.path.split(__file__)[0]))


def get_path_parent_path(path, parent_dir_name):
    d = os.path.dirname(os.path.realpath(path))
    ds = os.path.split(d)
    while True:
        if ds[1] == '':
            return ''
        elif ds[1] == parent_dir_name:
            return d
        else:
            d = ds[0]
            ds = os.path.split(d)
