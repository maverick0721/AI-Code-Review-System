import hashlib
import json
import os

CACHE_FILE = "data/cache.json"

if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "w") as f:
        json.dump({}, f)


def get_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()


def get_cache(prompt):

    with open(CACHE_FILE) as f:
        cache = json.load(f)

    key = get_hash(prompt)

    return cache.get(key)


def set_cache(prompt, result):

    with open(CACHE_FILE) as f:
        cache = json.load(f)

    key = get_hash(prompt)

    cache[key] = result

    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)