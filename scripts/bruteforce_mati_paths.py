import os
import json
import argparse
from common import ioi_hash

parser = argparse.ArgumentParser(description="Bruteforce MATI paths")
parser.add_argument("-o", "--output", type=str, default="bruteforced_mati_paths.txt", help="Output file name. Defaults to bruteforced_mati_paths.txt.")
args = parser.parse_args()

with open(os.path.join("paths", "MATI.json"), "r") as f:
    mati_data = json.load(f)

found = []
base_folders = set()

for entry in mati_data:
    path = entry.get("path", "")
    if path:
        base_folder = path[: path.rfind("/") + 1]
        base_folders.add(base_folder)

for entry in mati_data:
    hint = entry.get("hint", "")
    if not hint:
        continue

    for base_folder in base_folders:
        mati_path = f"{base_folder}{hint}.mi].pc_mi"

        if ioi_hash(mati_path) == entry["hash"]:
            print("FOUND: " + mati_path)
            found.append(mati_path)

with open(args.output, "w") as f:
    for item in found:
        f.write(f"{item}\n")

