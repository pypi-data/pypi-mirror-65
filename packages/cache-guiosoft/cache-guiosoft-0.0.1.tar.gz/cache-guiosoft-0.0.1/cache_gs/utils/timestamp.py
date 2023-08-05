import base64
from hashlib import sha1


def int_to_base64(i: int) -> str:
    """ Returns a 12 char length representation of i in base64 """
    return base64.b64encode(i.to_bytes(8, 'big'))


def base64_to_int(b: str) -> int:
    """ Returns a int from a base64 string """
    return int.from_bytes(base64.b64decode(b), 'big')


def section_key_hash(section: str, key: str) -> str:
    """ Returns a sha1 hash (40 chars) from section_key value """
    sk = ("_" if not isinstance(section, str) or not section else section)+"." +\
        ("_" if not isinstance(key, str) or not key else key)
    hash = sha1(sk.encode('utf-8')).hexdigest()
    return hash
