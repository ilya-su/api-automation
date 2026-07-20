import pathlib

import yaml


def read_yaml(file):
    file = pathlib.Path(__file__).parent.parent / 'test_data' / file
    with open(file, 'r', encoding='utf-8') as f:
        values =  yaml.safe_load(f)
    return values