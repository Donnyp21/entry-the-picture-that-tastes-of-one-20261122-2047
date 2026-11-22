"""Prepare the artwork for the-picture-that-tastes-of-one entry.

Build-time tool only (run once, here, with Pillow). Takes the
AI-generated macro honeycomb photograph (SRC, 1920x1280), centre-crops
it to a square so the dripping honey stays in frame, resizes it to
1024x1024, and saves it as art.jpg at JPEG quality 88 -- well inside
the competition's caps (whole JPEG, at most 1 MiB, at most
1024x1024 pixels). main.py re-checks those caps before copying.
"""

from PIL import Image

SRC = "media-generation-art-0-0a05f4b8-a8c8-4e18-8e08-dfd6ffec2f10.jpg"
DST = "art.jpg"
SIDE = 1024
QUALITY = 88

im = Image.open(SRC).convert("RGB")
w, h = im.size
side = min(w, h)
left = (w - side) // 2
top = (h - side) // 2
im = im.crop((left, top, left + side, top + side))
im = im.resize((SIDE, SIDE), Image.LANCZOS)
im.save(DST, "JPEG", quality=QUALITY, optimize=True)
print(f"wrote {DST}: {im.size[0]}x{im.size[1]}")
