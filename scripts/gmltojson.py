#!/usr/bin/python3

import sys
import subprocess
import os

usage = ("Converts CityGML into CityJSON:"
         "gmltojson.py [input file]")


def readable(file):
    print(file)
    f = open(file, "r")
    return f.readable()


def writable(file):
    f = open(file, "w")
    return f.writable()


def generate_output_path(input_file):
    input_path_wihout_suffix = os.path.splitext(input_file)[0]
    return input_path_wihout_suffix + ".json"


def process_args():
    input_arg = sys.argv[1]
    input_file = os.path.join(os.getcwd(), input_arg)
    output_file = generate_output_path(input_file) #sys.argv[2]
    return input_file, output_file


def parse_args():
    if len(sys.argv) < 2:
        print(usage)
        return None, None
    else:
        return process_args()


def check_inputs(input_file, output_file):
    if not readable(input_file) or not writable(output_file):
        raise Exception("Source or destination files were not specified or accesible.")


def find_tools_path(__file__):
    launcher_abs_path = os.path.dirname(os.path.realpath(__file__))
    metacity_abs_path = os.path.dirname(launcher_abs_path)
    gmltools_path = "tools/citygmltools"
    gmltools_dir_rootpath = os.path.join(metacity_abs_path, gmltools_path)
    gmltools_version_path = os.listdir(gmltools_dir_rootpath)

    if len(gmltools_version_path) > 1:
        raise Exception(f"More than one version of CityGML tools available: {gmltools_version_path}")

    gmltools_path = os.path.join(gmltools_dir_rootpath, gmltools_version_path[0], "citygml-tools")
    return gmltools_path


def print_output(proc):
    for line in iter(proc.stdout.readline, b""):
        print(line.decode("utf-8"), end="")


def run_conversion(input_file, gmltools_path):
    proc = subprocess.Popen([gmltools_path, "to-cityjson", input_file], 
                 stdout=subprocess.PIPE,
                 stderr=subprocess.STDOUT)
    print_output(proc)
    return_code = proc.wait()
    return return_code


if __name__ == "__main__":
    input_file, output_file = parse_args()
    if input_file is None:
        quit()
    check_inputs(input_file, output_file)
    gmltools_path = find_tools_path(__file__)
    return_code = run_conversion(input_file, gmltools_path)
    #print(return_code)

