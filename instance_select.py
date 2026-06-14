import json
import os


def get_instance_list(mc_path):
    mc_path = os.path.join(mc_path, 'versions/instances/')
    instances = []
    for item in os.listdir(mc_path):
        if os.path.isdir(os.path.join(mc_path, item)):
            instances.append(item)
    return instances


def get_instance_version(mc_path, instance_name):
    instance_path = os.path.join(mc_path, 'versions/instances/', instance_name)
    if os.path.exists(instance_path):
        try:
            with open(os.path.join(instance_path, 'manifest.json'), 'r') as f:
                data = json.load(f)
            return data['minecraft']['version'], data['minecraft']['modLoaders'][0]['id']
        except FileNotFoundError:
            print("manifest.json not found for instance:", instance_name)

    return None, None


if __name__ == '__main__':
    print(get_instance_list("./run/"))