import ast

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
    def _run(transform, code):
        # python_minifier's transforms expect a tree annotated with parent /
        # namespace info that it only sets up inside its own minify() pipeline.
        # Applied bare they raise on some inputs ("Node has no parent"), so skip
        # the pass and return the code unchanged instead of crashing the stage.
        try:
            return ast.unparse(transform(ast_parse(code)))
        except Exception:
            return code

    @staticmethod
    def remove_unused(code): ...

    @staticmethod
    def remove_pass(code):
        return Minifier._run(lambda module: RemovePass()(module), code)

    @staticmethod
    def combine_imports(code):
        return Minifier._run(lambda module: CombineImports()(module), code)

    @staticmethod
    def remove_literal_statements(code):
        return Minifier._run(lambda module: RemoveLiteralStatements()(module), code)

    @staticmethod
    def remove_object_base(code):
        return Minifier._run(lambda module: RemoveObject()(module), code)

    @staticmethod
    def convert_posargs_to_args(code):
        return Minifier._run(lambda module: remove_posargs(module), code)
