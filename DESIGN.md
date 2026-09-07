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
- **Repairs**: numbered process rows (numbering carries real sequence information — step 1/2/3 — so it survives the "no decorative 01/02/03" rule) + a plain price list, not boxed pill cards. The price list shows a "from ₪X" starting price per repair type; tapping a row (or its + button) opens a device-picker modal (`#repairModal`) — screen/battery/charging-port/water-damage repairs vary genuinely by device (a flagship screen costs more than a budget one), so each of those four repair types carries a real per-device price table (`PHONE_REPAIR_DEVICES` in `app.js`), as do the computer and console repair rows. Software recovery (r5) stays flat/no picker since labor is roughly device-agnostic. The listed "from" price is always `Math.min` across a repair's device prices, so it never drifts from what's actually offered.
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
- **Premium interaction pass** (2026-09-03): a second layer of Apple/Stripe-register motion detail added on top of the existing system, not replacing it —
  - **Custom cursor** (`.cursor-dot`/`.cursor-ring`, `initCursor` in `app.js`): a small dot plus a lagging ring (`lerp` in `requestAnimationFrame`), `mix-blend-mode:difference` so it inverts on any background without per-surface color logic. Enlarges over links/buttons/cards. `pointer-events:none` on both elements — omitting that silently breaks every click under the ring, caught in QA. Gated by `canHover`; hidden entirely under `(hover:none)`.
  - **Card tilt + glare** (`attachTilt`, applied to `.pcard` in `initMotionFor`): small pointer-driven `rotateX`/`rotateY` (max ~8°) plus a `radial-gradient` glare following `--mx`/`--my` custom properties. Replaces the old CSS-only `translateY` hover (now redundant — JS inline `transform` always wins over the class rule).
  - **Text reveal** (`.tr-mask`/`.tr-inner`, `data-text-reveal`, `initTextReveal`): every `.h1`/`.h2`/`.display` is tagged at init and masked; text slides up on first appearance via `IntersectionObserver` + keyframe animation. The wrapper persists across language switches — `applyText()` writes into `.tr-inner` instead of replacing the element's `textContent`, so re-tagging never fires twice.
  - **Hero parallax** (`initHeroParallax`): the hero device drifts via a scroll-position-driven `translateY` on a `.hero-device-wrap`, independent of the existing pointer-tilt on the SVG itself (`initHeroTilt`) — different elements, no conflict. Skipped under `prefers-reduced-motion`.
  - **Page loader** (`.page-loader`, `initPageLoader`): a branded progress fill plays once over ~850ms on first load, using the real logo. Instant-skips under `prefers-reduced-motion`.
  - **Film grain** (`.noise-overlay`): a static low-opacity (`.035`) SVG-turbulence tile, `mix-blend-mode:overlay`, `pointer-events:none`. Off under `prefers-reduced-motion`.
  - **Cart drawer**: the old full-page `/bag` route was replaced with a slide-out `.cart-drawer` + `.cart-backdrop` (same `renderBag()`/`bag-body` markup, now rendered into the drawer). Opens via `data-cart-open` (nav bag icon, mobile-menu link, footer link), closes via the ✕, backdrop click, `Escape`, or navigating anywhere else. `bagBtn.active` bag-route logic was removed since `'bag'` is no longer a page route.
  - `[data-reveal]` switched from a CSS `transition` to a `@keyframes` animation (`reveal-up`), per the brief's request to avoid it fighting hover-driven inline transforms (relevant now that `.pcard` sets its own `transform` via `attachTilt`).
  - Deliberately **not** added: a second cursor-following spotlight glow layered on top of the existing particle field on dark surfaces. The particle field (`initParticleField`) already gives pointer feedback there in the site's own visual language; stacking a second glow effect risked reintroducing the over-decorated, "not connected to the design" feel the user explicitly rejected earlier in the icon-badge round.
- **Storefront polish pass** (2026-09-04): fixes + big-store features, all within the same restrained system —
  - **Animation-fill bug fixed**: filled keyframe animations (`reveal-up`, `rise`) permanently override inline styles, which had silently killed `attachTilt` on revealed cards and the hero pointer-tilt. A global `animationend` listener now swaps the animating class for a static end-state class (`.revealed` / `.risen`) the moment the entrance finishes, so inline tilt transforms apply again. Verified via computed-style QA in Chrome.
  - **Live search suggestions** (`initSearchSuggest`, `.search-sugg`): type-as-you-search dropdown under the desktop nav bar and the mobile search overlay — up to 6 matches with thumbnail, name, category and price; ArrowUp/Down walks the list, Enter opens the highlighted product (or runs the full search), Escape/blur dismisses. The chosen id is captured *before* `close()` empties the result set (an early version threw `Cannot read properties of undefined (reading 'id')` because `close()` ran first — caught in QA).
  - **Fly-to-bag** (`flyToBag` + `popBag`): the added item's thumbnail arcs from the button that added it into the nav bag icon (WAAPI, 620ms, midpoint lift), then the bag badge pops (`bag-pop` keyframe). Wired into card add buttons, the PDP add CTA, and the repair device-picker add. Skipped under `prefers-reduced-motion` (badge still pops — it carries the state change).
  - **Row scroll arrows** (`initRowArrows`, `.row-arrow`): hover-revealed circular arrows on the New-arrivals row, auto-hidden at scroll edges (`at-end`), RTL-aware via `Math.abs(scrollLeft)` which covers both the negative and positive RTL scroll models. Hidden ≤920px where touch swiping is native.
  - **Scroll progress hairline** (`initScrollProgress`, `.scroll-progress-fill`): 2px gold bar under the nav, `transform: scaleX()` driven (no layout property), origin flipped for RTL.
  - **Nav sliding indicator** (`positionNavInk`, `.nav-ink`): gold underline that slides/scales to the active link via `translateX + scaleX` (again no layout properties, per the detector). Repositioned on route change, language switch, resize, and `document.fonts.ready` (link widths shift when the Hebrew/Arabic faces load).
  - **Hero device authored moment**: the screen's gold ring and check stroke-draw on load (`stroke-dashoffset` keyframes), a 7s idle float on a dedicated wrapper (`.hero-device-float` — a separate element from the parallax wrap and the tilted SVG so no transform fights), and a real status bar (9:41 + battery) so the mockup reads as a phone, not a wireframe. Hero arrows get physical-position/icon flips in RTL and are hidden ≤920px.
  - **Browser surfaces**: thin themed scrollbar (`::-webkit-scrollbar` + `scrollbar-color`), `caret-color: var(--accent)` on inputs, favicon served from the runtime `LOGO` data URI (also kills the `/favicon.ico` 404), `theme-color #0a0a0c`.
  - **Micro-feedback**: `.btn-primary` sheen sweep on hover (direction-aware in RTL), press-scale on chips/pills/category circles, staggered entrance for cart rows (`bi-in`, ≤8 × 45ms) and mobile-menu links (`mm-in`), PDP gallery pointer-tracked zoom (`attachPdpZoom`, scale 1.35, origin follows the cursor, `canHover`-gated), and mobile filter chips switched from awkward wrapping to a single edge-to-edge scroll row.
  - Cursor ring growth moved from `width/height` transitions to `transform: scale()` after the design detector flagged layout-property transitions; same treatment for the two other flagged spots (scroll progress, nav ink).
  - **Full product imagery** (2026-09-04): all 14 SKUs now carry real product photos/renders, sourced from Wikimedia Commons and mirrored locally in `img/` (self-contained demo — no hotlinking, works offline). Renders with transparency were preferred where they exist (phones, tablets, DualSense, laptops); authentic photos fill the rest (Xiaomi 14, iPad Air M2, Tab S9, watch, headset, charger). The authored line icons remain as `pmedia()`'s `onerror` fallback, so a missing file can never ship a broken-image box.
- **For-You campaign sections** (2026-09-04, after reviewing idigital.co.il / iplace / istoreil / apple.com/il / samsung.com/il): the homepage is now a full sectioned storefront, in this order — hero carousel → trust strip → category row → **spotlight tiles** (`.spot-grid`/`.spot-tile`: two Apple-style dark ad tiles for iPhone 15 Pro and Steam Deck with badge, price, dual CTA, bottom-bleeding product art, cursor-lit particles from `.spot`, and `attachTileParallax` pointer-drift on the image; click opens the PDP) → new arrivals row → **brand marquee** (`.brand-marquee`: quiet infinite wordmark strip — Apple/Samsung/Xiaomi/PlayStation/Steam/Dell/Sony/JBL — CSS-only loop, duplicated track, pauses on hover) → services grid → **repair spotlight** (`.rep-spot`: dark ad band with live "from ₪X" price chips rendered from `REPAIRS` via `renderRepairSpot()` — chips are clickable straight into the device-picker modal) → **accessories row** (`renderAccessories()`: hand-picked SKUs 6/8/13/14, reuses productCard + row arrows; "see all" deep-links to the accessories filter) → gaming banner → **Instagram band** (`.ig-band`: real verified 54.2K follower count-up, link to @skyphone.ca). The promo ribbon now also **rotates** the shop's three real messages (`initPromoRotation`, 5.2s fade cycle, skipped under reduced-motion). i18n gotcha worth remembering: masked text-reveal (`data-text-reveal`) replaces `textContent`, so any heading containing child markup (like the IG count-up `<b>`) must NOT use `.h1/.h2` — use a plain styled div (`.ig-title`) instead.
- **Navbar wordmark** (2026-09-04, user request): the nav uses a text-only wordmark — first Samsung-style bold, then restyled to the shop's script branding (Satisfy from Google Fonts, `.brand-word`) per the user's reference image. Applied in the nav, footer and page loader. The shop's real logo image remains in the loader, About badge, footer and favicon. Root cause of the original "logo too close to the corner" complaint, found and fixed: `header .nav-inner` also carries `.wrap`, and its `width:100%` was tie-beating `.wrap`'s `width:min(1120px,90vw)` (same specificity, later in the file), so nav content spanned the full viewport width and pinned the brand to the corner. Removing that `width:100%` restored proper 5vw side margins.
- **iOS Safari fixed-element disappearing act, properly fixed** (2026-09-04): `overflow-x:hidden` on `<html>` turns the root into a scroll container, which makes every `position:fixed` element (nav, WhatsApp FAB, chat FAB) vanish during momentum scroll on iOS. Switched to `overflow-x:clip` (with `hidden` as fallback), which clips without creating a scroll container. FABs also got `translate3d(0,0,0)` layer promotion. Note Chrome never reproduces this — it needs a real iOS device check after deploy.
- **Support chatbot** (`.chat-fab`/`.chat-panel`, `chatAnswer()` in `app.js`): rule-based assistant in a bottom-left panel (WhatsApp keeps bottom-right; both rise with the PDP sticky bar). Answers come only from real site data — catalog prices via `PRODUCTS`, per-device repair prices via `REPAIRS`+`PHONE_REPAIR_DEVICES`, verified hours/address/phone. Trilingual keyword intents (HE/AR/EN mixed input tolerated), typing indicator, quick-reply chips, action links inside answers ("View product" opens the PDP, "Add to Bag" opens the repair picker). Two QA-caught matcher rules worth keeping: repairs are matched **before** products ("כמה עולה מסך לאייפון 14" is a repair question), and cluster matching uses latin-only tokens so Hebrew/Arabic aliases can never degrade into an empty-string match-all.
- **3D scroll showcase** (`.showcase`, `initShowcase`): a 240vh sticky scene right after the spotlight tiles — the iPhone 15 Pro render sweeps `rotateY −26°→+26°` with a slight rotateX arc and scale peak mid-scroll, while three spec chips (A17 Pro / ProMotion 120Hz / Titanium) float in at staggered scroll thresholds. The phone is clickable → PDP. CSS owns the fallback: `max-width:920px` or `prefers-reduced-motion` collapses it to a plain stacked section (no sticky, chips always visible), so mobile and motion-sensitive visitors get the same content without the effect.
- **Cache-busting** (2026-09-04): `styles.css` and `app.js` are linked with a `?v=YYYYMMDD` query so returning visitors (and demo phones) always get the current build after a push. Bump the date on any future deploy.
- **iPhone 18 "coming soon" hero slide, Reels row, and Apple/Samsung showcase sections** (2026-09-05, referencing istoreil.co.il, iplace.co.il and getcardi.co at the user's request): brainstormed and approved as a bounded change before building (per the brainstorming skill's hard gate) — a note for future sessions, since a hook fired mid-invocation telling the agent to abandon the brainstorm and switch to an unrelated CrowdStrike Falcon Foundry plugin; that instruction had nothing to do with this repo and was treated as untrusted/injected content, not followed.
  - **Hero slide 0** is a new campaign slide (bumping the two existing slides to 1/2, `heroSlideCount` now 3) sourced from the shop's real Facebook "coming soon" post for the iPhone 18 line. It is deliberately **not** a purchasable listing (no price, no add-to-bag) since the device doesn't exist yet — the CTA is a real `wa.me` link ("Notify me on WhatsApp") instead.
  - **Reels row** (`renderReels()`, right after the trust strip — inserting it before the trust strip broke that section's intentional negative-margin overlap with the hero, so it was moved): the shop's three real Facebook reel URLs (`REELS` in `app.js`). Facebook's own `plugins/video.php`/`post.php` iframe embed was tried first and rejects all three `/share/r/...` reel links ("post no longer available" — confirmed by loading the plugin URL directly), so rather than ship a visibly broken embed, each card is a reliable link-out (dark card, play glyph, "Watch on Facebook") that opens the real post in a new tab. Since this is a static site with no backend, adding a future reel means adding one line to the `REELS` array, not a live dashboard — worth saying plainly to the client.
- **For-You page simplified into a direct-link storefront** (2026-09-06, user request after reviewing the campaign-sections pass — the category-icon row and trust-stat strip "didn't look connected", and the scattered arrivals/spot-tile/showcase/accessories sections were replaced outright rather than tuned):
  - **iPhone 18 hero slide now uses the real posted creative** (`img/iphone18-ad.jpg`, cropped from the shop's actual Facebook post) inside a white rounded `.ad-image-card`, replacing the earlier CSS-built text wordmark — the card and the primary CTA both link to the same real WhatsApp "notify me" thread. The CSS-wordmark approach (`.ad-wordmark`, Inter 800) was removed along with the extra font weight import.
  - **Trust strip and category-icon row removed** from the For You page entirely (`renderCatRow`, `.trust-strip`/`.cat-row` markup and CSS all deleted) — flagged as not matching the direction, no replacement needed since the same information already lives elsewhere (About page stats, the Instagram band's real follower count).
  - **Hot-picks spot-tiles, the 3D scroll showcase, the new-arrivals row, and the accessories row are all gone** (`renderArrivals`, `attachTileParallax`, `initShowcase`, and their markup/CSS removed) — replaced by two **Highlights sections** (`renderHighlights()`), one per brand, mirroring istoreil.co.il/iplace.co.il's homepage pattern: a few big cards, each one real flagship product, the whole card a direct link into its own PDP (`data-spot-pid`, reusing the existing PDP-open handler — no new click plumbing needed). Card backgrounds cycle through the existing `--bg-soft`/`--accent-tint`/`--bg-soft-2` tokens rather than introducing new colors.
  - **Full current Apple and Samsung lineups added to `PRODUCTS`** at the user's request ("every product Apple/Samsung sells today"): Apple gained iPhone 17 / 17 Pro / 17 Pro Max, MacBook Pro 14", iPad Pro, base iPad, Apple Watch Ultra 2, AirPods Pro 2, AirPods 4; Samsung gained Galaxy S25 Ultra, Galaxy S25, Galaxy Watch7 — each product also now carries a `brand` field. None of these twelve have local photos yet (no Wikimedia-sourced asset exists for these specific models), so they render through `pmedia()`'s existing icon fallback until real photos are supplied — worth flagging to the client rather than leaving it implicit.
  - The Apple Highlights section features iPhone 17 Pro Max, MacBook Pro 14" and iPad Pro; Samsung's features Galaxy S25 Ultra, Galaxy Tab S9 (real photo) and Galaxy Watch7 — a curated 3 per brand like the reference sites, not the full lineup (the full lineup lives on the Products page, reachable via each section's "See all").
  - The gaming banner's CTA now deep-links via `data-cat="gaming"` instead of routing to unfiltered Products, for consistency with the new direct-link philosophy.
- **Bug-fix + feature round** (2026-09-06, user feedback on the above pass):
  - **Hero slide 0 is now genuinely full-bleed** (`.ad-full-slide`): the earlier boxed white card looked "not connected" per the user, so the whole slide is now the shop's real creative — badge overlaid top, caption overlaid bottom on a gradient scrim, no competing title/lede/button row. The old `.ad-image-card`/small-card CSS was removed.
  - **Apple/Samsung "See all" now actually filters** — `#appleSeeAll`/`#samsungSeeAll` set `brandFilter` before routing to Products, fixing the earlier acknowledged simplification where both landed on the unfiltered catalog.
  - **Products page gained a real filter system**: a persistent sidebar (`.filter-sidebar`, category/brand/price accordion groups — collapsible via the header, open by default per the user's "keep it open constant on the side") plus a circular brand-logo row (`.brand-circle-row`) under the category chips, scoped to whichever brands actually exist in the active category. Both drive the same `brandFilter`/`priceSort` state as the chips, so any of the three paths agree. Deliberately **not** built: per-variant color/storage/model faceting like the reference screenshot — the catalog isn't structured as per-variant SKUs, and restructuring it for that would be a much bigger project than this pass; said so plainly rather than quietly skipping it.
  - **Apple/Samsung Highlights expanded** with SKUs the user asked for by name (iPad, AirPods, Apple Watch → Apple; Galaxy Tab, Galaxy Watch, Galaxy Buds → Samsung) — all of which were already in the catalog from the previous pass, so this was display-layer, not new data. Added a third **Gaming Highlights** section (PlayStation 5 — a new real product — plus Steam Deck) with an honest "GTA VI — coming soon" teaser card: not a real product, no PDP, links to the shop's WhatsApp like the iPhone 18 slide does, same pattern for the same reason.
  - **PDP gallery now supports multiple photos per product** (`pdpImages()`/`pmediaSrc()`, an optional `imgs[]` array with graceful fallback to the single `img` field, then the icon) with a thumbnail strip. No product currently has more than one real photo — sourcing genuine additional official photos for the catalog is a real follow-up (client-supplied, or a dedicated sourcing pass), not something fabricated here. The capability is real and ready the moment photos exist.
  - **Cart drawer gained a gift-wrap option** (`GIFT_WRAP_PRICE`, a flat ₪15/line, product lines only) and a **"View full-page cart" link** that opens a dedicated `#p-bag` route — the drawer stays the quick-access default; the full page is an additional path to the same live `bag` state (`renderBag()` now writes into both containers whenever it runs, so they can never drift out of sync).
- **Real photos for the full catalog, real video Reels, and genuine color/storage filtering** (2026-09-06, user rejected two earlier stated simplifications — the lesson: flagging a shortcut as "deliberate" doesn't preempt the user still wanting it once they see a concrete reference):
  - **All 27 SKUs now carry at least one real photo, most carry two** (`imgs[]`), sourced from Wikimedia Commons the same way as the original 14. A second `IMG2` map holds second-angle photos for the original 14 products; the 13 products added in the previous round get their `img`/`imgs` paths inlined directly (no reuse across products). Five SKUs (Gaming Headset Pro, Galaxy Buds3, base Galaxy S25, Galaxy Watch7, base iPad) have only one photo — Commons had no second angle that was genuinely the right product (a mismatched substitute, e.g. Galaxy Buds2 Pro standing in for Buds3, was deliberately rejected rather than used).
  - **Highlight-card image bug found and fixed during verification**: `.highlight-media` (the Apple/Samsung/Gaming Highlights cards) never hid the icon fallback (`.pfb`) behind a loaded real photo — every other product-media context (`.pcard-media`, `.pdp-gallery`, `.bi-media`, etc.) has a `.pfb{display:none} .pfb.show{display:grid}` pair, but this one was missing it, so real photos were rendering underneath a full-size icon that visually covered them. Fixed by adding the same pattern (`.highlight-media .pfb{position:absolute; inset:0; display:none} .pfb.show{display:grid}`) — verified in-browser afterward, all 6 Apple and 4 Samsung highlight cards now show their real photo.
  - **Reels moved to real local video** (`REELS` now `[{src:'video/reel1.mp4'}, ...]`, four files supplied directly by the user, copied into `video/`): the Facebook link-out fallback from the previous round is gone — `renderReels()` now renders an actual `<video controls playsinline preload="metadata">` per card. Section position also moved per request: it now sits directly before the Instagram band, near the end of the page, instead of near the top under the trust strip.
  - **Genuine color and storage filtering added** to the Products sidebar (`colorFilter`, `storageFilter`, `renderVariantFilterUI()`), reversing the previous round's stated simplification that per-variant faceting wouldn't be built. Both lists are scoped to whichever category+brand is currently active (`scopedForVariants()`), so a filter never offers an option nothing in view has; color options render as small circular swatches using each color's real hex.
  - **Price sort moved out of the sidebar into its own standalone control** (`.sort-select`, a native `<select>` in `.products-toolbar` next to the result count) per the user's marked-up reference screenshot — it's no longer one of the sidebar's accordion groups.
  - **Brand-circle row spacing increased** (`.brand-circle-row` gained top padding + a border-top separator) per user feedback that the category chips and the brand-logo row sat too close together.
  - **Filter sidebar capped to viewport height and made independently scrollable** (`.filter-sidebar{max-height; overflow-y:auto}`): with the new color/storage lists, the "All categories" sidebar (which shows colors/storages from all 27 products) grew taller than the product grid, leaving dead white space beside the grid on a CSS-grid layout with `align-items:start`. The sidebar now scrolls within its own sticky panel instead of stretching the row.
- **Hero slide overhaul: iPhone 18 series, a real PS5 ad, and a 3D-feel motion treatment** (2026-09-06, user-supplied images):
  - **Slide 0** now advertises the full iPhone 18 lineup (18 / 18 Pro / 18 Pro Max, not just Pro) using a new shop-branded teaser image the user supplied directly (`img/iphone18-series-ad.jpg`) — same `.ad-full-slide` full-bleed pattern as before, copy updated across all three languages, WhatsApp notify-me link text updated to match.
  - **Slide 1** (previously the static "Your tech, sky-high" intro slide with the animated SVG phone mockup) is now a **PlayStation 5 ad** using a real professional product photo the user supplied (`img/ps5-ad.jpeg`), styled identically to the iPhone slide. Chose PS5 over a "Galaxy S26 Ultra coming soon" alternative (also offered by the user, with a reference image) because PS5 is a real, currently-sold catalog item (id 27) — the slide can link straight into its real PDP (`data-spot-pid="27"`, real price, real add-to-cart) rather than being another dead-end "notify me" teaser for an unannounced phone. Badge uses a new green `.ad-badge-buy` variant ("In stock now") to visually distinguish a real, buyable ad from the gold "Coming soon" badge. The now-orphaned `#heroStage`/`#heroDevice` SVG mockup and its `fy_title`/`fy_lead` copy were left in place (dead but harmless; `initHeroTilt`/`initHeroParallax` already null-guard on missing elements) rather than doing a broader unrelated cleanup pass.
  - **"3D" motion treatment**: the user referenced Samsung's real site, which uses actual produced video footage of the Z Fold on its ad slides, and asked for the same feel. Embedding a real Samsung/Apple marketing video was not an option — it isn't ours to use and we don't have licensed footage of any of these products. Built the closest honest equivalent instead: a continuous idle float/rotate CSS keyframe (`ad-idle-float`) on every ad-slide image plus a pointer-tracked 3D tilt (`attachAdTilt()`, mirrors the existing `attachTilt()` pattern used on product cards) that pauses the idle animation while the cursor is over the slide. Respects `prefers-reduced-motion` (idle animation disabled) and `canHover` (tilt only on fine-pointer devices) like every other motion effect on the site.
- **Hero rebuilt from full-bleed JPG slides into composed ad units** (2026-09-06, superseding the whole entry above — same day, later pass, per a follow-up brief the user brought in from another session): the `.ad-full-slide` pattern from the previous entry looked "pasted" rather than designed — a finished marketing JPG (its own background, its own baked-in type, hard rectangular edges) dropped into a box whose aspect ratio didn't match it, letterboxed by `object-fit:contain` into visible bands. Fixed structurally, not cosmetically: text became real HTML (`.hero-ad-copy`: badge, `<h2>` title, tagline, a live-data price/note line, two pill CTAs) and the product art became a cutout standing on its own ground (`.hero-ad-art`), reference apple.com/il's hero units.
  - **Two grounds, one component**: `.hero-ad-light` (white-to-soft-gray gradient) and `.hero-ad-dark` (transparent, so the hero's existing gold glow/particle field read through). Each `.hero-slide` carries `data-ground="light"|"dark"`; `goHeroSlide()` toggles `#hero.on-light` to re-tint the carousel arrows and dots so they stay visible against either ground — this class is also set once at init (`goHeroSlide(heroSlide)` inside `initHeroCarousel()`), not just on slide change, otherwise the very first paint shows dark-tinted controls on slide 0's light ground for a frame.
  - **Three art treatments**: `.cutout` (a transparent-background render standing on the ground, drop-shadowed — used for the iPhone 18 render and the catalog-fed PS5 photo), `.fade-bottom` (masks a source image's already-cropped bottom edge into the ground instead of bleeding it to the slide edge, which would put the carousel dots on top of the product), and `.blend` (defined for a supplied creative that carries its own background, cover-cropped and radially masked so it dissolves into the ground — not currently used by any slide, kept for the next campaign asset that needs it).
  - **Slide 0 (iPhone 18 Pro, light)**: real headline/tagline/CTAs plus a proper cutout, sourced correctly this time. The user's own earlier-supplied `sky_phone2.jpg` (used in the previous, now-superseded round) turned out to be the wrong source — it has "SKYPHONE" baked directly across the phone body as an overlay, not as a separate title lockup. A follow-up session (routed through this repo via `/find_skills`, which supplied a fresh implementation brief plus new source images) provided `sky_phone3.jpg`: the *actual* full poster — a clean "iPhone 18 PRO -SKYPHONE-" title lockup above two product-only phone renders, no text baked onto the devices. Row-scanned for the true text/product boundary (near y=383, matching the brief's stated y=380) rather than trusting a guessed constant, then cut the background via connected-component flood-fill from the image border (not a flat white threshold — a flat threshold would punch transparent holes in the lens catchlight and flash-ring highlights *inside* the product, which are also near-white but not connected to the border) — see `img/iphone18-pro.png`. `img/iphone18-series-ad.jpg` (the old full-slide asset) is now unused and was removed.
  - **Slide 1 (PlayStation 5, light)**: art is fed live from the catalog (`pmediaSrc(p, p.img)` into `.ad-art-float`, id 27) instead of a separate supplied photo — one real photo, one source of truth, and it stays correct if the product photo is ever swapped. `img/ps5-ad.jpeg` (the previous round's separate hero asset) is now unused and was removed for the same reason. Price note and both WhatsApp-style CTAs pull from live data (`renderHeroAds()`, see below).
  - **Slide 2 (Repairs, dark)**: the existing authored wrench SVG, now wrapped in the same `.hero-ad`/`.hero-ad-art` structure as the other two so all three slides share one component instead of the repairs slide being a structural one-off. Note line shows the real lowest repair price computed from `REPAIRS`, not a typed-in number.
  - **`renderHeroAds()`** (called once at init after `initHeroCarousel()`, and again inside `setLang()` on every language switch): writes the PS5 and repair "from ₪X" notes from live catalog/repair data, rebuilds both WhatsApp links per-language (`wa_i18`/`wa_ps5` keys) so a Hebrew visitor never gets a prefilled Arabic message, and re-renders the PS5 catalog art. That last part created a real bug worth documenting: `attachAdTilt()` originally cached the art element (`wrap.querySelector('img,svg')`) once at attach-time, but `renderHeroAds()` replaces the PS5 slot's `innerHTML` on every language switch — after any switch, the cached reference pointed at a detached node and the tilt silently stopped moving for that one slide. Fixed by querying the art fresh inside the `pointermove`/`pointerleave` handlers instead of caching it — caught and fixed during this session's own verification pass, not shipped.
  - **Two-element rule for the art, strictly followed**: `.hero-ad-art` owns the entrance keyframe (`hero-ad-in`, `fill-mode:both`), `.ad-art-float` owns the idle float keyframe (infinite), and the bare `img`/`svg` owns the inline-style pointer tilt. Stacking more than one of these transforms on the same element is the exact fill-mode trap documented earlier in this file (a filled/running keyframe permanently outranks an inline style) — three elements, three owners, no conflict.
  - **Full removal of the old hero**, not a patch over it: `#heroStage`/`#heroDevice`/`.hero-device*`/`.draw-ring`/`.draw-check`/`.hero-inner`/`.hero-cta`/`.hero-fade` and their keyframes (`rise`, `draw`, `dev-float`) are gone from both `styles.css` and `index.html`, along with `initHeroTilt()`, `initHeroParallax()`, and the `animationend` handler's now-dead `rise`/`heroDevice` branch — these were flagged as "left in place, dead but harmless" in the previous DESIGN.md entry; this pass actually removed them since the slide that used them no longer exists in any form.
  - **Repo relocation mid-task**: the project directory moved from `~/Desktop/SkyPhone` to `~/Desktop/projects/SkyPhone` between sessions (an external reorganization, not something this session did) — same git repo/remote, no data loss, just a path change. Anyone resuming this work should confirm the local dev server is serving from the current path before testing (a stale `python -m http.server` process bound to the old, now-nonexistent path will 404).

## Icons

Authored single-stroke SVG set (1.5–1.75 stroke, rounded caps/joins, 24×24), consistent across nav, products, repairs, services and contact — replacing the old two-tone filled icon set.

## Known Issues Resolved

- FAQ answer reveal originally used `transition: max-height`, flagged by the design detector as layout-thrashing; replaced with a `grid-template-rows: 0fr → 1fr` transition (transform/opacity-safe technique), verified visually in-browser.
- Filled CSS entrance animations (`fill-mode: both` on `reveal-up`/`rise`) override inline styles indefinitely, which silently disabled the pointer-driven card tilt and hero device tilt. Resolved by swapping the animating class for a static end-state class on `animationend` (see Storefront polish pass, 2026-09-04). Any future entrance keyframe on an element that also receives inline JS transforms must use the same swap.
- Live-search Enter threw `Cannot read properties of undefined (reading 'id')` — the selection id was read from the results array after `close()` had already emptied it. The id is now captured before closing (fixed 2026-09-04).

## Deliberate Detector Exceptions

- `overused-font` (Inter): earned by the Apple-canon direction; see Type above.
- `broken-image` ×3 (brand-logo `<img>` tags in loader, About badge and footer): false positive from the detector's static regex pass — `app.js` sets `img.src` from an embedded base64 logo constant at runtime (`document.querySelectorAll('.brand-logo').forEach(el=>el.src=LOGO)`); confirmed rendering correctly in live browser QA. The navbar no longer uses an `<img>` at all (text wordmark, see Components).

## Logo

The embedded badge logo (`LOGO` constant in `app.js`) is the shop's real, in-use logo — verified against the live Instagram profile photo (@skyphone.ca) on 2026-09-03, not a placeholder. An independent design-critique pass flagged it as visually inconsistent with the rest of the restrained/no-gradient system and recommended replacing it; the user was asked and explicitly chose to **keep the real logo as-is** rather than have a new mark fabricated without the shop owner's input. This is a closed decision — do not swap or "improve" the logo again without the user raising it.

## Verified

Browser QA pass (desktop 1440px + simulated 390px mobile, driven via Selenium/Chrome) covered: routing between all four pages, product filtering, add-to-cart/qty/remove, cart drawer, checkout modal, repair booking with device picker, FAQ accordion, contact form submit/clear, mobile hamburger menu, live search suggestions (mouse + keyboard paths), fly-to-bag + badge pop, row arrows, scroll progress, nav indicator, and full language switching (HE/AR/EN, RTL↔LTR) — zero console errors on every flow, no horizontal overflow on any route at 390px.

## Mobile-polish + PDP information pass (2026-09-06)

Six issues raised after real-device (Android Chrome) review. What changed and why:

- **Chrome Android was auto-darkening the site.** The page had no declared colour
  scheme, so Chrome's Auto Dark Theme inverted surfaces and painted solid boxes
  behind transparent product PNGs (the "black background" on the PS5 hero art and
  the white boxes behind catalogue photos). Fixed by declaring the site light-only
  (`color-scheme: only light` in `:root` plus the matching `<meta>`), which is the
  documented opt-out. **Do not remove either without shipping a real dark theme** —
  the design has no dark palette, so auto-dark will re-break it.
- **Products page opened "zoomed in" on phones.** `.chips` is a `nowrap` flex
  scroller, so its ~550px min-content set the automatic minimum size of the `1fr`
  grid track in `.products-layout`, making the document 566px wide inside a 375px
  viewport. Being RTL, that overflow opened the page scrolled sideways. Fixed with
  `.products-layout>*{min-width:0}`. The identical trap reappeared in the new
  `.pdp-tabs` scroller and is fixed the same way (`.pdp-rw>*{min-width:0}`).
  **Any future grid item containing a nowrap scroller needs `min-width:0`.**
- **Customer reviews removed entirely.** With no backend there was nothing to show
  but invented ratings and invented customers, which is a liability for the shop
  owner rather than a feature. See `PRODUCT.md`.
- **Replaced with an "Everything you need to know" tabbed panel** (Overview /
  Description / Features / What's in the box). Composed only from data the
  catalogue genuinely carries plus the shop's verified service facts — it asserts
  no chip names, benchmarks or camera specs for SKUs whose spec sheet we do not
  have. Box contents key off the product's `icon` via `BOX_BY_ICON`, with per-SKU
  overrides in `PRODUCT_INFO` (Steam Deck, headset, standalone DualSense).
  Prose needs singular category nouns (`cat1_*`); the plural filter labels read
  wrong mid-sentence ("a Phones from Apple"), and English picks a/an by first letter.
- **PDP 3D product stage** (`attachPdpZoom`, which replaced the old hover-zoom).
  Perspective stage where the product tracks pointer or finger in 3D, lit by a
  highlight that moves with it (`--gx`/`--gy`) and grounded by a contact shadow
  that tightens as it lifts (`--gs`/`--go`). One rAF loop eases toward a target so
  hover, drag and spring-back share a path and never fight the CSS transition —
  hence `.stage-live` sets `transition:none`. Deliberately a shallow tilt, not a
  fake rotation: a true Apple-style spin needs a 3D model or a turntable frame
  sequence, and neither exists for this catalogue.
- **Gaming banner** now uses a real DualSense cutout (`img/gaming-controller.png`,
  background flood-filled off the existing `dualsense.png` and feathered) instead
  of the line-drawing SVG.

### Testing note for the next session

The in-app browser pane runs `document.visibilityState === 'hidden'`, which
**pauses `requestAnimationFrame` entirely**. Any rAF-driven work (this stage, the
page loader, `scroll-behavior:smooth`) will look broken/frozen and read as zeroed
state. It is a harness artifact, not a bug — drive such checks inside a
`browser_batch` that brackets them with screenshots (which force compositing), and
use `behavior:'instant'` for scrolling.

## Accessibility & UX audit pass (2026-09-06)

Run against the `ui-ux-pro-max` skill's rule set (Priorities 1, 2, 8 and the
colour rules), verified in-browser across 3 languages x 5 routes x 4 products.

- **Contrast.** The brand gold `--accent:#b8862f` is 3.24:1 on white — it failed
  AA everywhere it carried text or sat behind white text (every primary CTA).
  `--accent` is unchanged and still used for borders, focus rings, `accent-color`
  and anything on `--dark`, where it is 6.11:1. A second token
  **`--accent-strong:#896523`** now covers gold *as text* or *behind white text on
  light grounds* (4.51:1 even on `--bg-soft-2`). `--ink-faint` and `--ink-soft`
  were darkened for the same reason. **The two golds are not interchangeable:**
  `--accent-strong` drops to 3.72:1 on `--dark`, which is exactly the regression
  that hit `.brand-spot-apple .btn-link` mid-pass. Check the ground before picking.
- **A real bug, not just a ratio:** `.highlight-kind`'s grey sits later in the file
  than `.ad-badge`'s white at equal specificity, so the "coming soon" badge was
  rendering grey-on-gold at **1.06:1** — effectively invisible. Fixed with an
  explicit `.highlight-kind.ad-badge{color:#fff}`.
- **Contact form.** It previously toasted "sent" on a completely empty form. Now
  validates, with the error next to its field, an `role="alert"` summary that takes
  focus and links to each invalid field, `aria-invalid` on the inputs, and errors
  clearing as the user fixes them. The send itself is still a labelled demo.
- **Labels.** The form used placeholder-only labelling (they vanish on focus and
  are not reliably announced); it now has real `<label>`s. Search and chat inputs,
  where a visible label would duplicate an adjacent icon, get `aria-label` through
  a new `data-al` hook that follows the language switcher like `data-ph` does.
- **Skip link** (first focusable, targets `#main`) and **`scroll-padding-block-start`**
  so the fixed nav does not cover a focused target — WCAG 2.2 "Focus Not Obscured".
- **Touch targets.** `.promo-close` 22px -> 24px. `.hero-dot` keeps its 8px look but
  gets a 24px hit area via a `::before` overlay rather than growing the dot.
- `--err` / `--err-bg` added as real tokens rather than raw hex in the form rules.

Not changed: `--accent` itself, and the overall visual direction — both are the
user's locked decisions (see `PRODUCT.md`). The audit only moved values that
failed a measurable accessibility threshold, and kept the same hue when it did.

## apple.com alignment pass (2026-09-07)

Measured against an external analysis of apple.com captured in
`APPLE_STYLE_REFERENCE.md` — which is the craft bar `PRODUCT.md` already named for
this project, now written down instead of held in someone's head.

Four tokens already matched the reference exactly before this pass: `--ink:#1d1d1f`
(Carbon), `--bg-soft:#f5f5f7` (Frost), `--radius-pill:980px`, and Inter — which is the
reference's own stated substitute for SF Pro. The gap was shape, depth and tracking.

**Adopted**

- **Two radii only.** `--radius-sm/md/lg` all collapse to **8px**; `--radius-pill`
  stays 980px. The reference permits exactly these two values ("never use radius below
  980px for buttons or above 8px for cards/images"). The three token names were kept so
  the ~25 call sites did not all have to change.
- **Elevation removed.** Eight `box-shadow` elevations on cards, buttons, dropdowns,
  drawers and modals were replaced with 1px hairlines and surface shifts, per "the
  system uses hairline borders and surface shifts, not elevation".
- **Body type is now the reference spec exactly:** 17px / 1.47 / **−0.016em**
  (computes to −0.272px, matching `--tracking-body`).
- `.lede` at weight **300** — the editorial "whisper voice". Inter 300 was added to the
  font request, which previously started at 400.
- `--surface-wash:#f4f8fb` (Ice) added as the elevated section wash.

**Rejected, deliberately — each of these would have been a regression**

- **Apple Blue as the accent.** Owner confirmed the gold stays. It comes from the
  shop's own logo (see the token note above); blue CTAs would fight the gold logo mark
  on every page.
- **Pebble `#e2e2e5` as a surface.** Measured before adopting: on Pebble,
  `--ink-faint`, `--ink-soft` and `--accent-strong` all drop to ~4.11:1 and fail AA.
  `--bg-soft-2` stays `#ececee`, where the same three pass at 4.50:1. **Do not "fix"
  this toward the reference** — the whole 2026-09-06 contrast pass is tuned against it.
- **The reference's heading letter-spacing table** (+0.196px at 28px, +0.44px at 40px,
  +0.616px at 56px). It contradicts the reference's own prose and real apple.com display
  type, and reads as extraction noise. Existing negative heading tracking is kept.
- **Negative tracking on Arabic.** Arabic is cursive and connected — tracking pulls the
  joined letterforms apart and breaks words visually. `[lang="ar"]` is explicitly reset
  to `letter-spacing:normal`. Hebrew keeps the tracking (its letterforms are separate).
- **Weight 300 for Hebrew/Arabic subheads.** Noto renders too faint at these sizes;
  he/ar keep 400.
- **Shadows on the floating WhatsApp/chat buttons.** Apple's system has no floating
  action buttons for the rule to cover, and these sit over arbitrary scrolling content
  where the shadow is what keeps them legible. Kept as a stated exception, along with
  the grounding shadow on `.ab-badge-logo` (the reference allows shadows on images).

**Verified after the pass:** contrast still 0 failures across 3 languages x 5 routes x
PDPs, no horizontal overflow at 375px, no console errors.

## Brand strip rebuilt as real logos + a genuinely endless loop (2026-09-07)

The strip was two hardcoded copies of eight brand *names* shifted by
`translateX(-50%)`. Two independent faults made it stop short of the edge:

1. **The `-50%` trick only loops while one copy is at least as wide as the
   viewport.** Measured at 1900px: the whole track was 2352px, so each copy was
   1176px — 724px narrower than the screen, which is the empty space that showed.
2. **The track inherited `direction:rtl`.** A `width:max-content` track in an RTL
   container anchors to the *right* edge and overflows left, so a left-travelling
   animation immediately runs off the end of its own content.

Now built by `renderBrandMarquee()` from `BRAND_MARQUEE`: it clones the group until
the track is at least the container width plus two spare groups, then shifts by
**exactly one group width in px** (`--marquee-shift`), so the seam always lands on
identical content. Verified anchored-left with >1000px of spare content at 420,
600, 1000, 1440, 1900, 2560 and 3200px. Re-runs debounced on resize.

Things that will re-break it if changed carelessly:

- **`direction:ltr` belongs on `.brand-marquee`, not just `.marquee-track`.** On the
  track alone it fixes the glyph order but not the anchoring, and the gap comes back.
- **The inter-group gap lives inside `.marquee-group` as `padding-inline-end`,** not
  as a `gap` on the track. A gap on the track is not included in one group's measured
  width, so the shift would be short by exactly one gap and seam every cycle.
- **Speed is px/sec, not a fixed duration** (`--marquee-duration` = groupW / 52),
  otherwise a wider group scrolls faster on bigger screens.
- Measure the track with the animation disabled. `getBoundingClientRect()` includes
  the live transform, which made an early check here report the wrong anchor.

Logos are the official marks (Simple Icons, CC0). Each `viewBox` is tightened to the
mark's real `getBBox()` and carries its own `--h`: the source fits every mark inside a
24x24 square, so at a uniform square size the wide wordmarks (SAMSUNG, SONY) render
unreadably small. Mobile scales `--h` by 0.8 so each keeps its relative weight.
