import random
import unicodedata
from itertools import permutations
from time import time

from ..storage.strings import (ascii_letters, ascii_lowercase, ascii_uppercase,
                               inbuilts)


class VariableNameGenerator:
    def __init__(self):
        self.options = [
            self.random_string,
            self.random_int,
            self.upper_lower,
            self.time_based,
            self.just_id,
            self.single_letters,
        ]

    def generate(self, id):
        return random.choice(self.options)(id)

    def random_string(self, id):
        lowercase = list(map(chr, range(97, 123)))
        uppercase = list(map(chr, range(65, 90)))
        return "".join(random.choice(ascii_letters) for i in range(random.randint(1, 300))) + str(id)

    def random_int(self, id):
        return "_{}_".format(random.randint(0, id * id ^ id))

    def upper_lower(self, id):
        letter = random.choice(ascii_lowercase)
        up = letter.upper()
        low = letter.lower()
        return "".join(random.choice(up + low) for i in range(id))

    def time_based(self, id):
        return (
            random.choice(ascii_letters)
            + str(time()).replace(".", "")
            + str(id)
        )

    def just_id(self, id):
        return random.choice(ascii_letters) + str(id)

    def single_letters(self, id):
        return random.choice(ascii_letters) * id


class RandomValueGenerator:
    def __init__(self):
        self.options = [self.random_string, self.random_int]

    def generate(self):
        return random.choice(self.options)()

    def random_string(self):
        return "".join(random.choice(ascii_lowercase + ascii_uppercase)for i in range(random.randint(1, 300)))

    def random_int(self):
        return random.randint(random.randint(0, 300), random.randint(300, 999))


class RandomTypeGenerator:
    def __str__() -> str:
        return random.choice(inbuilts)


class StrToHexGenerator:
    def generate(code: str) -> str:
        _str = ''
        for byte in [hex(ord(character)) for character in code]:
            _str += '\\x' + byte[2:]
        return _str


class UnicodeChars:
    def generate(length=random.randint(1, 10)) -> str:
        # for i in range(0x110000):
        #     c = chr(i)
        #     if c.isidentifier():
        #         start_characters.append(c)
        #     elif ('a' + c).isidentifier():
        #         continue_characters.append(c)
        allowed_categories = ('LC', 'Ll', 'Lu', 'Lo', 'Lu')
        rtl_categories, last_orientation = ('AL', 'R'), 'L'
        big_list = list(map(chr, range(1580, 0xFFFF)))  # highest unicode
        finished_char = []  # we have it as a list so we can shuffle it later

        while len(finished_char) < length:
            char = random.choice(big_list)
            if unicodedata.category(char) in allowed_categories:
                orientation = unicodedata.bidirectional(char)
                if last_orientation in rtl_categories:
                    if orientation not in rtl_categories:
                        finished_char.append(char)
                else:
                    if orientation in rtl_categories:
                        finished_char.append(char)
                last_orientation = orientation

        random.shuffle(finished_char)
        return "".join(finished_char)
