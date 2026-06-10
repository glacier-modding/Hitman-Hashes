import json
import os
import argparse

parser = argparse.ArgumentParser(description="Generates pins.json from pins in CPPT.json.", allow_abbrev=False)
parser.add_argument('-o', '--output', type=str, default="pins.json", help="Output file name. Defaults to pins.json")
args = parser.parse_args()

pins_data = []

cppt_file = os.path.join("paths", "CPPT.json")

with open(cppt_file) as f:
    entities = json.load(f)

for entity in entities:
    pins = entity.get("pins")

    if pins and pins != "":
        pins_data.append({
            "hash": entity["hash"],
            "path": entity["path"],
            "in": sorted(
                pins.get("in", []),
                key=lambda e: e.get("pin", "").lower()
            ),
            "out": sorted(
                pins.get("out", []),
                key=lambda e: e.get("pin", "").lower()
            )
        })

pins_data.sort(key=lambda e: e["path"].lower())

with open(args.output, "w", newline='\n') as f:
    json.dump(pins_data, f, indent=4)

print("pins.json generated and sorted successfully!")
