import json
import os
from common_functions import *

output_directory = "paths"

def update_data(data, hash_val, path_val):
    for entry in data.values():
        if entry["hash"] == hash_val:
            if ioi_hash(path_val) == hash_val:
                entry["path"] = path_val.lower()
                entry.pop("hint", None)
            else:
                if "path" in entry and entry["path"] != "":
                    print(f"Hash: {hash_val} already has a path {entry['path']}. Skipping addition of hint: {path_val.lower()}.")
                    continue
                entry["hint"] = path_val.lower()
            break

all_data = {}
for file_name in os.listdir(output_directory):
    if file_name.endswith(".json"):
        hash_type = file_name.split('.')[0]
        all_data[hash_type] = read_json_file(os.path.join(output_directory, file_name))

with open("new_paths.txt", 'r') as f:
    for line in f:
        parts = line.strip().split(',', 1)
        hash_with_type, path = parts[0], parts[1]
        
        hash_val, hash_type = infer_type(hash_with_type)
        
        if hash_type and hash_type in all_data:
            update_data(all_data[hash_type], hash_val, path)

for hash_type, data in all_data.items():
    write_json_file(os.path.join(output_directory, f"{hash_type}.json"), data)

print("Paths added successfully!")
