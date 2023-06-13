import ast
import argparse
import dis
import tokenize
import symtable


parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("--source", action="store_true")
parser.add_argument("--tokenize", action="store_true")
parser.add_argument("--ast", action="store_true")
parser.add_argument("--symtable", action="store_true")
parser.add_argument("--co", action="store_true")
parser.add_argument("--dis", action="store_true")
args = parser.parse_args()


with open(args.input, "rb") as f:
    source = f.read()


if args.source:
    print("=========================")
    print(f"Loaded file {args.input}")
    print("=========================")
    print(f"RAW BYTES {source}")
    print("=========================")
    print("\n\n\n")


if args.tokenize:
    print("=========================")
    print(f"Tokens for {args.input}")
    print("=========================")
    with open(args.input, "rb") as f:
        tokens = list(tokenize.tokenize(f.readline))

    # Output the tokenization
    for token in tokens:
        token_type = token.type
        # if args.exact:  # What are exact types?
        #     token_type = token.exact_type
        token_range = "%d,%d-%d,%d:" % (token.start + token.end)
        print(
            "%-20s%-15s%-15r"
            % (token_range, tokenize.tok_name[token_type], token.string)
        )
    print("=========================")
    print("\n\n\n")


if args.ast:
    print("=========================")
    print(f"AST {args.input}")
    print("=========================")
    mod = ast.parse(source)
    print(ast.dump(mod, indent=2))
    print("=========================")
    print("\n\n\n")


if args.symtable:
    print("=========================")
    print(f"SYMTABLE of {args.input}")
    print("=========================")
    table = symtable.symtable(source.decode(), args.input, "exec")

    def describe_symtable(
        st: symtable.SymbolTable | symtable.Function | symtable.Class, indent=0
    ):
        def print_d(s, *args):
            prefix = " " * indent
            print(prefix + s, *args)

        stype = st.get_type()

        print_d(f"Symtable: type={stype} name={st.get_name()}")
        print_d("|-nested:", st.is_nested())
        print_d("|-identifiers:", list(st.get_identifiers()))

        if stype == "function":
            print_d("function specific attrs:")
            print_d("|-parameters:", st.get_parameters())
            print_d("|-locals:", st.get_locals())
            print_d("|-globals:", st.get_globals())
            print_d("|-nonlocals:", st.get_nonlocals())
            print_d("|-frees:", st.get_frees())

        if stype == "class":
            print_d("class specific attrs:")
            print_d("|-methods", st.get_methods())

        print_d("symbols:")
        for symbol in st.get_symbols():
            print_d(f'Symbol "{symbol.get_name()}"')
            for symbol_attr in dir(symbol):
                if symbol_attr.startswith("is_"):
                    if getattr(symbol, symbol_attr)():
                        print_d("|+" + symbol_attr.removeprefix("is_"))

        print_d("children:")
        for child_st in st.get_children():
            describe_symtable(child_st, indent + 5)

    describe_symtable(table)
    print("=========================")
    print("\n\n\n")

codeobj = compile(source=source, filename="emptyfilename", mode="exec", optimize=0)


if args.co:
    print("=========================")
    print("Code object data")
    print("=========================")
    print("Name:", codeobj.co_name)
    print("Consts:")
    for i, const in enumerate(codeobj.co_consts):
        print("  ", i, ". ", const, sep="")
    print("Names:")
    for i, name in enumerate(codeobj.co_names):
        print("  ", i, ". ", name, sep="")
    print("Code:", codeobj.co_code)
    print("=========================")
    print("\n\n\n")


if args.dis:
    print("=========================")
    print("Disassembler")
    print("=========================")
    dis.dis(codeobj)
    print("=========================")
    print("\n\n\n")
