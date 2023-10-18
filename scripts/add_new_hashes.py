import json
import os
from common_functions import *

output_directory = "paths"

def update_data(data, hash_val, game_flags):
    if hash_val not in data:
        data[hash_val] = {"hash": hash_val, "path": "", "gameFlags": 0}
    data[hash_val]["gameFlags"] |= game_flags

def read_json_file(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            entries = json.load(f)
            return {entry["hash"]: entry for entry in entries}
    return {}

def write_json_file(filename, data):
    with open(filename, 'w', newline='\n') as f:
        json.dump(list(data.values()), f, indent=2)

all_data = {}
for file_name in os.listdir(output_directory):
    if file_name.endswith(".json"):
        hash_type = file_name.split('.')[0]
        all_data[hash_type] = read_json_file(os.path.join(output_directory, file_name))

with open("new_hashes.txt", 'r') as f:
    for line in f:
        hash_with_type, game_flags_str = line.strip().split(':')
        game_flags_str = game_flags_str.split(',')
        game_flags = sum(GAME_FLAGS[flag_str] for flag_str in game_flags_str)

        hash_val, hash_type = infer_type(hash_with_type)

        if hash_type:
            update_data(all_data.setdefault(hash_type, {}), hash_val, game_flags)

for hash_type, data in all_data.items():
    write_json_file(os.path.join(output_directory, f"{hash_type}.json"), data)

print("Hashes and game flags updated successfully!")
