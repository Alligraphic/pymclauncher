from helper import create_dir

def create_dirs():
    dirs = [
        './run/assets/indexes/',
        './run/assets/objects/',
        './run/libraries/',
        './run/versions/'
    ]
    for directory in dirs:
        create_dir(directory)


if __name__ == "__main__":
    create_dirs()
