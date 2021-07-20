import os
import ntpath

def readable(file):
    print(file)
    f = open(file, "r")
    return f.readable()


def writable(file):
    f = open(file, "w")
    return f.writable()


def id_from_filename(file_name):
    return os.path.splitext(ntpath.basename(file_name))[0]
