import os
import ntpath
import json

def readable(file):
    f = open(file, "r")
    return f.readable()


def writable(file):
    f = open(file, "w")
    return f.writable()


def id_from_filename(file_name):
    return os.path.splitext(ntpath.basename(file_name))[0]


def write_json(filename, data):
    if os.path.exists(filename):
        print(f'File {filename} already exists, rewriting...')
        os.remove(filename)

    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


def read_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

