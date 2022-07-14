import io

from ...conf_parser import Config
from .methods import reducers, removers, transformers


class Minifier:
    def __init__(self, code: str):
        self.code = code

    def minify(self):
        rem_cd = removers.remove_comments_and_docstrings
        transform_int = transformers.IntegerToPower

        if Config.get('RemoveComments'):
            self.code = rem_cd(self.code)

        # if Config.get('IntegerToPower'):
        #     transformer = transform_int()
        #     self.code = transformer.visit(self.code)

        min_obj = io.StringIO(reducers.reducer(self.code))
        return "".join([a for a in min_obj.readlines() if a.strip()])
