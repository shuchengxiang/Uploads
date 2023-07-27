import os
import json
import yaml

def load_json_data(filename):
    with open(filename,'r', encoding="utf-8") as f:
        return json.load(f)

def load_yaml_data(filename):
    with open(filename, 'r', encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_txt_data(filename):
    with open(filename, 'r', encoding="utf-8") as f:
        return f.read()

def write_json_data(filename, data):
    parent_dir = os.path.abspath(os.path.dirname(filename))
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def write_yaml_data(filename, data):
    parent_dir = os.path.abspath(os.path.dirname(filename))
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)
    with open(filename, 'w') as f:
        yaml.safe_dump(data, f)

def write_txt_data(filename, data):
    parent_dir = os.path.abspath(os.path.dirname(filename))
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)
    with open(filename, 'w') as f:
        return f.write(str(data))