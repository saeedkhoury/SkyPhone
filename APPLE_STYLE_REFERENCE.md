# Apple — style reference (external)

Source: <https://styles.refero.design/style/aecac5da-f397-4ddf-b71f-de1efc434cb8>
Captured 2026-09-07. This is a **third-party analysis of apple.com**, kept here so the
choices in `DESIGN.md` can be traced back to what they were actually measured against.

It matters because `PRODUCT.md` already names the craft bar for this project as
"apple.com and the Apple Store app" — this file is that bar, written down.

> "Apple's design language is a study in restraint: near-white canvas, generous
> breathing room, and one vivid blue accent that makes every action feel deliberate.
> Typography is the primary voice… The product IS the design… chrome recedes into thin
> borders, ghost navigation, and hairline rules."

## What Sky Phone already matched before this pass

| Token | Apple | Sky Phone | |
|---|---|---|---|
| Primary ink | Carbon `#1d1d1f` | `--ink:#1d1d1f` | exact |
| Page canvas | Frost `#f5f5f7` | `--bg-soft:#f5f5f7` | exact |
| Button radius | `980px` | `--radius-pill:980px` | exact |
| Typeface | SF Pro, substitute **Inter** | Inter | matches the reference's own substitute |

## Adopted in this pass

- **Card / image / input radius → 8px.** The reference allows exactly two radii:
  `980px` for anything interactive, `8px` for everything else. Sky Phone was on
  12/18/28px.
- **Elevation removed.** "Never add drop shadows to cards, buttons, or nav — the system
  uses hairline borders and surface shifts, not elevation." Panels now carry a 1px
  hairline instead.
- **Body type at 17px with −0.016em tracking.** "The negative tracking is what makes
  Apple type feel precise, not the size alone."
- **Weight 300 for editorial subheads** (`.lede`) — the "whisper voice".
- `--surface-wash:#f4f8fb` (Ice) as the elevated section wash.

## Deliberately NOT adopted, with reasons

- **Apple Blue `#0071e3` as the accent.** Sky Phone's gold is drawn from the shop's own
  verified logo (see `DESIGN.md`), not from a reference site. Blue CTAs would fight the
  gold logo mark on every page. Owner confirmed 2026-09-07: keep the gold.
- **Pebble `#e2e2e5` as a surface.** Measured: on Pebble, `--ink-faint`, `--ink-soft`
  and `--accent-strong` all drop to ~4.11:1 and **fail WCAG AA**. `--bg-soft-2:#ececee`
  is kept because the type tuned against it passes at 4.50:1. Accessibility outranks
  palette fidelity.
- **The reference's letter-spacing table for headings** (+0.196px at 28px, +0.44px at
  40px, +0.616px at 56px). It contradicts the reference's own prose ("negative tracking
  that tightens as size grows") and real apple.com display type, and reads as extraction
  noise. Sky Phone keeps its existing negative heading tracking (−0.03em / −0.035em).
- **Negative tracking on Arabic.** Arabic is a cursive, connected script — letter-spacing
  visually breaks words apart. Tracking is scoped away from `[lang="ar"]`.
- **Shadows on the floating WhatsApp/chat buttons.** Apple's system has no floating action
  buttons at all, so the rule does not really cover them; they sit over arbitrary
  scrolling content and need the shadow to stay legible. Kept as a stated exception.

## Reference tokens (verbatim from source)

```css
:root {
  --color-apple-blue: #0071e3;   /* filled action buttons only */
  --color-link-blue:  #0066cc;   /* outlined actions, inline links */
  --color-signal-blue:#2997ff;   /* decorative only */
  --color-carbon:     #1d1d1f;
  --color-frost:      #f5f5f7;
  --color-ice:        #f4f8fb;
  --color-smoke:      #333333;
  --color-graphite:   #474747;
  --color-ash:        #707070;
  --color-mist:       #858585;
  --color-onyx:       #000000;
  --color-pebble:     #e2e2e5;

  --text-caption: 12px;  --leading-caption: 1.33;  --tracking-caption: -0.264px;
  --text-body-sm: 14px;  --leading-body-sm: 1.29;  --tracking-body-sm: -0.224px;
  --text-body:    17px;  --leading-body:    1.47;  --tracking-body:    -0.272px;
  --text-subheading: 21px; --leading-subheading: 1.24;
  --text-heading-sm: 28px; --text-heading: 40px;
  --text-heading-lg: 44px; --text-display: 56px;

  --spacing-unit: 4px;      /* 4 8 12 16 20 24 40 48 56 */
  --page-max-width: 1440px; --section-gap: 64px;
  --card-padding: 24px;     --element-gap: 12px;

  --radius-cards: 8px;  --radius-images: 8px;
  --radius-inputs: 8px; --radius-buttons: 980px; --radius-tags: 980px;

  --shadow-xl: rgba(0,0,0,0.22) 3px 5px 30px 0px;  /* product images ONLY */

  --surface-canvas: #f5f5f7;
  --surface-elevated-wash: #f4f8fb;
  --surface-pebble: #e2e2e5;
}
```

## Rules worth re-reading before touching UI

**Do**
- One accent, one job — used sparingly so each appearance carries weight.
- Pair a filled primary with an *outlined* secondary; never stack two filled buttons.
- Full-bleed product photography; never constrain hero images to a max-width box.
- 980px radius on every interactive pill; full-bleed section grounds, not cards-in-cards.

**Don't**
- No drop shadows on cards, buttons or nav.
- No weight above 600 for product names (700 is for promotional lockups only).
- No card or panel inside a `#f5f5f7` section — the canvas *is* the surface.
- Never mix accent roles in one element.
