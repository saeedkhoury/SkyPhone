# Sky Phone

Website for **Sky Phone** — a phone, tablet and computer shop and repair lab in
Kafr Kanna, trading since 2010. Trilingual: Hebrew and Arabic (RTL), English (LTR).
Prices in shekels (₪).

Live: <https://saeedkhoury.github.io/SkyPhone/>

## Architecture

A static site — three files, no framework, no build step, no server:

| File | Contains |
|---|---|
| `index.html` | All markup. Pages are `<section>` elements toggled by JS. |
| `styles.css` | All styling, driven by CSS custom properties in `:root`. |
| `app.js` | Catalog data, routing, cart, filters, languages, chat assistant. |

Nothing to install and nothing to deploy but the files themselves. It runs on any
static host — GitHub Pages, Netlify, Cloudflare Pages, or ordinary shared hosting.

For local work, serve the folder rather than opening the file directly, so relative
paths behave exactly as they do live:

```bash
python3 -m http.server 8901
```

## Changing the shop's content

Everything the shop would routinely edit sits at the top of `app.js`:

- **`PRODUCTS`** — one object per item: `{id, name, cat, price, icon, brand, colors,
  storage, img, imgs, desc}`. `desc` holds one description per language (`he`, `ar`, `en`).
- **`REPAIRS`** — repair services and their indicative prices.
- **`IMG`** / **`IMG2`** — image paths; the files live in `img/`.
- **`REELS`** — the video strip; files live in `video/`.
- **`SHOP_WA`** — the shop's WhatsApp number. Every order, enquiry and chat link on
  the site is built from this one constant.
- **`T`** — all site copy, in three languages, keyed by `data-t` attributes in the HTML.

## Orders and enquiries

There is no payment gateway. The cart and the contact form both compose a formatted
message and hand it to the shop's WhatsApp as a prefilled draft, which the customer
sends and the shop answers on the number it already watches. Payment happens in store.

This is deliberate for a shop of this size: no card fees, no PCI obligations, no
checkout to maintain, and orders arrive where staff already are. Adding a real
gateway later does not require rebuilding the site.

## Chat assistant

The bubble in the corner answers from the site's own data — a price it quotes is
the price on the product page, because it reads the same `PRODUCTS` and `REPAIRS`
arrays. There is no API behind it and nothing to pay for per message.

It replies in the language the customer typed in, remembers the device under
discussion so follow-ups like "and the battery?" work, and ends every answer it
cannot close itself with a WhatsApp button carrying the customer's own question.
Its keywords and canned answers live in `CHAT_INTENTS`, `CHAT_REP_KW` and the
`chat_*` keys in `T`.

## Addresses

Pages have their own URLs (`#/products`, `#/product/17`, `#/repairs`, `#/bag`,
`#/about`). Any of them can be pasted into WhatsApp or bookmarked and it opens on the
right page, with a matching tab title. Back and Forward behave normally.

## Analytics

`ANALYTICS_ID` at the top of `index.html` is empty, so no tracking script loads and
no third-party request is made. Put a GA4 Measurement ID there to switch reporting
on. Visits, WhatsApp clicks and cart checkouts are already instrumented.

## Assets

- `img/` — every product image ships as both an original and a WebP twin; the browser
  picks the smaller one it supports.
- `video/` — reels, each with a poster frame so the strip never shows black.
- Icons, `og-image.jpg` (link previews) and `site.webmanifest` are at the root.

## Accessibility and support

Built to WCAG 2.2 AA: contrast checked, touch targets at least 44px, full keyboard
operation, visible focus, form errors announced. Tested from 320px up, in all three
languages, in both text directions.
