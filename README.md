# Sky Phone

The website for **Sky Phone**, a real phone/tablet/computer shop and repair lab in
Kafr Kanna, Israel, trading since 2010. Trilingual: Hebrew and Arabic (RTL), English
(LTR). Currency is the Israeli shekel (₪).

Live: https://saeedkhoury.github.io/SkyPhone/

## What this is

A static single-page app — no framework, no build step, no backend:

- `index.html` — all markup for every "page" (they're `<section>` elements toggled
  by JS, not separate URLs — see the note on this below)
- `styles.css` — all styling
- `app.js` — all behavior: routing, the product/repair catalog, cart, filters,
  language switching, the chatbot, everything

That's the whole app. Open `index.html` in a browser and it works — no `npm install`,
no build, no server required for basic browsing. For local testing where relative
paths behave exactly like the live site, run a tiny static server instead of opening
the file directly:

```bash
python3 -m http.server 8901
# then open http://localhost:8901/index.html
```

## Where the data lives

Everything a shop owner would actually want to change is in `app.js`, near the top:

- **Products** — the `PRODUCTS` array (starts around line 65). Each product is one
  object: `{id, name, cat, price, icon, brand, colors, storage, img, imgs, desc}`.
  `desc` has three keys — `he`, `ar`, `en` — one description per language.
- **Repair services and prices** — the `REPAIRS` array (starts around line 178).
- **Product photos** — the `IMG` map (starts around line 48) holds shared image
  paths; product objects reference files that live in `img/`.
- **Reels/videos** — the `REELS` array (starts around line 193) lists video files
  that live in `video/`.
- **All UI text** — the `T` object holds every string on the site, three times over
  (Hebrew, Arabic, English), keyed the same way in each language block. If you're
  adding new copy, add the same key to all three language blocks or it'll show up
  blank in two of the three languages.

### To change a price

Find the product in `PRODUCTS`, change its `price` field. That's it — every place
the price is shown (product card, product page, cart, hero ads, the chatbot) reads
from this one array, nothing is duplicated elsewhere.

### To add a new product

Copy an existing entry in `PRODUCTS` with a similar shape (same category), give it a
new unique `id` (one higher than the current maximum), and fill in its fields. Add a
real photo to `img/` and reference it in `img`/`imgs`. If you don't have a photo yet,
you can leave `img` unset — the site falls back to a generic icon rather than
breaking.

### To change opening hours, address, or phone number

These are **real values that must stay accurate** — search `app.js` for the current
value (e.g. search for the phone number `052-722-3916` or the address text) and
update every place it appears. Also update the JSON-LD block near the top of
`index.html`'s `<head>` if hours or address are added there (they are currently
deliberately left out — see "Known gaps" below).

## Deploying

This repo deploys via GitHub Pages from the `main` branch. Pushing to `main` is the
entire deploy step — there's nothing else to run or build.

```bash
git add -A
git commit -m "describe what changed and why"
git push origin main
```

GitHub Pages typically picks up a push within a minute or two.

### Don't forget to bump the cache-busting version

`index.html` links `styles.css` and `app.js` with a version query string:

```html
<link rel="stylesheet" href="styles.css?v=20260906i">
<script src="app.js?v=20260906i"></script>
```

**Every time you edit `styles.css` or `app.js`, bump this date/letter before
pushing.** Without it, a browser that already visited the site keeps using its
cached copy of the old file and won't see your change — the classic "I pushed but
nothing changed" bug.

## Known gaps (intentional, not oversights)

- **Opening hours are not published anywhere on this site's structured data**
  (the JSON-LD block in `<head>`) because they were never confirmed with the shop
  owner. Guessing them is worse than leaving them out — a wrong hour in Google
  sends someone to a closed shop. Confirm with the owner, then add `openingHours`
  to the JSON-LD block.
- **No real payment processing.** Checkout builds a WhatsApp message with the order
  details and opens a chat to the shop — the actual sale and payment happen the way
  they already do today, in person or over the phone. This is explained plainly to
  the customer in the confirmation modal, not hidden.
- **Analytics needs a real Measurement ID.** `index.html`'s `<head>` has a Google
  Analytics snippet with a placeholder ID (`G-XXXXXXXXXX`) — swap it for the real
  one or analytics silently collects nothing.
- **Single-page routing.** Every "page" and all 27 products live at one URL — there
  are no real per-product links to share or bookmark, and Google can only ever index
  one page with one title. Fixing this is a bigger architecture change (real URLs,
  the History API, per-route titles) — tracked separately, not done piecemeal.

## For whoever picks this up next

If that's future-you: you will not remember any of the above. Start by reading this
file fully, then open `app.js` and search for the thing you're trying to change
before touching anything — the file is long but everything lives in one obvious
place once you know the key names above.
