import os
import json
import argparse

parser = argparse.ArgumentParser(description="Get subtypes for templates and blueprints", allow_abbrev=False)
parser.add_argument('-i', '--input', type=str, required=False, help="Path to folder containing QN entity.json files.")
parser.add_argument('-o', '--output', type=str, default="new_entity_subtypes.txt", help="Output file name. Defaults to new_entity_subtypes.txt.")
args = parser.parse_args()

matched_entities = set()

for dirpath, dirnames, filenames in os.walk(args.input):
    for filename in filenames:
        if filename.endswith('.entity.json'):
            full_path = os.path.join(dirpath, filename)
            
            with open(full_path, 'r') as file:
                data = json.load(file)

                subtype = data.get('subType')
                
                temp_hash = data.get('tempHash')
                if temp_hash:
                    matched_entities.add(f"{temp_hash}.TEMP,{subtype}")
                
                tblu_hash = data.get('tbluHash')
                if tblu_hash:
                    matched_entities.add(f"{tblu_hash}.TBLU,{subtype}")

with open(args.output, "w") as f:
    for entity in matched_entities:
        f.write(f"{entity}\n")