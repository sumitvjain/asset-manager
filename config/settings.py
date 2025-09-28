# from platformdirs import user_documents_dir
# from pathlib import Path
from config import constant
import os
import json


# DOCUMENTS_DIRPATH = user_documents_dir()

# APP_DIRNAME = ".app"
# CONFIG_FILENAME = "config.json"
# AVAILABLE_EXTENSIONS = ["exr", "jpeg", "jpg", "png", "mov"]
# DEFAULT_ENABLED_EXTS = {"jpeg", "jpg"}
# CONFIG_FILEPATH = Path(DOCUMENTS_DIRPATH) / APP_DIRNAME / CONFIG_FILENAME
# STYLE_QSSPATH =   Path(os.path.dirname(__file__)) / "style.qss" 


con = constant.Constant()

def create_json_file(app_dir_path):
    jsn_fle_pth = os.path.join(app_dir_path, con.CONFIG_FILENAME)
    project = {}

    for num in range(1, 11):
        extension_dict = {ext: (ext in con.DEFAULT_ENABLED_EXTS) for ext in con.AVAILABLE_EXTENSIONS}

        project[f"proj_{num:02}"] = {
            "name" : f"Project_{num:02}",
            "extension": extension_dict
        }

        with open(jsn_fle_pth, "w") as json_file:
            json.dump(project, json_file, indent=4)
    print("config file created ----------- ", jsn_fle_pth)
 


def setup_config():
    # app_dir_path = Path(DOCUMENTS_DIRPATH) / "/app"
    # print("app_dir_path --- ", app_dir_path)
    config_dir_path = os.path.dirname(con.CONFIG_FILEPATH)

    if not os.path.exists(config_dir_path):
        # config_dir_path.mkdir(exist_ok=True)
        os.makedirs(config_dir_path)
        create_json_file(config_dir_path)

    elif not con.CONFIG_FILENAME in os.listdir(config_dir_path):
        create_json_file(config_dir_path)
 