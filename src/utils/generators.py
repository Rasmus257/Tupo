import random
from time import time

from .strings import ascii_letters, ascii_lowercase, ascii_uppercase


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
    def __init__(self):
        letter = random.choice(ascii_letters)
        self.options = [
            "str", "int", "float", "bool", "list", "dict", "tuple", "set", "bytes", "bytearray", 'hash',
            "memoryview", "complex", "range", "slice", "hex", "oct", "bin", "chr", "ord", f"lambda {letter}: {letter}",
            "locals", "globals", "vars", "dir", "eval", "exec", "compile", "repr", "format", "input", "open", "type",
            'abs', 'help', 'min', 'setattr', 'all', 'hex', 'next', 'any', 'divmod', 'id', 'object', 'sorted', 'ascii',
            'enumerate', 'input', 'staticmethod', 'isinstance', 'sum', 'filter', 'issubclass', 'pow', 'super', 'iter',
            'print', 'callable', 'format', 'len', 'property', 'type', 'frozenset', 'list', 'range', 'vars', 'classmethod',
            'getattr', 'locals', 'zip', 'globals', 'map', 'reversed', '__import__', 'hasattr', 'max', 'round', 'delattr'
        ]

    def generate(self) -> type:
        return random.choice(self.options)


class StrToHexGenerator:
    def generate(self, code: any) -> str:
        _str = ''
        for byte in [hex(ord(character)) for character in code]:
            _str += '\\x' + byte[2:]
        return _str
