import ast

import astunparse

from ...conf_parser import Config
from .methods import reducers, removers, transformers


class Minifier:
    def __init__(self, code: str):
        self.code = code

    def minify(self):
        rem_cd = removers.rem_comments_and_docstrings
        tree = ast.parse(rem_cd(self.code))
        transform_int = transformers.IntegerToPower

        if Config.get('IntegerToPower'):
            transformer = transform_int()
            transformer.visit(tree)

        return astunparse.unparse(tree)
