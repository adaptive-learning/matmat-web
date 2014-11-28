import string


def generate_random_string(lenght):
    import random
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(lenght))
