import os
import shutil
import sys
from multiprocessing import Process
from tempfile import mkdtemp

import analyzer

from config import conf
from src import Config, MainHandler, antivm_code
from src import rem_comments_and_docstrings as rem_cd

__author__ = 'Rdimo'
__version__ = '1.0.0'
__license__ = 'MIT'


class Tupo:
    def __init__(self):
        self.src = os.getcwd() + "/src"
        self.tools = self.src + "/tools"
        self._file, self.name, self.icon, self.imports = self.configurate()

    def execute(self, args):
        os.system(f'pipenv run {args}')

    def install(self, args):
        os.system(f'pipenv install {args}')

    def cleanup(self):
        shutil.move(f'dist/{self.name}.exe', f'{self.name}.exe')
        for _dir in ['build', 'dist', '__pycache__']:
            if os.path.exists(_dir):
                shutil.rmtree(_dir, ignore_errors=True)
        if os.path.exists(self.name + '.spec'):
            os.remove(self.name + '.spec')
        # os.system('pipenv clean')

    def get_imports(self, code):
        imports = []
        code_array = []
        for i in code.splitlines():
            if i.startswith("import") or i.startswith("from"):
                imports.append(i)
            else:
                code_array.append(i)
        code = '\n'.join(c for c in code_array)
        # to remove duplicate imports
        imports = list(dict.fromkeys(imports))
        code = '\n'.join(imports) + '\n' + code
        return code, imports

    def configurate(self):
        file_path = 'test/test.py'
        name = 'test'
        icon = None
        content = open(file_path).read()

        code = rem_cd(content)  # removing comments, docstrings, etc. to avoid issues further down the line

        if Config.is_enabled('Protectors') and Config.get('AntiDebug'):
            code = antivm_code + code

        code, imports = self.get_imports(code)

        if conf.get('CompressOnly') is True:
            return os.path.abspath(file_path), str(name), icon, imports
        del conf['CompressOnly']

        H = MainHandler(code)
        code = H()

        with open(file='yes.py', mode='wb') as f:
            f.write(code.encode('utf-8'))

        return os.path.abspath(file_path), str(name), icon, imports

    def main(self):
        print('[+] Setting up virtual environment...')
        print(self.imports)
        pyinstaller = f"pyinstaller --onefile --clean --upx-dir={self.tools}"
        print('[+] Installing dependencies...')
        self.install('pyinstaller')
        for i in self.imports:
            self.install(i)
            pyinstaller += f' --hidden-import={i}'
        if Config.get('EncryptBytecode'):
            self.install('tinyaes')
            pyinstaller += f' --key={os.urandom(32)}'

        if self.icon is None:
            pyinstaller += ' -i NONE'
        else:
            pyinstaller += f' -i {self.icon}'

        pyinstaller += f' -n {self.name} {self._file}'
        p = Process(target=self.execute, args=(pyinstaller, ))
        p.start()
        p.join()
        os.system('exit')
        self.cleanup()


if __name__ == "__main__":
    supported_ver = 3
    windows = 'nt'

    if os.name != windows:
        raise SystemExit('[!] Sorry! Tupo only works for Windows!')

    if sys.version_info[0] != supported_ver:
        raise ImportError('[!] Sorry! Tupo Only supports Python3 --> https://www.python.org/downloads/')
    # Tupo().main()
    Tupo()
