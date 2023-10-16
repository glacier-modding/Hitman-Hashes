import json
import os
from common_functions import *

output_directory = "paths"

def update_json(hash_val, path_val, hash_type):
    json_filename = os.path.join(output_directory, f"{hash_type}.json")
    
    if os.path.exists(json_filename):
        with open(json_filename, 'r') as f:
            data = json.load(f)

        for entry in data:
            if entry["hash"] == hash_val:
                if ioi_hash(path_val) == hash_val:
                    entry["path"] = path_val.lower()
                    entry.pop("hint", None)  
                else:
                    entry["hint"] = path_val.lower()
                break

        with open(json_filename, 'w', newline='\n') as f:
            json.dump(data, f, indent=2)
    else:
        return

with open("new_paths.txt", 'r') as f:
    for line in f:
        parts = line.strip().split(',')
        hash_with_type, path = parts[0], parts[1]
        
        hash_val, hash_type = infer_type(hash_with_type)
        
        if hash_type:
            update_json(hash_val, path, hash_type)

print("Paths added successfully!")
