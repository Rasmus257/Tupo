import ast

import astunparse

from ...conf_parser import Config
from .methods import reducers, removers, transformers


class Minifier:
    def __init__(self, code: str):
        self.code = code

    def minify(self):
        rem_cd = removers.rem_comments_and_docstrings
        tree = ast.parse(self.code)
        transform_int = transformers.IntegerToPower
        transform_funcs = transformers.FunctionToLambda
        transform_combinewiths = transformers.CombineWithStatements

        if Config.get('IntegerToPower'):
            transformer = transform_int()
            transformer.visit(tree)

        if Config.get('FunctionToLambda'):
            transformer = transform_funcs()
            transformer.visit(tree)

        return astunparse.unparse(tree)
