import os
import json
import argparse
from common import ioi_hash

parser = argparse.ArgumentParser(description="Bruteforce TEMP paths")
parser.add_argument('-o', '--output', type=str, default="bruteforced_temp_paths.txt", help="Output file name. Defaults to bruteforced_temp_paths.txt.")
args = parser.parse_args()

with open(os.path.join("paths", "TEMP.json"), "r") as f:
    temp_data = json.load(f)

found = []
base_paths = set()

for entry in temp_data:
    path = entry.get("path", "")
    if path and ".template?" in path:
        base_path = path.split(".entitytemplate")[0]
        base_path = base_path[:base_path.rfind("/") + 1]
        base_paths.add(base_path)

template_path_end = ".entitytemplate].pc_"

for entry in temp_data:
    hint = entry.get("hint", "")
    if not hint:
        continue 
    
    for base_path in base_paths:
        path_entitytype = f"{base_path}{hint}{template_path_end}entitytype"
        path_entitytemplate = f"{base_path}{hint}{template_path_end}entitytemplate"
        
        if ioi_hash(path_entitytype) == entry["hash"]:
            print("FOUND: " + path_entitytype)
            found.append(f"{path_entitytype}")
            found.append(f"{base_path}{hint}{template_path_end}entityblueprint")
        if ioi_hash(path_entitytemplate) == entry["hash"]:
            print("FOUND: " + path_entitytemplate)
            found.append(f"{path_entitytemplate}")
            found.append(f"{base_path}{hint}{template_path_end}entityblueprint")

with open(args.output, "w") as f:
    for item in found:
        f.write(f"{item}\n")
