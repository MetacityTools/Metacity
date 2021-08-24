import os
import ntpath
import json

def readable(file):
    f = open(file, "r")
    return f.readable()


def writable(file):
    f = open(file, "w")
    return f.writable()


def filename(file_path):
    return ntpath.basename(file_path)


def id_from_filename(file_path):
    return os.path.splitext(filename(file_path))[0]


def write_json(filename, data):
    if os.path.exists(filename):
        print(f'File {filename} already exists, rewriting...')
        os.remove(filename)

    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


def read_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)
