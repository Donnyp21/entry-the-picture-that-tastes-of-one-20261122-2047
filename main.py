"""the-picture-that-tastes-of-one-20261122-2047 entry: one ingredient,
honey, in one picture.

The entry is a macro photograph of a golden honeycomb with thick honey
dripping from it, generated for this brief and prepared by
prepare_art.py (centre-cropped square, resized to 1024x1024, saved as
art.jpg). One ingredient only: honey -- honeycomb and honey, nothing
else in the frame, so a single look tells you exactly what it tastes
of. The comb fills the frame edge to edge, the honey glistens and
drips, and the picture still reads as honey at 300 pixels wide.

This program validates the checked artwork (art.jpg, beside this
file) against the competition's caps (a whole JPEG, at most 1 MiB, at
most 1024x1024 pixels) and copies it to the output directory as
entry.png. The rules tell PNG from JPEG by the file's first bytes, so
the name stays entry.png while the bytes stay JPEG.

Python 3.13 standard library only. No network. Deterministic: the
output is a byte-for-byte copy of art.jpg.
"""

import os
import shutil
import struct
import sys

LIMIT_BYTES = 1_048_576   # the rules cap the output at 1 MiB
LIMIT_SIDE = 1024         # and at 1024 x 1024 pixels
ARTWORK = "art.jpg"
OUT_NAME = "entry.png"

# JPEG markers that carry no length field (SOI, EOI, TEM, RST0-7).
STANDALONE = {0x01, 0xD8, 0xD9} | set(range(0xD0, 0xD8))
# Start-of-frame markers whose segment holds the picture's size.
SOF = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
       0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}


def jpeg_size(path):
    """Return (width, height) read from a JPEG start-of-frame segment."""
    with open(path, "rb") as fh:
        if fh.read(2) != b"\xff\xd8":
            raise ValueError("not a JPEG: missing start-of-image marker")
        while True:
            head = fh.read(2)
            if len(head) < 2 or head[0] != 0xFF:
                raise ValueError("not a JPEG: segment header missing")
            marker = head[1]
            if marker in STANDALONE:
                if marker == 0xD9:
                    break
                continue
            raw = fh.read(2)
            if len(raw) < 2:
                raise ValueError("not a JPEG: truncated segment")
            seg_len = struct.unpack(">H", raw)[0]
            if marker in SOF:
                fh.read(1)  # sample precision
                height, width = struct.unpack(">HH", fh.read(4))
                return width, height
            fh.seek(seg_len - 2, os.SEEK_CUR)
    raise ValueError("not a JPEG: no start-of-frame segment found")


def whole_jpeg(path):
    """True when the file's last two bytes are the JPEG end marker."""
    with open(path, "rb") as fh:
        fh.seek(-2, os.SEEK_END)
        return fh.read(2) == b"\xff\xd9"


def run():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, ARTWORK)
    out_dir = (os.environ.get("MAKEFUN_OUTPUT_DIR")
               or os.environ.get("MAKEFUN_OUTPUT")
               or "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, OUT_NAME)

    nbytes = os.path.getsize(src)
    if not 0 < nbytes <= LIMIT_BYTES:
        print(f"error: {ARTWORK} is {nbytes} bytes, "
              f"outside 1..{LIMIT_BYTES}", file=sys.stderr)
        return 1
    try:
        width, height = jpeg_size(src)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if width > LIMIT_SIDE or height > LIMIT_SIDE:
        print(f"error: {ARTWORK} is {width}x{height}, "
              f"over the {LIMIT_SIDE}x{LIMIT_SIDE} cap", file=sys.stderr)
        return 1
    if not whole_jpeg(src):
        print(f"error: {ARTWORK} has no end-of-image marker",
              file=sys.stderr)
        return 1
    print(f"checked {ARTWORK}: {width}x{height}, {nbytes} bytes")

    shutil.copyfile(src, dst)
    if os.path.getsize(dst) != nbytes:
        print("error: the copy's size differs from the artwork",
              file=sys.stderr)
        return 1
    print(f"wrote {dst}: {nbytes} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
