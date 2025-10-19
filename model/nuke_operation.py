import nuke
import sys
import subprocess

file_path = path = sys.argv[1]


def get_meta_data():

    nuke.scriptNew()

    # raw_path = file_path.replace('\\', '/')
    node = nuke.createNode("Read", f"file {{{file_path}}}", inpanel=False)

    meta_data_dict = {}
    for key, value in node.metadata().items():
        meta_data_dict[key] = value

    nuke.scriptClear()

    if meta_data_dict:
        return True, meta_data_dict
    else:
        return False, meta_data_dict



    path = sys.argv[1]
    print('path ---- ', path)



def fetch_meta_data(image_path):
    print('image_path ---- ', image_path)
    