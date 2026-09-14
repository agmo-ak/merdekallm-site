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

1. ~~**Google Analytics**~~ — done. Created GA4 property "Merdeka LLM"
   (measurement ID `G-9WQLFXK292`) under the same ak@agmostudio.com account
   that already runs Agmo Group's GA, with its own data stream for
   merdekallm.com. It's wired into every page in `build.py`. Data will start
   appearing in GA within ~48 hours of the new site going live at the real
   domain (it won't show real traffic while only tested on localhost/GitHub
   Pages default domain).
2. **Formspree** — `build.py` still has `FORMSPREE_ENDPOINT =
   "https://formspree.io/f/YOUR_FORM_ID"` as a placeholder — I can't create
   this account for you. Create a free form at formspree.io (verify
   merdeka@agmogroup.com as the receiving address), grab the form endpoint,
   put it in `build.py`, and rebuild. It's TODO-tagged — search for `TODO`.

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
