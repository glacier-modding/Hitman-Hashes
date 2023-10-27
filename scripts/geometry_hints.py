import os
import json
import re
from collections import defaultdict

dir_path = 'H:\\Tools\\rpkg\\QN\\' # QN files must not have any paths in them

temp_references = defaultdict(lambda: defaultdict(int))

# Removes numbers from the end of the entity name
pattern = re.compile(r'(_\d+|\d+)$')

for dirpath, dirnames, filenames in os.walk(dir_path):
    for filename in filenames:
        if filename.endswith('.entity.json'):
            full_path = os.path.join(dirpath, filename)
            
            with open(full_path, 'r') as file:
                data = json.load(file)
                
                for entity in data['entities'].values():
                    blueprint = entity.get('blueprint', '')
                    # Linked templates + geometry templates blueprint hashes
                    if blueprint.endswith('00B4FF13E74E586F') or blueprint.endswith('00F4A1A8B9394135') or blueprint.endswith('00F5C5148B9F676D') or blueprint.endswith('0055940FD55AFF09') or blueprint.endswith('00E9D42DAEBE559B') or blueprint.endswith('00181EBCF53A405D') or blueprint.endswith('008130A85A690BE8') or blueprint.endswith('00C7E348A80A6E6E') or blueprint.endswith('002E141E1B1C6EFE'):
                        name = pattern.sub('', entity.get('name', ''))
                        factory = entity.get('factory', '')
                        temp_references[factory][name] += 1

# Get the most frequently entity name (should make the hints more accurate)
matched_entities = {}
for factory, names in temp_references.items():
    most_frequent_name = max(names, key=names.get)
    matched_entities[factory] = f"{factory}.TEMP,{most_frequent_name}"

for entity in matched_entities.values():
    print(entity)