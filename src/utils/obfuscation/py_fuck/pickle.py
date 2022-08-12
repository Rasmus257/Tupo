import math
import pickle
from ast import AST, parse


class ASTObj():
    def __repr__(self): return "\\AST"


def chunkify(lst, n) -> list:
    return [lst[i::n] for i in range(n)]


def get_compressed_path_list(path_list) -> list:
    paths = []
    [paths.extend(p) for p in [path for path, _ in path_list]]
    return paths


def get_required_path_strings(pickled_objects) -> list:
    paths = get_compressed_path_list(pickled_objects)
    return list(set(filter(lambda item: type(item) is str, paths)))


def get_required_path_integers(pickled_objects) -> list:
    paths = get_compressed_path_list(pickled_objects)
    return list(set(filter(lambda item: type(item) is int, paths)))


def get_all_bytestrings(pickled_objects) -> list:
    return [bts.decode('ISO-8859-1') for _, bts in pickled_objects]


def get_required_characters(pickled_objects) -> list:
    string_list = "".join(get_required_path_strings(pickled_objects))
    bytes_list = "".join(get_all_bytestrings(pickled_objects))
    return list(set(string_list + bytes_list))


def get_required_pathlists(pickled_objects) -> list:
    return [path_list for path_list, _ in pickled_objects]


def get_pickled_object_list(code: str) -> list:
    global ast
    ast = parse(code)
    visited = []
    deleted_paths = []
    pickled_objects = []

    def walk_ast_dict(obj, path: list) -> None:
        field = {}
        if isinstance(obj, AST):
            visited.append(path)
            for key, v in obj.__dict__.items():
                if key in obj._fields:
                    field[key] = v
            walk_ast_dict(field, path + [ASTObj()])

        elif type(obj) is dict:
            for key, v in obj.items():
                walk_ast_dict(v, path + [key])

        elif type(obj) is list:
            for i, item in enumerate(obj):
                walk_ast_dict(item, path + [i])

    def get_exec_path(path) -> str:
        access_string = "ast"
        for item in path:
            if type(item) is int:
                access_string += f"[{item}]"
            elif type(item) is str:
                access_string += f".{item}"
        return access_string

    def pickle_ast_object(path) -> None:
        obj_to_pickle = eval(get_exec_path(path))
        pickled_objects.append((path, pickle.dumps(obj_to_pickle)))

    def delete_ast_item_at_path(path) -> None:
        if path == []:
            exec("global ast;ast=None")
        else:
            exec(get_exec_path(path) + "=None")
        deleted_paths.append(path)

    def recursively_pickle(path) -> None:
        target_index = max(index for index, item in enumerate(path) if type(item) == ASTObj) if len(path) > 0 else None
        item_path = path[:target_index]
        if not item_path in deleted_paths:
            pickle_ast_object(item_path)
            delete_ast_item_at_path(item_path)

    walk_ast_dict(ast, [])
    for path in reversed(sorted(visited, key=len)):
        recursively_pickle(path)
    return pickled_objects


def nearest_sqrt(number) -> int:
    floor_sqrt = math.floor(math.sqrt(number))
    ceil_sqrt = math.floor(math.sqrt(number))
    floor_diff, ceil_diff = number - floor_sqrt, ceil_sqrt - number
    return floor_sqrt if floor_diff >= ceil_diff else ceil_sqrt


def create_sqrt_number(number) -> str:
    if number < 3:
        return str(number)
    num_sqrt = nearest_sqrt(number)
    nearest_perfect_square = num_sqrt ** 2
    distance = abs(number - nearest_perfect_square)
    symbol = "+" if number > nearest_perfect_square else ("-" if number < nearest_perfect_square else None)
    if symbol is None:
        return f"{create_sqrt_number(num_sqrt)}**2"
    else:
        return f"({create_sqrt_number(num_sqrt)}**2{symbol}{create_sqrt_number(distance) if distance > 2 else distance})"
