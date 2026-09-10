#!/usr/bin/env python3
"""Prepare a picture for the Sky Phone hero.

    python3 tools/hero-image.py ~/Downloads/whatever.jpg iphone-duo

Writes img/<name>.png, img/<name>.webp and img/<name>-sm.webp, which is exactly
the set the hero's <picture> asks for. Then add one entry to HERO_SLIDES in
app.js — see docs/hero-images.md.

What it does, and why each step is here:

  1. Strips a baked-in text band. Shop-forwarded promo images usually carry the
     product name and a tagline burned into the pixels. The hero has its own
     translated title, tag and note layers, so baked-in text both duplicates
     them and shows the wrong language to two thirds of the audience. The
     script finds the tall blank band that separates the text block from the
     photograph and keeps only what is below it.
  2. Keys out the background by flooding inward from the border, so light
     regions *inside* the product - a screen, a white chassis - survive where a
     plain colour threshold would punch holes in them.
  3. Trims to the content and writes the three variants at hero sizes.

Requires Pillow and cwebp (both already used by this project).
"""
import subprocess, sys
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image

FULL_W, SMALL_W = 1200, 520
ROOT = Path(__file__).resolve().parent.parent


def strip_text_band(im, min_gap=120):
    """Drop everything above the tallest blank band in the top half.

    A promo image is text, a generous gap, then the photograph. That gap is the
    tallest run of empty rows in the upper half, and nothing inside a product
    photograph comes close to it. An image with no such gap is returned whole.
    """
    a = np.asarray(im).astype(int)
    h, w, _ = a.shape
    bg = a[:12, :12].reshape(-1, 3).mean(0)
    ink = (np.abs(a - bg).sum(2) > 28).sum(1) > 3

    # Scan the whole image, but only accept a gap that *starts* in the top
    # 60%: below that it is separation inside the photograph, not the divide
    # between the caption and the picture. Scanning only the top half would
    # miss the real gap whenever it straddles the midpoint, which is exactly
    # where a caption-then-photo layout tends to put it.
    limit = int(h * 0.6)
    runs, run = [], None
    for y in range(h):
        if not ink[y]:
            run = y if run is None else run
        elif run is not None:
            runs.append((run, y))
            run = None
    if run is not None:
        runs.append((run, h))

    candidates = [r for r in runs if r[0] < limit and r[1] - r[0] >= min_gap and r[1] < h]
    if not candidates:
        return im, None
    best = max(candidates, key=lambda r: r[1] - r[0])
    return im.crop((0, best[1], w, h)), best


def key_background(im, tol=30):
    """Make the flat page background transparent, from the border inward."""
    a = np.asarray(im).astype(int)
    h, w, _ = a.shape
    bg = np.array(a[:8, :8].reshape(-1, 3).mean(0)).round()
    close = np.abs(a - bg).sum(2) <= tol

    seen = np.zeros((h, w), bool)
    q = deque()
    edges = [(y, x) for x in range(w) for y in (0, h - 1)]
    edges += [(y, x) for y in range(h) for x in (0, w - 1)]
    for y, x in edges:
        if close[y, x] and not seen[y, x]:
            seen[y, x] = True
            q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and close[ny, nx] and not seen[ny, nx]:
                seen[ny, nx] = True
                q.append((ny, nx))

    rgba = np.dstack([a.astype(np.uint8), np.where(seen, 0, 255).astype(np.uint8)])
    return Image.fromarray(rgba, "RGBA"), bg, seen.mean()


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    src, name = Path(sys.argv[1]).expanduser(), sys.argv[2]
    if not src.exists():
        sys.exit(f"no such file: {src}")

    out = ROOT / "img"
    im = Image.open(src).convert("RGB")
    print(f"source        {im.size[0]}x{im.size[1]}  {src.name}")

    im, band = strip_text_band(im)
    print(f"text band     {'removed rows 0-%d' % band[1] if band else 'none found — kept whole image'}")

    im, bg, share = key_background(im)
    print(f"background    {tuple(int(c) for c in bg)} — {share:.0%} of pixels made transparent")
    if share < 0.05:
        print("              WARNING: almost nothing was removed. If this picture has a\n"
              "              photographic (not flat) background, cut it out by hand instead.")

    im = im.crop(im.getbbox())
    print(f"trimmed       {im.size[0]}x{im.size[1]}")

    png = out / f"{name}.png"
    big = im.resize((FULL_W, round(im.size[1] * FULL_W / im.size[0])), Image.LANCZOS)
    # The PNG is only the fallback for browsers without WebP, so it is
    # palette-quantised. FASTOCTREE is the one Pillow mode that keeps alpha.
    big.quantize(colors=200, method=Image.FASTOCTREE).save(png, optimize=True)

    small = im.resize((SMALL_W, round(im.size[1] * SMALL_W / im.size[0])), Image.LANCZOS)
    tmp = out / f".{name}-sm.png"
    small.save(tmp)
    for source, dest, q in ((big, out / f"{name}.webp", 88), (small, out / f"{name}-sm.webp", 84)):
        stage = out / f".{dest.stem}.png"
        source.save(stage)
        subprocess.run(["cwebp", "-quiet", "-q", str(q), "-alpha_q", "100",
                        str(stage), "-o", str(dest)], check=True)
        stage.unlink()
    tmp.unlink(missing_ok=True)

    print()
    for f in (png, out / f"{name}.webp", out / f"{name}-sm.webp"):
        print(f"  wrote  img/{f.name:<28} {f.stat().st_size // 1024:>4} KB")
    print(f"\nNow add a slide to HERO_SLIDES in app.js with art:{{img:'img/{name}.png'}}")
    print("and the three T keys it names. See docs/hero-images.md.")


if __name__ == "__main__":
    main()
