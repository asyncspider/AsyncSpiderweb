import hashlib
from random import sample


def make_md5(value):
    m = hashlib.md5()
    m.update(value.encode('utf8'))
    res = m.hexdigest()
    return res

def random_letters(min=97, max=123):
    letters = [chr(i) for i in range(min, max)]
    code = "".join(sample(letters, 6))
    return code

