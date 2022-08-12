import ast
import random

import astunparse

from src.conf_parser import Config

from ...modules.generators import Generator
from ...storage.errors import InvalidOption
from ...storage.strings import allowed_shuffle_types
from .visitors import HideConstants, TypeReplacer, VarObfuscator

ast.PyCF_ALLOW_TOP_LEVEL_AWAIT = 0x200
ast.PyCF_TYPE_COMMENTS = 0x4


def length_generalizer(min_length: int = 1, max_length: int = 50):
    return random.randint(min_length, max_length)


class TypeHandler:
    lg = lambda _min, _max: length_generalizer(min_length=_min, max_length=_max)
    letter_type = Config.get('RenameIdentifiersType')
    if letter_type not in allowed_shuffle_types:
        print(f'[-] {letter_type} is not a valid type')
        raise InvalidOption('Invalid option for SyntaxShuffler', letter_type)
    seed = getattr(Generator, letter_type + '_chars')(length=lg(5, 50))
    main_chr = getattr(Generator, letter_type + '_chars')(length=1)

    def __init__(self, code: str):
        self.tree = ast.parse(code, 'Tupo')
        self.lg = self.__class__.lg
        self.seed = self.__class__.seed
        self.main_chr = self.__class__.main_chr
        self.letter_type = self.__class__.letter_type

        # with open('ast_tree_dump.txt', 'wb') as f:
        #     f.write(ast.dump(ast.parse(code, 'Tupo'), include_attributes=True, indent=4).encode())

    def rename_types(self):
        v = VarObfuscator(seed=self.seed, letters=[getattr(Generator, self.letter_type + '_chars')() for _ in range(self.lg(10, 50))])
        v.visit(self.tree)
        self.tree = ast.fix_missing_locations(self.tree)

        random.seed(self.seed)
        shuffled = list(range(len(v.constants)))
        random.shuffle(shuffled)
        shuffled_constants = [v.constants[shuffled.index(i)] for i in range(len(v.constants))]

        # add raw string to it to avoid syntax errors
        for i in range(len(shuffled_constants)):
            shuffled_constants[i] = f'{shuffled_constants[i]}'

        out = f"""
import random as {self.main_chr}
{self.main_chr}.seed('{self.seed}')
{self.seed} = [{",".join(shuffled_constants)}]
{self.main_chr}.shuffle({self.seed})
""" + astunparse.unparse(self.tree)

        return out

    def replace_types(self):
        v = TypeReplacer()
        v.visit(self.tree)

        return astunparse.unparse(self.tree)

    def constant_shuffle(self):
        v = HideConstants(seed=self.seed)
        v.visit(self.tree)

        return astunparse.unparse(self.tree)
