import json
import os
from common import ioi_hash
import argparse

parser = argparse.ArgumentParser(description="Bruteforce DLGE paths", allow_abbrev=False)
parser.add_argument('-i', '--input', type=str, required=False, default="DLGEs.JSON", help="Path to DLGEs.JSON. Extract using rpkg-cli: .\\rpkg-cli.exe -dev_dlge_names")
parser.add_argument('-o', '--output', type=str, default="new_dlge_paths.txt", help="Output file name. Defaults to new_dlge_paths.txt.")
args = parser.parse_args()

found = []

with open(args.input, "r") as f:
    dlges = json.load(f)

    for dlge in dlges:
        foundIt = False
        for depend in dlges[dlge]:
            if not foundIt and ".wav" in depend:
                d = depend[depend.find("/voices/english(us)")+19:depend.rfind(".wav")]
                shortPaths = d.split("_")
                sweetDialogItem = d.rsplit('/', 1)[-1]

                for s in range(len(shortPaths)):
                    shortPath = "_".join(shortPaths[:s+1])

                    dlgePath = f"[assembly:/localization/hitman6/conversations{shortPath}.sweetdialog].pc_dialogevent"
                    dlgePathDialogItem = f"[assembly:/localization/hitman6/conversations{shortPath}.sweetdialog?/{sweetDialogItem}.sweetdialogitem].pc_dialogevent"

                    if dlge == ioi_hash(dlgePath) or dlge == ioi_hash(dlgePathDialogItem):
                        found.append(f"{dlge}.DLGE,{dlgePath if dlge == ioi_hash(dlgePath) else dlgePathDialogItem}")
                        foundIt = True
                        break

with open(args.output, "w") as f:
    for item in found:
        f.write(f"{item}\n")