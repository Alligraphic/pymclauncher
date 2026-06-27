import json
import os

import requests


def choose(options: list[str]) -> int:
    for pos, text in enumerate(options):
        print(f"{pos + 1}: {text}")

    while True:
        try:
            answer = int(input(f"Select[1-{len(options)}]:")) - 1
            if 0 <= answer < len(options):
                return answer
        except ValueError:
            pass


def ask_yes_no(text: str) -> bool:
    while True:
        answer = input(f"{text}[y/n]:").strip().upper()

        if answer == "Y":
            return True
        elif answer == "N":
            return False
        else:
            print("Invalid answer. Use y or n.")


def download_file(url: str, path: str):
    response = requests.get(url)
    with open(path, "wb") as f:
        f.write(response.content)


def download_json(url: str, path: str):
    response = requests.get(url)
    json_data = response.json()
    with open(path, "w") as f:
        json.dump(json_data, f, indent=4)


def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def validate_mc_version(version: str | None, mc_path) -> bool:
    if version is None:
        return False
    else:
        # return true if the version folder exists
        return os.path.exists(os.path.join(mc_path, "versions", version))


def get_game_args(mc_path: str, version: str) -> list[str]:
    with open(os.path.join(mc_path, "versions", version, f"{version}.json"), "r") as f:
        data = json.load(f)
    game_args = data["arguments"]["game"]
    return game_args


def get_jvm_args(mc_path: str, version: str) -> list[str]:
    with open(os.path.join(mc_path, "versions", version, f"{version}.json"), "r") as f:
        data = json.load(f)
    jvm_args = data["arguments"]["jvm"]

    classpath_seperator = ";" # TODO: check for os this works for windows only

    for arg_idx in range(len(jvm_args)):
        jvm_args[arg_idx] = (
            jvm_args[arg_idx]
                .replace("${version_name}", version)
                .replace("${library_directory}", f"{os.path.join(mc_path, 'libraries')}")
                .replace("${classpath_separator}", classpath_seperator)
        )

    return jvm_args


def get_main_class(mc_path: str, version: str) -> list[str]:
    with open(os.path.join(mc_path, "versions", version, f"{version}.json"), "r") as f:
        data = json.load(f)
    main_class = data["mainClass"]
    return [main_class]
