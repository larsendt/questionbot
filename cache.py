import hashlib
import os
import functools
import json

CACHE_DIR = "cache"
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def make_id(args, kwargs):
    print args
    _id = "".join(args) 
    if kwargs:
        _id += "".join(kwargs.keys()) + "".join(kwargs.values())
    _id = _id.encode("utf-8")
    return hashlib.sha1(_id).hexdigest()

def cache_get(_id):
    path = os.path.join(CACHE_DIR, _id)
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    else:
        return None
        
def cache_set(_id, obj):
    path = os.path.join(CACHE_DIR, _id)
    with open(path, "w") as f:
        json.dump(obj, f)

def cache_exists(_id):
    path = os.path.join(CACHE_DIR, _id)
    return os.path.exists(path)

def disk_cache(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print args
        _id = make_id(args, kwargs)
        if cache_exists(_id):
            return cache_get(_id)
        else:
            ret = func(*args, **kwargs)
            cache_set(_id, ret)
            return ret
    return wrapper
