import tokenizer
from generate_replacement import generate
import token
import re

pattern_search = { 'if_pat': '\s*if\s*\w+',
                'for_pat': '\s*for\s*\w+\s*in\s*',
                'imp_pat': '\s*import\s*\w*',
                'met_pat': '\s*\w*\(\w*\)\s*',
                'ass_pat': '\s*\w*\s*\=\s*\w*',
                'wh_pat': '\s*while\s*\w*\:',
                'with_pat': '\s*with\s*[^\s.]*\s*'
                }

ignore_variable = ['__name__', '__main__', '__doc__', '__getattr__',
                '__setattr__', '__class__', '__bases__', '__subclasses__',
                '__init__', '__dict__', 'and', 'not']

replacement_dic = {}
import_list = []

def obfuscate(source):
    lines = tokenizer.tokenize_file(source)
    for ind, line in enumerate(lines):
        for p in pattern_search.keys():
            match = re.search(pattern_search.get(p), line)
            if match:
                search_variable_to_replace(line)
        if not line == '\n':
            lines[ind] = replace(line)
    return lines

def search_variable_to_replace(line):
    token_line = tokenizer.tokenize_line(line)
    for ind, tok in enumerate(token_line):
        old = ''
        # case 1: ( var ) or ( var ,
        if token_line[ind][1] == '(' and token_line[ind+1][0] == token.NAME and (token_line[ind+2][1] == ')' or token_line[ind+2][1] == ','):
            old = token_line[ind+1][1]

        # case 2 , var ) or , var ,
        elif token_line[ind][1] == ',' and token_line[ind+1][0] == token.NAME and (token_line[ind+2][1] == ')' or token_line[ind+2][1] == ','):
            old = token_line[ind+1][1]

        # case 3: assignment
        elif token_line[ind][0] == token.NAME and (token_line[ind+1][1] == '=' or token_line[ind+2][1] == '='):
            old = token_line[ind][1]

        # case 4: as var :
        elif token_line[ind][1] == 'as' and ((token_line[ind+1][0] == token.NAME and token_line[ind+2][1] == ':') or token_line[ind+1][0] == token.NAME):
            old = token_line[ind+1][1]

        # case 5: for var
        elif token_line[ind][1] == 'for' and token_line[ind+1][0] == token.NAME:
            old = token_line[ind+1][1]

        # case 6: if var
        elif token_line[ind][1] == 'if' and token_line[ind+1][0] == token.NAME and not token_line[ind+2][1] == '(':
            old = token_line[ind+1][1]

        # case 7: save import module
        elif token_line[ind][1] == 'import' and token_line[ind+1][0] == token.NAME:
            import_list.append(token_line[ind+1][1])

        replace = generate()
        if old not in replacement_dic.keys() and not old == '' and replace not in replacement_dic.items():
            replacement_dic[old] = replace

def replace(line):
    token_line = tokenizer.tokenize_line(line)
    for ind, token in enumerate(token_line):
        if token_line[ind][1] in replacement_dic and token_line[ind][1] not in ignore_variable:
            if ind > 1 and token_line[ind-2][1] in import_list:
                continue
            token_line[ind][1] = replacement_dic.get(token_line[ind][1])

    return tokenizer.untokenize_line(token_line)
