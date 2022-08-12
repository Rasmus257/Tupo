import ast


class CombineWithStatements(ast.NodeTransformer):

    def visit_With(self, node):
        if len(node.body) == 1 and isinstance(node.body[0], ast.With):
            child_with = node.body[0]
            node.items.extend(child_with.items)
            node.body = child_with.body
        return self.generic_visit(node)
