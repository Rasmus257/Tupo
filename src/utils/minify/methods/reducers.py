import io
import tokenize


def reducer(code):
    return join_multiline_pairs(remove_spaces(code))


def clean(tkns):
    last_line, last_col, out = -1, 0, ""

    for tok in tkns:
        token_string = tok[1]
        start_line, start_col = tok[2]
        end_line, end_col = tok[3]

        if start_line > last_line:
            last_col = 0

        if start_col > last_col and token_string != '\n':
            out += (" " * (start_col - last_col))

        out += token_string
        last_col = end_col
        last_line = end_line
    return out


def remove_spaces(code):
    joining_strings = False
    prev_tok, minified, new_str = None, "", ""
    last_line, last_col = -1, 0
    nl_types = (tokenize.NL, tokenize.NEWLINE)

    for tok in tokenize.generate_tokens(io.StringIO(code).readline):
        token_type = tok[0]
        token_string = tok[1]
        start_line, start_col = tok[2]
        end_line, end_col = tok[3]

        if start_line > last_line:
            last_col = 0

        if token_type != tokenize.OP:
            if start_col > last_col and token_type not in nl_types:
                if prev_tok[0] != tokenize.OP:
                    minified += (" " * (start_col - last_col))

            if token_type == tokenize.STRING:
                if prev_tok[0] == tokenize.STRING:
                    string_type = token_string[0]
                    prev_string_type = prev_tok[1][0]
                    minified = minified.rstrip(" ")

                    if not joining_strings:
                        minified = minified[:(len(minified) - len(prev_tok[1]))]
                        prev_string = prev_tok[1].strip(prev_string_type)
                        new_str = (prev_string + token_string.strip(string_type))
                        joining_strings = True
                    else:
                        new_str += token_string.strip(string_type)
        else:
            if token_string in ('}', ')', ']'):
                if prev_tok[1] == ',':
                    minified = minified.rstrip(',')

            if joining_strings:
                minified += "'''" + new_str + "'''"
                joining_strings = False

            if token_string == '@':
                if prev_tok[0] == tokenize.NEWLINE:
                    minified += (" " * (start_col - last_col))

        if not joining_strings:
            minified += token_string

        last_col = end_col
        last_line = end_line
        prev_tok = tok
    return minified


def join_multiline_pairs(source, pair="()"):
    opener, closer = pair[0], pair[1]
    open_count, out_tokens = 0, []

    for tok in tokenize.generate_tokens(io.StringIO(source).readline):
        token_type = tok[0]
        token_string = tok[1]
        if token_type == tokenize.OP and token_string in pair:
            if token_string == opener:
                open_count += 1
            elif token_string == closer:
                open_count -= 1
            out_tokens.append(tok)
        elif token_type in (tokenize.NL, tokenize.NEWLINE):
            if open_count == 0:
                out_tokens.append(tok)
        else:
            out_tokens.append(tok)
    return clean(out_tokens)
