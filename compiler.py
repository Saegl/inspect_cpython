import marshal
import argparse


cmdparser = argparse.ArgumentParser()
cmdparser.add_argument('input')
cmdparser.add_argument('output')

args = cmdparser.parse_args()


MAGIC_NUMBER = (3425).to_bytes(2, 'little') + b'\r\n'

def _pack_uint32(x):
    """Convert a 32-bit integer to little-endian."""
    return (int(x) & 0xFFFFFFFF).to_bytes(4, 'little')

with open(args.input, mode='rb') as f:
    data = f.read()


code = compile(data, 'hello.py', 'exec', dont_inherit=True, optimize=0)

fdata = bytearray(MAGIC_NUMBER)
fdata.extend(_pack_uint32(0))
fdata.extend(_pack_uint32(0)) # mtime
fdata.extend(_pack_uint32(0)) # source_size
fdata.extend(marshal.dumps(code))


with open(args.output, mode='wb') as f:
    f.write(fdata)
