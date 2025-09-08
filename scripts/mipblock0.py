import os
import json
import argparse

parser = argparse.ArgumentParser(description="Mipblock0 paths")
parser.add_argument('-o', '--output', type=str, default="mipblock0.txt", help="Output file name. Defaults to mipblock0.txt.")
args = parser.parse_args()

with open(os.path.join("paths", "TEXD.json"), "r") as f:
    texd_data = json.load(f)

mipblock0_paths = []

for entry in texd_data:
    path = entry.get("path", "")
    if path and ".pc_mipblock1" in path:
        mipblock0 = path.replace(".pc_mipblock1", ".pc_mipblock0")
        mipblock0_paths.append(mipblock0)

with open(args.output, "w") as f:
    for item in mipblock0_paths:
        f.write(f"{item}\n")
