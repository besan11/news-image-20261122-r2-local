# Entry program — news-image-20261122 round 2.
# Copies the rendered front page (entry.png, stored beside this file)
# into the grader's output directory. Standard library only.
#
# Grader lesson, applied here: the output directory is a bind mount in
# the grader, so this program NEVER deletes it or anything inside it.
# It only writes one file, entry.png, and checks the bytes afterwards.

import hashlib
import os
import shutil
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    dst = os.path.join(out_dir, "entry.png")

    with open(src, "rb") as f:
        data = f.read()
    if data[:8] != PNG_MAGIC:
        print("entry.png is not a PNG", file=sys.stderr)
        return 1
    if len(data) > 1048576:
        print("entry.png is over 1 MiB", file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    with open(dst, "wb") as f:
        f.write(data)

    with open(dst, "rb") as f:
        written = f.read()
    if hashlib.sha256(written).hexdigest() != hashlib.sha256(data).hexdigest():
        print("written bytes differ from entry.png", file=sys.stderr)
        return 1
    print("wrote %s (%d bytes)" % (dst, len(written)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
