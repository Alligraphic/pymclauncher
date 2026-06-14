import json
import os
import requests

import helper


MC_VERSION = "26.1.2"
MC_PATH = os.path.abspath("./run/")
NEO_FORGE_VERSION = "neoforge-26.1.2.64-beta"

def download_libs(version, mc_path = MC_PATH):
    print(f"Downloading {version} libs...")
    with open(os.path.join(mc_path, "versions", version, f"{version}.json"), "r") as f:
        manifest = json.load(f)

    # get the libraries list from the json
    libraries = manifest["libraries"]

    libs =[]
    for lib in libraries:

        lib_path = lib["downloads"]["artifact"]["path"]
        lib_dir = os.path.dirname(lib_path)
        lib_name = os.path.basename(lib_path)
        lib_url = lib["downloads"]["artifact"]["url"]

        # create the dir if it doesn't exist
        if not os.path.exists(os.path.join(mc_path, f"libraries/{lib_dir}/")):
            os.makedirs(os.path.join(mc_path, f"libraries/{lib_dir}/"))

        # download the file from the url if it doesn't exist
        if not os.path.exists(os.path.join(mc_path, f"libraries/{lib_path}")):
            print("\tDownloading " + str(lib_name) + " from " + lib_url)
            helper.download_file(lib_url, os.path.join(mc_path, f"libraries/{lib_path}"))

        libs.append(os.path.abspath(os.path.join(mc_path, f"libraries/{lib_path}")))

    # save libs in a json file
    with open(os.path.join(mc_path, f"versions/{version}/libraries_{version}.json"), "w") as f:
        json.dump(libs, f, indent=4)


def main():
    download_libs(MC_VERSION)
    download_libs(NEO_FORGE_VERSION)


if __name__ == "__main__":
    main()
