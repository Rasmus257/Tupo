import os
import shutil
import sys
from multiprocessing import Process

from config import conf
from src import Config, MainHandler, antivm_code
from src import rem_comments_and_docstrings as rem_cd
from src.utils.storage.errors import VersionError

__author__ = 'Rdimo'
__version__ = '1.0.0'
__license__ = 'MIT'


class Tupo:
    def __init__(self, file_path, name, icon):
        self.src = os.getcwd() + "/src"
        self.tools = self.src + "/tools"
        self._file, self.name, self.icon, self.imports = self.configurate(file_path, name, icon)

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

    def configurate(self, file_path=None, name=None, icon=None):
        content = open(file_path, 'rb').read().decode()

        code = rem_cd(content)  # removing comments, docstrings, etc. to avoid issues further down the line

        if Config.is_enabled('Protectors') and Config.get('AntiDebug'):
            code = antivm_code + code

        code, imports = self.get_imports(code)

        if conf.get('CompressOnly') is True:
            return os.path.abspath(file_path), str(name), icon, imports
        del conf['CompressOnly']
        import ast
        with open('ast_tree_dump.txt', 'wb') as f:
            f.write(ast.dump(ast.parse(code, 'Tupo'), include_attributes=True, indent=4).encode())
        H = MainHandler(code)
        code = H()

        if name.endswith('.py'):
            name = name[:-3]
        with open(file=f'test-obf/{name}.py', mode='wb') as f:
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
    args = sys.argv
    supported_ver = (3, 8)
    windows = 'nt'

    if os.name != windows:
        raise SystemExit('[!] Sorry! Tupo only works for Windows!')

    if sys.version_info[:2] < (3, 8):
        raise VersionError('[!] Sorry! Tupo Only supports Python3.8+ --> https://www.python.org/downloads/')

    # Tupo().main()

    try:
        file_path = args[1]
    except IndexError:
        file_path = r'.\test-obf\test_general.py'
    name = os.path.basename(file_path)
    icon = None
    Tupo(file_path=file_path, name=name, icon=icon)
