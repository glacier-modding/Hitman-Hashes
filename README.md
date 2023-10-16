# Hitman-Hashes
<!-- TOTAL_COMPLETION_BADGE_START -->
![Completion Badge](https://img.shields.io/badge/Total%20Completion-69.93%-red)
<!-- TOTAL_COMPLETION_BADGE_END -->
## Statistics
See [STATISTICS.md](STATISTICS.md).

## Game flags
| Game  | Bit Representation (Binary) |
| ----- | --------------------------- |
| Alpha | 0b000001                    |
| H1    | 0b000010                    |
| H2    | 0b000100                    |
| H3    | 0b001000                    |
| Beta  | 0b010000                    |
| SA    | 0b100000                    |

## Scripts
This repository contains three main scripts merge.py, add_paths.py and add_new_hashes.py. They must be ran from the repository's root directory like `python ./scripts/add_paths.py`.

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

### add_new_hashes.py
Adds new hashes into the JSON files.

Requires a `new_hashes.txt` file in the repository's root directory which contains data structured like:

```
000A4FB9B5FDAB19.WSGT:h3
004B66043E12A8E3.WSGB:h3
005EA1E72FC62DEC.WSGT:h3
0054C5081030A3D0.WSGB:h3
003B993A25498AE6.AIBB:h2,h3
```

Possible games are: `alpha`, `h1`, `h2`, `h3`, `beta` and `sa`.