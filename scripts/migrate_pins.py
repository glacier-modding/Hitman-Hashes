import os
import json
import argparse

parser = argparse.ArgumentParser(description="Migrate pins", allow_abbrev=False)
parser.add_argument('-i', '--input', type=str, required=True, default="pins.json", help="pins.json file.")
args = parser.parse_args()

cppt_file = os.path.join("paths", "CPPT.json")

with open(cppt_file) as f:
    entities = json.load(f)

with open(os.path.join(args.input)) as f:
    pins_data = json.load(f)

pins = {
    entry["hash"]: {
        "in": entry["in"],
        "out": entry["out"]
    }
    for entry in pins_data
}

for entity in entities:
    if entity["hash"] in pins:
        entity["pins"] = pins[entity["hash"]]

with open(cppt_file, "w", newline='\n') as f:
    json.dump(entities, f, indent=2)