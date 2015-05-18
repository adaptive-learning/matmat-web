from functools import wraps
import hashlib
import string
import re
from django.core.cache import cache


def generate_random_string(lenght):
    import random
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(lenght))


def cache_pure(f, expiration=60 * 60 * 24 * 30):
    """ Cache decorator for functions taking one or more arguments. """

    @wraps(f)
    def wrapper(*args, **kwargs):
        if len(args) > 0 and re.match(r"<.+ object at \w+>", repr(args[0])) is not None:
            key_args = [args[0].__class__] + list(args[1:])
        else:
            key_args = args

        key = "{}:args:{}-kwargs:{}".format(f.__name__, repr(key_args), repr(kwargs))
        hash = hashlib.sha1(key).hexdigest()
        if hash in cache:
            value = cache.get(hash)
            return value

        value = f(*args, **kwargs)
        cache.set(hash, value, expiration)

        return value

    return wrapper