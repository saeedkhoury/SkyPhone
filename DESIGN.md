# Design

<!-- impeccable:design-schema 1 -->

## Direction

Apple-Store Premium Retail (canon, user-selected over two grounded alternatives — "Souq Signage" and "Circuit & Precision" — during the direction round). Craft bar: apple.com and the Apple Store app.

THESIS: restraint and space are the luxury signal — the old dark magenta/gold gradient theme (glare-tilt cards, eyebrow labels, gradient text) is replaced with a light, spacious, single-accent system; a dark surface is used only where Apple itself uses it (hero, feature spotlights, banners), never as the whole site.

## Palette

- `--bg` #ffffff / `--bg-soft` #f5f5f7 / `--bg-soft-2` #ececee — light grounds (Apple's classic off-white section tone)
- `--ink` #1d1d1f / `--ink-soft` #6e6e73 / `--ink-faint` #8a8a8e — text
- `--dark` #0a0a0c / `--dark-2` #161618 — full-bleed dark surfaces (hero, feature spotlight, gaming banner, footer-adjacent panels)
- `--accent` #0068d6 (single accent, "sky" blue — doubles as literal brand reference and Apple-blue register) / `--accent-tint` #eaf3fd / `--accent-glow` for physical-light glows only, never decorative gradients
- No gradient text anywhere. No colored borders. No eyebrows/kickers.

## Type

Inter (self-hosted via Google Fonts) for EN, Noto Sans Hebrew for HE, Noto Sans Arabic for AR — chosen as the closest broadly-available substitute for Apple's SF Pro family, matching weight and x-height across all three scripts so no language reads as a second-class citizen. This is a deliberate, brief-earned exception to the "avoid Inter as a generic default" guidance: the direction *is* the Apple system-type register, confirmed by the user.

Display scale: clamp(40px,7vw,88px) down to clamp(19px,2vw,23px), tracking -0.03 to -0.035em on display sizes, body 15–17px.

## Components

- **Nav**: translucent blur, thin (52px), pill language switch, pill cart badge.
- **Buttons**: pill radius (`--radius-pill: 980px`), primary/secondary/on-dark/link variants.
- **Product cards** (`.pcard`): pedestal-style — soft radial shadow ground, centered image/icon, restrained hover (translateY + shadow, no 3D tilt/glare).
- **Services**: asymmetric feature grid (`.feature-grid`) — one large dark spotlight panel + two smaller light panels, not three identical cards.
- **Repairs**: numbered process rows (numbering carries real sequence information — step 1/2/3 — so it survives the "no decorative 01/02/03" rule) + a plain price list, not boxed pill cards.
- **Contact info**: single bordered panel with divided rows, not a grid of identical icon-cards.
- **FAQ**: grid-template-rows accordion (not `max-height`, to avoid layout-thrash — see Known Issues Resolved below).
- **Modal**: used only for checkout (an action that legitimately needs interruption to explain the payment placeholder).

## Icons

Authored single-stroke SVG set (1.5–1.75 stroke, rounded caps/joins, 24×24), consistent across nav, products, repairs, services and contact — replacing the old two-tone filled icon set.

## Known Issues Resolved

- FAQ answer reveal originally used `transition: max-height`, flagged by the design detector as layout-thrashing; replaced with a `grid-template-rows: 0fr → 1fr` transition (transform/opacity-safe technique), verified visually in-browser.

## Deliberate Detector Exceptions

- `overused-font` (Inter): earned by the Apple-canon direction; see Type above.
- `broken-image` ×3 (brand-logo `<img>` tags): false positive from the detector's static regex pass — `app.js` sets `img.src` from an embedded base64 logo constant at runtime (`document.querySelectorAll('.brand-logo').forEach(el=>el.src=LOGO)`); confirmed rendering correctly in live browser QA (nav, About badge, footer).

## Verified

Browser QA pass (desktop 1440px + simulated 390px mobile) covered: routing between all four pages, product filtering, add-to-cart/qty/remove, checkout modal, repair booking, FAQ accordion, contact form submit/clear, mobile hamburger menu, and full language switching (HE/AR/EN, RTL↔LTR) — no console errors on any flow.
