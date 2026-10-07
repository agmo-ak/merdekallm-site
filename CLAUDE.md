# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Static marketing site for merdekallm.com (Merdeka LLM by Agmo Group), served by GitHub Pages. A small dependency-free Python generator produces every HTML page; the generated output is committed at the repo root alongside the generator. `.github/workflows/pages.yml` deploys on every push to `main`, publishing only the generated files (it does not run `build.py`, so rebuild before committing).

## Commands

```bash
python3 build.py                 # regenerate all pages, sitemap.xml and llms.txt in place
python3 -m http.server 8420      # local preview at http://localhost:8420 (same as .claude/launch.json)
```

There are no tests, linter or package dependencies. Verify changes by rebuilding, checking `git diff` on the generated HTML, and previewing locally.

## Architecture

- `build.py`: site-wide config (nav, footer, contact details, GA ID, FormSubmit endpoint, GSC verification), the HTML shell (`page_shell`), JSON-LD helpers, the CSP meta tag, a minimal markdown-to-HTML converter, and `write_page()`. Running it calls `pages_content.build_all()`.
- `pages_content.py`: page bodies as Python f-string HTML, one `build_*()` function per page, plus blog loading, `sitemap.xml` and `llms.txt` generation. It imports helpers from `build.py`.
- `content-source/*.md`: blog posts. Filename is the slug (`/post/<slug>/`). Frontmatter keys: `title`, `author`, `date` (YYYY-MM-DD), `readtime`.
- `assets/`: hand-written `css/styles.css`, `js/main.js` (mobile nav + AJAX contact form submit), images.
- Everything else at the root (`index.html`, `*/index.html`, `post/*/index.html`, `404.html`, `sitemap.xml`, `llms.txt`) is **generated output**. Edit the generator, not these files, or the next build overwrites the change.

URL slugs deliberately match the old Wix site for SEO continuity. Do not rename them.

## Gotchas

- **Adding a page** means touching several places: a `build_*()` in `pages_content.py`, a call in `build_all()`, the `STATIC_PATHS` list (sitemap), the page list in `build_llms_txt()`, and `NAV`/`FOOTER_COLS` in `build.py` if it should be linked.
- **CSP is strict** (`CSP_META` in `build.py`): no inline `style="..."` attributes and no inline scripts. The only inline script is the GA bootstrap, allowed by a SHA-256 hash computed from `GA_INLINE_SCRIPT` at build time. Any new external host (scripts, fetch, forms, images) must be added to the CSP or it will be blocked.
- **Markdown converter supports only** `#` headings, paragraphs, `-`/`*` and numbered lists, `**bold**` and `*italic*`. No links, images, code or tables; extend `markdown_to_html()` if a post needs them.
- **Contact form** posts to FormSubmit.co (`FORMSUBMIT_ENDPOINT`). The `_honey` hidden field is a spam honeypot; keep it.
- **What gets published** is decided by the "Collect site files" step in `pages.yml`: the listed root files, `assets/`, `post/`, and every top-level folder containing an `index.html`. A new root-level site file (e.g. a verification file) must be added there; a new folder of notes or source must never contain an `index.html`. The repo itself is public, so excluding files from the site does not make them private.
- **Sitemap `lastmod`** comes from git (`last_modified()` in `pages_content.py`): today for a source file with uncommitted edits, otherwise its last commit date. All static pages share `pages_content.py`'s date.
- `NOTES.md` holds deployment history and open items (FormSubmit activation, security headers needing a proxy, CAA record).
