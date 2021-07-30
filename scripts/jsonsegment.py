#!/usr/bin/python3

from argparse import ArgumentParser
from metacity.project import MetacityProject
from metacity.io.cj import load_cj_file


usage = ("Segment CityJSON file, "
         "exports segments according to LOD and geometry type"
         "into directory 'segmented'.")


def process_args():
    parser = ArgumentParser(description=usage)
    parser.add_argument('cj_input_file', type=str, help='CityJSON input file')
    parser.add_argument('-a', '--append', help='Appends processed data to existing project, if project does not exist, creates a new project', action="store_true")
    parser.add_argument('output_dir', type=str, help='Output directory, will be emptied if alreay exists')
    args = parser.parse_args()
    input_file = args.cj_input_file
    output_folder = args.output_dir
    append_action = args.append
    return input_file, output_folder, append_action


if __name__ == "__main__":
    input_file, output_dir, append_action = process_args()
    project = MetacityProject(output_dir, append_action)
    layer = project.layer('layer1')
    load_cj_file(layer, input_file)

        

        



        










