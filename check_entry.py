# Self-check for the round-2 entry. Standard library only.
# Verifies: PNG magic, size <= 1 MiB, dimensions 1024x1024, and that
# main.py run twice (grader conditions: no network, read-only repo,
# output as a mount) writes byte-identical output and leaves a
# pre-existing file in the output directory untouched.
#
# Run: python3 check_entry.py

import hashlib
import os
import shutil
import struct
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(33)
    assert head[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG"
    w, h = struct.unpack(">II", head[16:24])
    return w, h


def run_main(out_dir, extra_env=None):
    env = dict(os.environ)
    env["MAKEFUN_OUTPUT_DIR"] = out_dir
    if extra_env:
        env.update(extra_env)
    proc = subprocess.run([sys.executable, os.path.join(HERE, "main.py")],
                          env=env, capture_output=True, text=True, timeout=60)
    return proc


def main():
    entry = os.path.join(HERE, "entry.png")
    size = os.path.getsize(entry)
    assert size <= 1048576, "entry.png over 1 MiB: %d" % size
    w, h = png_size(entry)
    assert (w, h) == (1024, 1024), "dimensions %dx%d" % (w, h)
    print("entry.png: %d bytes, %dx%d, sha256 %s" % (size, w, h, sha256(entry)))

    digests = []
    for run in (1, 2):
        tmp = tempfile.mkdtemp(prefix="grader-run-%d-" % run)
        try:
            sentinel = os.path.join(tmp, "keep-me.txt")
            with open(sentinel, "w") as f:
                f.write("pre-existing\n")
            proc = run_main(tmp)
            assert proc.returncode == 0, \
                "run %d exit %d: %s" % (run, proc.returncode, proc.stderr)
            assert os.path.exists(sentinel), \
                "run %d removed a pre-existing file" % run
            with open(sentinel) as f:
                assert f.read() == "pre-existing\n", \
                    "run %d modified a pre-existing file" % run
            out = os.path.join(tmp, "entry.png")
            assert os.path.exists(out), "run %d wrote no entry.png" % run
            digests.append(sha256(out))
            print("run %d: exit 0, output sha256 %s" % (run, digests[-1]))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    assert digests[0] == digests[1], "two runs differ"
    assert digests[0] == sha256(entry), "output differs from entry.png"
    print("two runs byte-identical: OK")
    print("ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
