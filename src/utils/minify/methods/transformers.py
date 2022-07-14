import ast
import math


class FunctionToLambda(ast.NodeTransformer):
    def visit_Functions(self, node):
        if node.decorator_list or node.returns:
            return node
        if not isinstance(node.body[0], ast.Return) or len(node.body) > 1:
            return node
        args = node.args

        if ((args.vararg and args.vararg.annotation) or
                (args.kwarg and args.kwarg.annotation)):
            return node

        if any(arg.annotation for arg in args.args):
            return node

        _return = node.body[0].value
        if _return is None:
            _return = ast.Name('None', ast.Load())
        lambda_ = ast.Lambda(args, _return)
        return ast.Assign([ast.Name(node.name, ast.Store())], lambda_)


class IntegerToPower(ast.NodeTransformer):
    def visit_Num(self, node):
        num = node.n
        if not isinstance(num, int):
            return node

        if num >= 10**5 and not math.log10(num) % 1:
            power_10 = int(math.log10(num))
            return ast.BinOp(ast.Num(10), ast.Pow(), ast.Num(power_10))

        elif num >= 2**17 and not math.log2(num) % 1:
            power_2 = int(math.log2(num))
            return ast.BinOp(ast.Num(2), ast.Pow(), ast.Num(power_2))

        return node


class CombineWithStatements(ast.NodeTransformer):
    def visit_With(self, node):
        self.generic_visit(node)
        if len(node.body) == 1 and isinstance(node.body[0], ast.With):
            child_with = node.body[0]
            node.items.extend(child_with.items)
            node.body = child_with.body
        return node
