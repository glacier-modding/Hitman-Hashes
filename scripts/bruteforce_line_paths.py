import json
from common import ioi_hash
import argparse

# This script isn't the best way to do this, but it works.
# It would have been better to check which LOCRs had paths and then check if they had any LINE dependencies.
# But I have no way of doing that in this repository.

parser = argparse.ArgumentParser(description="Bruteforce LINE paths")
parser.add_argument('-o', '--output', type=str, default="new_line_paths.txt", help="Output file name. Defaults to new_line_paths.txt.")
args = parser.parse_args()

with open("paths\\LOCR.json", "r") as f:
    locr_data = json.load(f)

with open("paths\\LINE.json", "r") as f:
    line_data = json.load(f)

found = []

for locr_entry in locr_data:
    locr_base_path = locr_entry["path"].rsplit('].', 1)[0]

    for line_entry in line_data:
        if "hint" in line_entry and line_entry["path"] == "":
            line_path = f"{locr_base_path}?/{line_entry['hint']}.sweetline].pc_sweetline"
            line_path_old_style = f"{locr_base_path}?{line_entry['hint']}.sweetline].pc_sweetline"

            if ioi_hash(line_path) == line_entry["hash"]:
                found.append(f"{line_entry['hash']}.LINE,{line_path}")
            elif ioi_hash(line_path_old_style) == line_entry["hash"]:
                found.append(f"{line_entry['hash']}.LINE,{line_path_old_style}")

with open(args.output, "w") as f:
    for item in found:
        f.write(f"{item}\n")
