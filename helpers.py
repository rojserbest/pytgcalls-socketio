from random import choice


def random_string():
    chars = "A B C D E F a b c d e f".split()
    to_return = ""

    for i in range(10):
        to_return += choice(chars)

    return to_return
