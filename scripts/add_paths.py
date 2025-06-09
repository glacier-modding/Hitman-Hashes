import os
from common import infer_type, find_type, ioi_hash, read_json_file, write_json_file
import argparse

parser = argparse.ArgumentParser(description="Add paths/hints", allow_abbrev=False)
parser.add_argument('-i', '--input', type=str, required=False, default="new_paths.txt", help="File which contains new paths/hints to add.")
parser.add_argument('--overwrite-hints', action='store_true', help="Overwrite existing hints with new ones.")
parser.add_argument('--add-line-hashes', action='store_true', help="Add line hashes to the LINE paths file.")
parser.add_argument('--add-wemids', action='store_true', help="Add Wem IDs to the WWEM paths file.")
parser.add_argument('--add-entity-subtypes', action='store_true', help="Add subtype information to TEMP/TBLU path files.")
args = parser.parse_args()

output_directory = "paths"

modified_types = set()
paths_added = 0
hints_added = 0
hints_overwritten = 0

def update_data(data, hash_val, path_val):
    global paths_added
    global hints_added
    global hints_overwritten

    if not path_val:
        print(f"Path/Hint is empty for hash: {hash_val}. Skipping.")
        return

    if hash_val in data:
        entry = data[hash_val]
        if ioi_hash(path_val) == hash_val:
            if "path" not in entry or entry["path"] == "":
                paths_added += 1
            else:
                print("Already added:", entry["path"])
            entry["path"] = path_val
            entry.pop("hint", None)
            modified_types.add(hash_type)

        if args.add_entity_subtypes:
            entry["subType"] = path_val
            modified_types.add(hash_type)
        if args.add_line_hashes:
            entry["lineHash"] = path_val.upper()
            modified_types.add(hash_type)
        if args.add_wemids:
            entry["wemId"] = path_val
            modified_types.add(hash_type)

        if not args.add_entity_subtypes and not args.add_line_hashes and not args.add_wemids:
            if "path" in entry and entry["path"] != "":
                return
            else:
                if "hint" not in entry or entry["hint"] == "":
                    hints_added += 1
                    entry["hint"] = path_val
                    modified_types.add(hash_type)
                elif args.overwrite_hints:
                    hints_overwritten += 1
                    entry["hint"] = path_val
                    modified_types.add(hash_type)

all_data = {}
for file_name in os.listdir(output_directory):
    if file_name.endswith(".json"):
        hash_type = file_name.split('.')[0]
        all_data[hash_type] = read_json_file(os.path.join(output_directory, file_name))

with open(args.input, 'r') as f:
    for line in f:
        if line.startswith("["):
            hash_val = ioi_hash(line.strip())
            parts = [hash_val, line.strip()]
        else:
            parts = line.strip().split(',', 1)
        hash_with_type, path = parts[0].upper(), parts[1].lstrip().lower()
        
        hash_val, hash_type = infer_type(hash_with_type)
        
        if not hash_type:
            hash_type = find_type(hash_val, all_data)

        if hash_type and hash_type in all_data:
            update_data(all_data[hash_type], hash_val, path)

for hash_type, data in all_data.items():
    if hash_type in modified_types:
        write_json_file(os.path.join(output_directory, f"{hash_type}.json"), data)

if paths_added or hints_added or hints_overwritten:
    if paths_added > 0:
        print(f"{paths_added} new path(s) added successfully!")
    if hints_added > 0:
        print(f"{hints_added} new hint(s) added/modified successfully!")
    if hints_overwritten > 0:
        print(f"{hints_overwritten} hint(s) overwritten successfully!")
else:
    print("No new paths or hints added.")