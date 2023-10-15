# Hitman-Hashes

## Game flags
| Game    | Bit Representation (Binary) |
|---------|-----------------------------|
| inAlpha | 0b000001                    |
| inH1    | 0b000010                    |
| inH2    | 0b000100                    |
| inH3    | 0b001000                    |
| inBeta  | 0b010000                    |
| inSA    | 0b100000                    |

## Scripts
This repository contains two main scripts merge.py and add_paths.py. They must be ran from the repository's root directory like `python ./scripts/add_paths.py`.

### merge.py
Generates the hash_list.txt. Takes a version number as an argument.

### add_paths.py
Adds paths to their assoicated hashes within the path's JSON files.

Requires a `new_paths.txt` file in the repository's root directory which contains data structured like:
```
000A4FB9B5FDAB19.WSGT,[assembly:/sound/wwise/exportedwwisedata/states/levelspecific_states/paris/fashionshowmusic_level_state.wwisestategroup].pc_entitytype
004B66043E12A8E3.WSGB,[assembly:/sound/wwise/exportedwwisedata/states/levelspecific_states/paris/fashionshowmusic_level_state.wwisestategroup].pc_entityblueprint
005EA1E72FC62DEC.WSGT,[assembly:/sound/wwise/exportedwwisedata/states/levelspecific_states/paris/paris_rain_puddle_state.wwisestategroup].pc_entitytype
0054C5081030A3D0.WSGB,[assembly:/sound/wwise/exportedwwisedata/states/levelspecific_states/paris/paris_rain_puddle_state.wwisestategroup].pc_entityblueprint
```
