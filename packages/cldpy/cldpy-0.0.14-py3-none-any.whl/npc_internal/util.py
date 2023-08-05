import hashlib


def get_fullname(clazz):
    return clazz.__module__ + '.' + clazz.__qualname__


def sha256_file(filename):
    h = hashlib.sha256()
    with open(filename, 'rb', buffering=0) as f:
        for b in iter(lambda : f.read(128*1024), b''):
            h.update(b)
    return h.hexdigest()[:32]
