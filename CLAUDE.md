# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Static marketing site for merdekallm.com (Merdeka LLM by Agmo Group), served by GitHub Pages. A small dependency-free Python generator produces every HTML page; the generated output is written to the repo root alongside the generator but is gitignored. `.github/workflows/pages.yml` runs `build.py` on every push to `main` and publishes only the generated files, so commit source changes only.

## Commands

```bash
python3 build.py                 # generate all pages, sitemap.xml and llms.txt in place (local preview; CI builds the live site)
python3 -m http.server 8420      # local preview at http://localhost:8420 (same as .claude/launch.json)
```

There are no tests, linter or package dependencies. Verify changes by rebuilding and previewing locally. The generated HTML is not in git, so `git diff` does not show it; to compare output, copy the built files aside before the change and `diff -r` after.

## Architecture

- `build.py`: site-wide config (nav, footer, contact details, GA ID, Formspree endpoint, GSC verification), the HTML shell (`page_shell`), JSON-LD helpers, the CSP meta tag, a minimal markdown-to-HTML converter, and `write_page()`. Running it calls `pages_content.build_all()`.
- `pages_content.py`: page bodies as Python f-string HTML, one `build_*()` function per page, plus blog loading, `sitemap.xml` and `llms.txt` generation. It imports helpers from `build.py`.
- `content-source/*.md`: blog posts. Filename is the slug (`/post/<slug>/`). Frontmatter keys: `title`, `author`, `date` (YYYY-MM-DD), `readtime`.
- `assets/`: hand-written `css/styles.css`, `js/main.js` (mobile nav + AJAX contact form submit), images.
- Everything else at the root (`index.html`, `*/index.html`, `post/*/index.html`, `404.html`, `sitemap.xml`, `llms.txt`) is **generated output** and gitignored. Edit the generator, not these files, or the next build overwrites the change.

URL slugs deliberately match the old Wix site for SEO continuity. Do not rename them.

## Gotchas

- **Adding a page** means touching several places: a `build_*()` in `pages_content.py`, a call in `build_all()`, the `STATIC_PATHS` list (sitemap), the page list in `build_llms_txt()`, and `NAV`/`FOOTER_COLS` in `build.py` if it should be linked.
- **CSP is strict** (`CSP_META` in `build.py`): no inline `style="..."` attributes and no inline scripts. The only inline script is the GA bootstrap, allowed by a SHA-256 hash computed from `GA_INLINE_SCRIPT` at build time. Any new external host (scripts, fetch, forms, images) must be added to the CSP or it will be blocked.
- **Markdown converter supports only** `#` headings, paragraphs, `-`/`*` and numbered lists, `**bold**`, `*italic*` and `[text](url)` links (site paths `/...` or `https://`; external ones open in a new tab). No images, code or tables; extend `markdown_to_html()` if a post needs them.
- **CSS/JS are cache-busted**: `asset_url()` in `build.py` links `styles.css` and `main.js` with a `?v=<content hash>`, because GitHub Pages caches them for 10 minutes and new HTML would otherwise render with an old stylesheet. CI rebuilds on deploy, so every page gets the new hash; rebuild locally to preview.
- **Contact form** posts to Formspree (`FORMSPREE_ENDPOINT`, form `xwlvlnzw`). The `_gotcha` hidden field is a spam honeypot; keep it.
- **What gets published** is decided by the "Collect site files" step in `pages.yml`: the listed root files, `assets/`, `post/`, and every top-level folder containing an `index.html`. A new root-level site file (e.g. a verification file) must be added there; a new folder of notes or source must never contain an `index.html`. The repo itself is public, so excluding files from the site does not make them private.
- **Sitemap `lastmod`** comes from git (`last_modified()` in `pages_content.py`): today for a source file with uncommitted edits, otherwise its last commit date. CI checks out with `fetch-depth: 0` for this; a shallow clone would give every file the newest commit's date. All static pages share `pages_content.py`'s date.
- `NOTES.md` holds deployment history and open items (Formspree confirmation, security headers needing a proxy, CAA record).
