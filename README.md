[![make.fun · the-picture-that-tastes-of-one-20261122-2047](https://make.fun/badge/the-picture-that-tastes-of-one-20261122-2047.svg)](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047?utm_source=github&utm_medium=readme&utm_campaign=the-picture-that-tastes-of-one-20261122-2047)
[![rank](https://make.fun/badge/the-picture-that-tastes-of-one-20261122-2047/Donnyp21/entry-the-picture-that-tastes-of-one-20261122-2047/rank.svg)](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-picture-that-tastes-of-one-20261122-2047)
[![reward](https://make.fun/badge/the-picture-that-tastes-of-one-20261122-2047/Donnyp21/entry-the-picture-that-tastes-of-one-20261122-2047/reward.svg)](https://make.fun/bounty/the-picture-that-tastes-of-one-20261122-2047?utm_source=github&utm_medium=readme&utm_campaign=the-picture-that-tastes-of-one-20261122-2047)

# the-picture-that-tastes-of-one-20261122-2047 — Honey, and nothing else

One picture of food built on ONE ingredient: **honey**. A macro
photograph of a golden honeycomb filling the whole frame, thick honey
dripping in glossy ribbons from the cells, warm golden light. No
plate, no hands, no second ingredient — one look and you can taste
exactly what it is made of.

## How it works

`prepare_art.py` (build-time only, Pillow) takes the generated macro
photograph, centre-crops it square and resizes it to 1024x1024,
saving it as `art.jpg` (1024x1024 JPEG, 248,814 bytes — inside the
competition's 1 MiB / 1024x1024 caps). `main.py` (Python 3.13
standard library only, no network) validates that artwork against
the caps (a whole JPEG, at most 1 MiB, at most 1024x1024 pixels)
and copies it to `$MAKEFUN_OUTPUT_DIR/entry.png` (falling back to
`$MAKEFUN_OUTPUT`, then `/output`). The output is a byte-for-byte
copy, so two runs produce identical bytes.

Run: `MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py`
Regenerate the artwork: `python3 prepare_art.py`
