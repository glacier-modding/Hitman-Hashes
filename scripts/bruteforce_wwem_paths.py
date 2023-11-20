import json
import argparse
from common import ioi_hash

parser = argparse.ArgumentParser(description="Bruteforce WWEM paths")
parser.add_argument("-o", "--output", type=str, default="new_wwem_paths.txt", help="Output file name. Defaults to new_wwem_paths.txt.")
parser.add_argument("--include-levels", action="store_true", help="Include level codenames.")
args = parser.parse_args()

with open("paths\\WWEM.json", "r") as f:
    wwem_data = json.load(f)

found = set()
max_attempts = 100
base_path = "[assembly:/sound/wwise/originals/sfx/"
level_codenames = (
    [
        "gecko",
        "bulldog",
        "fox",
        "llama",
        "rat",
        "wolverine",
        "stingray",
        "falcon",
        "raccoon",
        "seagull",
        "hawk",
        "magpie",
        "skunk",
        "mongoose",
        "hippo",
        "flamingo",
        "sheep",
        "snowcrane",
        "bull",
        "tiger",
        "spider",
        "octopus",
        "peacock",
        "dugong",
        "vanilla",
    ]
    if args.include_levels
    else [""]
)
conversion_names = [
    "vorbis quality high",
    "level_music_conversion_settings",
    "ingame_music_conversion_settings",
    "default conversion settings",
    "dialogue_conversion_settings",
    "music conversion settings",
    "default",
    "music",
    # "custom",
    # "level",
    # "ingame",
    # "level_music",
    # "ingame_music",
    # "amb",
    # "ambience",
]

for entry in wwem_data:
    if not entry.get("path") and "hint" in entry and "wemId" in entry:
        filename_hint = entry["hint"].split("/")[-1].split(".")[0]
        if filename_hint.startswith("play_"):
            filename_hint = filename_hint[5:]
        if filename_hint.endswith("_play"):
            filename_hint = filename_hint[:-5]
        # if filename_hint.endswith("_play_01"):
        #     filename_hint = filename_hint[:-8]
        # if "_play_" in filename_hint:
        #     filename_hint = filename_hint.replace("_play_", "_")

        wem_id = entry["wemId"]
        entry_hash = entry["hash"]

        for level_codename in level_codenames:
            codename_path = f"{level_codename}/" if level_codename else ""
            for conversion in conversion_names:
                full_path = f"{base_path}{codename_path}{filename_hint}.wav]({conversion},{wem_id}).pc_wem"
                # print(full_path)
                if ioi_hash(full_path) == entry_hash:
                    found.add(f"{entry_hash}.WWEM,{full_path}")
                    break

                for i in range(1, max_attempts):
                    numbered_filename_hint = f"{filename_hint}_{i:02}"
                    full_path = f"{base_path}{codename_path}{numbered_filename_hint}.wav]({conversion},{wem_id}).pc_wem"
                    # print(full_path)
                    if ioi_hash(full_path) == entry_hash:
                        found.add(f"{entry_hash}.WWEM,{full_path}")
                        break

with open(args.output, "w") as f:
    for path in found:
        f.write(f"{path}\n")
