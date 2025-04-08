import os
import json
import argparse

parser = argparse.ArgumentParser(description="Generate LINE hints using the lines.json file from the https://github.com/glacier-modding/Hitman-l10n-Hashes repository", allow_abbrev=False)
parser.add_argument('-i', '--input', type=str, required=True, help="lines.json file.")
parser.add_argument('-o', '--output', type=str, required=False, default="line_hints.txt", help="Output file name. Defaults to line_hints.txt.")
args = parser.parse_args()

with open(args.input, "r") as file1:
    data_lines = json.load(file1)

with open(os.path.join("paths", "LINE.json")) as file2:
    data_line = json.load(file2)

for item in data_line:
    hash_value = item.get("hash")
    line_hash = item.get("lineHash")
    if line_hash in data_lines and data_lines[line_hash]:
        with open(args.output, "a") as f:
            f.write(f"{hash_value}.LINE,{data_lines[line_hash]}\n")
