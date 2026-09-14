# Merdeka LLM site — build notes

Static site generator: `build.py` + `pages_content.py` render everything in
`content-source/*.md` (blog posts) and the hand-written page bodies into
plain static HTML under folder-per-slug (`/why-sovereignty-matters/index.html`
etc.), matching the URL structure of the old Wix site.

To rebuild after editing content or templates:

```bash
python3 build.py
```

## Still needs your input before this is fully live

1. **Google Analytics** — `build.py` has `GA_MEASUREMENT_ID = "G-XXXXXXXXXX"`
   as a placeholder. No GA4 property exists yet for merdekallm.com under
   ak@agmostudio.com — create one (analytics.google.com → Admin → Create
   Property), grab the `G-XXXXXXXXXX` measurement ID from its Web data
   stream, put it in `build.py`, and rebuild.
2. **Formspree** — `build.py` has `FORMSPREE_ENDPOINT =
   "https://formspree.io/f/YOUR_FORM_ID"` as a placeholder. Create a free
   form at formspree.io (verify merdeka@agmogroup.com as the receiving
   address), grab the form endpoint, put it in `build.py`, and rebuild.
3. Both are TODO-tagged in `build.py` — search for `TODO`.

## What was preserved from the live Wix site

- Exact URL slugs for every page and blog post (SEO continuity).
- The existing Search Console verification meta tag
  (`google-site-verification`) — keeps the already-verified
  `https://www.merdekallm.com/` property working once DNS points here.
- All 12 blog posts, verbatim.
- Site metadata (title, description, OG/Twitter tags), the favicon, and the
  homepage hero illustration and OG image, re-hosted locally under
  `/assets/images/`.

## Deliberate changes from the live site

- **Legal pages** (privacy, terms, refund, accessibility) were still Wix's
  unedited template text on the live site — the accessibility page even had
  literal `[enter organization name]`-style placeholders still in it. I
  filled in the obvious placeholders with real details (Agmo Group,
  merdekallm.com, contact info) but did not write new legal terms — you may
  want a lawyer to draft real ones.
- **`/llm-training-as-a-service`** was returning a 404 on the live site (even
  though linked in nav + sitemap). Reconstructed a full page from the
  homepage's TaaS blurb (Phison aiDAPTIV+ / SNS partnership) per your
  instruction.
