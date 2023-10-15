import json
import os
from common_functions import *

output_directory = "paths"

GAME_FLAGS = {
    "alpha": 0b000001,
    "h1": 0b000010,
    "h2": 0b000100,
    "h3": 0b001000,
    "beta": 0b010000,
    "sa": 0b100000
}

def update_json(hash_val, hash_type, game_flags_str):
    game_flags = 0
    for flag_str in game_flags_str:
        game_flags |= GAME_FLAGS[flag_str]

    json_filename = os.path.join(output_directory, f"{hash_type}.json")

    data = []
    if os.path.exists(json_filename):
        with open(json_filename, 'r') as f:
            data = json.load(f)

        for entry in data:
            if entry["hash"] == hash_val:
                entry["gameFlags"] = game_flags
                break
        else:
            data.append({
                "hash": hash_val,
                "path": "",
                "gameFlags": game_flags
            })

    else:
        data.append({
            "hash": hash_val,
            "path": "",
            "gameFlags": game_flags
        })

    with open(json_filename, 'w', newline='\n') as f:
        json.dump(data, f, indent=2)

with open("new_hashes.txt", 'r') as f:
    for line in f:
        hash_with_type, game_flags_str = line.strip().split(':')
        game_flags_str = game_flags_str.split(',')

        hash_val, hash_type = infer_type(hash_with_type)

        if hash_type:
            update_json(hash_val, hash_type, game_flags_str)

print("Hashes and game flags updated successfully!")
