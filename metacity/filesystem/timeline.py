from metacity.filesystem import base
import os 
import shutil

def timeline_dir(layer_dir):
    return os.path.join(layer_dir, base.TIMELINE)


def timeline_config(timeline_dir):
    return os.path.join(timeline_dir, "timeline.json")

def interval_file(timeline_dir: str, interval_file: str):
    return os.path.join(timeline_dir, interval_file)

def interval(timeline_dir: str, start_time: int):
    return interval_file(timeline_dir, f"interval{start_time}.json")

def interval_list(timeline_dir: str):
    return os.listdir(timeline_dir)


def clear_timeline(timeline_dir):
    shutil.rmtree(timeline_dir)
    os.mkdir(timeline_dir)
