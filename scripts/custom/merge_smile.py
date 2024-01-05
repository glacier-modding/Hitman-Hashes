import json
import os
import argparse
from newsmile import SmileEncoder
import brotli

parser = argparse.ArgumentParser(description="Merge JSON files and generate a hash list in Smile binary format. Just TEMP and TBLU.", allow_abbrev=False)
parser.add_argument('version', type=int, help="Current version number to be embedded in the hash list.")
parser.add_argument('-o', '--output', type=str, default="entity_hash_list.sml", help="Output Smile binary file name. Defaults to entity_hash_list.sml.")
args = parser.parse_args()

input_directory = "paths"

allowed_json_files = ['TEMP.json', 'TBLU.json']

merged_data = []

for json_file_name in allowed_json_files:
    json_file = os.path.join(input_directory, json_file_name)
    if not os.path.exists(json_file):
        continue

    with open(json_file, "r") as f:
        data = json.load(f)

        for entry in data:
            merged_entry = {
                'hash': entry['hash'],
                'resourceType': os.path.splitext(json_file_name)[0],
                'path': entry.get('path', ''),
                'hint': entry.get('hint', ''),
                'gameFlags': entry['gameFlags']
            }
            merged_data.append(merged_entry)

smile_encoder = SmileEncoder()
smile_encoded_data = smile_encoder.encode({
    "version": args.version,
    "entries": merged_data
})

compressed_data = brotli.compress(smile_encoded_data)

with open(args.output, "wb") as f:
    f.write(compressed_data)

print("Hash list merged and encoded in Smile binary format successfully!")
