import math
from random import sample

from .pickle import *


def obfuscate(code: str) -> str:
    def create_num(number):
        factors = []
        if number == 0:
            return zero
        if number == 1:
            return one
        while number % 2 == 0:
            factors.append(2)
            number //= 2
        for i in range(3, int(math.sqrt(number)) + 1, 2):
            while number % i == 0:
                factors.append(i)
                number //= i
        if number > 2:
            factors.append(number)
        return "*".join(f"{create_sqrt_number(n)}" for n in factors) if len(factors) > 1 else create_sqrt_number(factors[0]).replace("0", zero).replace("1", one).replace("2", two)

    rnd_sample = sample(["_", "__", "___", "____", "_____", "______", "_______", "________"], 8)
    rnd_sample_lamdba = lambda i: sample(["_" + "_" * i for i in range(i)], i)

    utility_class_id, char_class_id, runtime_class_id, ast_wrapper_class_id, number_class_id, built_ast_id, pickled_objects, ast_obj_filler_class_id = rnd_sample
    u_blank_string, u_getattr, u_getbuiltin, u_create_type, u_dict, u_globals, u_class, u_dir, u_name, u_ge, u_iter, u_int, u_float, u_complex, u_ord, u_True, u_empty_list, u_empty_dict, u_chr, u_hex, u_equals_comp, u_pow, u_str, u_reversed, u_file = rnd_sample_lamdba(
        25)
    a_create_exec_path, a_walk_pickled_objects, a_undo_pickling, a_do_exec, a_get_global_decl, a_semicolon, a_underscore, a_quote, a_equals_pickle_loads, a_open_paren, a_close_paren, a_string_join, a_open_bracket, a_close_bracket, a_period, a_hyphen, a_do_iso_encoding = rnd_sample_lamdba(
        17)

    output = f"{utility_class_id}=lambda _:type(*_);_0_=str;{runtime_class_id}=dict;"

    zero_name, one_name, two_name = sample(["_", "__", "___"], 3)
    zero, one, two = f"{number_class_id}.{zero_name}", f"{number_class_id}.{one_name}", f"{number_class_id}.{two_name}"
    output += f"_0=lambda _0:_0.__code__.co_argcount;{built_ast_id}=None;__0=_0;{number_class_id}={utility_class_id}([_0_(),(),{runtime_class_id}("
    numbers = [f"{zero_name}=_0(lambda:__0)", f"{one_name}=_0(lambda _0:_0)", f"{two_name}=_0(lambda _0,__0:_0)"]
    output += ",".join(sample(numbers, len(numbers))) + f")]);{pickled_objects}=[];"
    output += f"{utility_class_id}={utility_class_id}([_0_(),(),{runtime_class_id}("

    utility_class_functions = [
        f"{u_blank_string}=lambda:{utility_class_id}.{u_getbuiltin}({utility_class_id}.{u_name}({utility_class_id}.{u_class}({utility_class_id}.{u_empty_list}()))[{create_num(2)}:{create_num(4)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_iter}())[{create_num(3)}])()",
        f"{u_getattr}=lambda _0,__0:{utility_class_id}.{u_getbuiltin}({utility_class_id}.{u_name}({utility_class_id}.{u_ge}({utility_class_id}.{u_int}()))[{create_num(2)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_complex}())[{create_num(5)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_iter}())[{create_num(1)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_float}())[{create_num(3)}]+({utility_class_id}.{u_name}({utility_class_id}.{u_iter}())[{create_num(1)}]*{create_num(2)})+{utility_class_id}.{u_name}({utility_class_id}.{u_ord}())[{create_num(1)}])(_0,__0)",
        f"{u_getbuiltin}=lambda _0:getattr({utility_class_id}.{u_globals}()()[{utility_class_id}.{u_name}({utility_class_id}.{u_dir}(()))[{create_num(1)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_dir}(()))[{create_num(1)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_class}({utility_class_id}.{u_True}()))[{create_num(0)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_class}(({utility_class_id},)))[{create_num(1)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_class}({utility_class_id}.{u_empty_list}()))[{create_num(1)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_class}({utility_class_id}.{u_empty_list}()))[{create_num(0)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_class}({utility_class_id}.{u_empty_list}()))[{create_num(3)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_class}({utility_class_id}.{u_int}()()))[:{create_num(2)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_class}({utility_class_id}.{u_empty_list}()))[{create_num(2)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_dir}(()))[{create_num(1)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_dir}(()))[{create_num(1)}]],_0)",
        f"{u_chr}=lambda _0:{utility_class_id}.{u_getbuiltin}({utility_class_id}.{u_name}({utility_class_id}.{u_complex}())[{create_num(0)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_hex}())[{create_num(0)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_iter}())[{create_num(3)}])(_0)",
        f"{u_reversed}=lambda:{utility_class_id}.{u_getbuiltin}({utility_class_id}.{u_name}({utility_class_id}.{u_iter}())[{create_num(3)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_iter}())[{create_num(2)}]+{utility_class_id}.{u_chr}({create_num(118)})+{utility_class_id}.{u_name}({utility_class_id}.{u_iter}())[{create_num(2)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_iter}())[{create_num(3)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_class}({utility_class_id}.{u_empty_list}()))[{create_num(2)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_iter}())[{create_num(2)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_class}({utility_class_id}.{u_empty_dict}()))[{create_num(0)}])",
        f"{u_create_type}=lambda _0:{utility_class_id}.{u_getbuiltin}({utility_class_id}.{u_name}({utility_class_id}.{u_class}(type({utility_class_id}.{u_blank_string}()))))(*_0)",
        f"{u_equals_comp}=lambda _0,__0:_0==__0",
        f"{u_globals}=lambda:globals",
        f"{u_dict}=lambda:{utility_class_id}.{u_getbuiltin}({utility_class_id}.{u_name}({utility_class_id}.{u_class}({utility_class_id}.{u_empty_dict}())))",
        f"{u_class}=lambda _:_.__class__",
        f"{u_dir}=lambda _:_.__dir__",
        f"{u_name}=lambda _:_.__name__",
        f"{u_ge}=lambda _:_.__ge__",
        f"{u_file}=lambda:__file__",
        f"{u_iter}=lambda:iter",
        f"{u_int}=lambda:{utility_class_id}.{u_class}({create_num(0)})",
        f"{u_float}=lambda:float",
        f"{u_complex}=lambda:complex",
        f"{u_ord}=lambda:ord",
        f"{u_True}=lambda:{utility_class_id}.{u_equals_comp}({utility_class_id},{utility_class_id})",
        f"{u_empty_list}=lambda:[]",
        f"{u_empty_dict}=lambda:{{}}",
        f"{u_hex}=lambda:hex",
        f"{u_pow}=lambda:pow",
        f"{u_str}=lambda:str"
    ]

    output += ",".join(sample(utility_class_functions, len(utility_class_functions))) + ")]);"
    output += f"{utility_class_id}.{u_getbuiltin}({utility_class_id}.{u_name}({utility_class_id}.{u_complex}())[{create_num(5)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_hex}())[{create_num(2)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_complex}())[{create_num(5)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_complex}())[{create_num(0)}])({utility_class_id}.{u_name}({utility_class_id}.{u_class}([]))[{create_num(1)}]+{utility_class_id}.{u_chr}({create_num(109)})+{utility_class_id}.{u_name}({utility_class_id}.{u_pow}())[{create_num(0)}]+"
    output += f"{utility_class_id}.{u_name}({utility_class_id}.{u_ord}())[{create_num(0)}:{create_num(2)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_class}([]))[{create_num(3)}]+{utility_class_id}.{u_chr}({create_num(32)})+{utility_class_id}.{u_name}({utility_class_id}.{u_pow}())[{create_num(0)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_iter}())[{create_num(0)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_complex}())[{create_num(0)}]+{utility_class_id}.{u_chr}({create_num(107)})+{utility_class_id}.{u_name}({utility_class_id}.{u_class}([]))[{create_num(0)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_complex}())[{create_num(5)}]);"
    output += f"{ast_obj_filler_class_id}={utility_class_id}.{u_create_type}([{utility_class_id}.{u_blank_string}(),(),{utility_class_id}.{u_dict}()()]);"
    output += f"{ast_wrapper_class_id}={utility_class_id}.{u_create_type}([{utility_class_id}.{u_blank_string}(),(),{utility_class_id}.{u_dict}()("

    ast_class_functions = [
        f"{a_do_exec}=lambda _0,__0:{utility_class_id}.{u_getbuiltin}({utility_class_id}.{u_name}({utility_class_id}.{u_complex}())[{create_num(5)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_hex}())[{create_num(2)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_complex}())[{create_num(5)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_complex}())[{create_num(0)}])(_0)",
        f"{a_equals_pickle_loads}=lambda:{utility_class_id}.{u_chr}({create_num(61)})+{utility_class_id}.{u_name}({utility_class_id}.{u_pow}())[{create_num(0)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_iter}())[{create_num(0)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_complex}())[{create_num(0)}]+{utility_class_id}.{u_chr}({create_num(107)})+{utility_class_id}.{u_name}({utility_class_id}.{u_class}([]))[{create_num(0)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_complex}())[{create_num(5)}]+{utility_class_id}.{u_chr}({create_num(46)})+{utility_class_id}.{u_name}({utility_class_id}.{u_class}([]))[{create_num(0)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_complex}())[{create_num(1)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_float}())[{create_num(3)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_ord}())[{create_num(2)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_globals}())[-{create_num(1)}]",
        f"{a_do_iso_encoding}=lambda _0:{utility_class_id}.{u_getattr}(_0,{utility_class_id}.{u_name}({utility_class_id}.{u_complex}())[{create_num(5)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_int}())[{create_num(1)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_complex}())[{create_num(0)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_ord}())[{create_num(0)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_ord}())[{create_num(2)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_complex}())[{create_num(5)}])({utility_class_id}.{u_chr}({create_num(73)})+{utility_class_id}.{u_chr}({create_num(83)})+{utility_class_id}.{u_chr}({create_num(79)})+{ast_wrapper_class_id}.{a_hyphen}()+{utility_class_id}.{u_str}()({create_num(8859)})+{ast_wrapper_class_id}.{a_hyphen}()+{utility_class_id}.{u_str}()({create_num(1)}))",
        f"{a_string_join}=lambda:{utility_class_id}.{u_getattr}({utility_class_id}.{u_str}()(),{utility_class_id}.{u_chr}({create_num(106)})+{utility_class_id}.{u_name}({utility_class_id}.{u_pow}())[{create_num(1)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_iter}())[{create_num(0)}]+{utility_class_id}.{u_chr}({create_num(110)}))",
        f"{a_create_exec_path}=lambda _0:({ast_wrapper_class_id}.{a_underscore}()*{create_num(len(built_ast_id))})+{ast_wrapper_class_id}.{a_string_join}()(({ast_wrapper_class_id}.{a_open_bracket}()+{utility_class_id}.{u_str}()(__0)+{ast_wrapper_class_id}.{a_close_bracket}())if({utility_class_id}.{u_equals_comp}({utility_class_id}.{u_create_type}([__0]),{utility_class_id}.{u_int}()))else(({ast_wrapper_class_id}.{a_period}()+__0)if({utility_class_id}.{u_equals_comp}({utility_class_id}.{u_create_type}([__0]),{utility_class_id}.{u_str}()))else({utility_class_id}.{u_str}()()))for(__0)in(_0))",
        f"{a_get_global_decl}=lambda:{utility_class_id}.{u_name}({utility_class_id}.{u_globals}())[:-{create_num(1)}]+{utility_class_id}.{u_chr}({create_num(32)})+{ast_wrapper_class_id}.{a_underscore}()*({create_num(len(built_ast_id))})+{ast_wrapper_class_id}.{a_semicolon}()",
        f"{a_walk_pickled_objects}=lambda:[{ast_wrapper_class_id}.{a_undo_pickling}(_0,{ast_wrapper_class_id}.{a_do_iso_encoding}(__0))for(_0,__0)in({utility_class_id}.{u_reversed}()({pickled_objects}))]",
        f"{a_undo_pickling}=lambda _0,__0:{ast_wrapper_class_id}.{a_do_exec}({ast_wrapper_class_id}.{a_get_global_decl}()+{ast_wrapper_class_id}.{a_create_exec_path}(_0)+{ast_wrapper_class_id}.{a_equals_pickle_loads}()+{ast_wrapper_class_id}.{a_open_paren}()+({ast_wrapper_class_id}.{a_underscore}()*{create_num(2)})+{utility_class_id}.{u_str}()({create_num(0)})+{ast_wrapper_class_id}.{a_close_paren}(),__0)",
        f"{a_semicolon}=lambda:{utility_class_id}.{u_chr}({create_num(59)})", f"{a_underscore}=lambda:{utility_class_id}.{u_chr}({create_num(95)})",
        f"{a_quote}=lambda:{utility_class_id}.{u_chr}({create_num(34)})", f"{a_open_paren}=lambda:{utility_class_id}.{u_chr}({create_num(40)})",
        f"{a_close_paren}=lambda:{utility_class_id}.{u_chr}({create_num(41)})", f"{a_open_bracket}=lambda:{utility_class_id}.{u_chr}({create_num(91)})",
        f"{a_close_bracket}=lambda:{utility_class_id}.{u_chr}({create_num(93)})", f"{a_period}=lambda:{utility_class_id}.{u_chr}({create_num(46)})",
        f"{a_hyphen}=lambda:{utility_class_id}.{u_chr}({create_num(45)})"]

    output += ",".join(ast_class_functions) + ")]);"
    objs = get_pickled_object_list(code)

    _splits = 20
    char_subclasses = ["", "", "", "", ""]
    char_pathstring_items = []
    char_mapping, string_mapping, int_mapping, byte_mapping, pathlist_mapping = {}, {}, {}, {}, {}
    c_subclass_pathstrings, c_subclass_pathints, c_subclass_chars, c_subclass_bytes, c_subclass_pathlists = sample(["_", "__", "___", "____", "_____"], 5)

    output += f"{char_class_id}={utility_class_id}.{u_create_type}([{utility_class_id}.{u_blank_string}(),(),{utility_class_id}.{u_dict}()("

    char_subclasses[0] += f"{c_subclass_chars}={utility_class_id}.{u_create_type}([{utility_class_id}.{u_blank_string}(),(),{utility_class_id}.{u_dict}()("
    required_characters = get_required_characters(objs)
    split_class_required_characters = chunkify(required_characters, _splits)
    split_class_required_characters_ids = sample(["_" + "_" * i for i in range(_splits)], _splits)

    for index, char_list in enumerate(split_class_required_characters):
        individual_character_variables = sample(["_" + "_" * i for i in range(len(char_list))], len(char_list))
        for char_index, char in enumerate(char_list):
            char_mapping[char] = [split_class_required_characters_ids[index], individual_character_variables[char_index]]

    char_subclass_list = ["" for _ in range(_splits)]
    for index, character_subclass in enumerate(split_class_required_characters):
        char_subclass_list[
            index] += f"{split_class_required_characters_ids[index]}={utility_class_id}.{u_create_type}([{utility_class_id}.{u_blank_string}(),(),{utility_class_id}.{u_dict}()("

        individual_characters = [f"{char_mapping[char][-1]}={utility_class_id}.{u_chr}({create_num(ord(char))})" for char in character_subclass]
        char_subclass_list[index] += ",".join(sample(individual_characters, len(individual_characters))) + ")])"
    char_subclasses[0] += ",".join(sample(char_subclass_list, len(char_subclass_list))) + ")])"

    char_subclasses[1] += f"{c_subclass_pathstrings}={utility_class_id}.{u_create_type}([{utility_class_id}.{u_blank_string}(),(),{utility_class_id}.{u_dict}()("
    required_strings = get_required_path_strings(objs)
    required_strings_ids = sample(["_" + "_" * i for i in range(len(required_strings))], len(required_strings))

    for i in range(len(required_strings)):
        string_mapping[required_strings[i]] = required_strings_ids[i]
        string_content = "+".join(f"{char_class_id}.{c_subclass_chars}.{'.'.join(char_mapping[ch])}" for ch in required_strings[i])
        char_pathstring_items.append(f"{required_strings_ids[i]}=lambda:{string_content}")
    char_subclasses[1] += ",".join(sample(char_pathstring_items, len(char_pathstring_items))) + ")])"

    char_subclasses[2] += f"{c_subclass_pathints}={utility_class_id}.{u_create_type}([{utility_class_id}.{u_blank_string}(),(),{utility_class_id}.{u_dict}()("
    required_integers = get_required_path_integers(objs)
    required_integers_ids = sample(["_" + "_" * i for i in range(len(required_integers))], len(required_integers))

    for i, integer in enumerate(required_integers):
        int_mapping[integer] = required_integers_ids[i]

    char_storage_pathint_items = [f"{required_integers_ids[i]}={create_num(required_integers[i])}" for i in range(len(required_integers))]
    char_subclasses[2] += ",".join(sample(char_storage_pathint_items, len(char_storage_pathint_items))) + ")])"

    char_subclasses[3] += f"{c_subclass_bytes}={utility_class_id}.{u_create_type}([{utility_class_id}.{u_blank_string}(),(),{utility_class_id}.{u_dict}()("
    required_bytes = list(set(get_all_bytestrings(objs)))
    split_class_required_bytes = chunkify(required_bytes, _splits)
    split_class_required_bytes_ids = sample(["_" + "_" * i for i in range(_splits)], _splits)

    for index, byte_list in enumerate(split_class_required_bytes):
        individual_byte_variables = sample(["_" + "_" * i for i in range(len(byte_list))], len(byte_list))
        for byte_index, byte_string in enumerate(byte_list):
            byte_mapping[byte_string] = [split_class_required_bytes_ids[index], individual_byte_variables[byte_index]]

    byte_subclass_list = ["" for _ in range(_splits)]
    for index, byte_subclass in enumerate(split_class_required_bytes):
        byte_subclass_list[
            index] += f"{split_class_required_bytes_ids[index]}={utility_class_id}.{u_create_type}([{utility_class_id}.{u_blank_string}(),(),{utility_class_id}.{u_dict}()("

        byte_strings = []
        for byte_string in byte_subclass:
            string_content = "+".join(f"{char_class_id}.{c_subclass_chars}.{'.'.join(char_mapping[char])}" for char in byte_string)
            byte_strings.append(f"{byte_mapping[byte_string][-1]}=lambda:{string_content}")

        byte_subclass_list[index] += ",".join(sample(byte_strings, len(byte_strings))) + ")])"
    char_subclasses[3] += ",".join(sample(byte_subclass_list, len(byte_subclass_list))) + ")])"

    char_subclasses[4] += f"{c_subclass_pathlists}={utility_class_id}.{u_create_type}([{utility_class_id}.{u_blank_string}(),(),{utility_class_id}.{u_dict}()("
    required_pathlists = get_required_pathlists(objs)
    split_class_required_pathlists = chunkify(required_pathlists, _splits)
    split_class_required_pathlists_ids = sample(["_" + "_" * i for i in range(_splits)], _splits)

    for index, pathlist_list in enumerate(split_class_required_pathlists):
        individual_pathlist_variables = sample(["_" + "_" * i for i in range(len(pathlist_list))], len(pathlist_list))
        for path_index, path_list in enumerate(pathlist_list):
            pathlist_mapping[str(path_list)] = [split_class_required_pathlists_ids[index], individual_pathlist_variables[path_index]]

    pathlist_subclass_list = ["" for _ in range(_splits)]
    for index, pathlist_subclass in enumerate(split_class_required_pathlists):
        pathlist_subclass_list[
            index] += f"{split_class_required_pathlists_ids[index]}={utility_class_id}.{u_create_type}([{utility_class_id}.{u_blank_string}(),(),{utility_class_id}.{u_dict}()("

        individual_pathlist_strings = []
        for path_list in pathlist_subclass:
            list_items = [ast_obj_filler_class_id if type(item) == ASTObj else (f"{char_class_id}.{c_subclass_pathstrings}.{string_mapping[item]}()" if type(
                item) == str else f"{char_class_id}.{c_subclass_pathints}.{int_mapping[item]}") for item in path_list]
            string_content = "[" + ",".join(list_items) + "]"
            individual_pathlist_strings.append(f"{pathlist_mapping[str(path_list)][-1]}=lambda:{string_content}")

        pathlist_subclass_list[index] += ",".join(sample(individual_pathlist_strings, len(individual_pathlist_strings))) + ")])"
    char_subclasses[4] += ",".join(sample(pathlist_subclass_list, len(pathlist_subclass_list))) + ")])"

    output += ",".join(sample(char_subclasses, len(char_subclasses))) + ")]);"

    items = []
    for path, byte_string in objs:
        item_string = f"({char_class_id}.{c_subclass_pathlists}.{'.'.join(p for p in pathlist_mapping[str(path)])}(),{char_class_id}.{c_subclass_bytes}.{'.'.join(p for p in byte_mapping[byte_string.decode('ISO-8859-1')])}())"
        items.append(item_string)

    output += f"{pickled_objects}=[{','.join(items)}];"
    output += f"{ast_wrapper_class_id}.{a_walk_pickled_objects}();"
    output += f"{utility_class_id}.{u_getbuiltin}({utility_class_id}.{u_name}({utility_class_id}.{u_complex}())[{create_num(5)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_hex}())[{create_num(2)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_complex}())[{create_num(5)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_complex}())[{create_num(0)}])({utility_class_id}.{u_getbuiltin}({utility_class_id}.{u_name}({utility_class_id}.{u_complex}())[:{create_num(4)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_iter}())[{create_num(0)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_class}([]))[{create_num(0)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_complex}())[{create_num(5)}])({built_ast_id},{utility_class_id}.{u_file}(),{utility_class_id}.{u_name}({utility_class_id}.{u_complex}())[{create_num(5)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_hex}())[{create_num(2)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_complex}())[{create_num(5)}]+{utility_class_id}.{u_name}({utility_class_id}.{u_complex}())[{create_num(0)}]))"

    return output
