import hashlib

def ioi_hash(string):
    if string:
        md5Result = hashlib.md5(string.encode("utf-8").lower()).hexdigest().upper()
        return "00" + md5Result[2:16]

def infer_type(hash_with_type):
    parts = hash_with_type.split('.')
    if len(parts) == 2:
        return parts[0], parts[1]
    return parts[0], None