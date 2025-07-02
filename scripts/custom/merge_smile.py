import json, os, argparse, brotli, time
from newsmile import SmileEncoder

parser = argparse.ArgumentParser(description="Merge JSON files and generate a hash list in Smile binary format.", allow_abbrev=False)
parser.add_argument('version', type=int, help="Current version number to be embedded in the hash list.")
parser.add_argument('-o', '--output', type=str, default="hash_list.sml", help="Output Smile binary file name. Defaults to hash_list.sml.")
parser.add_argument('-q', '--quality', type=int, default=9, help="Quality level passed to brotli [1 - 11, default: 9]")
parser.add_argument('-g', '--glacierkit', action="store_true", help="If it should be exported using GlacierKit's format.")
parser.add_argument('-s', '--skip-compression', action="store_true", help="If brotli compression should be skipped.")
args = parser.parse_args()

input_directory = "paths"

json_files = [os.path.join(input_directory, f) for f in sorted(os.listdir(input_directory)) if f.endswith(".json")]

merged_data = [] if not args.glacierkit else {}

start = time.monotonic_ns()
end = None
for json_file in json_files:
    with open(json_file, "r") as f:
        data = json.load(f)
        resource_type = os.path.basename(json_file).split('.')[0]

        for entry in data:
            if args.glacierkit:
                merged_data[entry['hash']] = {
                    'resourceType': resource_type,
                    'path': entry.get('path', ''),
                    'hint': entry.get('hint', '')
                }
            else:
                merged_data.append({
                    'hash': entry['hash'],
                    'resourceType': resource_type,
                    'path': entry.get('path', ''),
                    'hint': entry.get('hint', ''),
                    'gameFlags': entry['gameFlags']
                })

smile_encoder = SmileEncoder()
smile_encoded_data = smile_encoder.encode({
    "version": args.version,
    "entries": merged_data
})

end = time.monotonic_ns()
print(f"Encoded to smile in {((end - start) / 1e9):.2f}s")

if not args.skip_compression:
    start = time.monotonic_ns()
    compressed_data = brotli.compress(smile_encoded_data, quality=args.quality)
    end = time.monotonic_ns()
    print(f"Compressed @ Quality {args.quality} in {((end - start) / 1e9):.2f}s")

with open(args.output, "wb") as f:
    f.write(compressed_data if not args.skip_compression else smile_encoded_data)

print(f"Hash list merged and encoded in Smile binary format{' [GlacierKit]' if args.glacierkit else ''} successfully!")
