#!/usr/bin/env python3
"""
Static site generator for merdekallm.com.
Reads content-source/*.md for blog posts, writes plain static HTML
(one folder-per-slug with index.html) into the repo root, ready for
GitHub Pages. No runtime dependency — this script only runs locally.
"""
import os
import re
import glob
import html
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Site-wide config
# ---------------------------------------------------------------------------
SITE_NAME = "Merdeka LLM"
SITE_TAGLINE = "by Agmo Group"
DOMAIN = "merdekallm.com"
BASE_URL = f"https://{DOMAIN}"
DEFAULT_DESCRIPTION = (
    "Merdeka LLM by Agmo Group offers Malaysia's first AI Sovereignty as a Service, "
    "empowering local businesses and government agencies with secure, locally hosted "
    "language models. Built for sovereignty, tailored to Malaysia's unique linguistic "
    "and cultural needs."
)
OG_IMAGE = f"{BASE_URL}/assets/images/og-image.png"

# Filled in once the user creates the properties — see NOTES.md
GA_MEASUREMENT_ID = "G-XXXXXXXXXX"  # TODO: replace once GA4 property is created
GSC_VERIFICATION = "EIqgZD8FoC7lPeDgGpcOZhCk8h2clPwHxMeJdOYbpPA"  # preserves the existing verified GSC property
FORMSPREE_ENDPOINT = "https://formspree.io/f/YOUR_FORM_ID"  # TODO: replace with real Formspree form id

NAV = [
    ("LLM Training as a Service", "/llm-training-as-a-service/"),
    ("LLM Gig Economy", "/llm-gig-economy/"),
    ("Merdeka Model Hub", "/merdeka-model-llm/"),
    ("Why Sovereignty Matters", "/why-sovereignty-matters/"),
    ("Blog", "/blog/"),
]

FOOTER_COLS = [
    ("Platform", [
        ("LLM Training as a Service", "/llm-training-as-a-service/"),
        ("LLM Gig Economy", "/llm-gig-economy/"),
        ("Merdeka Model Hub", "/merdeka-model-llm/"),
        ("Why Sovereignty Matters", "/why-sovereignty-matters/"),
    ]),
    ("Community", [
        ("Become a Curator", "/curator/"),
        ("Become a Contributor", "/contributor/"),
        ("Blog", "/blog/"),
    ]),
    ("Legal", [
        ("Privacy Policy", "/privacy-policy/"),
        ("Terms & Conditions", "/terms-and-conditions/"),
        ("Refund Policy", "/refund-policy/"),
        ("Accessibility Statement", "/accessibility-statement/"),
    ]),
]

ADDRESS_LINES = [
    "Agmo Group",
    "Level 38, MYEG Tower,",
    "Empire City Damansara,",
    "Jalan PJU 8, Damansara Perdana,",
    "47820 Petaling Jaya, Selangor, Malaysia.",
]
EMAIL = "merdeka@agmogroup.com"
PHONE = "+603-7664 8515"

TOPICS = [
    "AI Sovereignty as a Service",
    "LLM Training as a Service",
    "LLM Gig Economy / Curatorship",
    "Partnerships",
    "Media / Press",
    "Other",
]

# ---------------------------------------------------------------------------
# Tiny markdown -> HTML (only the subset our blog posts actually use)
# ---------------------------------------------------------------------------
def inline_md(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", text)
    return text


def markdown_to_html(md_text):
    lines = md_text.strip("\n").split("\n")
    html_parts = []
    i = 0
    list_stack = None  # 'ul' or 'ol'

    def close_list():
        nonlocal list_stack
        if list_stack:
            html_parts.append(f"</{list_stack}>")
            list_stack = None

    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            close_list()
            i += 1
            continue

        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            close_list()
            level = min(len(m.group(1)) + 1, 6)  # article h1 is page title, so md # -> h3+
            level = 3 if len(m.group(1)) == 3 else (4 if len(m.group(1)) == 4 else level)
            html_parts.append(f"<h{level}>{inline_md(m.group(2))}</h{level}>")
            i += 1
            continue

        m = re.match(r"^[-*]\s+(.*)$", line)
        if m:
            if list_stack != "ul":
                close_list()
                html_parts.append("<ul>")
                list_stack = "ul"
            html_parts.append(f"<li>{inline_md(m.group(1))}</li>")
            i += 1
            continue

        m = re.match(r"^\d+\.\s+(.*)$", line)
        if m:
            if list_stack != "ol":
                close_list()
                html_parts.append("<ol>")
                list_stack = "ol"
            html_parts.append(f"<li>{inline_md(m.group(1))}</li>")
            i += 1
            continue

        close_list()
        # paragraph: gather until blank line
        buf = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,6})\s+", lines[i]) \
                and not re.match(r"^[-*]\s+", lines[i]) and not re.match(r"^\d+\.\s+", lines[i]):
            buf.append(lines[i].rstrip())
            i += 1
        html_parts.append(f"<p>{inline_md(' '.join(buf))}</p>")

    close_list()
    return "\n".join(html_parts)


def parse_frontmatter(md_text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", md_text, re.S)
    if not m:
        return {}, md_text
    fm_raw, body = m.group(1), m.group(2)
    fm = {}
    for line in fm_raw.split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm, body


# ---------------------------------------------------------------------------
# HTML shell
# ---------------------------------------------------------------------------
def ga_snippet():
    return f"""
    <script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', '{GA_MEASUREMENT_ID}');
    </script>"""


def nav_html(active_path):
    items = []
    for label, href in NAV:
        cls = ' class="active"' if href == active_path else ""
        items.append(f'<li><a href="{href}"{cls}>{label}</a></li>')
    return "\n          ".join(items)


def mobile_nav_html(active_path):
    items = ['<a href="/#contact" style="color:var(--brand)">Join the AI Revolution &rarr;</a>']
    items += [f'<a href="{href}">{label}</a>' for label, href in NAV]
    items.append('<a href="/curator/">Become a Curator</a>')
    items.append('<a href="/contributor/">Become a Contributor</a>')
    return "\n    ".join(items)


def footer_html():
    cols = []
    for title, links in FOOTER_COLS:
        li = "\n        ".join(f'<li><a href="{href}">{label}</a></li>' for label, href in links)
        cols.append(f"""
      <div class="footer-col">
        <h4>{title}</h4>
        <ul>
        {li}
        </ul>
      </div>""")
    year = datetime.now().year
    return f"""
  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <a class="brand" href="/">
            <img src="/assets/images/favicon.svg" alt="" width="28" height="28">
            {SITE_NAME}
          </a>
          <p>Malaysia's sovereign AI platform — built by Malaysians, hosted in Malaysian data centers, trained on local data. Powered by Agmo Group.</p>
        </div>
        {"".join(cols)}
      </div>
      <div class="footer-bottom">
        <span>&copy; {year} AGMO MERDEKA LLM. All rights reserved.</span>
        <span>{ADDRESS_LINES[1]} {ADDRESS_LINES[2]} {ADDRESS_LINES[3]} {ADDRESS_LINES[4]}</span>
      </div>
    </div>
  </footer>"""


def contact_section():
    topic_opts = "\n            ".join(f'<option>{t}</option>' for t in TOPICS)
    return f"""
  <section id="contact">
    <div class="container">
      <div class="section-head center">
        <span class="eyebrow">Get in touch</span>
        <h2>Let's Shape the Future Together</h2>
        <p>Join us in building a brighter tomorrow — reach out anytime.</p>
      </div>
      <div class="contact-wrap">
        <div class="contact-info">
          <h3>Contact details</h3>
          <div class="contact-item">
            <div>
              <strong>Address</strong>
              {ADDRESS_LINES[0]}<br>{ADDRESS_LINES[1]}<br>{ADDRESS_LINES[2]}<br>{ADDRESS_LINES[3]}<br>{ADDRESS_LINES[4]}
            </div>
          </div>
          <div class="contact-item">
            <div><strong>Email</strong><a href="mailto:{EMAIL}">{EMAIL}</a></div>
          </div>
          <div class="contact-item">
            <div><strong>Phone</strong><a href="tel:{PHONE.replace(' ', '')}">{PHONE}</a></div>
          </div>
        </div>
        <div class="form-card">
          <form data-contact-form action="{FORMSPREE_ENDPOINT}" method="POST">
            <div class="form-row">
              <div class="field">
                <label for="fname">First name *</label>
                <input id="fname" name="First Name" type="text" required>
              </div>
              <div class="field">
                <label for="lname">Last name</label>
                <input id="lname" name="Last Name" type="text">
              </div>
            </div>
            <div class="form-row">
              <div class="field">
                <label for="email">Email *</label>
                <input id="email" name="Email" type="email" required>
              </div>
              <div class="field">
                <label for="phone">Phone no.</label>
                <input id="phone" name="Phone" type="tel">
              </div>
            </div>
            <div class="field">
              <label for="topic">What topic are you interested in? *</label>
              <select id="topic" name="Topic" required>
                {topic_opts}
              </select>
            </div>
            <button class="btn btn-primary btn-block" type="submit">Submit</button>
            <p class="form-status" role="status" aria-live="polite"></p>
            <p class="form-note">We'll only use these details to respond to your enquiry.</p>
          </form>
        </div>
      </div>
    </div>
  </section>"""


def page_shell(*, title, description, path, body, active_nav=None, og_image=None, extra_head=""):
    canonical = f"{BASE_URL}{path}"
    og_image = og_image or OG_IMAGE
    full_title = title if title == SITE_NAME else f"{title} | {SITE_NAME} {SITE_TAGLINE}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{html.escape(description, quote=True)}">
<link rel="canonical" href="{canonical}">
<meta name="google-site-verification" content="{GSC_VERIFICATION}">
<meta property="og:title" content="{html.escape(full_title, quote=True)}">
<meta property="og:description" content="{html.escape(description, quote=True)}">
<meta property="og:image" content="{og_image}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE_NAME} {SITE_TAGLINE}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(full_title, quote=True)}">
<meta name="twitter:description" content="{html.escape(description, quote=True)}">
<meta name="twitter:image" content="{og_image}">
<link rel="icon" href="/assets/images/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/images/favicon.svg">
<link rel="stylesheet" href="/assets/css/styles.css">
{extra_head}{ga_snippet()}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <nav class="nav" aria-label="Primary">
    <a class="brand" href="/">
      <img src="/assets/images/favicon.svg" alt="" width="30" height="30">
      {SITE_NAME}
    </a>
    <ul class="nav-links">
      {nav_html(active_nav)}
    </ul>
    <div class="nav-cta">
      <a class="btn btn-primary" href="/#contact">Join the AI Revolution</a>
      <button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false">&#9776;</button>
    </div>
  </nav>
  <div class="mobile-nav">
    {mobile_nav_html(active_nav)}
  </div>
</header>
<main id="main">
{body}
</main>
{footer_html()}
<script src="/assets/js/main.js"></script>
</body>
</html>"""


def write_page(rel_path, html_str):
    if rel_path == "/":
        out = os.path.join(ROOT, "index.html")
    else:
        out_dir = os.path.join(ROOT, rel_path.strip("/"))
        os.makedirs(out_dir, exist_ok=True)
        out = os.path.join(out_dir, "index.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html_str)
    print("wrote", os.path.relpath(out, ROOT))


# ---------------------------------------------------------------------------
# Pages are defined in pages_content.py to keep this file focused on the
# templating/build machinery.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import pages_content
    pages_content.build_all()
