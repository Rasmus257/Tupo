class SourceTypeReplacer:
    def __init__(self, code):
        self.source = code

    def __repr__(self):
        return self.replace(self.source)

    def replace(self):
        return self.source.replace('"""', '\"\"\"').replace('\\', '\\\\').replace('\n', '\\n')
