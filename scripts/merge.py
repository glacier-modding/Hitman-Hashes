import json
import os
import argparse
from common_functions import *

parser = argparse.ArgumentParser(description="Merge JSON files and generates a hash list.")
parser.add_argument('version', type=int, help="Current version number to be embedded in the hash list.")
parser.add_argument('--game', choices=GAME_FLAGS.keys(), nargs='*', help="Game to generate the hash list for. Defaults to all.")
args = parser.parse_args()

if not args.game:
    args.game = list(GAME_FLAGS.keys())

input_directory = "paths"

json_files = [os.path.join(input_directory, f) for f in sorted(os.listdir(input_directory)) if f.endswith(".json")]

merged_data = []

total_hashes = 0
matching_hashes = 0

for json_file in json_files:
    with open(json_file, "r") as f:
        data = json.load(f)
        for entry in data:
            if entry.get('gameFlags') is None or not any(entry['gameFlags'] & GAME_FLAGS[game] for game in args.game):
                continue
            if entry.get('path'):
                path = entry['path']
            elif entry.get('hint'):
                path = entry['hint']
            else:
                path = ''
            
            total_hashes += 1
            calculated_hash = ioi_hash(path)
            if calculated_hash == entry['hash']:
                matching_hashes += 1
            merged_entry = f"{entry['hash']}.{os.path.basename(json_file).split('.')[0]},{path}"
            merged_data.append(merged_entry)

completion_percentage = (matching_hashes / total_hashes) * 100 if total_hashes else 0

comments = [
    f"# Hash list completion: {completion_percentage:.4f}%",
    f"# Hashes={total_hashes}",
    f"# CurrentVersion={args.version}"
]

def sort_key(entry):
    path = entry.split(",")[1]
    return (path == "", path)

merged_data.sort(key=sort_key)

with open("hash_list.txt", "w", newline='\n') as f:
    for comment in comments:
        f.write(comment + "\n")
    for entry in merged_data:
        f.write(entry + "\n")

print("Hash list merged and sorted successfully!")
