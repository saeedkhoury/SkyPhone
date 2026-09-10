#!/usr/bin/env python3
"""Prepare a picture for the Sky Phone hero.

    python3 tools/hero-image.py ~/Downloads/whatever.jpg iphone-duo
    python3 tools/hero-image.py ~/Downloads/graphic.jpg repair-collage --soft

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
  3. Strips solid black letterbox bars. A screenshot or a re-encoded video
     frame often carries a few rows of pure black on one edge; the key reads
     them as artwork and they survive as a hard line across the finished image.
  4. Trims to the content and writes the three variants at hero sizes.

--soft is for designed graphics rather than product renders: a composition whose
own panels and cards are the same light grey as its background, so a flood fill
either leaks into them or fuses them into one blob. It removes the true outside
outright, then fades every light neutral pixel wherever it sits. What replaces
them is the hero's own light panel, which is the same tone — so it merges
instead of sitting in a box. Only use it on slides with ground:'light'; on a
dark panel those fills would show through as dark patches.

Requires Pillow and cwebp (both already used by this project).
"""
import subprocess, sys
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image

# 1100 is not arbitrary: picture() labels the full file `1100w` in its
# srcset, and the browser derives display density from that descriptor —
# a file narrower than its own label is reported at the wrong size.
FULL_W, SMALL_W = 1100, 520
ROOT = Path(__file__).resolve().parent.parent


def trim_black_bars(a):
    """Drop whole edge rows/columns that are essentially pure black."""
    lum = a.mean(2)
    t, b, l, r = 0, a.shape[0], 0, a.shape[1]
    while t < b and lum[t].mean() < 8: t += 1
    while b - 1 > t and lum[b - 1].mean() < 8: b -= 1
    while l < r and lum[:, l].mean() < 8: l += 1
    while r - 1 > l and lum[:, r - 1].mean() < 8: r -= 1
    return a[t:b, l:r], (t, a.shape[0] - b, l, a.shape[1] - r)


def key_soft(a):
    """For designed graphics: hard-remove the outside, fade light neutrals."""
    from scipy import ndimage as nd
    h, w, _ = a.shape
    lum, sat = a.mean(2), a.max(2) - a.min(2)
    K = np.ones((3, 3), bool)
    bg = (lum >= 188) & (sat <= 10)
    # Seal gaps in hairline outlines so the flood cannot leak into a panel.
    fl = bg & ~nd.binary_dilation(~bg, K, iterations=12)
    seeds = np.zeros((h, w), bool)
    seeds[0, :] = seeds[-1, :] = True
    seeds[:, 0] = seeds[:, -1] = True
    seeds &= fl
    lab, _ = nd.label(fl)
    keep = set(np.unique(lab[seeds])); keep.discard(0)
    outer = nd.binary_dilation(np.isin(lab, list(keep)), K, iterations=12) & bg
    t = np.clip((lum - 212) / 34.0, 0, 1)
    neutral = np.clip((14 - sat) / 10.0, 0, 1)
    alpha = np.clip(1 - t * neutral, 0, 1)
    alpha[outer] = 0.0
    alpha = nd.gaussian_filter(alpha, 0.6)
    rgba = np.dstack([a.astype(np.uint8), (alpha * 255).astype(np.uint8)])
    return Image.fromarray(rgba, "RGBA"), outer.mean()


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
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    soft = "--soft" in sys.argv
    if len(args) != 2:
        sys.exit(__doc__)
    src, name = Path(args[0]).expanduser(), args[1]
    if not src.exists():
        sys.exit(f"no such file: {src}")

    out = ROOT / "img"
    im = Image.open(src).convert("RGB")
    print(f"source        {im.size[0]}x{im.size[1]}  {src.name}")

    arr, bars = trim_black_bars(np.asarray(im).astype(float))
    if any(bars):
        im = Image.fromarray(arr.astype(np.uint8))
        print(f"black bars    stripped top={bars[0]} bottom={bars[1]} left={bars[2]} right={bars[3]}")
    else:
        print("black bars    none")

    im, band = strip_text_band(im)
    print(f"text band     {'removed rows 0-%d' % band[1] if band else 'none found — kept whole image'}")

    if soft:
        im, share = key_soft(np.asarray(im).astype(float))
        print(f"background    soft key — {share:.0%} removed outright, light neutrals faded")
        print("              remember: art:{img:…, shadow:false} on a ground:'light' slide")
    else:
        im, bg, share = key_background(im)
        print(f"background    {tuple(int(c) for c in bg)} — {share:.0%} of pixels made transparent")
    if not soft and share < 0.05:
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
    # A soft key writes a smooth, detailed alpha channel, and alpha is what
    # dominates the file size here — lossless alpha on this kind of image costs
    # roughly 2.4x for a difference of under half a level once it composites
    # onto a light panel. Hard-edged cut-outs keep lossless alpha.
    aq = "60" if soft else "100"
    for source, dest, q in ((big, out / f"{name}.webp", 88 if not soft else 74),
                            (small, out / f"{name}-sm.webp", 84 if not soft else 74)):
        stage = out / f".{dest.stem}.png"
        source.save(stage)
        subprocess.run(["cwebp", "-quiet", "-q", str(q), "-alpha_q", aq,
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
