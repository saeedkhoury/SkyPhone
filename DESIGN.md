# Design

<!-- impeccable:design-schema 1 -->

## Direction

Structural reference: iDigital.co.il, at the user's explicit request ("copy the design and web idea... to my store and my logo"). This is a **structural** reference, not a brand clone: the layout patterns (promo ribbon, header search, category icon row, hero carousel, PDP sticky buy bar, WhatsApp bubble) are adopted; iDigital's own teal brand color, financing/installment plans, trade-in valuation, and "reserve in store" flow are explicitly NOT copied — Sky Phone doesn't offer those, and iDigital's brand color belongs to iDigital, not to Sky Phone. Underlying layout craft (spacing, restraint, no gradient text, no decorative eyebrows, authored icon set) still follows the original Apple-Store-Premium-Retail craft floor.

THESIS: a real e-commerce structure the client already trusts (because a competitor uses it), rebuilt in Sky Phone's own verified identity — same layout muscle memory as a big site, none of the fabricated services.

## Palette

- `--bg` #ffffff / `--bg-soft` #f5f5f7 / `--bg-soft-2` #ececee — light grounds
- `--ink` #1d1d1f / `--ink-soft` #6e6e73 / `--ink-faint` #8a8a8e — text
- `--dark` #0a0a0c / `--dark-2` #161618 — full-bleed dark surfaces (hero, feature spotlight, gaming banner, promo ribbon)
- `--accent` #b8862f — warm gold, drawn directly from the shop's real verified logo (gold wordmark on black), not from any reference site's brand color / `--accent-tint` #faf3e6 / `--accent-glow` for physical-light glows only, never decorative gradients
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
- **Product detail page** (`#p-product`): dedicated page per product, modeled on real e-commerce PDPs (referenced iDigital.co.il's layout at the user's request) — sticky gallery, color swatches, storage/size pills, quantity stepper, add-to-bag, a "More in <category>" row, and a sticky bottom buy bar (price + Add to Bag, shown via IntersectionObserver once the main CTA scrolls out of view). Colors and storage tiers use each device's real published options (e.g. actual Apple/Samsung color names and storage sizes), not fabricated shop-specific data. Deliberately does **not** copy iDigital's financing/installment breakdown, trade-in valuation, "iDigital Care" warranty upsell, or "reserve in store" flow — Sky Phone doesn't offer those, and inventing them would misrepresent the shop.
- **Promo ribbon** (`.promo-ribbon`): top bar with real info (same-day repair, WhatsApp number), dismissible; nav shifts up to fill the space when closed (`body.ribbon-closed`).
- **Header search**: functional client-side product search (name substring match), desktop inline bar / mobile toggle-to-overlay, routes to Products with results (or a real empty state, not a silent no-op).
- **Category icon row** (`.cat-row`): horizontal circles for each real category (Phones/Tablets/Computers/Gaming/Accessories/Repairs) with computed "from ₪X" starting prices, linking straight into a filtered Products view.
- **Hero carousel**: 2 slides (brand message, repairs) with prev/next arrows + dots, 6s autoplay that pauses on hover and is skipped entirely under `prefers-reduced-motion`. The gaming banner further down the page is intentionally not duplicated as a 3rd slide.
- **WhatsApp floating button**: fixed bottom-right, links to the shop's real WhatsApp number, rises above the PDP sticky bar when both are visible together.
- **Particle field** (`.particle-canvas`, `initParticleField` in `app.js`): canvas field of ~25–70 small dash particles, applied uniformly to every dark `.spot` surface — hero, gaming banner, About badge. Particles near the cursor ignite in the brand gold with a soft glow (`shadowBlur`) and fade back to dim white when the cursor moves away — referenced antigravity.google's and gemini.google's cursor-lit particle fields, reworked in Sky Phone's single-accent palette rather than Google's four-color one. Canvas-based for performance; the animation loop only runs while something is glowing or the pointer is inside the section. Gated by the same `canHover` check as the rest of the motion system, so touch visitors never load it.
- A hero-specific variant using floating icon badges with spring-physics repulsion was tried and reverted (2026-09-03) — it read as disconnected clip-art rather than matching the site's aesthetic, and didn't reflect what antigravity.google actually does (which is the same dash-particle field, not icon badges). The hero now uses the same particle field as the rest of the dark surfaces, at its natural higher particle count for the larger area.

## Icons

Authored single-stroke SVG set (1.5–1.75 stroke, rounded caps/joins, 24×24), consistent across nav, products, repairs, services and contact — replacing the old two-tone filled icon set.

## Known Issues Resolved

- FAQ answer reveal originally used `transition: max-height`, flagged by the design detector as layout-thrashing; replaced with a `grid-template-rows: 0fr → 1fr` transition (transform/opacity-safe technique), verified visually in-browser.

## Deliberate Detector Exceptions

- `overused-font` (Inter): earned by the Apple-canon direction; see Type above.
- `broken-image` ×3 (brand-logo `<img>` tags): false positive from the detector's static regex pass — `app.js` sets `img.src` from an embedded base64 logo constant at runtime (`document.querySelectorAll('.brand-logo').forEach(el=>el.src=LOGO)`); confirmed rendering correctly in live browser QA (nav, About badge, footer).

## Logo

The embedded badge logo (`LOGO` constant in `app.js`) is the shop's real, in-use logo — verified against the live Instagram profile photo (@skyphone.ca) on 2026-09-03, not a placeholder. An independent design-critique pass flagged it as visually inconsistent with the rest of the restrained/no-gradient system and recommended replacing it; the user was asked and explicitly chose to **keep the real logo as-is** rather than have a new mark fabricated without the shop owner's input. This is a closed decision — do not swap or "improve" the logo again without the user raising it.

## Verified

Browser QA pass (desktop 1440px + simulated 390px mobile) covered: routing between all four pages, product filtering, add-to-cart/qty/remove, checkout modal, repair booking, FAQ accordion, contact form submit/clear, mobile hamburger menu, and full language switching (HE/AR/EN, RTL↔LTR) — no console errors on any flow.
