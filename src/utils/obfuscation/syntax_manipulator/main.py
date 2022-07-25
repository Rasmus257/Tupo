import ast
import random

import astunparse

from ...modules.generators import UnicodeChars
from .node_transformers import StringHexifyer, TypeReplacer, VarObfuscator


def length_generalizer(min_length: int = 1, max_length: int = 50):
    return random.randint(min_length, max_length)


class TypeHandler:
    lg = lambda _min, _max: length_generalizer(min_length=_min, max_length=_max)
    seed = UnicodeChars.generate(length=lg(5, 50))
    main_chr = UnicodeChars.generate(length=1)
    nonlatin_chars = UnicodeChars.generate()

    def __init__(self, code: str):
        self.tree = ast.parse(code)
        self.lg = self.__class__.lg
        self.seed = self.__class__.seed
        self.main_chr = self.__class__.main_chr
        self.nonlatin_chars = self.__class__.nonlatin_chars

    def rename_types(self):
        v = VarObfuscator(seed=self.seed, letters=[UnicodeChars.generate() for _ in range(self.lg(5, 50))])
        v.visit(self.tree)

        random.seed(self.seed)
        shuffled = list(range(len(v.constants)))
        random.shuffle(shuffled)
        shuffled_constants = [v.constants[shuffled.index(i)] for i in range(len(v.constants))]

        out = f"""import random as {self.main_chr}
{self.main_chr}.seed('{self.seed}')
{self.seed}=[{",".join(shuffled_constants)}]
{self.main_chr}.shuffle({self.seed})
""" + astunparse.unparse(self.tree)

        return out

    def replace_types(self):
        v = TypeReplacer()
        v.visit(self.tree)

        return astunparse.unparse(self.tree)

    def hide_strings(self):
        v = StringHexifyer(seed=self.seed)
        v.visit(self.tree)

        return astunparse.unparse(self.tree)
