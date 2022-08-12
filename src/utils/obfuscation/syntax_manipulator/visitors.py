import ast
import inspect
import types

from ....conf_parser import Config
from ...storage.strings import inbuilt_types, inbuilts
from .node_transformer import IntegerObfuscator, StringObfuscator


class HideConstants(ast.NodeTransformer):
    def __init__(self, seed: str):
        self.seed = seed

    def visit_Constant(self, node: ast.Constant) -> any:
        if node.value == self.seed:
            return self.generic_visit(node)

        if isinstance(node.value, str):
            if Config.get('ConstantShuffler') is True:
                node.value = bytes.hex(node.value.encode())
            # return self.generic_visit(node)
            # node = StringObfuscator(node).transform()

        elif isinstance(node, ast.Num):
            ints = {
                0: '(()==[])+(()==[])',
                1: '(()==())-(()==[])',
                2: '(()==())+(()==())',
                3: '(()==())+(()==())+(()==())',
                4: '(()==())+(()==())+(()==())+(()==())',
                5: '(()==())+(()==())+(()==())+(()==())+(()==())',
                6: '(()==())+(()==())+(()==())+(()==())+(()==())+(()==())',
                7: '(()==())+(()==())+(()==())+(()==())+(()==())+(()==())+(()==())',
                8: '(()==())+(()==())+(()==())+(()==())+(()==())+(()==())+(()==())+(()==())',
                9: '(()==())+(()==())+(()==())+(()==())+(()==())+(()==())+(()==())+(()==())+(()==())'
            }
            if node.n in ints.keys():  # only obfuscate single digits (0-9), otherwise the file size will be as big as my ass
                return ast.Name(id=ints[node.n], ctx=ast.Load())
            else:
                if type(node.n) == int:
                    return ast.Call(func=ast.Name(id='int', ctx=ast.Load()), args=[IntegerObfuscator(node).transform()], keywords=[], starargs=None, kwargs=None)
                elif type(node.n) == float:
                    return IntegerObfuscator(node).transform()

        return self.generic_visit(node)


class TypeReplacer(ast.NodeTransformer):
    def __init__(self):
        pass

    def visit_Constant(self, node: ast.Constant) -> any:
        # TODO add more types to replace
        if isinstance(node.value, bool):
            if node.value is True:
                return ast.Name(id='(()==())', ctx=ast.Load())
            else:
                return ast.Name(id='(()==[])', ctx=ast.Load())

        if isinstance(node.value, types.NoneType):
            return ast.Name(id='exec(str())', ctx=ast.Load())

        return self.generic_visit(node)

    # def visit_Pass(self, node: ast.Pass) -> any:
        # return ast.Ellipsis()
        # AST.COPYLOCATION SDFIOHFDSH98UFDSIUHOFSDOUGIFSDUIOGHFSDUOIHGFDSUOGHIFDSOUIHFOIUHSDFUHIOFSDHUIO
        # ast.copy_location(node, node)


class VarObfuscator(ast.NodeTransformer):
    def __init__(self, seed: str, letters: list) -> None:
        self.letters = letters
        self.seed = seed
        self.seen = {}
        self.imports = []
        self.ignores = []
        self.constants = []

        if Config.get('ConstantShuffler') is True:
            hex_to_str = """lambda x: bytes.fromhex(x).decode()"""
            self.pos = self.add_to_constants(hex_to_str)

    def visit_Expr(self, node: ast.Expr) -> any:
        # TODO: obfuscate docstrings instead of just removing them
        if isinstance(node.value, str):  # just for docstrings
            node.value = self.obf_var(node.value)
        return self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> any:
        if not node.name.startswith("__"):
            node.name = self.obf_var(node.name)
        return self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> any:
        return self.visit_FunctionDef(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> any:
        node.name = self.obf_var(node.name)
        node.decorator_list = [self.visit(decorator) for decorator in node.decorator_list]
        return self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> any:
        for alias in node.names:
            self.imports.append(alias.name)
            self.imports.append(alias.asname) if alias.asname is not None else None
            if alias.asname is not None:
                alias.asname = self.obf_var(alias.asname)
            else:
                alias.asname = self.obf_var(alias.name)
        return self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> any:
        for alias in node.names:
            self.imports.append(alias.name)
            self.imports.append(alias.asname) if alias.asname is not None else None
            if alias.asname is not None:
                alias.asname = self.obf_var(alias.asname)
            else:
                alias.asname = self.obf_var(alias.name)

        return self.generic_visit(node)

    def visit_Name(self, node: ast.Name) -> any:
        node_parent = inspect.currentframe().f_back.f_back.f_locals
        if node.id in inbuilts:
            if isinstance(node_parent.get('node'), ast.FunctionDef) and node_parent.get('field') == 'decorator_list':
                return self.generic_visit(node)
            node.id = self.add_to_constants(node.id)
        else:
            node.id = self.obf_var(node.id)

        return self.generic_visit(node)

    def visit_Constant(self, node: ast.Constant) -> any:
        if isinstance(node.value, str):
            node.value = repr(node.value).replace('\'', '').replace('"', '')

        node_parent = inspect.currentframe().f_back.f_back.f_locals
        # check if the string is inside an f-string
        if isinstance(node_parent.get('node'), ast.JoinedStr):
            for part in node_parent.get('node').values:
                if isinstance(part, ast.Constant):
                    if part.value == node.value:
                        # obfuscate the string inside the f-string and then add it to the constants and call it from there
                        node = ast.FormattedValue(value=ast.Constant(value=str(node.value)), conversion=-1, format_spec=None)
                        return self.generic_visit(node)

        new_node = ast.Name()
        new_node.id = self.add_to_constants(node.value, convert=True)
        return new_node

    def visit_Attribute(self, node: ast.Attribute) -> any:
        for _import in self.imports:
            try:
                if hasattr(__import__(_import), node.attr) or node.attr in self.imports or node.value.id in self.imports:
                    return self.generic_visit(node)
                else:
                    node.attr = self.obf_var(node.attr)
                    return self.generic_visit(node)
            except (ModuleNotFoundError, AttributeError):
                pass
        return self.generic_visit(node)

    def visit_arg(self, node: ast.arg) -> any:
        if node.arg is not None:
            node.arg = self.obf_var(node.arg)
        return self.generic_visit(node)

    def visit_keyword(self, node: ast.keyword) -> any:
        if node.arg is None:
            return self.generic_visit(node)

        if node.arg == 'metaclass':
            return self.generic_visit(node)

        # this whole bit is to prevent obfuscating keywords that belongs to an inbuilt function or class
        # for example, this can occur if a lambda has the same keyword name as an inbuilt function or class
        for inbuilt in inbuilt_types:
            try:
                if isinstance(inbuilt, types.BuiltinFunctionType):
                    argspec = inspect.getfullargspec(inbuilt).args
                    node_parent = inspect.currentframe().f_back.f_back.f_locals
                    if node.arg in argspec and not isinstance(node_parent.get('new_node'), ast.Lambda):
                        return self.generic_visit(node)
            except (ValueError, TypeError):
                pass

        for _import in self.imports:
            node_parent = inspect.currentframe().f_back.f_back.f_locals
            parent_node = node_parent.get('new_node')
            try:
                if hasattr(__import__(_import), parent_node.attr) or parent_node.attr in self.imports or parent_node.value.id in self.imports:
                    # ignores all keywords that belong to a module
                    # (e.g. os.getenv(key=value))
                    # in this case we don't obfuscate the "key" keyword
                    for _ in node_parent.get('node').keywords:
                        return self.generic_visit(node)
                    return self.generic_visit(node)
            except (ModuleNotFoundError, AttributeError):
                pass
        node.arg = self.obf_var(node.arg)
        return self.generic_visit(node)

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> any:
        if node.name:
            node.name = self.obf_var(node.name)
        return self.generic_visit(node)

    def visit_Global(self, node: ast.Global) -> any:
        return ast.Global([self.obf_var(n) for n in node.names])

    def visit_Nonlocal(self, node: ast.Nonlocal) -> any:
        return ast.Nonlocal([self.obf_var(n) for n in node.names])

    def add_to_constants(self, constant: any, convert: bool = False) -> str:
        if convert:
            if isinstance(constant, str):
                constant = "\"{}\"".format(constant)
            elif isinstance(constant, int) or isinstance(constant, float):
                constant = str(constant)
            else:
                return constant

        if constant in self.constants:
            if Config.get('ConstantShuffler') is True:
                try:
                    real_val = ast.literal_eval(constant)
                except (ValueError, TypeError, SyntaxError):
                    real_val = constant
                if real_val not in inbuilts:
                    if isinstance(real_val, str):
                        return "{}({}[{}])".format(self.pos, self.seed, self.constants.index(constant))
            return "{}[{}]".format(self.seed, self.constants.index(constant))
        else:
            self.constants.append(constant)
            try:
                if Config.get('ConstantShuffler') is True:
                    try:
                        real_val = ast.literal_eval(constant)
                    except (ValueError, SyntaxError):
                        real_val = constant
                    if real_val not in inbuilts:
                        if isinstance(real_val, str):
                            return "{}({}[{}])".format(self.pos, self.seed, self.constants.index(constant))
            except AttributeError:
                return "{}[{}]".format(self.seed, len(self.constants) - 1)
            return "{}[{}]".format(self.seed, len(self.constants) - 1)

    def get_var_name(self, i: int):
        # ?TODO? make iterable, not recursive
        letter = self.letters[i % len(self.letters)]
        if i >= len(self.letters):
            return letter + self.get_var_name(i // len(self.letters))
        return letter

    def obf_var(self, oldName: str) -> str:
        if oldName in self.seen:
            return self.seen[oldName]

        for key in self.seen:
            if oldName == key:
                return self.seen[key]

        newName = self.get_var_name(len(self.seen))
        self.seen[oldName] = newName
        return newName
