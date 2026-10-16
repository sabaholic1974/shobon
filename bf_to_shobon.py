#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

BF_TO_SHOBON = {
    ">": "(´・ω・｀)",
    "<": "(´･ω・`)",
    "+": "(´・ω･`)",
    "-": "(´・ω・`)",
    ".": "(´･ω･｀)",
    ",": "(´･ω・ `)",
    "[": "( ´･ω･`)",   # ※先頭に半角スペース1つ
    "]": "(´･ω･`)",
}

BF_CHARS = set(BF_TO_SHOBON.keys())

def convert(bf_src: str) -> str:
    # brainfuckの8命令以外は無視
    out = []
    for ch in bf_src:
        if ch in BF_CHARS:
            out.append(BF_TO_SHOBON[ch])
    return "".join(out)

def main():
    # 使い方:
    #   python3 bf_to_shobon.py input.bf > output.shobon
    #   python3 bf_to_shobon.py input.bf output.txt
    if len(sys.argv) < 2:
        print("Usage: bf_to_shobon.py <input.bf> [output.txt]", file=sys.stderr)
        sys.exit(1)

    in_path = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) >= 3 else None

    with open(in_path, "r", encoding="utf-8", errors="ignore") as f:
        bf_src = f.read()

    shobon = convert(bf_src)

    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(shobon)
    else:
        sys.stdout.write(shobon)

if __name__ == "__main__":
    main()
