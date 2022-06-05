from src import Config


class Obfuscation(object):
    def __init__(self, src):
        self.code = src

    def init(self):
        if not Config.get_setting('Obfuscate'):
            return
        if Config.get_setting('DeadCode'):
            self.dead_code_injector()
        if Config.get_setting('OneLine'):
            self.minify()

    def add_layer(self):

        def wall(layer):
            pass

        for i in range(Config.get_setting('LayerAmount')):
            self.wall()

    def dead_code_injector(self):
        pass

    def minify(self):
        pass
