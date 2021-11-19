from metacity.filesystem import base
import os 
import shutil

def timeline_dir(layer_dir):
    return os.path.join(layer_dir, base.TIMELINE)


def timeline_config(timeline_dir):
    return os.path.join(timeline_dir, "timeline.json")



def clear_timeline(timeline_dir):
    shutil.rmtree(timeline_dir)
    os.mkdir(timeline_dir)
