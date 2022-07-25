import ast

from ....conf_parser import Config
from ...storage.strings import inbuilts, replacements


class StringHexifyer(ast.NodeTransformer):
    def __init__(self, seed: str):
        self.seed = seed

    def visit_Constant(self, node: ast.Constant) -> any:
        if isinstance(node.value, str) and node.value != self.seed:
            node.value = bytes.hex(node.value.encode())
        return self.generic_visit(node)


class TypeReplacer(ast.NodeTransformer):
    def __init__(self):
        pass

    def visit_Constant(self, node: ast.Constant) -> any:
        for key, value in replacements.items():
            if type(node.value) == type(key):
                node.value = value
        return self.generic_visit(node)


class VarObfuscator(ast.NodeTransformer):
    def __init__(self, seed: str, letters: list) -> None:
        self.letters = letters
        self.seed = seed
        self.seen = {}
        self.constants = []

        if Config.get('HideStrings') is True:
            hex_to_str = """lambda x: bytes.fromhex(x).decode()"""
            self.pos = self.add_to_constants(hex_to_str)

    def visit_Import(self, node: ast.Import) -> any:
        for alias in node.names:
            alias.asname = self.obf_var(alias.name)
        return self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> any:
        node.name = self.obf_var(node.name)
        return self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> any:
        if not node.name.startswith("_"):
            node.name = self.obf_var(node.name)
        for a in node.args.args:
            a.arg = self.obf_var(a.arg)
        return self.generic_visit(node)

    def visit_Constant(self, node: ast.Constant) -> any:
        new_node = ast.Name()
        new_node.id = self.add_to_constants(node.value, convert=True)
        return new_node

    def visit_Name(self, node: ast.Name) -> any:
        if node.id in inbuilts:
            node.id = self.add_to_constants(node.id)
        else:
            node.id = self.obf_var(node.id)
        return self.generic_visit(node)

    def add_to_constants(self, constant: any, convert: bool = False) -> str:
        if convert:
            if isinstance(constant, str):
                constant = "\"{}\"".format(constant)
            elif isinstance(constant, int) or isinstance(constant, float):
                constant = str(constant)
            else:
                return constant

        if constant in self.constants:
            if Config.get('HideStrings') is True:
                try:
                    real_val = ast.literal_eval(constant)
                except ValueError:
                    real_val = constant
                if isinstance(real_val, str) and real_val not in inbuilts:
                    return "{}({}[{}])".format(self.pos, self.seed, self.constants.index(constant))
            return "{}[{}]".format(self.seed, self.constants.index(constant))
        else:
            self.constants.append(constant)
            try:
                if Config.get('HideStrings') is True:
                    try:
                        real_val = ast.literal_eval(constant)
                    except ValueError:
                        real_val = constant
                    if isinstance(real_val, str) and real_val not in inbuilts:
                        return "{}({}[{}])".format(self.pos, self.seed, len(self.constants) - 1)
            except AttributeError:
                return "{}[{}]".format(self.seed, len(self.constants) - 1)
            return "{}[{}]".format(self.seed, len(self.constants) - 1)

    def get_var_name(self, i: int):
        letter = self.letters[i % len(self.letters)]
        if i >= len(self.letters):
            return letter + self.get_var_name(i // len(self.letters))
        return letter

    def obf_var(self, oldName: str) -> str:
        if oldName in self.seen:
            return self.seen[oldName]

        newName = self.get_var_name(len(self.seen))
        self.seen[oldName] = newName
        return newName
