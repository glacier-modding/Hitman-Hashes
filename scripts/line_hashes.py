import os
import argparse
import struct

parser = argparse.ArgumentParser(description="Get LINE hashes from LINE files", allow_abbrev=False)
parser.add_argument('-i', '--input', type=str, required=True, help="Path to folder containing LINE files.")
parser.add_argument('-o', '--output', type=str, default="line_hashes.txt", help="Output file name. Defaults to line_hashes.txt.")
args = parser.parse_args()

matched_lines = set()

for dirpath, dirnames, filenames in os.walk(args.input):
    for filename in filenames:
        if filename.endswith('.LINE'):
            full_path = os.path.join(dirpath, filename)

            with open(full_path, 'rb') as file:
                binary_data = file.read(4)
                line_hash = struct.unpack('<I', binary_data[:4])[0]
                matched_lines.add(f"{filename},{line_hash:08X}")

with open(args.output, "w") as f:
    for line in matched_lines:
        f.write(f"{line}\n")
