import ast
import random

import astunparse

from ....conf_parser import Config
from ...modules.generators import UnicodeChars
from .node_transformers import TypeReplacer, VarObfuscator


class TypeHandler:
    def __init__(self, code: str):
        self.tree = ast.parse(code)
        self.lg = lambda _min, _max: self.length_generalizer(min_length=_min, max_length=_max)
        self.seed = UnicodeChars.generate(length=self.lg(5, 50))
        self.main_chr = UnicodeChars.generate(length=1)
        self.nonlatin_chars = UnicodeChars.generate()

        # self.original_code = astunparse.unparse(self.tree)

    def rename_types(self):
        v = VarObfuscator(seed=self.seed, letters=[UnicodeChars.generate() for _ in range(self.lg(25, 100))])
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
        v = TypeReplacer()
        v.visit(self.tree)

        return astunparse.unparse(self.tree)

    def length_generalizer(self, min_length: int = 1, max_length: int = 50):
        return random.randint(min_length, max_length)
