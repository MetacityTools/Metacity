import os
import json


def readable(file):
    f = open(file, "r")
    return f.readable()


def writable(file):
    f = open(file, "w")
    return f.writable()


def write_json(filename, data):
    if os.path.exists(filename):
        os.remove(filename)

    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


def read_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def dir_from_path(path):
    return os.path.dirname(path)

def change_suffix(path, suffix):
    base = os.path.splitext(path)[0]
    return f"{base}.{suffix}"

def get_suffix(path):
    return os.path.splitext(path)[1][1:]