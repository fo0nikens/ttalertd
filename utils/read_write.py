#! /usr/bin/python3
# James Loye Colley
import json
import yaml
from os.path import isfile


def read_data(path):
    if 'credentials' not in path:
        with open(path) as file_in:
            return json.load(file_in)
    with open(path, 'r') as yml_in:
        return yaml.load(yml_in)['twilio']


def write_data(path, data):
    with open(path, 'w') as file_out:
        json.dump(data, file_out)


def default_values():
    with open('utils/credentials.yml', 'r') as yml_in:
        return yaml.load(yml_in)['defaults']


def files_exist():
    path1 = 'utils/memory.json'
    path2 = 'utils/credentials.yml'
    return isfile(path1) and isfile(path2)


def get_structure():
    return {
        "users": [],
        "load_averages": 0,
        "number_of_users": 0,
        "cmds": [],
        "iterations": 0
    }
