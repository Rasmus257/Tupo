import io
import tokenize


def remove_comments_and_docstrings(code) -> str:
    """
    removes comments, docstrings and shebangs. 

    Example:
        def test():
            '''
            idk what this does
            '''
            pass # yes

    Will be minified to:
        def test():
            pass
    """
    prev_toktype = tokenize.INDENT
    last_line, last_col, out = -1, 0, ""

    for tok in tokenize.generate_tokens(io.StringIO(code).readline):
        token_type, token_string = tok[0], tok[1]
        start_line, start_col = tok[2]
        end_line, end_col = tok[3]

        if start_line > last_line:
            last_col = 0

        if start_col > last_col:
            out += (" " * (start_col - last_col))

        if token_type == tokenize.COMMENT:
            pass

        elif token_type == tokenize.STRING:
            if prev_toktype != tokenize.INDENT:
                if prev_toktype != tokenize.NEWLINE:
                    if start_col > 0:
                        out += token_string
        else:
            out += token_string

        prev_toktype = token_type
        last_col = end_col
        last_line = end_line

    out = '\n'.join(l for l in out.splitlines() if l.strip())
    return out
