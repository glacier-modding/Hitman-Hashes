import json
import argparse
from common import ioi_hash

parser = argparse.ArgumentParser(description="Bruteforce PRIMs to ECPT/ECPB paths")
parser.add_argument('-o', '--output', type=str, default="bruteforced_ecpt_paths.txt", help="Output file name. Defaults to bruteforced_ecpt_paths.txt.")
args = parser.parse_args()

with open("paths\\PRIM.json", "r") as f:
    prim_data = json.load(f)

with open("paths\\ECPT.json", "r") as f:
    ecpt_data = json.load(f)

with open("paths\\ECPB.json", "r") as f:
    ecpb_data = json.load(f)

ecpt_hashes = {entry["hash"] for entry in ecpt_data}
ecpb_hashes = {entry["hash"] for entry in ecpb_data}
found = []

for entry in prim_data:
    path = entry.get("path", "")
    if path and ".prim]" in path:
        ecpt_path = path.replace(".prim]", ".mat]").replace(".pc_prim", ".pc_entitytype")
        ecpt_hash = ioi_hash(ecpt_path)
        
        if ecpt_hash in ecpt_hashes:
            print("FOUND: " + ecpt_path)
            found.append(ecpt_path)
        
        ecpb_path = ecpt_path.replace(".pc_entitytype", ".pc_entityblueprint")
        ecpb_hash = ioi_hash(ecpb_path)
        
        if ecpb_hash in ecpb_hashes:
            print("FOUND: " + ecpb_path)
            found.append(ecpb_path)

with open(args.output, "w") as f:
    for item in found:
        f.write(f"{item}\n")
