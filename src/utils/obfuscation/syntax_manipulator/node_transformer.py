import ast
import random


class StringObfuscator:
    def __init__(self, node):
        self.node = node
        self.str = self.node.s

    def transform(self) -> str:
        if len(self.str) == 0:
            return self.none()
        elif len(self.str) == 1:
            return self.single()
        return self.multi()

    def none(self):
        return ast.Call(func=ast.Name(id='str', ctx=ast.Load()),
                        args=[], keywords=[], starargs=None, kwargs=None)

    def single(self):
        return ast.Call(func=ast.Name(id='chr', ctx=ast.Load()),
                        args=[ast.Num(ord(self.str), **dict(kind=None))], keywords=[], starargs=None, kwargs=None)

    def multi(self):
        i = random.randrange(len(self.str))
        return ast.BinOp(left=ast.Str(s=self.str[:i], **dict(kind=None)), right=ast.Str(s=self.str[i:], **dict(kind=None)), op=ast.Add())


class IntegerObfuscator:
    def __init__(self, node):
        self.node = node
        self.num = str(self.node.n)

    def transform(self) -> int or float:
        if len(self.num) == 0:
            return self.zero()
        elif len(self.num) == 1:
            return self._int()
        else:
            return self._float()

    def zero(self):
        return ast.Call(
            func=ast.Name(id='int', ctx=ast.Load()),
            args=[ast.BinOp(left=ast.Num(n=random.random(), **dict(kind=None)), right=ast.Num(n=0, **dict(kind=None)), op=ast.Mult())],
            keywords=[], starargs=None, kwargs=None
        )

    def _int(self, _range=100):
        s = random.randint(-_range, _range)
        return ast.BinOp(left=ast.Num(n=self.node.n - s, **dict(kind=None)), right=ast.Num(n=s, **dict(kind=None)), op=ast.Add())

    def _float(self):
        s = random.random()
        return ast.BinOp(left=ast.Num(n=self.node.n - s, **dict(kind=None)), right=ast.Num(n=s, **dict(kind=None)), op=ast.Add())
