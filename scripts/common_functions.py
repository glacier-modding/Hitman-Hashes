import hashlib

GAME_FLAGS = {
    "alpha": 0b000001,
    "h1": 0b000010,
    "h2": 0b000100,
    "h3": 0b001000,
    "beta": 0b010000,
    "sa": 0b100000,
    "unknown": 0b1000000
}

def ioi_hash(string):
    if string:
        md5Result = hashlib.md5(string.encode("utf-8").lower()).hexdigest().upper()
        return "00" + md5Result[2:16]

def infer_type(hash_with_type):
    parts = hash_with_type.split('.')
    if len(parts) == 2:
        return parts[0], parts[1]
    return parts[0], None