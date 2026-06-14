import os
import json

import update_version_manifest
import create_user_profile
import instance_select
import create_dirs
import download_assets
import download_libs
import mc_run
import helper


MC_PATH = os.path.abspath("./run/")


def new_version():
    wants_download = helper.ask_yes_no("Do you want to download a new version of Minecraft?")

    if not wants_download:
        return wants_download

    version = update_version_manifest.download_manifest(MC_PATH)

    download_assets.download_assets(version, MC_PATH)
    download_libs.download_libs(version, MC_PATH)

    return wants_download


def select_mc_version():
    mc_versions = [
        d for d in os.listdir(os.path.join(MC_PATH, "versions"))
        if os.path.isdir(os.path.join(MC_PATH, "versions", d)) and d[0].isdigit()
    ]

    if not mc_versions:
        print("No Minecraft versions found")
        if not new_version():
            print("Please download a version of Minecraft to continue")
            return None

    mc_version = mc_versions[helper.choose(mc_versions)]

    if not os.path.exists(os.path.join(MC_PATH, "versions", mc_version, f"{mc_version}.jar")):
        with open(os.path.join(MC_PATH, "versions", mc_version, f"{mc_version}.json"), "r") as f:
            jar_url = json.load(f)["downloads"]["client"]["url"]
        print(f"Downloading {mc_version}.jar...")
        helper.download_file(jar_url, os.path.join(MC_PATH, "versions", mc_version, f"{mc_version}.jar"))

    return mc_version


def select_neoforge_version(mc_version):
    neoforge_versions = [
        d for d in os.listdir(os.path.join(MC_PATH, "versions"))
        if os.path.isdir(os.path.join(MC_PATH, "versions", d)) and d.startswith("neoforge") and mc_version in d
    ]
    if not neoforge_versions:
        print("No neoforge versions found")
        print("Please Install a neoforge version")
        return None

    return neoforge_versions[helper.choose(neoforge_versions)]


def select_instance():
    if helper.ask_yes_no("Do you want to select an existing instance?"):
        instances = instance_select.get_instance_list(MC_PATH)
        if len(instances) == 0:
            print("No instances found")
            return None, None, None
        instance = instances[helper.choose(instances)]
        mc_version, modloader = instance_select.get_instance_version(MC_PATH, instance)
        return mc_version, modloader, instance
    return None, None, None


def get_mc_version() -> tuple[str, str, str | None]:
    mc_version, modloader, instance = select_instance()
    if not mc_version or not modloader:
        mc_version = select_mc_version()
        modloader = select_neoforge_version(mc_version)

    if not helper.validate_mc_version(mc_version, MC_PATH):
        print("Invalid Minecraft version", mc_version)
        exit(1)

    if not helper.validate_mc_version(modloader, MC_PATH):
        print("Invalid Modloader version")
        exit(1)

    if 'neoforge' not in modloader:
        print("Selected modloader is not neoforge, launching this instance may cause crashes.")

    return str(mc_version), str(modloader), instance


def main():
    create_dirs.create_dirs(MC_PATH)

    username, client_token = create_user_profile.user_profile(MC_PATH)

    new_version()

    mc_version, neoforge_version, instance = get_mc_version()

    # download_libs.download_libs(neoforge_version)

    with open(os.path.join(MC_PATH, "versions", mc_version, f"{mc_version}.json"), "r") as f:
        asset_id = json.load(f)["assets"]

    mc_run.run_neo_forge(mc_version, neoforge_version, asset_id, MC_PATH, instance, username, client_token)


if __name__ == "__main__":
    main()
