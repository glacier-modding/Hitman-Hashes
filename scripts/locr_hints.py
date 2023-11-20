import os
import json
import argparse

parser = argparse.ArgumentParser(description="Get hints for LOCR resources using zuitextentity entity names", allow_abbrev=False)
parser.add_argument("-i", "--input", type=str, required=True, help="Path to folder containing entity.json files.")
parser.add_argument("-o", "--output", type=str, default="locr_hints.txt", help="Output file name. Defaults to locr_hints.txt.")
args = parser.parse_args()

resources = set()

target_factory = "[modules:/zuitextentity.class].pc_entitytype"

for dirpath, dirnames, filenames in os.walk(args.input):
    for filename in filenames:
        if filename.endswith(".entity.json"):
            full_path = os.path.join(dirpath, filename)

            with open(full_path, "r") as file:
                data = json.load(file)

                for entity in data["entities"].values():
                    if entity.get("factory") == target_factory:
                        entity_name = entity.get("name")
                        text_list_resource = (
                            entity.get("properties", {})
                            .get("m_pTextListResource", {})
                            .get("value", {})
                            .get("resource")
                        )
                        if not text_list_resource.startswith("00"):
                            continue
                        if text_list_resource and entity_name:
                            resources.add(
                                f"{text_list_resource}.LOCR,{entity_name.replace(' ', '_')}"
                            )

with open(args.output, "w") as f:
    for resource in resources:
        f.write(f"{resource}\n")
