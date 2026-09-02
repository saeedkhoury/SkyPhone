# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Split static site: `index.html`, `styles.css`, `app.js` (no build step, no framework — matches the original single-file demo's zero-dependency approach, easy to preview and hand off).

## Users

Primary users are local retail customers of Sky Phone, a neighborhood tech shop and repair service (est. 2010). They fall into three overlapping groups: (1) trust/speed-driven customers who need a phone, tablet, or laptop repaired quickly by people they trust with their only device; (2) price-conscious shoppers comparing new/used phones, tablets, computers, and gaming gear; (3) customers who specifically value being served in their own language — Hebrew, Arabic, or English — by the same shop.

Secondary audience for this artifact: the freelancer's client (the shop owner) evaluating this build as a purchasable/deployable website — the demo must read as professional and trustworthy enough to justify the sale.

## Product Purpose

Sky Phone's site lets customers browse and buy phones/tablets/computers/gaming gear/accessories, book device repairs (screen, battery, charging port, water damage, software, laptop/PC, console) with indicative pricing, and reach the shop (phone, WhatsApp, address, hours) — all in Hebrew, Arabic, or English. Success is a visitor understanding what's in stock and what a repair costs, then calling, messaging, or adding items to a bag with confidence the shop is legitimate and skilled.

## Positioning

A single neighborhood shop that credibly does three things other local competitors usually split across separate businesses: sell new/used devices, repair them same-day with genuine parts and warranty, and serve the community natively in Hebrew, Arabic, and English. The trilingual same-day-repair combination is the differentiator, not price alone.

## Operating Context

- Trade-in: customer brings an old device, gets credit toward a new one.
- Repairs: customer describes device + fault, gets an indicative quote, drops off or ships the device, picks up in-store or gets home delivery.
- Purchases: browse by category (phones, tablets, computers, gaming, accessories), add to bag, checkout (payment integration is out of scope for this demo — a clearly labeled placeholder stands in).
- Contact: phone, WhatsApp, physical address, opening hours, and a contact form, plus Facebook/Instagram.
- All of the above must work correctly in all three languages, including RTL layout for Hebrew and Arabic and LTR for English.

## Capabilities and Constraints

- No backend/build step for this demo: static HTML/CSS/JS only, real payment/order/CRM/email integration is out of scope and must be visibly marked as a demo placeholder rather than silently faked.
- Real contact details verified from the shop's own public Instagram (@skyphone.ca, 54.2K followers) on 2026-09-03: phone/WhatsApp **052-722-3916**, address **Kafr Kanna, Main Street (Wadi al-Hai road)**. Opening hours were not published anywhere public — still a placeholder until the client confirms.
- The real Facebook **business Page** is facebook.com/skyphone.ca (linked from the Instagram bio). The Facebook URL the user originally supplied resolves to the owner's personal profile, not the business Page — use the business Page for the site's social link.
- Existing embedded base64 logo is confirmed as the shop's real logo (verified against the Instagram profile photo: gold phone + wrench + gears badge, "SKY PHONE — EST 2010" — matches the site's existing "established 2010" copy exactly).
- Currency: Israeli shekel (₪).
- Must support Hebrew (RTL), Arabic (RTL), English (LTR) with a working language switcher that re-renders all copy and direction instantly.

## Brand Commitments

- Name: Sky Phone. Established 2010.
- Existing embedded logo asset is the placeholder brand mark to keep for this demo.
- Standing visual direction (chosen by user over grounded alternatives, canon path): Apple-Store Premium Retail — near-black/near-white grounds, huge negative space, restrained single-accent color (not the old magenta/gold), pedestal-style product presentation, SF Pro-adjacent system sans type, minimal chrome, full-bleed sectioned storytelling. Craft bar: apple.com and the Apple Store app. Applies to future surfaces on this site unless the user changes it.

## Evidence on Hand

- Full HE/AR/EN copy for every section (hero, services, products, repairs, about, FAQ, contact, footer) already exists in the prior single-file build and should be preserved as the real, approved product copy — not regenerated.
- Product catalog (14 SKUs across phones/tablets/computers/gaming/accessories) and repair price list (7 services) exist and should be preserved as real demo data.
- Verified via the shop's public Instagram (2026-09-03): real logo, real phone/WhatsApp number, real address, real Facebook business Page URL — see Capabilities and Constraints. The account has 54.2K followers and 1,756 posts, almost entirely premium/designer phone-case and accessory content (Hermès- and Versace-pattern cases, gift-wrapped packaging) plus some repair/retail-counter footage — real, usable social-proof numbers for a "trusted by" element, but do not fabricate testimonial quotes or review scores, which were not present.
- Still no real product photography, customer testimonials, press, or case studies on hand for the catalog itself — the product images already in use (Wikimedia Commons stock photos + authored line icons) remain the placeholders; do not fabricate customer-facing claims beyond the verified facts above.

## Product Principles

1. Trilingual parity is a product requirement, not an afterthought — every screen must work identically well in HE/AR/EN, RTL and LTR.
2. Every interactive element (cart, filters, repair booking, FAQ, form, checkout) must actually function in this demo, even where the backend is a labeled placeholder — a client evaluating this to buy it should be able to click through the whole flow without hitting a dead end.
3. The shop is a trust business (people hand over their only phone) — visual and interaction design should read as premium and dependable, not flashy or templated.
4. Preserve existing approved copy and catalog data; redesign changes the visual system, not the product facts.

## Accessibility & Inclusion

No formal standard specified. Must support correct bidi (RTL/LTR) behavior across all three languages, readable contrast, and keyboard-operable interactive elements (nav, filters, cart, FAQ accordion, form) as a baseline.
