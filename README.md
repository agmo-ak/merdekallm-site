# merdekallm.com

The marketing site for **Merdeka LLM** by Agmo Group, live at [merdekallm.com](https://www.merdekallm.com/).

It is a plain static site. A small Python script turns page templates and Markdown blog posts into HTML, and GitHub Pages serves the result. There is no framework, no `npm install` and no third-party Python packages.

## Quick start

You need Python 3 and nothing else.

```bash
python3 build.py                 # generate every page, sitemap.xml and llms.txt (for local preview)
python3 -m http.server 8420      # preview at http://localhost:8420
```

## How it fits together

| Path | What it is |
| --- | --- |
| `build.py` | Site-wide settings (nav, footer, contact details, analytics, form endpoint), the shared page layout and a tiny Markdown converter. Run this file to build the site. |
| `pages_content.py` | The content of each page, one `build_*()` function per page. Also builds the blog index, `sitemap.xml` and `llms.txt`. |
| `content-source/*.md` | Blog posts, one file per post. |
| `assets/` | Hand-written CSS, JavaScript and images. |
| `index.html`, `*/index.html`, `post/`, `404.html`, `sitemap.xml`, `llms.txt` | **Generated output.** Not in git (see `.gitignore`). Do not edit these by hand: the next build overwrites them. |
| `NOTES.md` | Deployment history and open to-dos. |

The generated files are not committed. The deploy workflow runs `python3 build.py` on every push to `main`, so commit only your source changes. Run the build locally only to preview.

**Using Claude Code?** The project hooks in `.claude/settings.json` rebuild the local preview when Claude edits a source file with its Edit or Write tool, and stop Claude from editing generated files directly. They do not run for edits made through shell commands or in your own editor. That does not matter for the live site, because CI always builds it.

## Common tasks

### Edit text on a page

Find the page's `build_*()` function in `pages_content.py` (for example `build_home()` or `build_sovereignty()`), change the text, rebuild, and preview.

Nav links, footer links, the contact email and similar site-wide details live near the top of `build.py`.

### Add a blog post

1. Create `content-source/<slug>.md`. The filename becomes the URL: `/post/<slug>/`.
2. Start it with frontmatter:

   ```markdown
   ---
   title: Malaysia AI Sovereignty
   author: Aik Keong Tan
   date: 2024-11-01
   readtime: 4 min read
   ---
   ```

3. Write the post below it. The converter understands `#` headings, paragraphs, bullet and numbered lists, `**bold**` and `*italic*`. Links, images, code and tables are not supported yet.
4. Rebuild. The post appears on `/blog/`, in the sitemap and in `llms.txt` automatically.

### Add a new page

This touches several places, so it is easy to miss one:

1. Add a `build_<name>()` function in `pages_content.py`.
2. Call it from `build_all()`.
3. Add its URL to `STATIC_PATHS` (for the sitemap).
4. Add it to the page list in `build_llms_txt()`.
5. If it should be linked, add it to `NAV` and/or `FOOTER_COLS` in `build.py`.

## Things that will bite you

- **Keep URL slugs as they are.** They match the old Wix site so search rankings carry over.
- **Strict Content Security Policy.** No inline `style="..."` attributes and no inline `<script>` blocks. Put styles in `assets/css/styles.css` and scripts in `assets/js/main.js`. If you add anything from a new external host (a script, font, image, API or form target), add that host to `CSP_META` in `build.py` or the browser will block it.
- **The contact form** sends through [Formspree](https://formspree.io/) (form `xwlvlnzw`). The hidden `_gotcha` field catches spam bots, so leave it in.
- **This repo is public.** Only the site files are deployed, but everything in the repo, including the generator and notes, can be read on GitHub. Never commit secrets or private details.

## Deployment

Every push to `main` runs `.github/workflows/pages.yml`. It runs `python3 build.py` (Python 3.14, full git history so the sitemap `lastmod` dates are correct), then copies only the site files (the root HTML files, `assets/`, `post/` and each page folder) into the Pages artifact and deploys it. Changes are usually live within a minute or two.

Two consequences:

- A new root-level file that the site needs (such as a search engine verification file) must be added to the "Collect site files" step in the workflow.
- Any top-level folder containing an `index.html` gets published. Do not put an `index.html` in a folder of notes or source files.

## Before you push

There are no automated tests. Instead:

1. Run `python3 build.py`. If it fails here, it fails in CI and the site does not deploy.
2. Preview locally and click through the pages you touched, including on a narrow (mobile) window.
3. Open the browser console and confirm there are no CSP errors.
