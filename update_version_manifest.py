import json
import os

from helper import choose, download_json


VERSION_MANIFEST_URL = "https://launchermeta.mojang.com/mc/game/version_manifest.json"


# Downloads the manifest file
def download_version_manifest():
    print(f"Downloading version manifest...")
    download_json(VERSION_MANIFEST_URL, "version_manifest.json")


def download_manifest(mc_path):
    download_version_manifest()
    with open("version_manifest.json", "r") as f:
        versions = json.load(f)["versions"][:20]

    versions_names = [version["id"] for version in versions]
    print("Please select a version to download the manifest for:")
    version = versions[choose(versions_names)]
    print(f"Downloading {version['id']}.json...")
    json_dir = os.path.join(mc_path, "versions", version["id"])
    if not os.path.exists(json_dir):
        os.makedirs(json_dir)
    download_json(version["url"], os.path.join(json_dir, f"{version['id']}.json"))

    return version["id"]


def main():
    download_manifest("./run/")


if __name__ == "__main__":
    main()
