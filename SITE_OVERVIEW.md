# Sky Phone — Full Site Description

A comprehensive description of the site, its architecture, design, and features — useful for briefing another developer, an AI, or documenting the build for the client.

**Sky Phone** is a trilingual (Hebrew/Arabic RTL, English LTR) e‑commerce demo website for a real neighborhood phone/tech shop and repair service in Kafr Kanna, Israel (established 2010). It's built as a static, zero-dependency, zero-backend single-page application — three files (`index.html`, `styles.css`, `app.js`), no framework, no build step — designed to be handed to the shop owner as a purchasable, deployable product (currently live on GitHub Pages).

## Business context

- Real shop: phone/tablet/computer/gaming retail + same-day device repair (screen, battery, charging port, water damage, software, laptop/PC, console).
- Real verified details: WhatsApp/phone `052-722-3916`, Instagram `@skyphone.ca` (54.2K followers), Facebook Page `facebook.com/skyphone.ca`, address in Kafr Kanna's Main Street.
- Positioning: the one shop that credibly does three things (sell, repair, and serve natively in Hebrew/Arabic/English) that competitors usually split across separate businesses.
- Currency: Israeli shekel (₪). Payment/checkout is a labeled demo placeholder — no real payment processing.

## Tech stack & architecture

- Pure HTML/CSS/vanilla JS. No React/Vue, no npm build, no backend, no database.
- Client-side SPA routing (`go(name)` in `app.js`) toggles `.page[hidden]` sections — routes: `foryou` (home), `products` (catalog), `product` (PDP), `repairs`, `bag` (full-page cart), `about`.
- All state lives in in-memory JS variables (`lang`, `route`, `filter`, `brandFilter`, `colorFilter`, `storageFilter`, `priceSort`, `searchQuery`, `bag`) — nothing persists across reloads (no localStorage), by design for a demo.
- i18n via a single `T` translation object keyed by language (`he`/`ar`/`en`), applied through `data-t`/`data-ph` attributes and an `applyText()` render pass; switching language re-renders all copy and flips the document's `dir` attribute (RTL for Hebrew/Arabic, LTR for English) instantly, including mirrored icons, mirrored scroll/arrow directions, and RTL-aware CSS throughout.

## Design system

- Direction: "Apple Store Premium Retail" — near-black/near-white grounds, large negative space, a single restrained accent color, minimal chrome, pedestal-style product presentation, system-sans type (with the shop's real script wordmark, Google Font "Satisfy," for the logo/brand name).
- Design tokens (CSS custom properties in `:root`): light surface `--bg #fff` / `--bg-soft #f5f5f7`, dark surface `--dark #0a0a0c`, ink colors, a single gold accent `--accent #b8862f` (sourced from the shop's real logo, not copied from any reference site), a spacing scale (`--space-1` through `--space-10`), a radius scale, and a shadow scale.
- Layout structure repeats a `.wrap` (max-width, centered) → `.section` (vertical rhythm) pattern throughout.
- Custom line-icon SVG set (single-stroke, rounded caps, 24×24) used consistently for nav, categories, services, repairs, contact.

## Pages

1. **For You (home)** — hero carousel of three composed ad units (real HTML headline/tagline/price-note/two pill CTAs, with a product cutout standing on its own light or dark ground, each with a pointer-tracked 3D tilt plus a continuous idle float): an iPhone 18 Pro "coming soon" ad (light ground, cutout render); a PlayStation 5 ad whose art and price are fed live from the product catalog (light ground, links straight to its real purchasable PDP); and a same-day-repair ad (dark ground, live lowest-price note) → **Apple Highlights** block (dark, big cards, direct links into each product's PDP) → **Samsung Highlights** block → **Gaming Highlights** block (includes a "GTA VI — coming soon" non-purchasable teaser card linking to WhatsApp) → infinite-scroll brand-wordmark marquee → services grid → repair promo band with live "from ₪X" price chips → gaming banner → **Reels** row (real local `<video>` clips, not embeds) → Instagram follower band (real, verified count).
2. **Products** — full catalog grid with a persistent left sidebar (Category, Brand, Color, Storage — collapsible accordion groups, capped height with its own scrollbar so it never overflows the grid) plus a circular brand-logo filter row scoped to the active category, a standalone price-sort `<select>` next to the result count, and a responsive product grid. All filters combine (AND) and reset each other's invalid combinations automatically.
3. **Product detail (PDP)** — name/price/description in the active language, color swatches, storage options (each with a price delta), quantity stepper, add-to-bag, and an image gallery with a thumbnail strip for products that have more than one real photo (falls back to a single image, then to the authored icon if no photo exists).
4. **Repairs** — process steps, a device-picker modal per repair type (screen/battery/port/water/etc.) with real per-device indicative pricing, add-to-bag from the picker.
5. **Bag (cart)** — available both as a slide-in drawer (quick access from any page) and a dedicated full page; both read/write the same live `bag` state so they can never drift out of sync. Line items support quantity, remove, and an optional flat-fee gift-wrap checkbox per product line.
6. **About** — shop story, stats, real logo.

## Data model

- `PRODUCTS`: 27 SKUs across phones/tablets/computers/gaming/accessories (full current Apple and Samsung lineups plus Xiaomi, Dell, Sony items), each with `id, name, cat, price, icon, brand, colors[], storage[], img, imgs[], desc:{he,ar,en}`. Every SKU has at least one real product photo (sourced from Wikimedia Commons, mirrored locally in `img/` so the site works offline with no hotlink risk); most have two for the PDP gallery.
- `REPAIRS`: 7 service types, each with a base price and a per-device price table (`PHONE_REPAIR_DEVICES`).
- Icons and images always have a graceful fallback chain: real photo → authored SVG icon (never a broken-image box).

## Interactive features

- **Live search** with a type-ahead suggestion dropdown (keyboard-navigable, thumbnail+name+price+category).
- **Rule-based support chatbot** (bottom-left panel) answering only from real site data — prices, repair costs, hours, address, phone — with trilingual keyword matching and quick-reply chips.
- **Fly-to-bag animation** — the added item's thumbnail arcs into the nav bag icon, badge pops.
- Row scroll arrows, hover-revealed and RTL-aware, on horizontally-scrolling rows (Reels, etc.).
- Scroll-progress hairline under the nav; a sliding underline indicator on the active nav link.
- Cursor-follow ring/spotlight effects and card tilt on desktop pointer devices only (`hover:hover` + `pointer:fine`, and skipped under `prefers-reduced-motion`).
- Scroll-reveal entrance animations (`data-reveal` + IntersectionObserver) throughout, and a page loader with the shop's animated logo mark.
- Everything above degrades cleanly on touch devices and under reduced-motion preference — no effect is required for the site to function.

## What's explicitly out of scope (by design, for a demo)

- No real payment processing (clearly labeled placeholder).
- No backend, no persistence — cart and filters reset on reload.
- No CMS — adding a product, repair price, or Reels video means editing the `PRODUCTS`/`REPAIRS`/`REELS` arrays directly in `app.js` and pushing.
