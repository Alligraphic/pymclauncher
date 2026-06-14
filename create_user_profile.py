import json
import uuid
import os


def create_user_profile(username, mc_path):
    data = {'clientToken': str(uuid.uuid4()), 'username': username, 'profiles': {}}
    with open(os.path.join(mc_path, 'launcher_profiles.json'), 'w') as f:
        json.dump(data, f)


def get_username_uuid(mc_path):
    with open(os.path.join(mc_path, 'launcher_profiles.json'), 'r') as f:
        data = json.load(f)
    return data['username'], data['clientToken']

def user_profile(mc_path):
    try:
        username, client_token = get_username_uuid(mc_path)
        print(f"Username: {username}, Client Token: {client_token}")
    except FileNotFoundError:
        print("No user profile found. Please create one.")
        username = input("Enter your Minecraft username: ")
        create_user_profile(username, mc_path)
        print("User profile created successfully.")
        username, client_token = get_username_uuid(mc_path)
        print(f"Username: {username}, Client Token: {client_token}")

    return username, client_token