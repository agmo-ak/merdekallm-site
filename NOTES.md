# Merdeka LLM site — build notes

Static site generator: `build.py` + `pages_content.py` render everything in
`content-source/*.md` (blog posts) and the hand-written page bodies into
plain static HTML under folder-per-slug (`why-sovereignty-matters/index.html`
etc.), matching the URL structure of the old Wix site.

**Repo layout**: the generated HTML is written to the repo root alongside
the generator but is not in git (`.gitignore`). `.github/workflows/pages.yml`
runs `build.py` and deploys the output on every push to `main`, copying only the site files into the Pages artifact, so `build.py`,
`pages_content.py`, `content-source/` and the notes files are not served
from merdekallm.com (Settings → Pages → Source = "GitHub Actions"). The
repo itself is public, so they are still readable on GitHub. History:
until 2026-10 Pages published the whole repo root, which served the source
files too; an earlier attempt to fix that by publishing `docs/` (2026-09-19)
broke the live site and was reverted. Until 2026-10-09 the generated HTML
was committed and CI did not build; a commit without a rebuild deployed stale
pages, so CI now builds and the output left git.

To preview locally after editing content or templates:

```bash
python3 build.py    # generates all pages, sitemap.xml and llms.txt in place
```

## Still needs your input before this is fully live

1. ~~**Google Analytics**~~ — done. Created GA4 property "Merdeka LLM"
   (measurement ID `G-9WQLFXK292`) under the same Google account
   that already runs Agmo Group's GA, with its own data stream for
   merdekallm.com. It's wired into every page in `build.py`. Data will start
   appearing in GA within ~48 hours of the new site going live at the real
   domain (it won't show real traffic while only tested on localhost/GitHub
   Pages default domain).
2. **Contact form** — posts to Formspree form `xwlvlnzw`
   (`FORMSPREE_ENDPOINT = "https://formspree.io/f/xwlvlnzw"` in `build.py`);
   where submissions are delivered is set in the Formspree dashboard, not in
   the site code. History: Formspree → FormSubmit.co (2026-09) → back to
   Formspree (2026-10). **Check once after deploy**: send a real test
   submission and confirm it arrives (new Formspree forms may require
   confirming the notification email first).
   - **Anti-spam**: honeypot field `_gotcha` (hidden off-screen via
     `.hp-field` in styles.css) — Formspree discards submissions where it's
     filled in. More levers are in the Formspree dashboard (reCAPTCHA,
     allowed-domain restriction, spam filtering).

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

## Performance/security audit fixes (2026-09-20)

- **Hero GIF was 2.5MB** (241 frames at ~50fps, way more than a decorative
  loop needs). Thinned to every 6th frame, resized to actual display width
  (420px), re-optimized with gifsicle → **387KB** (85% smaller), visually
  identical. `assets/images/hero-rocket.gif` in place, no code changes
  needed.
- **Content-Security-Policy** added (meta tag — see CSP_META in build.py).
  Locks script/style/connect/form-action down to self + the specific
  Google Analytics and Formspree hosts actually used; the one inline
  script (gtag bootstrap) is allowed via its exact SHA-256 hash rather
  than a blanket `unsafe-inline`. Removed the handful of inline
  `style="..."` attributes across the site so `style-src` didn't need
  `unsafe-inline` either. Note: CSP via `<meta>` ignores `frame-ancestors`
  — that, plus HSTS/X-Frame-Options/X-Content-Type-Options, need a real
  HTTP header, which GitHub Pages custom domains don't support without
  fronting the site with something like Cloudflare. Not done here since
  it's a bigger infra change — flag if you want to pursue it.
- **`Referrer-Policy: strict-origin-when-cross-origin`** added via meta tag.
- No CAA DNS record exists for merdekallm.com — not a vulnerability, but
  worth adding (`CAA 0 issue "letsencrypt.org"`) so only Let's Encrypt
  (who GitHub Pages actually uses) can issue certificates for the domain.
  I have the DNS access to add this if you want it done.
