import json
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
