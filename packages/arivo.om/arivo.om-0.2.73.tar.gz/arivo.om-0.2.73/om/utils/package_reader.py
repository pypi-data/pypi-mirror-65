import glob
import json
import logging
import os
from dotenv import dotenv_values
import yaml


def load_hw_env(path):
    env_dict = dotenv_values(path)
    try:
        env_dict["HARDWARE_TYPE"] = json.loads(env_dict["HARDWARE_TYPE"])
    except:
        pass
    return env_dict


def get_hw_packages(type, package_dir="/opt/openmodule/dist2/"):
    """get hardware packages matching type with prefix match, so it's possible to match as specific as necessary

    Args:
        type (str): prefix to match, e.g. "io" for all io packages or "cam-ip-avigilon" for all avigilon cameras
        package_dir (str): path to directory containing the hardware packages
    Returns:
        list of directories of the matching hardware packages
    """
    all_dirs = sorted(glob.glob(os.path.join(package_dir, "hw-*")))
    all_dirs = [d for d in all_dirs if os.path.isdir(d) and os.path.exists(os.path.join(d, "env"))]
    matching_dirs = []
    for d in all_dirs:
        env = os.path.join(d, "env")
        try:
            env_dict = load_hw_env(env)
            for hw_type in env_dict.get("HARDWARE_TYPE", []):
                if hw_type.startswith(type):
                    matching_dirs.append(d)
                    break
        except Exception as e:
            logging.error("Unexpected error while loading hardware env file " + env)
    return matching_dirs


def get_hw_settings(type, package_dir="/opt/openmodule/dist2/"):
    """get settings of the hardware packages prefix-matching type

    Args:
        type (str): prefix to match, e.g. "io" for all io packages or "cam-ip-avigilon" for all avigilon cameras
        package_dir (str): path to directory containing the hardware packages
    Returns:
        list of {"env": dict, "yml": [dict,list,None]}, where in "env" one can find the env variables as a dict and in
            "yml" one can find the yaml settings
    """
    hw_dirs = get_hw_packages(type, package_dir)
    hw_settings = []
    for d in hw_dirs:
        env = os.path.join(d, "env")
        yml = os.path.join(d, "yml")
        try:
            hw_settings.append({"env": load_hw_env(env), "yml": {}})
        except:
            logging.error("Unexpected error while loading hardware env file " + env)
        if os.path.exists(os.path.join(d, "yml")):
            try:
                with open(yml) as f:
                    hw_settings[-1]["yml"] = yaml.load(f, Loader=yaml.FullLoader)
            except:
                logging.error("Failed to load yml " + yml)
    return hw_settings


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    print("1", get_hw_packages("io"))
    print("2", get_hw_settings("cam"))
    print("3", get_hw_settings("cam", "/tmp"))

