import os
from common import infer_type, ioi_hash, read_json_file, write_json_file

output_directory = "paths"

modified_types = set()
paths_added = 0
hints_added = 0

def update_data(data, hash_val, path_val):
    global paths_added
    global hints_added

    if not path_val:
        print(f"Path/Hint is empty for hash: {hash_val}. Skipping.")
        return

    for entry in data.values():
        if entry["hash"] == hash_val:
            if ioi_hash(path_val) == hash_val:
                if "path" not in entry or entry["path"] == "":
                    paths_added += 1
                entry["path"] = path_val
                entry.pop("hint", None)
                modified_types.add(hash_type)
            else:
                if "path" in entry and entry["path"] != "":
                    # print(f"Hash: {hash_val} already has a path {entry['path']}. Skipping addition of hint: {path_val}.")
                    continue
                else:
                    if "hint" not in entry or entry["hint"] == "":
                        hints_added += 1
                    entry["hint"] = path_val
                    modified_types.add(hash_type)
            break

all_data = {}
for file_name in os.listdir(output_directory):
    if file_name.endswith(".json"):
        hash_type = file_name.split('.')[0]
        all_data[hash_type] = read_json_file(os.path.join(output_directory, file_name))

with open("new_paths.txt", 'r') as f:
    for line in f:
        parts = line.strip().split(',', 1)
        hash_with_type, path = parts[0], parts[1].lstrip().lower()
        
        hash_val, hash_type = infer_type(hash_with_type)
        
        if hash_type and hash_type in all_data:
            update_data(all_data[hash_type], hash_val, path)

for hash_type, data in all_data.items():
    if hash_type in modified_types:
        write_json_file(os.path.join(output_directory, f"{hash_type}.json"), data)

if paths_added or hints_added:
    if paths_added > 0:
        print(f"{paths_added} new path(s) added successfully!")
    if hints_added > 0:
        print(f"{hints_added} new hint(s) added successfully!")
else:
    print("No new paths or hints added.")