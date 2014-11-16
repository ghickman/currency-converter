import os
import pickle


def get_cache_path():
    """Get the filesystem path to the cache."""
    cache_dir = os.path.expanduser('~/.config/currency_converter')

    if not os.path.exists(cache_dir):
        os.mkdir(cache_dir)

    return os.path.join(cache_dir, 'cache.pickle')


def get_cache():
    """Get the cache from its pickled file."""
    cache_path = get_cache_path()
    if not os.path.exists(cache_path):
        return {}

    with open(cache_path, 'rb') as f:
        return pickle.load(f)


def write_cache(key, value):
    """Pickle the cache to the cache file."""
    cache = get_cache()
    cache[key] = value

    with open(get_cache_path(), 'wb') as f:
        pickle.dump(cache, f)
