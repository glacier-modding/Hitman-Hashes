import json
import os
import argparse
from common import GAME_FLAGS, ioi_hash

parser = argparse.ArgumentParser(description="Merge JSON files and generates a hash list.", allow_abbrev=False)
parser.add_argument('version', type=int, help="Current version number to be embedded in the hash list.")
parser.add_argument('-g', '--game', choices=GAME_FLAGS.keys(), nargs='*', help="Game to generate the hash list for. Defaults to all.")
parser.add_argument('-o', '--output', type=str, default="hash_list.txt", help="Output file name. Defaults to hash_list.txt.")
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

        resource_type = os.path.basename(json_file).split('.')[0]

        for entry in data:
            if entry.get('gameFlags') is None or not any(entry['gameFlags'] & GAME_FLAGS[game] for game in args.game):
                continue
            if entry.get('path'):
                path = entry['path']
            elif entry.get('hint'):
                path = entry['hint']
            else:
                path = ''

            extra_str = ''

            if resource_type == 'LINE' and entry['path'] == "":
                extra_str = f"({entry['lineHash']})" if 'lineHash' in entry else ''
            if entry.get('hint') and entry['hint'] != "":
                extra_str = f" ({entry['lineHash']})" if 'lineHash' in entry else ''
            
            if resource_type == 'TEMP' and entry['path'] == "":
                extra_str = f"({entry['subType']})" if 'subType' in entry else ''
            if entry.get('hint') and entry['hint'] != "":
                extra_str = f" ({entry['subType']})" if 'subType' in entry else ''

            if resource_type == 'TBLU' and entry['path'] == "":
                extra_str = f"({entry['subType']})" if 'subType' in entry else ''
            if entry.get('hint') and entry['hint'] != "":
                extra_str = f" ({entry['subType']})" if 'subType' in entry else ''

            total_hashes += 1
            calculated_hash = ioi_hash(path)
            if calculated_hash == entry['hash']:
                matching_hashes += 1

            merged_entry = f"{entry['hash']}.{resource_type},{path}{extra_str}"
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

with open(args.output, "w", newline='\n') as f:
    for comment in comments:
        f.write(comment + "\n")
    for entry in merged_data:
        f.write(entry + "\n")

print("Hash list merged and sorted successfully!")
