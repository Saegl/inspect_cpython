# Inspect CPython

My notes on how to inspect CPython interpreter and it's bytecode


## Show Abstract Syntax Tree

```bash
python -m ast example_programs/hello.py
```


## Show bytecode

```bash
python -m dis example_programs/hello.py
```


## Compile to bytecode

```bash
python -m py_compile example_programs/hello.py
```