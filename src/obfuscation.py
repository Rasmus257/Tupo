import re
import sys
import time
import zlib
import lzma
import random
import marshal
import inspect
import threading
import python_minifier

from tqdm import tqdm
from .config import Config
from .utils.strings import replacements
from .utils.layers import LayerGenerator
from .utils.generators import VariableNameGenerator, RandomValueGenerator, RandomTypeGenerator, StrToHexGenerator


class Obfuscation(object):
    def __init__(self, src):
        self.code = src
        self.random_name = VariableNameGenerator().generate
        self.random_val = RandomValueGenerator().generate
        self.random_type = RandomTypeGenerator().generate
        self.str_hex = StrToHexGenerator().generate

    def __call__(self):
        defaults = Config.defaults
        for key in defaults.keys():
            val = Config.get_setting(key)
            print(f'[+] {key}: {"Enabled" if val and type(val) is bool else val if val and type(val) is not bool else "Disabled"}')
        print()
        return self.init()

    def init(self):
        methods = [[self.Minify, True, True], [self.add_layers], [self.DeadCode], [self.Minify, True, False], [self.Marshal], [self.Protectors, True]]
        # methods = [[self.Minify, True, True]]
        """Specify a custom bar string formatting.
        May impact performance.
        [default: '{l_bar}{bar}{r_bar}'], where l_bar='{desc}: {percentage:3.0f}%|' and r_bar='| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, ' '{rate_fmt}{postfix}]'
        Possible vars: l_bar, bar, r_bar, n, n_fmt, total, total_fmt, percentage, elapsed, elapsed_s, ncols, nrows, desc, unit, rate, rate_fmt, rate_noinv,
        rate_noinv_fmt, rate_inv, rate_inv_fmt, postfix, unit_divisor, remaining, remaining_s, eta.
        Note that a trailing ": " is automatically removed after {desc} if the latter is empty.
        """
        pbar = tqdm(
            methods,
            file=sys.stdout,
            # leave=False,
            ncols=100,
            total=len(methods),
            bar_format='''{l_bar} {bar} {n_fmt}/{total_fmt} {rate_fmt} eta {remaining}''',
            unit=' threads',
            ascii="━━",
            colour='cyan',
            unit_divisor=1,
            smoothing=0.1,
            miniters=1,
            mininterval=0.1,
        )

        def close_pbar():
            '''[+] Done!'''
            if pbar.n == pbar.total:
                pbar.set_description('[+] Done!')
                pbar.close()
        methods.append([close_pbar])

        for func in pbar:
            pbar.set_description(func[0].__doc__)
            func_name = func[0].__name__
            func_args = [*func[1:]] if len(func) >= 2 else [None]
            confg = Config.get_setting(func_name)
            if type(confg) is bool and confg is False:
                continue
            if any(arg is not None for arg in func_args):
                process = threading.Thread(target=func[0], args=func_args, daemon=True)
            else:
                process = threading.Thread(target=func[0], daemon=True)
            # waiting a little bit so everything can catch up
            time.sleep(0.7)
            process.start()
            process.join()

        return self.code

    def add_layers(self):
        '''Adding Layers'''
        random_wall = LayerGenerator(self.code).generate

        for i in range(Config.get_setting('LayerAmount')):
            self.code = random_wall()

    def DeadCode(self):
        '''Adding Dead Code'''
        variables_amount = random.randint(100, 400)

        for i in range(1, variables_amount):
            data = self.random_val()
            if type(data) == str:
                data = f'"{data}"'
            if i % 2 == 0:
                self.code = f"{self.random_name(i)}: {self.random_type()} = {data}\n" + self.code
            else:
                self.code = self.code + f"\n{self.random_name(i)}: {self.random_type()} = {data}"

    def Minify(self, compress: bool = ..., replace: bool = ...) -> ...:
        """Compressing Code"""
        self.code = python_minifier.minify(
            self.code,
            remove_annotations=False,
            rename_globals=True,
            # preserve_locals=None,
            # preserve_globals=None,
        )
        formatted_code = re.sub(r"(;)\1+", ";", '''exec("""{};""")'''.format(self.code.replace("\n", ";").replace('"""', '\\"\\"\\"')))

        if formatted_code[0] == ';':
            self.code = formatted_code[1:]
        self.code = formatted_code
        if replace is True:
            pass
        if compress is True:
            og_size = len(self.code)
            compressed = lzma.compress(zlib.compress(self.code.encode(), level=9), preset=9 | lzma.PRESET_EXTREME)
            # print(f'\n[+] Compressed code: {og_size} --> {len(compressed)} bytes | {round(len(compressed) / len(self.code) * 100, 1)}%')
            first_part, last_part = 'getattr(__import__("', '"), "decompress")'
            convert = lambda x: first_part + x + last_part
            lzma_ = self.str_hex(convert('lzma'))
            zlib_ = self.str_hex(convert('zlib'))
            self.code = f"""exec(eval('{zlib_}')(eval('{lzma_}')({compressed})))"""

    def Marshal(self):
        '''Marshalling Code'''
        # fake python error that serves no purpose except to make it look like an error occured if someone tries to replace "exec" with "print"
        fake_error = 'File "<string>", line 1\n    \n    ^\nSyntaxError: invalid syntax'
        marshal_code = marshal.dumps(compile(self.code, fake_error, 'exec'))
        # print(f'\n[+] Marshalled code: {len(self.code)} bytes | {round(len(marshal_code) / len(self.code) * 100, 1)}%')
        self.code = r"exec(__import__('\x6d\x61\x72\x73\x68\x61\x6c').loads({}), {})".format(marshal_code, {})

    def Protectors(self, anti_decompile: bool = ...) -> ...:
        '''Adding Self Protectors'''
        if anti_decompile is True:
            for_the_skids = f"\"\"\"{self.str_hex('Better luck next time skid 😂')}\"\"\"\n\n"
            self.code = for_the_skids + "for i in range(1):" + self.code
