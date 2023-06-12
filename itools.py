import ast
import argparse
import dis


parser = argparse.ArgumentParser()
parser.add_argument('input')
parser.add_argument('--source', action='store_true')
parser.add_argument('--ast', action='store_true')
parser.add_argument('--co', action='store_true')
parser.add_argument('--dis', action='store_true')
args = parser.parse_args()


with open(args.input, 'rb') as f:
    source = f.read()


if args.source:
    print('=========================')
    print(f"Loaded file {args.input}")
    print('=========================')
    print(f"RAW BYTES {source}")
    print('=========================')
    print('\n\n\n')


if args.ast:
    print('=========================')
    print(f"AST {args.input}")
    print('=========================')
    mod = ast.parse(source)
    print(ast.dump(mod, indent=2))
    print('=========================')
    print('\n\n\n')

codeobj = compile(
    source=source,
    filename='emptyfilename',
    mode='exec',
    optimize=0
)


if args.co:
    print('=========================')
    print("Code object data")
    print('=========================')
    print(dir(codeobj))
    print("Name:", codeobj.co_name)
    print("Consts:")
    for i, const in enumerate(codeobj.co_consts):
        print('  ', i, '. ', const, sep='')
    print("Names:")
    for i, name in enumerate(codeobj.co_names):
        print('  ', i, '. ', name, sep='')
    print("Code:", codeobj.co_code)
    print('=========================')
    print('\n\n\n')


if args.dis:
    print('=========================')
    print("Disassembler")
    print('=========================')
    dis.dis(codeobj)
    print('=========================')
    print('\n\n\n')
