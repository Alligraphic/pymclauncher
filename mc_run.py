import subprocess
import os
import json

import helper

JAVA_PATH = "javaw"  # or full path to java.exe
MC_DIR = os.path.abspath("./run/")
MC_VERSION = "26.1.2"
ASSET_INDEX = 30

NEO_FORGE_VERSION = "neoforge-26.1.2.64-beta"


def build_classpath(mc_version, modloader_version, mc_path=MC_DIR):
    with open(os.path.join(mc_path, "versions", mc_version, f"libraries_{mc_version}.json"), "r") as f:
        mc_libraries = json.load(f)

    with open(os.path.join(mc_path, "versions", modloader_version, f"libraries_{modloader_version}.json"), "r") as f:
        modloader_libraries = json.load(f)

    classpath_seperator = ";" # TODO: check for os this works for windows only

    classpath = classpath_seperator.join(list(set(mc_libraries + modloader_libraries)))
    return classpath


def run_neo_forge(
        mc_version,
        modloader_version,
        asset_index,
        mc_path=MC_DIR,
        instance=MC_DIR,
        username='Player',
        client_token="00000000-0000-0000-0000-000000000000",
        java_path=JAVA_PATH,
        ram=10
):
    classpath = build_classpath(mc_version, modloader_version, mc_path=mc_path)

    if not instance:
        instance_path = mc_path
    else:
        instance_path = os.path.join(mc_path, "versions", "instances", instance)

    # options = {
    #     "username": username,
    # }
    #
    # command = minecraft_launcher_lib.command.get_minecraft_command(
    #     modloader_version,
    #     mc_path,
    #     options
    # )
    #
    # for line in command:
    #     print(f'"{line}",')

    command = [
        java_path,
        "--show-module-resolution",
        f"-Xmx{ram}G",
        # "-XX:+UseZGC",
    ]

    atm_args = [
        "-XX:+UnlockExperimentalVMOptions",
        "-XX:+UseG1GC",
        "-XX:G1NewSizePercent=20",
        "-XX:G1ReservePercent=20",
        "-XX:MaxGCPauseMillis=50",
        "-XX:G1HeapRegionSize=32M",
        "-XX:+UseStringDeduplication",
        "-XX:+UseCompactObjectHeaders",
    ]
    classpath_arg = [
        '-cp',  # classpath
        classpath,
    ]
    jvm_args = helper.get_jvm_args(mc_path, modloader_version)
    main_class = helper.get_main_class(mc_path, modloader_version)
    options = [
        # options
        '--username', username,
        '--version', modloader_version,
        '--gameDir', instance_path,
        '--assetsDir', os.path.join(mc_path, 'assets'),
        '--assetIndex', f'{asset_index}',
        '--uuid', client_token,
        '--accessToken', '{token}',
        '--clientId', client_token,
        '--xuid', '${auth_xuid}',
        '--versionType', 'release',
    ]
    game_args = helper.get_game_args(mc_path, modloader_version)

    command = command + atm_args + classpath_arg + jvm_args + main_class + options + game_args

    # for line in command:
    #     print(f'"{line}",')

    env = os.environ.copy()

    # Force NVIDIA GPU
    env["SHIM_MCCOMPAT"] = "0x800000001"
    env["SHIM_RENDERING_MODE"] = "ENABLE"

    subprocess.run(command, cwd=instance_path, env=env)


def main():
    run_neo_forge(MC_VERSION, NEO_FORGE_VERSION, ASSET_INDEX)


if __name__ == "__main__":
    main()
