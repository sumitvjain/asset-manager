# import nuke
import sys
import subprocess







def get_meta_data(file_path):
    # import nuke
    print("Nuke Version:", nuke.NUKE_VERSION_STRING)
    print("Root name:", nuke.root().name())

    nuke.scriptNew()

    # raw_path = file_path.replace('\\', '/')
    node = nuke.createNode("Read", f"file {{{file_path}}}", inpanel=False)

    meta_data_dict = {}
    for key, value in node.metadata().items():
        meta_data_dict[key] = value

    # nuke.scriptClear()
    # nuke.scriptClose()
    nuke.scriptExit()

    print("meta_data_dict --- ", meta_data_dict)
    if meta_data_dict:
        return True, meta_data_dict
    else:
        return False, meta_data_dict


    path = sys.argv[1]
    print('path ---- ', path)



def fetch_meta_data(image_path):
    print('image_path ---- ', image_path)
    



if __name__ == "__main__":
    file_path = path = sys.argv[1]
    get_meta_data(file_path)

#####################################

