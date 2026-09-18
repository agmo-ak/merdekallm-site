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
2. ~~**Contact form**~~ — done, using FormSubmit.co (no account needed) —
   `FORMSUBMIT_ENDPOINT = "https://formsubmit.co/ajax/merdeka@agmogroup.com"`
   in `build.py`. **One thing left**: FormSubmit.co requires a one-time
   confirmation — the *first* real submission to merdeka@agmogroup.com will
   trigger an activation email from FormSubmit.co to that inbox; someone
   with access needs to click "Confirm" in it once before submissions start
   arriving normally. Until then, submissions made before confirmation are
   silently dropped (visitors still see "Thanks — we'll be in touch
   shortly", so it's worth doing a real test submission and confirming
   right after the site goes live).
   - **Anti-spam**: added a honeypot field (`_honey`, hidden off-screen via
     `.hp-field` in styles.css) — FormSubmit auto-discards any submission
     where it's filled in, which naive spam bots that blindly fill every
     `<input>` will trip. Also removed the `_captcha value="false"` override
     we'd set earlier, since that was explicitly telling FormSubmit to skip
     its own spam filtering. If spam through the honeypot keeps showing up,
     the next lever is FormSubmit's `_captcha` challenge — but that may
     require switching off the AJAX endpoint (redirects to a challenge page
     instead of a silent fetch), so it's a bigger UX tradeoff.

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
