#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

TOKENS = [
    "(´・ω・｀)",  # >
    "(´･ω・`)",   # <
    "(´・ω･`)",   # +
    "(´・ω・`)",  # -
    "(´･ω･｀)",   # .
    "(´･ω・ `)",  # ,
    "( ´･ω･`)",   # [
    "(´･ω･`)",    # ]
]

TO_BF = {
    "(´・ω・｀)": ">",
    "(´･ω・`)": "<",
    "(´・ω･`)": "+",
    "(´・ω・`)": "-",
    "(´･ω･｀)": ".",
    "(´･ω・ `)": ",",
    "( ´･ω･`)": "[",
    "(´･ω･`)": "]",
}

def tokenize(src: str):
    """Extract only the shobon tokens, ignoring all other chars."""
    i = 0
    out = []
    n = len(src)
    # どのトークンも固定文字列なので、愚直にスキャンします
    while i < n:
        matched = False
        for t in TOKENS:
            if src.startswith(t, i):
                out.append(TO_BF[t])
                i += len(t)
                matched = True
                break
        if not matched:
            i += 1
    return out

def build_bracket_map(code):
    stack = []
    mp = {}
    for i, c in enumerate(code):
        if c == "[":
            stack.append(i)
        elif c == "]":
            if not stack:
                raise SyntaxError(f"Unmatched ']' at instruction {i}")
            j = stack.pop()
            mp[i] = j
            mp[j] = i
    if stack:
        raise SyntaxError(f"Unmatched '[' at instruction {stack[-1]}")
    return mp

def run(code, inp_bytes: bytes):
    tape = [0]
    ptr = 0
    ip = 0
    in_i = 0
    out = bytearray()

    br = build_bracket_map(code)

    while ip < len(code):
        c = code[ip]

        if c == ">":
            ptr += 1
            if ptr == len(tape):
                tape.append(0)

        elif c == "<":
            ptr -= 1
            if ptr < 0:
                raise IndexError("Pointer moved to negative index")

        elif c == "+":
            tape[ptr] = (tape[ptr] + 1) & 0xFF

        elif c == "-":
            tape[ptr] = (tape[ptr] - 1) & 0xFF

        elif c == ".":
            out.append(tape[ptr])

        elif c == ",":
            if in_i < len(inp_bytes):
                tape[ptr] = inp_bytes[in_i]
                in_i += 1
            else:
                tape[ptr] = 0  # EOF -> 0

        elif c == "[":
            if tape[ptr] == 0:
                ip = br[ip]  # jump to matching ]
        elif c == "]":
            if tape[ptr] != 0:
                ip = br[ip]  # jump back to matching [

        ip += 1

    return bytes(out)

def main():
    # 使い方:
    #   python3 shobon.py program.txt < input.bin > output.bin
    if len(sys.argv) < 2:
        print("Usage: shobon.py <program_file>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        src = f.read()

    code = tokenize(src)
    inp = sys.stdin.buffer.read() if "," in code else b""
    out = run(code, inp)
    sys.stdout.buffer.write(out)

if __name__ == "__main__":
    main()
