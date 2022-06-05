import os
import sys
import shutil
from src import Config
from multiprocessing import Process

__author__ = 'Rdimo'
__version__ = '1.0.0'


class PyHide:
    def __init__(self):
        self.src = os.getcwd() + "/src"
        self.tools = self.src + "/tools"
        self._file, self.name, self.icon = self.configurate()

    def execute(self, args):
        os.system(f'pipenv run {args}')

    def install(self, args):
        os.system(f'pipenv install {args}')

    def cleanup(self):
        shutil.move(f'dist/{self.name}.exe', f'{self.name}.exe')
        for _dir in ['build', 'dist', '__pycache__']:
            if os.path.exists(_dir):
                shutil.rmtree(_dir, ignore_errors=True)
        if os.path.exists(self.name+'.spec'):
            os.remove(self.name+'.spec')
        # os.system('pipenv clean')

    def configurate(self):
        _file = input('Enter file: ')
        if not os.path.exists(_file):
            print(f"Coudln't find \"{_file}\"!")
            sys.exit(0)
        if not _file.endswith('.py'):
            print(f"{_file} is not a python file!")
            sys.exit(0)
        name = input('Enter name: ')
        icon = input('Enter icon (optional): ')
        if icon and (not os.path.exists(icon) or not os.path.isfile(icon) or not icon.endswith('.ico')):
            print(f"Coudln't find \"{icon}\", either it doesn't exist or it's not a valid file!")
            sys.exit(0)
        else:
            icon = None
        return os.path.abspath(_file), str(name), icon

    def main(self):
        pyinstaller = f"pyinstaller --onefile --clean --upx-dir={self.tools}"
        self.install('pyinstaller')

        if Config.get_setting('EncryptBytecode'):
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
    PyHide().main()
