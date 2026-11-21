#!/usr/bin/env python3
"""Copy entry.png (next to this script) to /output/entry.png, byte for byte."""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "entry.png")
    dst_dir = "/output"
    os.makedirs(dst_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(dst_dir, "entry.png"))


if __name__ == "__main__":
    main()
