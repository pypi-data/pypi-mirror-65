# Authorr: Bartholomew Roberts
# License: WTFPL
'''Yarr ain't RPC, Ritchie!

A simple RPC implementation using a binary serialization protocol. It supports
the basic built-in types, numpy arrays work if available on both client and
server. Hence, yarr is well equipped to efficiently handle large binary booty.

While it's not as insecure as pickle, causing a stack overflow should be easy
for someone malicious like that landlubber Blackbeard.

Example Server:
>>> yarr.yarr(('localhost', 8000), [print])

Example Client:
>>> yarr.call(('localhost', 8000), 'print', 'Ahoy Lads!')
'''

import struct
import socket
import socketserver
import traceback
try:
    import numpy
    _HAVE_NUMPY = True
except ImportError:
    _HAVE_NUMPY = False

_TAG = {list:7, tuple:8, set:9, frozenset:10, bytes:11, bytearray:12}
_CAST = {v:k for k,v in _TAG.items()}

def dump(obj, file):
    '''Write object to an open file object. Can raise TypeError.'''
    otype = type(obj)
    if otype == type(None):
        file.write(struct.pack('<B', 0))
    elif otype == bool:
        file.write(struct.pack('<B?', 1, obj))
    elif otype == int and obj.bit_length() <= 64:
        file.write(struct.pack('<Bq', 2, obj))
    elif otype == float:
        file.write(struct.pack('<Bd', 3, obj))
    elif otype == complex:
        file.write(struct.pack('<Bdd', 4, obj.real, obj.imag))
    elif otype == int: # bignum
        size = (obj.bit_length() + 7) // 8
        file.write(struct.pack('<BI', 5, size))
        file.write(obj.to_bytes(size, 'little', signed=True))
    elif otype == str:
        tmp = obj.encode('utf8', 'surrogateescape')
        file.write(struct.pack('<BI', 6, len(tmp)))
        file.write(tmp)
    elif otype in (list, tuple, set, frozenset):
        file.write(struct.pack('<BI', _TAG[otype], len(obj)))
        for el in obj:
            dump(el, file)
    elif otype in (bytes, bytearray):
        file.write(struct.pack('<BI', _TAG[otype], len(obj)))
        file.write(obj)
    elif otype == dict:
        file.write(struct.pack('<BI', 13, len(obj)))
        for key, val in obj.items():
            dump(key, file)
            dump(val, file)
    elif _HAVE_NUMPY and otype == numpy.ndarray:
        file.write(struct.pack('<B', 254))
        dump(obj.dtype.str, file)
        dump(obj.tobytes(), file)
    else:
        raise TypeError(type(obj))

def load(file):
    '''Read object from an open file object. Can raise TypeError.'''
    tag, = struct.unpack('<B', file.read(1))
    if 5 <= tag <= 13:
        size, = struct.unpack('<I', file.read(4))
    if tag == 0: # none
        return None
    elif tag == 1: # bool
        return struct.unpack('<?', file.read(1))[0]
    elif tag == 2: # int
        return struct.unpack('<q', file.read(8))[0]
    elif tag == 3: # float
        return struct.unpack('<d', file.read(8))[0]
    elif tag == 4: # complex
        return complex(*struct.unpack('<dd', file.read(16)))
    elif tag == 5: # bignum
        return int.from_bytes(file.read(size), 'little', signed=True)
    elif tag == 6: # str
        return file.read(size).decode('utf8', 'surrogateescape')
    elif tag in (7, 8, 9, 10): # list tuple set frozenset
        return _CAST[tag](load(file) for _ in range(size))
    elif tag in (11, 12): # bytes bytearray
        return _CAST[tag](file.read(size))
    elif tag == 13: # dict
        return dict((load(file), load(file)) for _ in range(size))
    elif _HAVE_NUMPY and tag == 254: # numpy.ndarray
        dtype = load(file)
        return numpy.frombuffer(load(file), dtype)
    else:
        raise TypeError(tag)

def call(address, func, *args, **kwargs):
    '''Call remote function on address. Can raise RuntimeError.'''
    sock = socket.socket()
    sock.connect(address)
    file = sock.makefile(mode='rwb', buffering=-1)
    # write function name and arguments
    dump(func, file)
    dump(args, file)
    dump(kwargs, file)
    file.flush()
    # check for error
    if load(file):
        raise RuntimeError(load(file))
    # read output
    return load(file)

def yarr(address, functions):
    '''Start server on address for list of functions.'''
    calls = {f.__name__: f for f in functions}

    class Handler(socketserver.StreamRequestHandler):
        def handle(self):
            # read function name and arguments
            func = load(self.rfile)
            args = load(self.rfile)
            kwargs = load(self.rfile)
            try:
                # call function
                output = calls[func](*args, **kwargs)
            except Exception as e:
                # signal error, write stacktrace
                dump(True, self.wfile)
                dump(traceback.format_exc(), self.wfile)
            else:
                # write output
                dump(False, self.wfile)
                dump(output, self.wfile)

    socketserver.TCPServer(address, Handler).serve_forever()
