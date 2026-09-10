# Adding a slide to the hero

Two steps: prepare the picture, add one entry. Nothing else in the site needs
touching — the dots, the slide count, the pointer tilt, the idle float, the
load stagger, the WhatsApp link and the analytics hook all follow from the
entry.

## 1. Prepare the picture

```bash
python3 tools/hero-image.py ~/Downloads/whatever.jpg iphone-duo
```

That writes the three files the hero asks for:

| File | Who gets it |
|---|---|
| `img/iphone-duo-sm.webp` | phones — the one almost everyone loads |
| `img/iphone-duo.webp` | desktop and retina |
| `img/iphone-duo.png` | browsers with no WebP; a fallback, so it is palette-quantised |

The script prints what it did. Three things it handles that matter:

**It strips baked-in text.** Promo images forwarded from suppliers usually have
the product name and a tagline burned into the pixels. The hero has its own
title, tag and note layers *that translate* — baked-in text duplicates them and
shows the wrong language to two thirds of the audience. The script finds the
blank band between the caption and the photograph and keeps only the picture.

**It cuts out the background** by flooding inward from the border, so light
areas *inside* the product — a screen, a white chassis — survive. A plain colour
threshold punches holes in exactly those places.

**It warns you when it could not help.** If the line says almost nothing was
removed, the picture has a photographic background and needs cutting out by
hand. Do not ship it as-is: the hero paints a gradient behind the art and a
rectangular photo will read as a grey box sitting on top of it.

## 2. Add the entry

In `app.js`, add to the top of `HERO_SLIDES` — array order is screen order:

```js
{ground:'light', badge:'soon_badge',
 title:{text:'iPhone Duo'}, tag:'ad_duo_tag', note:'ad_duo_note',
 art:{img:'img/iphone-duo.png', fade:true, alt:'…'},
 cta:[{style:'primary',   label:'ad_duo_cta',  wa:'wa_duo', ev:'hero_duo_notify'},
      {style:'secondary', label:'ad_i18_cta2', cat:'phones', brand:'apple'}]},
```

### Fields

| Field | Meaning |
|---|---|
| `ground` | `light` or `dark` — panel treatment, and which ink the nav switches to |
| `badge` | a `T` key; add `badgeMod:'stock'` for the green in-stock pill |
| `title` | `{text:'…'}` for a product name, or a `T` key for a translated one |
| `tag` / `note` | `T` keys. Use `noteId` instead of `note` to have `renderHeroAds()` fill the line with a live catalog price |
| `art.img` | the PNG from step 1 |
| `art.pid` | instead of `img` — take the picture from that catalog product, and make the art clickable through to it |
| `art.svg` | raw markup, for a slide with no photograph |
| `art.fade` | fades the bottom of the picture into the panel |
| `cta[].style` | `primary`, `secondary`, or `on-dark` for a dark slide |
| `cta[].wa` | a `T` key holding the prefilled WhatsApp message; pair with `ev` for the analytics label |
| `cta[].route` / `cat`+`brand` / `pid` | go to a page / a filtered catalog / a product |

### 3. Add the copy

Every `T` key named above must exist in **all three** languages in `app.js`, or
the slide ships with blank lines. For the entry above that is `ad_duo_tag`,
`ad_duo_note`, `ad_duo_cta` and `wa_duo` — in `he`, `ar` and `en`.

Then bump the `?v=` stamp on `styles.css` and `app.js` in `index.html` so
returning visitors get the new files.

## Why the hover comes for free

The builder always wraps the picture in the same two elements:

```html
<div class="hero-ad-art cutout fade-bottom">   <!-- pointer tilt attaches here -->
  <span class="ad-art-float">                  <!-- idle float keyframe lives here -->
    <picture>…</picture>
```

`initMotionFor()` attaches the tilt to every `.hero-ad-art` on the page, so a
new slide gets it by existing. The two effects are on **separate elements on
purpose**: a running keyframe permanently outranks an inline style, so putting
the float and the tilt on one element silently kills the tilt. If you ever
hand-write hero markup, keep that split.
