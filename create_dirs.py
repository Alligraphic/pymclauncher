import os

from helper import create_dir

def create_dirs(mc_path):
    create_dir(mc_path)
    dirs = [
        'assets/indexes/',
        'assets/objects/',
        'libraries/',
        'versions/',
        'versions/instances/',
    ]
    for directory in dirs:
        create_dir(os.path.join(mc_path, directory))


if __name__ == "__main__":
    create_dirs("./run/")