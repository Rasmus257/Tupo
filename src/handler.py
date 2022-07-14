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
from .utils.modules.generators import (RandomTypeGenerator,
                                       RandomValueGenerator, StrToHexGenerator,
                                       VariableNameGenerator)
from .utils.modules.layers import LayerGenerator
from .utils.obfuscate.AST import obfuscate
from .utils.storage.strings import replacements


class Handler:
    def __init__(self, src):
        self.code = src
        self.random_name = VariableNameGenerator().generate
        self.random_val = RandomValueGenerator().generate
        self.random_type = RandomTypeGenerator()
        self.str_hex = StrToHexGenerator().generate
        self.defaults = Config.defaults

        self.stats = {
            'original_size': len(self.code),
            'compressed_size': 0,
            'final_size': 0,
        }

    def __call__(self):
        del self.defaults['CompressOnly']
        for key in self.defaults.keys():
            val = Config.is_enabled(key)
            print(f'[+] {key}: {"Enabled" if val else "Disabled"}')  # and type(val) is bool else val if val and type(val) is not bool
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
            if isinstance(val, dict):
                for k in val.keys():
                    funcs_to_check.append(k)
            if Config.is_enabled(key):
                funcs_to_check.append(key)
        functions = list(filter(('Enabled').__ne__, funcs_to_check))
        # get all functions that belongs to this class
        # inspect.getmembers(self, predicate=inspect.ismethod) would also work but the order will not be top to bottom
        for method in Handler.__dict__.values():
            if inspect.isfunction(method) and method.__name__ in functions:
                conf_name = Config.get(method.__name__)
                if isinstance(conf_name, dict):
                    if conf_name.get('Enabled') is True:
                        enabled_funcs.append(method.__name__)
                else:
                    if conf_name is True:
                        enabled_funcs.append(method.__name__)

        self.pbar = tqdm(
            enabled_funcs,
            file=sys.stdout,
            # leave=False,
            ncols=100,
            total=len(enabled_funcs),
            bar_format='''{l_bar} {bar} {n_fmt}/{total_fmt} {rate_fmt} eta {remaining}''',
            unit=' threads',
            ascii="━━",
            colour='cyan',
            unit_divisor=1,
            smoothing=0.1,
            miniters=1,
            mininterval=0.1,
        )
        enabled_funcs.append('close_pbar')

        for func in self.pbar:
            func = getattr(self, func)
            self.pbar.set_description(func.__doc__)
            # func_args = [*func[1:]] if len(func) >= 2 else [None]

            # we use threading to avoid blocking the main thread from errors
            process = threading.Thread(target=func, daemon=True)
            # waiting a little bit so everything can catch up
            time.sleep(0.7)
            process.start()
            process.join()

        self.stats['final_size'] = len(self.code)
        self.log_stats()
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
                self.code = self.code + f"\n{self.random_name(i)}: {self.random_type()} = {data}"

    def ReplaceTypes(self) -> None:
        '''Replacing Types'''
        pass

    def RenameTypes(self) -> None:
        '''Renaming Types'''
        pass

    def HexStrings(self):
        """Converting Strings to Hex"""
        pass

    def EncryptBytecode(self) -> None:
        """Hooking bytecode encryption"""
        pass

    def Minifier(self) -> None:
        """Compressing Code"""
        from .utils.minify.minifier import Minifier
        self.code = Minifier(self.code).minify()

        if Config.get('ReplaceTypes') is True:
            pass

    def Marshal(self) -> None:
        '''Marshalling Code'''
        # fake python error that serves no purpose except to make it look like an error occured if someone tries to replace "exec" with "print"
        fake_error = 'File "<string>", line 1\n    \n    ^\nSyntaxError: invalid syntax'
        # eval - if the source is a single expression
        # exec - if the source is a block of statements
        # single - if the source is a single interactive statement
        marsh = marshal.dumps(compile(self.code, fake_error, 'exec'))
        self.code = "exec(__import__('\\x6d\\x61\\x72\\x73\\x68\\x61\\x6c').loads({}), {})".format(marsh, {})

    def LayerObfuscation(self):
        '''Adding Layers'''
        random_wall = LayerGenerator(self.code).generate

        for i in range(Config.get('LayersAmount')):
            self.code = random_wall()

    def ASTObfuscation(self):
        """Adding AST Transformation"""
        random.seed(self.code)
        self.code = obfuscate(self.code)
        compressed = lzma.compress(zlib.compress(self.code.encode(), level=9), preset=9 | lzma.PRESET_EXTREME)
        first_part, last_part = 'getattr(__import__("', '"), "decompress")'
        convert = lambda x: first_part + x + last_part
        self.code = f"""exec(eval('{convert('zlib')}')(eval('{convert('lzma')}')({compressed})))"""
        self.stats['compressed_size'] = len(self.code)

    def Protectors(self) -> None:
        '''Adding Self Protectors'''
        if Config.get('AntiDecompile') is True:
            for_the_skids = f"\"\"\"{self.str_hex('Better luck next time skid')}\"\"\"\n\n"
            self.code = for_the_skids + "for i in range(1):\n\twhile True:\n\t\texec('''" + self.code + "''')\n\t\tbreak"

    def log_stats(self):
        '''Logging Stats'''
        original_size = self.stats['original_size']
        compressed_size = self.stats['compressed_size']
        final_size = self.stats['final_size']

        print(f'\n[+] Original code: {original_size} bytes')
        try:
            print(f'[+] Compressed code: {compressed_size} bytes | {round(original_size / compressed_size * 100, 1)}%')
        except ZeroDivisionError:
            print(f'[+] Compressed code: null bytes | 0%')
        print(f'[+] Final code: {final_size} bytes')
