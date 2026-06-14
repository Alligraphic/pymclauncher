import requests
import os
import json
from tqdm import tqdm

import helper

BASE_URL = "https://resources.download.minecraft.net"


def download_asset(hash_value, mc_dir):
    subdir = hash_value[:2]
    url = f"{BASE_URL}/{subdir}/{hash_value}"

    path = os.path.join(mc_dir, "assets", "objects", subdir, hash_value)
    os.makedirs(os.path.dirname(path), exist_ok=True)

    if not os.path.exists(path):
        r = requests.get(url)
        with open(path, "wb") as f:
            f.write(r.content)


def download_assets(version, mc_dir):
    with open(os.path.join(mc_dir, "versions", version, f"{version}.json"), "r") as f:
        version_data = json.load(f)

    asset_index = version_data["assetIndex"]["id"]

    if not os.path.exists(os.path.join(mc_dir, "assets", "indexes", f"{asset_index}.json")):
        asset_index_url = version_data["assetIndex"]["url"]
        helper.download_json(asset_index_url, os.path.join(mc_dir, "assets", "indexes", f"{asset_index}.json"))

    with open(os.path.join(mc_dir, "assets", "indexes", f"{asset_index}.json"), "r") as f:
        indexes = json.load(f)

    objects = indexes["objects"]
    for obj in tqdm(objects.keys()):
        obj_hash = objects[obj]["hash"]
        download_asset(obj_hash, mc_dir)


def main():
    download_assets("26.1.2", "./run/")


if __name__ == "__main__":
    main()
