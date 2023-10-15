import hashlib

def ioi_hash(string):
    if string:
        md5Result = hashlib.md5(string.encode("utf-8").lower()).hexdigest().upper()
        return "00" + md5Result[2:16]
