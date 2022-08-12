import ast

import astunparse
from python_minifier import (CombineImports, RemoveLiteralStatements,
                             RemoveObject, RemovePass, remove_posargs)

from src.utils.storage.errors import UnstableSyntaxError

from ...conf_parser import Config
from .methods.removers import rem_comments_and_docstrings
from .methods.transformers import CombineWithStatements


def ast_parse(source):
    return ast.parse(source, 'Tupo')


class Minifier(object):
    @staticmethod
    def remove_unused(code): ...

    @staticmethod
    def remove_pass(code):
        module = RemovePass()(ast_parse(code))
        return astunparse.unparse(module)

    @staticmethod
    def combine_imports(code):
        module = CombineImports()(ast_parse(code))
        return astunparse.unparse(module)

    @staticmethod
    def remove_literal_statements(code):
        # NOT WORKING
        module = RemoveLiteralStatements()(ast_parse(code))
        return astunparse.unparse(module)

    @staticmethod
    def remove_object_base(code):
        module = RemoveObject()(ast_parse(code))
        return astunparse.unparse(module)

    @staticmethod
    def convert_posargs_to_args(code):
        module = remove_posargs(ast_parse(code))
        return astunparse.unparse(module)
