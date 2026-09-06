# Handoff — where things stand

Written 2026-09-06, at the end of the hero-rebuild task. Read this first if picking
this project back up cold.

## Repo location (important — this moved)

The project directory moved from `~/Desktop/SkyPhone` to `~/Desktop/projects/SkyPhone`
between sessions (an external reorganization, not something done as part of this
task). Same git repo, same remote, no data lost — just a different path. **If a local
dev server 404s, it's almost certainly still bound to the old, now-nonexistent path —
kill it and restart from the new location:**

```bash
cd ~/Desktop/projects/SkyPhone
python3 -m http.server 8901
```

- Repo: `https://github.com/saeedkhoury/SkyPhone.git`
- Live: `https://saeedkhoury.github.io/SkyPhone/` (GitHub Pages, deploys from `main`)
- Latest commit at the time of writing: `95708c4` — "Rebuild hero into composed ad
  units instead of full-bleed JPG slides" — pushed to `main`.

## What just happened

A separate session (routed through this one via the `/find_skills` command, which
doesn't actually apply here — the input was a full implementation brief, not a skill
search) had already prepared: a detailed spec for rebuilding the homepage hero, and
three raw source images at the repo root (`sky_phone3.jpg` — the correct, full iPhone
18 teaser poster; `playstation.jpeg`; `26 ultra.webp`). This session executed that
brief end-to-end:

1. **Removed the old hero entirely** — it was three slides, each a finished JPG/SVG
   mockup dropped into a fixed box (`.ad-full-slide`, `object-fit:contain`), which
   letterboxed into visible bands whenever the image's aspect ratio didn't match the
   box. All of `.hero-device*`, `.draw-ring`/`.draw-check`, `.hero-inner`, `.hero-cta`,
   `.hero-fade`, their keyframes, and the two JS functions that drove pointer-tilt/
   parallax on the old mockup (`initHeroTilt`, `initHeroParallax`) are gone.
2. **Rebuilt it as three composed ad units** — real HTML (badge, `<h2>` title,
   tagline, a live-data price/note line, two pill CTAs) with the product art as a
   transparent-background cutout standing on its own ground, light or dark per slide,
   modeled on apple.com/il's hero pattern. See `DESIGN.md`'s newest entry for the full
   technical breakdown (grounds, art treatments, the two-element animation-ownership
   rule, the exact bug that was found and fixed during verification).
3. **Slide 0 — iPhone 18 Pro** (light ground): the cutout image was regenerated from
   the *correct* source. An earlier round had used `sky_phone2.jpg`, which has
   "SKYPHONE" baked directly across the phone body — this session's supplied
   `sky_phone3.jpg` is the actual clean poster (title lockup cleanly separated from
   the product shot), which is what `img/iphone18-pro.png` is now cut from.
4. **Slide 1 — PlayStation 5** (light ground): art and price are now pulled live from
   the product catalog (`PRODUCTS` id 27) instead of a separate static image, and the
   slide links straight into its real, purchasable product page.
5. **Slide 2 — Repairs** (dark ground): same composed structure as the other two,
   with a live "from ₪X" note computed from the real repairs data.
6. **Verified in-browser** (desktop, all three languages, RTL controls, zero console
   errors, no horizontal overflow) and found + fixed one real bug along the way: the
   pointer-tilt effect cached its target element once at page-load, which went stale
   the moment the PS5 slide's art got rebuilt on a language switch. Fixed by querying
   the element fresh inside the event handlers instead of caching it.

## Cleaned up

- Deleted the now-unused `img/iphone18-series-ad.jpg` and `img/ps5-ad.jpeg` (the
  previous round's separate hero assets, superseded by the catalog-fed/regenerated
  approach above).
- Deleted the raw source files that were sitting at the repo root
  (`sky_phone1/2/3.jpg`, `playstation.jpeg`, `26 ultra.webp`, a stray root-level
  `iphone18-pro.png`) once their useful content was processed into `img/`.
- Cache-busting query bumped to `?v=20260906f` on both `styles.css` and `app.js`.

## Not fully verified — worth a look before calling this done

- **Mobile viewport (390×844)**: the browser automation's window-resize tool didn't
  actually shrink the CSS viewport in this environment (kept reporting 1440×723
  regardless of the requested size), so the ≤920px responsive rules for the new hero
  CSS were reviewed by eye but not screenshot-verified at a real mobile width. The
  CSS follows the same `@media (max-width:920px)` patterns already proven elsewhere
  in this codebase, so risk is low, but a real device/DevTools check is worth doing.
- **`prefers-reduced-motion`**: not pixel-verified live (no easy way to toggle OS-level
  reduced-motion from this browser automation setup). The CSS includes the guard
  (`@media (prefers-reduced-motion:reduce){ .ad-art-float{animation:none} }`)
  following the same pattern used everywhere else on the site.
- **`.hero-ad-art.blend`** (the third art treatment defined in the CSS, for a supplied
  creative that carries its own background) isn't used by any current slide — it's
  there and ready for whenever a future campaign asset needs it, but is unexercised
  code until then.

## Known pre-existing items, unrelated to this task

- No real payment processing (demo placeholder, documented in `PRODUCT.md`).
- No backend — cart/filters reset on reload.
- A handful of catalog SKUs have only one real photo instead of two (documented in
  `PRODUCT.md` — Commons had no accurate second angle for them).

## Where to look for more detail

- `DESIGN.md` — full running log of every design decision on this project, newest
  entries at the bottom of the relevant section. The hero-rebuild entry has the
  complete technical rationale for every choice above.
- `SITE_OVERVIEW.md` — a from-scratch description of the whole site (architecture,
  design system, pages, data model, features) for briefing someone with zero prior
  context.
- `PRODUCT.md` — business/product facts (real shop details, positioning, what's
  in-scope vs. explicitly out-of-scope for this demo).
