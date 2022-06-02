#!/usr/bin/env python3
import os, sys

from pathlib import Path
from configparser import ConfigParser

AWS_CREDENTIAL_PATH = os.path.join(Path.home(),'.aws','credentials')

def read_config(path):
    config = ConfigParser()
    config.read(path)
    return config

def write_config(path, config):
    with open(path, "w") as destination:
        config.write(destination)

def set_default_profile(profile_id):
    config = read_config(AWS_CREDENTIAL_PATH)
    if config.has_section(profile_id):
        if config.has_section("default"):
            config.remove_section("default")
        config.add_section("default")
        config.set("default", "region", config.get(profile_id, 'region'))
        config.set("default", "aws_access_key_id", config.get(profile_id, 'aws_access_key_id'))
        config.set("default", "aws_secret_access_key ", config.get(profile_id, 'aws_secret_access_key'))
        config.set("default", "aws_session_token", config.get(profile_id, 'aws_session_token'))
        write_config(AWS_CREDENTIAL_PATH, config)
    elif profile_id == 'none' and config.has_section('default'):
        config.remove_section('default')
        write_config(AWS_CREDENTIAL_PATH, config)
    else:
        print("Profile not found:", profile_id)

def get_profiles():
    config = read_config(AWS_CREDENTIAL_PATH)
    if (config.has_section('default')):
        config.remove_section('default')
    return config.sections()

def main():
    if len(sys.argv) < 2:
        profiles = get_profiles()
        profiles.insert(0, 'None (Delete default profile)')
        for i, item in enumerate(profiles):
            print(i, item)
        profile_index = int(input('Select a profile to set as default: '))
        while profile_index < 0 or profile_index >= len(profiles):
            print("Invalid profile.")
            profile_index = int(input('Select a profile to set as default: '))
        if profile_index == 0:
            profile_id = 'none'
        else:
            profile_id = profiles[profile_index]
    else:
        profile_id = sys.argv[1]

    print('Set', profile_id, 'as default')
    set_default_profile(profile_id)
