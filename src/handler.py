import ast
import inspect
import lzma
import marshal
import random
import re
import sys
import threading
import time
import zlib

from tqdm import tqdm

from config import conf

from .conf_parser import Config
from .utils.minify.minifier import Minifier
from .utils.modules.generators import (RandomTypeGenerator,
                                       RandomValueGenerator, StrToHexGenerator,
                                       VariableNameGenerator)
from .utils.modules.layers import LayerGenerator
from .utils.obfuscation.py_fuck.main import obfuscate
from .utils.obfuscation.syntax_manipulator.main import TypeHandler


class MainHandler:
    def __init__(self, src):
        self.code = src
        self.random_name = VariableNameGenerator().generate
        self.random_val = RandomValueGenerator().generate
        self.random_type = RandomTypeGenerator()
        self.str_hex = StrToHexGenerator().generate
        self.defaults = Config.defaults

        self.stats = {
            'original_size': sys.getsizeof(self.code),
            'final_size': 0,
        }

    def __call__(self):
        del self.defaults['CompressOnly']
        for key in self.defaults.keys():
            val = Config.is_enabled(key)
            print(f'[+] {key}: {"Enabled" if val else "Disabled"}')
        print()
        return self.init()

    def close_pbar(self) -> None:
        '''[+] Done!'''
        if self.pbar.n == self.pbar.total:
            self.pbar.set_description('[+] Done!')
            self.pbar.close()

    def init(self):
        filtered_config = conf.copy()
        del filtered_config['Executable']
        funcs_to_check = []
        enabled_funcs = []

        for key, val in filtered_config.items():
            if Config.is_enabled(key) is True:
                # filter out the disabled options and rule out the whole dict if "Enabled" is False
                for func in list(filter(('Enabled').__ne__, val)):
                    if Config.get(func) is True:
                        funcs_to_check.append(func)

        # get all functions that belongs to this class
        # inspect.getmembers(self, predicate=inspect.ismethod) would also work but the order will not be top to bottom
        for method in MainHandler.__dict__.values():
            if inspect.isfunction(method) and method.__name__ in funcs_to_check:
                enabled_funcs.append(method.__name__)

        self.pbar = enabled_funcs
        progressbar_on_off = Config.get('ProgressBar')
        if progressbar_on_off is True:
            self.pbar = tqdm(
                enabled_funcs,
                file=sys.stdout,
                # leave=False,
                ncols=100,
                total=len(enabled_funcs),
                bar_format='''{l_bar} {bar} {n_fmt}/{total_fmt} {rate_fmt} eta {remaining}''',
                unit=' threads',
                ascii=" ━",
                colour='cyan',
                unit_divisor=1,
                smoothing=0.1,
                miniters=1,
                mininterval=0.1,
            )
            enabled_funcs.append('close_pbar')

        for func in self.pbar:
            func = getattr(self, func)
            if progressbar_on_off is True:
                self.pbar.set_description(func.__doc__)
            # func_args = [*func[1:]] if len(func) >= 2 else [None]
            process = threading.Thread(target=func, daemon=True)
            if progressbar_on_off is True:
                time.sleep(random.uniform(0.1, 0.7))
            process.start()
            process.join()

        self.stats['final_size'] = sys.getsizeof(self.code)
        self.log_stats()

        # with open('ast_tree_dump_last.txt', 'wb') as f:
        # f.write(ast.dump(ast.parse(self.code, 'Tupo'), include_attributes=True, indent=4).encode())

        return self.code

    def DeadCode(self):
        '''Adding Dead Code'''
        min_amount = Config.get('MinAmount')
        max_amount = Config.get('MaxAmount')
        variables_amount = random.randint(min_amount, max_amount)

        for i in range(1, variables_amount):
            data = self.random_val()
            if type(data) == str:
                data = f'"{data}"'
            if i % 2 == 0:
                self.code = f"{self.random_name(i)}: {self.random_type()} = {data}\n" + self.code
            else:
                self.code = self.code + \
                    f"\n{self.random_name(i)}: {self.random_type()} = {data}"

    ######## SOURCE OBFUSCATION AND RENAMING ########

    def RenameIdentifiers(self) -> None:
        '''Renaming Types'''
        S = TypeHandler(self.code)
        self.code = S.rename_types()

    def ReplaceTypes(self) -> None:
        '''Replacing Types'''
        S = TypeHandler(self.code)
        self.code = S.replace_types()

    def ConstantShuffler(self):
        """Obfuscating Types"""
        S = TypeHandler(self.code)
        self.code = S.constant_shuffle()

    def EncryptBytecode(self) -> None:
        """Hooking bytecode encryption"""
        ...

    ######## MINIFIERS ########

    def RemoveUnused(self):
        """Removing Unused Code"""
        ...
        # self.code = Minifier.remove_unused(self.code)

    def RemovePass(self):
        """Removing Pass Statements"""
        self.code = Minifier.remove_pass(self.code)

    def RemoveLiteralStatements(self):
        """Removing Literal Statements"""
        self.code = Minifier.remove_literal_statements(self.code)

    def CombineImports(self):
        """Combining Imports"""
        self.code = Minifier.combine_imports(self.code)

    def RemoveObjectBase(self):
        """Removing Object Base"""
        self.code = Minifier.remove_object_base(self.code)

    def ConvertPosargsToArgs(self):
        """Converting Posargs To Args"""
        self.code = Minifier.convert_posargs_to_args(self.code)

    ######## MORE OBFUSCATION ########

    def Marshal(self) -> None:
        '''Marshalling Code'''
        # fake python error that serves no purpose except to make it look like an error occured if someone tries to replace "exec" with "print"
        fake_error = 'File "<string>", line 1\n    \n    ^\nSyntaxError: invalid syntax'
        # eval - if the source is a single expression
        # exec - if the source is a block of statements
        # single - if the source is a single interactive statement
        marsh = marshal.dumps(compile(self.code, fake_error, 'exec'))
        self.code = f"exec(__import__('\\x6d\\x61\\x72\\x73\\x68\\x61\\x6c').loads({marsh}), {{}})"

    def LayerObfuscation(self):
        ...
        # NOT IMPLEMENTED
        # '''Adding Layers'''
        # random_wall = LayerGenerator(self.code).generate
#
        # for i in range(Config.get('LayersAmount')):
        # self.code = random_wall()

    def ASTObfuscation(self):
        """Adding AST Transformation"""
        random.seed(self.code)
        self.code = obfuscate(self.code)
        compressed = lzma.compress(zlib.compress(
            self.code.encode(), level=9), preset=9 | lzma.PRESET_EXTREME)
        first_part, last_part = 'getattr(__import__("', '"), "decompress")'
        def convert(x): return first_part + x + last_part
        self.code = f"""exec(eval('{convert('zlib')}')(eval('{convert('lzma')}')({compressed})))"""

    def Protectors(self) -> None:
        '''Adding Self Protectors'''
        if Config.get('AntiDecompile') is True:
            for_the_skids = f"\"\"\"{self.str_hex('Better luck next time skid')}\"\"\"\n\n"
            self.code = for_the_skids + \
                "for i in range(1):\n\twhile True:\n\t\texec('''" + \
                self.code + "''')\n\t\tbreak"

    ######## CONSOLE LOGGING ########

    def log_stats(self):
        '''Logging Stats'''
        original_size = self.stats['original_size']
        final_size = self.stats['final_size']

        print(f'\n[+] Original code: {original_size} bytes')
        print(f'[+] Final code: {final_size} bytes')
        print(
            f'[+] Compression ratio: {original_size - final_size} bytes ({round(100 - (final_size / original_size) * 100, 2)}%)')
