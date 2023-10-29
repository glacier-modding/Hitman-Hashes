import os
import argparse

parser = argparse.ArgumentParser(description="Extract a list of hashes from RPKG files.")
parser.add_argument('-g', '--game', required=True, type=str, default="h3", help="Specify the game. Possible options are alpha, h1, h2, h3, beta, and sa.")
parser.add_argument('-i', '--input', type=str, required=True, help="Path to game's runtime folder.")
parser.add_argument('-o', '--output', type=str, default="new_hashes.txt", help="Output folder and/or name. Defaults to new_hashes.txt.")
args = parser.parse_args()

if args.output:
    if args.output.endswith(os.sep) or (os.path.isdir(args.output) if os.path.exists(args.output) else args.output.endswith("/") or args.output.endswith("\\")):
        args.output = os.path.join(args.output, "new_hashes.txt")
    
    directory = os.path.dirname(args.output)
    
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

def readHexFromFile(file, offset, length):
	file.seek(offset)
	hexdata = file.read(length)
	hexstr = ''
	for h in hexdata:
		hexstr = hex(h)[2:].zfill(2) + hexstr
	return hexstr

def readStrFromFile(file, offset, length):
	file.seek(offset)
	return file.read(length).decode()

def readLongFromFile(file, offset):
	data = readHexFromFile(file, offset, 0x4)
	return int(data, 16)

def readLongLongFromFile(file, offset):
	data = readHexFromFile(file, offset, 0x8)
	return int(data, 16)

def extractHashes(game, input):
	hashes = []
	for root, dirs, files in os.walk(input):
		dirs.sort()
		files.sort()
		for file in files:
			if file.lower().endswith(".rpkg"):
				filePath = root + "\\" + file
				print(filePath)
				with open(filePath, 'rb') as f:
					if "patch" in os.path.basename(filePath).lower():
						isPatch = True
						print("Patch file.")
					else:
						isPatch = False
						print("Not a patch file.")
					header = f.read(4)
					if header == b'GKPR' and game == "alpha":
						offset = 0x1C
						hashCount = readLongFromFile(f, offset)
						print("Hashes in RPKG: " + str(hashCount))
						offset += 0x4
						tableOffset = readLongFromFile(f, offset)
						offset1 = 0x28
						offset2 = 0x28 + tableOffset
						for h in range(hashCount):
							hashValue = readHexFromFile(f, offset1, 0x8).upper()
							offset1 += 0x10
							hashValue += "." + readStrFromFile(f, offset2, 0x4).upper()[::-1]
							offset2 += 0x4
							hashDependsSize = readLongFromFile(f, offset2)
							offset2 += 0x14 + hashDependsSize
							hashes.append(hashValue)
					elif header == b'GKPR':
						offset = 0x4
						hashCount = readLongFromFile(f, offset)
						print("Hashes in RPKG: " + str(hashCount))
						offset += 0x4
						tableOffset = readLongFromFile(f, offset)
						offset = 0x10
						if isPatch:
							patchCount = readLongFromFile(f, offset)
							offset += 0x8 * patchCount + 0x4
						offset1 = offset							
						offset2 = offset + tableOffset
						for h in range(hashCount):
							hashValue = readHexFromFile(f, offset1, 0x8).upper()
							offset1 += 0x14
							hashValue += "." + readStrFromFile(f, offset2, 0x4).upper()[::-1]
							offset2 += 0x4
							hashDependsSize = readLongFromFile(f, offset2)
							offset2 += 0x14 + hashDependsSize
							hashes.append(hashValue)
					elif header == b'2KPR':
						offset = 0xD
						hashCount = readLongFromFile(f, offset)
						print("Hashes in RPKG: " + str(hashCount))
						offset += 0x4
						tableOffset = readLongFromFile(f, offset)
						offset = 0x19
						if isPatch:
							patchCount = readLongFromFile(f, offset)
							offset += 0x8 * patchCount + 0x4
						offset1 = offset							
						offset2 = offset + tableOffset
						for h in range(hashCount):
							hashValue = readHexFromFile(f, offset1, 0x8).upper()
							offset1 += 0x14
							hashValue += "." + readStrFromFile(f, offset2, 0x4).upper()[::-1]
							offset2 += 0x4
							hashDependsSize = readLongFromFile(f, offset2)
							offset2 += 0x14 + hashDependsSize
							hashes.append(hashValue)
	hashes = list(set(hashes))
	hashesString = ""
	for h in hashes:
		hashesString += h + ":" + game + "\n"
	return hashesString

with open(args.output, "w") as f:
	f.write(extractHashes(args.game, args.input))