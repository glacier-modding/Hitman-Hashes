import os
import json
import argparse

parser = argparse.ArgumentParser(description="Get hints for templates and blueprints")
parser.add_argument('--input', type=str, required=False, help="Path to folder containing QN entity.json files.")
parser.add_argument('--output', type=str, default="new_entity_hints.txt", help="Output folder and/or name. Defaults to new_entity_hints.txt.")
args = parser.parse_args()

matched_entities = []

# Linked templates + geometry templates blueprint hashes
ignored_blueprints = {
    '00B4FF13E74E586F', '00F4A1A8B9394135', '00F5C5148B9F676D', '0055940FD55AFF09', 
    '00E9D42DAEBE559B', '00181EBCF53A405D', '008130A85A690BE8', '00C7E348A80A6E6E', 
    '002E141E1B1C6EFE'
}

for dirpath, dirnames, filenames in os.walk(args.input):
    for filename in filenames:
        if filename.endswith('.entity.json'):
            full_path = os.path.join(dirpath, filename)
            
            with open(full_path, 'r') as file:
                data = json.load(file)

                should_skip = data.get('tbluHash') in ignored_blueprints
                if should_skip:
                    continue

                root_entity_key = data.get('rootEntity')
                if root_entity_key:
                    root_entity = data['entities'].get(root_entity_key)
                    root_entity_name = root_entity.get('name', '')
                else:
                    continue
                
                temp_hash = data.get('tempHash')
                if temp_hash:
                    matched_entities.append(f"{temp_hash}.TEMP,{root_entity_name}")
                
                tblu_hash = data.get('tbluHash')
                if tblu_hash:
                    matched_entities.append(f"{tblu_hash}.TBLU,{root_entity_name}")

with open(args.output, "w") as f:
    for entity in matched_entities:
        f.write(f"{entity}\n")