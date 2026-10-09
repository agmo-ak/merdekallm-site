"""Page content/body HTML for the Merdeka LLM static site."""
import os
import re
import glob
import html
import subprocess
from build import (
    ROOT, PUBLISH_DIR, page_shell, write_page, contact_section, markdown_to_html,
    parse_frontmatter, DEFAULT_DESCRIPTION, EMAIL, PHONE, BASE_URL, SITE_NAME, OG_IMAGE,
)

ICONS = {
    "train": "&#9881;",   # gear
    "gig": "&#129309;",   # handshake
    "shield": "&#128737;", # shield
    "server": "&#128421;", # server
    "channels": "&#128225;",
    "flag": "&#127471;",   # MY-ish placeholder
}


def hero(eyebrow, title, lede, actions="", art="", badges=""):
    badges = f'\n        <div class="hero-badges">{badges}</div>' if badges else ""
    return f"""
  <section class="hero">
    <div class="container hero-grid">
      <div>
        <span class="eyebrow">{eyebrow}</span>
        <h1>{title}</h1>
        <p class="lede">{lede}</p>
        <div class="hero-actions">{actions}</div>{badges}
      </div>
      <div class="hero-art">{art}</div>
    </div>
  </section>"""


JOIN_BTN = '<a class="btn btn-primary" href="/#contact">Join the AI Revolution</a>'

# MerdekaLLM-Sasbadi-27b on MalayMMLU, from our internal evaluation run.
# Not a leaderboard listing: don't claim a rank until it is listed.
MALAYMMLU = {
    "model": "MerdekaLLM-Sasbadi-27b",
    "date": "2026-08-26",
    "overall": "84.9",
    "questions": "24,213",  # full MalayMMLU set, not the leaderboard's 1,100 sample
    # Scored generate-and-parse, same as the leaderboard. If a run ever switches to
    # first-token logprob, compare against ILMU's official 87.2% instead.
    "categories": [
        ("STEM", "87.49"),
        ("Language", "87.23"),
        ("Social science", "80.60"),
        ("Humanities", "87.31"),
        ("Others", "84.43"),
    ],
}
MALAYMMLU_PAPER_URL = "https://aclanthology.org/2024.findings-emnlp.36/"

# Comparison rows from the Pendakwah Teknologi MalayMMLU leaderboard (credited on
# the page). Copied by hand, so re-check the source when updating.
# (model, organisation, overall, STEM, Language, Social science, Humanities, Others)
PENDAKWAH_URL = "https://pendakwah.tech/bahasa/mmlu/"
PENDAKWAH_RETRIEVED = "7 October 2026"
PENDAKWAH_LEADERBOARD = [
    ("Gemini 3.1 Pro", "Google", "91.5", 91, 96, 89, 93, 89),
    ("GPT-5.5", "OpenAI", "89.3", 89, 93, 85, 90, 89),
    ("Claude Opus 4.8", "Anthropic", "88.7", 86, 90, 86, 92, 89),
    ("Kimi K3", "Moonshot (Ollama Cloud)", "87.5", 89, 91, 84, 90, 83),
    ("Qwen 3.7 Max", "Alibaba", "86.6", 83, 92, 86, 91, 81),
    ("DeepSeek V4 Pro 0813", "DeepSeek (Ollama Cloud)", "85.5", 86, 89, 82, 87, 84),
    ("Qwen 3.5 397B", "Alibaba (Ollama Cloud)", "85.4", 85, 90, 81, 87, 84),
    ("ILMU GLM-5.1", "YTL AI Labs", "84.0", 85, 86, 80, 85, 84),
    ("DeepSeek V4 Pro", "DeepSeek", "83.8", 85, 89, 80, 84, 81),
    ("ILMU v3.1", "YTL AI Labs", "83.1", 84, 87, 80, 84, 81),
    ("MiniMax M3", "MiniMax (Ollama Cloud)", "82.8", 85, 85, 79, 87, 78),
    ("Grok 4.3", "xAI", "82.3", 81, 84, 80, 83, 83),
    ("GLM-5.2", "Z.ai", "81.8", 83, 86, 84, 81, 75),
    ("Mistral Large 3", "Mistral (Ollama Cloud)", "81.5", 82, 86, 79, 82, 77),
    ("Kimi K2.6", "Moonshot", "80.7", 85, 86, 75, 81, 76),
    ("Mistral Large 2512", "Mistral", "80.4", 79, 83, 80, 82, 77),
    ("MiniMax M3", "MiniMax", "79.6", 82, 84, 77, 79, 76),
    ("Llama 4 Maverick", "Meta", "78.1", 84, 79, 76, 78, 74),
    ("ILMU Vision v1.3", "YTL AI Labs", "74.9", 79, 75, 73, 74, 74),
    ("ILMU Mini v3.3", "YTL AI Labs", "71.8", 74, 72, 72, 71, 70),
    ("GLM-5.3", "Z.ai (Ollama Cloud)", "71.6", 65, 74, 70, 76, 74),
]


DATA_PARTNER_BTN = '<a class="btn btn-primary" href="/#contact">Become a data partner</a>'


def data_partner_callout(domain, who):
    return f"""
        <div class="hub-callout">
          <h4>Become our {domain} data partner</h4>
          <p>We&rsquo;re building the next Merdeka {domain} model with a partner who knows the field: {who}.</p>
        </div>"""


MALAYSIAN_ORGS = {"YTL AI Labs"}
# Leaderboard leaders shown in the comparison table as the frontier reference.
FRONTIER_SHOWN = 3


# Total parameters (billions) from each developer's own model card or repo.
# Only models with an official count are plotted; closed models are left out.
GLM5_URL = "https://github.com/zai-org/GLM-5"
MISTRAL_L3_URL = "https://huggingface.co/mistralai/Mistral-Large-3-675B-Instruct-2512"
MODEL_PARAMS = {
    "Kimi K3": (2800, "https://huggingface.co/moonshotai/Kimi-K3"),
    "DeepSeek V4 Pro 0813": (1600, "https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813"),
    "DeepSeek V4 Pro": (1600, "https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro"),
    "Qwen 3.5 397B": (397, "https://huggingface.co/Qwen/Qwen3.5-397B-A17B"),
    "MiniMax M3": (428, "https://huggingface.co/MiniMaxAI/MiniMax-M3"),
    "GLM-5.2": (744, GLM5_URL),
    "GLM-5.3": (744, GLM5_URL),
    "Mistral Large 3": (675, MISTRAL_L3_URL),
    "Mistral Large 2512": (675, MISTRAL_L3_URL),
    "Kimi K2.6": (1000, "https://huggingface.co/moonshotai/Kimi-K2.6"),
    "Llama 4 Maverick": (400, "https://huggingface.co/meta-llama/Llama-4-Maverick-17B-128E-Instruct"),
    # Fine-tuned from Z.ai's GLM-5.1, and fine-tuning keeps the parameter count.
    "ILMU GLM-5.1": (744, GLM5_URL),
}


def malaysian_runner_up():
    """Best Malaysian model on the leaderboard. Fails the build if it beats ours,
    so the '#1 Malaysian model' claim can't outlive the data behind it."""
    best = max((r for r in PENDAKWAH_LEADERBOARD if r[1] in MALAYSIAN_ORGS), key=lambda r: float(r[2]))
    assert float(MALAYMMLU["overall"]) > float(best[2]), (
        f"{best[0]} ({best[2]}) beats {MALAYMMLU['model']}: drop the '#1 Malaysian model' claim")
    return best


MY_TAG = '<span class="tag-my" title="Malaysian-built model">MY</span>'

# Size comparison with the runner-up Malaysian model. Memory is weights only at
# FP16 (2 bytes/param), the precision our MalayMMLU score was measured at.
MODEL_SIZE = {
    "ours_b": 27,
    "rival": "ILMU GLM-5.1",
    "rival_base": "GLM-5.1",
    "rival_b": MODEL_PARAMS["ILMU GLM-5.1"][0],
    "rival_source": GLM5_URL,
}
GPU_GB = 80


def size_facts():
    s = MODEL_SIZE
    ours_gb, rival_gb = s["ours_b"] * 2, s["rival_b"] * 2
    return {
        "ratio": round(s["rival_b"] / s["ours_b"]),
        "ours_gb": ours_gb,
        "rival_tb": f"{rival_gb / 1000:.1f}",
        "rival_gpus": -(-rival_gb // GPU_GB),
    }


def density_facts():
    """Intelligence density: MalayMMLU accuracy points per billion total parameters
    (what you must hold in memory to host it), over the models in the size chart.
    Fails the build if another model is denser, so the 'highest' claim can't go stale."""
    ours = float(MALAYMMLU["overall"]) / MODEL_SIZE["ours_b"]
    others = [(r[0], float(r[2]) / MODEL_PARAMS[r[0]][0])
              for r in PENDAKWAH_LEADERBOARD if r[0] in MODEL_PARAMS]
    next_name, next_d = max(others, key=lambda o: o[1])
    assert ours > next_d, f"{next_name} is denser than {MALAYMMLU['model']}: drop the 'highest density' claim"
    return {"ours": f"{ours:.1f}", "next": next_name, "next_d": f"{next_d:.2f}", "ratio": round(ours / next_d)}


def fmt_params(b):
    return f"{b / 1000:g}T" if b >= 1000 else f"{b:g}B"


def size_chart():
    """Static SVG scatter: total parameters (log x) vs MalayMMLU accuracy.
    Colours come from CSS classes so dark mode works; hover is in main.js."""
    import math
    pts = [(MALAYMMLU["model"], "Agmo Group &times; Sasbadi", MODEL_SIZE["ours_b"],
            float(MALAYMMLU["overall"]), "ours")]
    for r in PENDAKWAH_LEADERBOARD:
        if r[0] in MODEL_PARAMS:
            kind = "my" if r[1] in MALAYSIAN_ORGS else "other"
            pts.append((r[0], r[1], MODEL_PARAMS[r[0]][0], float(r[2]), kind))
    # Draw ours last so it sits on top.
    pts.sort(key=lambda p: p[4] == "ours")
    runner_up = malaysian_runner_up()
    my_names = ", ".join(p[0] for p in pts if p[4] == "my")
    gpu_max_b = GPU_GB // 2  # FP16: 2 bytes per parameter

    def render(compact):
        # Wide layout for desktop; compact one for phones keeps text legible
        # instead of scaling the wide chart down or scrolling it sideways.
        W, H, ML, MR, MT, MB = (400, 380, 40, 14, 36, 48) if compact else (720, 430, 56, 24, 36, 52)
        PW, PH = W - ML - MR, H - MT - MB
        X0, X1, Y0, Y1 = 10, 5000, 70, 90

        def x(b):
            return ML + (math.log10(b) - math.log10(X0)) / (math.log10(X1) - math.log10(X0)) * PW

        def y(a):
            return MT + (Y1 - a) / (Y1 - Y0) * PH

        grid = ""
        for a in range(Y0, Y1 + 1, 5):
            grid += (f'<line class="chart-grid" x1="{ML}" x2="{W - MR}" y1="{y(a):.1f}" y2="{y(a):.1f}"/>'
                     f'<text class="chart-tick" x="{ML - 8}" y="{y(a) + 4:.1f}" text-anchor="end">{a}</text>')
        for b in (10, 100, 1000):
            grid += (f'<line class="chart-grid" x1="{x(b):.1f}" x2="{x(b):.1f}" y1="{MT}" y2="{MT + PH}"/>'
                     f'<text class="chart-tick" x="{x(b):.1f}" y="{MT + PH + 18}" text-anchor="middle">{fmt_params(b)}</text>')

        band_lines = (["Fits one", f"{GPU_GB} GB GPU"] if compact
                      else [f"Fits one {GPU_GB} GB GPU", f"(up to {gpu_max_b}B)"])
        band = f'<rect class="chart-band" x="{ML}" y="{MT}" width="{x(gpu_max_b) - ML:.1f}" height="{PH}"/>'
        band += "".join(f'<text class="chart-band-label" x="{ML + 6}" y="{MT + 16 + 14 * i}">{t}</text>'
                        for i, t in enumerate(band_lines))

        marks = ""
        for name, org, b, acc, kind in pts:
            cx, cy = x(b), y(acc)
            tip = f"{acc:.1f}% &middot; {fmt_params(b)} parameters|{name} &middot; {org}"
            label = f"{name}, {org}: {acc:.1f}% MalayMMLU accuracy, {fmt_params(b)} parameters"
            r = 7 if kind == "ours" else 5
            marks += (f'<g class="chart-pt pt-{kind}" tabindex="0" role="img" aria-label="{label}" '
                      f'data-tip="{tip}"><circle class="chart-hit" cx="{cx:.1f}" cy="{cy:.1f}" r="12"/>'
                      f'<circle class="chart-dot" cx="{cx:.1f}" cy="{cy:.1f}" r="{r}"/></g>')

        # Selective direct labels: ours, plus the Malaysian runner-up where there's room.
        ox, oy = x(MODEL_SIZE["ours_b"]), y(float(MALAYMMLU["overall"]))
        ours_value = f'{MODEL_SIZE["ours_b"]}B &middot; {MALAYMMLU["overall"]}%'
        if compact:
            labels = (f'<text class="chart-label is-strong" x="{ox - 4:.1f}" y="{oy + 24:.1f}">{MALAYMMLU["model"]}</text>'
                      f'<text class="chart-label" x="{ox - 4:.1f}" y="{oy + 39:.1f}">{ours_value}</text>')
        else:
            rx, ry = x(MODEL_PARAMS[runner_up[0]][0]), y(float(runner_up[2]))
            labels = (f'<text class="chart-label is-strong" x="{ox + 14:.1f}" y="{oy - 2:.1f}">{MALAYMMLU["model"]}</text>'
                      f'<text class="chart-label" x="{ox + 14:.1f}" y="{oy + 14:.1f}">{ours_value}</text>'
                      f'<text class="chart-label" x="{rx - 12:.1f}" y="{ry + 4:.1f}" text-anchor="end">'
                      f'{runner_up[0]} &middot; {runner_up[2]}%</text>')

        axes = (f'<text class="chart-axis-title" x="{ML}" y="{MT - 14}">MalayMMLU accuracy (%)</text>'
                f'<text class="chart-axis-title" x="{ML + PW / 2:.1f}" y="{H - 8}" text-anchor="middle">'
                f'Total parameters (log scale)</text>')
        cls = "chart-compact" if compact else "chart-wide"
        return (f'<svg class="{cls}" viewBox="0 0 {W} {H}" role="group" '
                f'aria-label="Scatter chart of model size against MalayMMLU accuracy">'
                f'{band}{grid}{axes}{marks}{labels}</svg>')

    rows = "".join(
        f'<tr><th scope="row">{name}</th><td>{fmt_params(b)}</td>'
        f'<td>{acc:.1f}</td><td>' + (
            f'<a href="{MODEL_PARAMS[name][1]}" target="_blank" rel="noopener">Model card</a>'
            if name in MODEL_PARAMS else "Agmo Group") + '</td></tr>'
        for name, org, b, acc, kind in sorted(pts, key=lambda p: -p[3])
    )
    return f"""
      <figure class="size-chart">
        <figcaption>
          <strong>Intelligence density: model size vs MalayMMLU accuracy</strong>
          <span>Higher and further left means more accuracy per parameter. Only models whose developers publish a
          parameter count. Hover or tab to a point for details.</span>
        </figcaption>
        <ul class="chart-legend">
          <li><span class="key key-ours"></span>{MALAYMMLU['model']}</li>
          <li><span class="key key-my"></span>{my_names}</li>
          <li><span class="key key-other"></span>Other models</li>
        </ul>
        <div class="chart-scroll">
          {render(False)}
          {render(True)}
          <div class="chart-tip" hidden></div>
        </div>
        <details class="chart-data">
          <summary>Chart data and sources</summary>
          <div class="cmp-wrap">
            <table class="cmp-table">
              <thead><tr><th scope="col">Model</th><th scope="col">Parameters</th><th scope="col">MalayMMLU</th>
              <th scope="col">Size source</th></tr></thead>
              <tbody>{rows}</tbody>
            </table>
          </div>
          <p class="cmp-credit">ILMU GLM-5.1 is fine-tuned from Z.ai&rsquo;s GLM-5.1, so it has the same parameter
          count. Accuracy from the Pendakwah Teknologi leaderboard, except
          {MALAYMMLU['model']} (internal evaluation). Total parameters; mixture-of-experts models use only part of
          them per token but must hold all of them in memory.</p>
        </details>
      </figure>"""


def local_hosting_section():
    s, f, d = MODEL_SIZE, size_facts(), density_facts()
    runner_up = malaysian_runner_up()
    assert runner_up[0] == s["rival"], f"Runner-up is now {runner_up[0]}: update MODEL_SIZE"
    rows = [
        ("MalayMMLU accuracy", f"{MALAYMMLU['overall']}%", f"{runner_up[2]}%"),
        ("Parameters", f"{s['ours_b']}B", f"{s['rival_b']}B (mixture-of-experts)"),
        ("Memory for the weights", f"~{f['ours_gb']} GB", f"~{f['rival_tb']} TB"),
        ("Hardware to host it", f"One {GPU_GB} GB GPU",
         f"~{f['rival_gpus']} &times; {GPU_GB} GB GPUs"),
    ]
    body = "".join(
        f'<tr><th scope="row">{label}</th><td class="is-ours">{ours}</td><td>{rival}</td></tr>'
        for label, ours, rival in rows
    )
    return f"""
  <section id="local">
    <div class="container">
      <div class="section-head center">
        <span class="eyebrow">Sovereign by size</span>
        <h2>Small enough to host in a school</h2>
        <p>At {s['ours_b']}B parameters, {MALAYMMLU['model']} runs on a single GPU server, so a school can host
        it on its own premises. It has the highest intelligence density in our comparison: the most MalayMMLU
        accuracy per parameter.</p>
      </div>
      {size_chart()}
      <div class="cmp-wrap">
        <table class="cmp-table vs-table">
          <caption class="visually-hidden">{MALAYMMLU['model']} compared with {s['rival']} on size and hosting</caption>
          <thead><tr><th scope="col"><span class="visually-hidden">Measure</span></th>
          <th scope="col" class="is-ours">{MALAYMMLU['model']} {MY_TAG}</th>
          <th scope="col">{s['rival']} {MY_TAG}</th></tr></thead>
          <tbody>{body}</tbody>
        </table>
      </div>
      <div class="grid grid-3 mt-lg">
        <div class="card"><h3>Student data stays in school</h3><p>Questions, answers and student work never
        leave the school&rsquo;s own server: sovereign by design, and simpler for PDPA compliance.</p></div>
        <div class="card"><h3>Modest hardware</h3><p>One GPU server is enough, so a school or district can
        own its AI instead of renting it.</p></div>
        <div class="card"><h3>No dependence on outside clouds</h3><p>It runs on the school network, so
        lessons don&rsquo;t stop when the internet or an overseas provider does.</p></div>
      </div>
      <p class="cmp-credit">Memory and GPU counts are for the model weights alone. Scores from the
      <a href="#malaymmlu">MalayMMLU comparison</a> below.</p>
      <details class="cmp-method">
        <summary>How we sized it</summary>
        <ul>
          <li>Memory is for the model weights alone; running a model also needs some extra memory for the
          conversation itself.</li>
          <li>{s['rival']} is fine-tuned from Z.ai&rsquo;s {s['rival_base']}, and fine-tuning does not change a
          model&rsquo;s parameter count ({s['rival_b']}B per
          <a href="{s['rival_source']}" target="_blank" rel="noopener">Z.ai&rsquo;s GLM-5 repository</a>).</li>
          <li>A mixture-of-experts model uses only part of its parameters for each token, but all of them must be
          held in memory to serve it.</li>
          <li>Intelligence density is MalayMMLU accuracy divided by total parameters, in points per billion:
          {d['ours']} for {MALAYMMLU['model']}, about {d['ratio']} times the next-densest model in the chart,
          {d['next']} ({d['next_d']}). We use total parameters because they set the hardware you need to host a
          model; counted per active parameter, mixture-of-experts models score higher.</li>
        </ul>
      </details>
    </div>
  </section>"""


def malaymmlu_comparison():
    ours = (MALAYMMLU["model"], "Agmo Group &times; Sasbadi", MALAYMMLU["overall"],
            *(round(float(score)) for _, score in MALAYMMLU["categories"]))
    # Show the top frontier models as the reference and every Malaysian model
    # (backs the #1 claim). Other models that beat ours are named under the
    # table, never silently dropped; link out for the rest.
    ours_score = float(MALAYMMLU["overall"])
    top = PENDAKWAH_LEADERBOARD[:FRONTIER_SHOWN]
    shown = top + [r for r in PENDAKWAH_LEADERBOARD if r[1] in MALAYSIAN_ORGS and r not in top]
    hidden_above = [r for r in PENDAKWAH_LEADERBOARD if r not in shown and float(r[2]) > ours_score]
    above_note = ""
    if hidden_above:
        names = [r[0] for r in hidden_above]
        names = names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]
        lo, hi = min(r[2] for r in hidden_above), max(r[2] for r in hidden_above)
        span = lo if lo == hi else f"{lo} to {hi}"
        above_note = f" {names} also score above ours ({span}); the rest are on the"
    else:
        above_note = " The rest are on the"
    rows = sorted(shown + [ours], key=lambda r: float(r[2]), reverse=True)
    runner_up = malaysian_runner_up()
    body = ""
    for r in rows:
        is_ours = r is ours
        tag = (f" {MY_TAG}" if is_ours or r[1] in MALAYSIAN_ORGS else "")
        tag += ' <span class="tag-ours">Ours</span>' if is_ours else ""
        cls = ' class="is-ours"' if is_ours else ""
        cats = "".join(f"<td>{v}</td>" for v in r[3:])
        if is_ours:
            params = f"{MODEL_SIZE['ours_b']}B"
        elif r[0] in MODEL_PARAMS:
            params = fmt_params(MODEL_PARAMS[r[0]][0])
        else:
            params = '<span class="cmp-na">Undisclosed</span>'
        body += (f'<tr{cls}><th scope="row">{r[0]}{tag}<span class="cmp-org">{r[1]}</span></th>'
                 f'<td class="cmp-params">{params}</td><td class="cmp-overall">{r[2]}</td>{cats}</tr>')
    return f"""
  <section class="section-alt" id="malaymmlu">
    <div class="container">
      <div class="section-head center">
        <span class="eyebrow">#1 Malaysian model on MalayMMLU</span>
        <h2>How {MALAYMMLU['model']} compares</h2>
        <p>Accuracy (%) on MalayMMLU, the Malay-language knowledge benchmark. At {MALAYMMLU['overall']}%,
        {MALAYMMLU['model']} scores highest of the Malaysian-built models ({MY_TAG}) in this comparison and sits
        among frontier models from Google, OpenAI and Anthropic.</p>
      </div>
      <div class="cmp-wrap">
        <table class="cmp-table">
          <caption class="visually-hidden">MalayMMLU accuracy by model and category</caption>
          <thead><tr><th scope="col">Model</th><th scope="col">Parameters</th><th scope="col">Overall</th><th scope="col">STEM</th>
          <th scope="col">Language</th><th scope="col">Social science</th><th scope="col">Humanities</th>
          <th scope="col">Others</th></tr></thead>
          <tbody>{body}</tbody>
        </table>
      </div>
      <p class="cmp-more">Top {FRONTIER_SHOWN} leaderboard models and every Malaysian model shown.{above_note}
      <a href="{PENDAKWAH_URL}" target="_blank" rel="noopener">full leaderboard</a>.</p>
      <p class="cmp-credit">Source: <a href="{PENDAKWAH_URL}" target="_blank" rel="noopener">Pendakwah Teknologi</a>,
      {PENDAKWAH_RETRIEVED}. Ours is an internal evaluation.</p>
      <details class="cmp-method">
        <summary>How we compared</summary>
        <ul>
          <li>{MALAYMMLU['model']} was scored the same way as the leaderboard (generate-and-parse) on the full
          {MALAYMMLU['questions']}-question MalayMMLU set; the leaderboard samples 1,100 of these.</li>
          <li>It is not a leaderboard entry. Its category scores are rounded to match the leaderboard.</li>
          <li>&ldquo;#1 Malaysian model&rdquo; compares the Malaysian-built models in this table.</li>
          <li>MalayMMLU by Poh et al., UM &times; YTL AI Labs
          (<a href="{MALAYMMLU_PAPER_URL}" target="_blank" rel="noopener">Findings of EMNLP 2024</a>).</li>
        </ul>
      </details>
    </div>
  </section>"""


def malaymmlu_benchmark():
    rows = "".join(
        f'<tr><th scope="row">{name}</th>'
        f'<td><meter min="0" max="100" value="{score}">{score}%</meter></td>'
        f'<td class="bench-val">{score}%</td></tr>'
        for name, score in MALAYMMLU["categories"]
    )
    return f"""
        <div class="hub-bench">
          <div class="bench-score">
            <h5>MalayMMLU benchmark</h5>
            <p class="bench-num">{MALAYMMLU['overall']}%</p>
            <p class="bench-label">overall accuracy</p>
            <p class="bench-badge">#1 Malaysian model</p>
            <p class="bench-badge bench-badge-alt">{MODEL_SIZE['ours_b']}B &middot; runs on one GPU</p>
          </div>
          <table class="bench-table">
            <caption class="visually-hidden">{MALAYMMLU['model']} MalayMMLU accuracy by category</caption>
            <thead><tr><th scope="col">Category</th><th scope="col"><span class="visually-hidden">Bar</span></th><th scope="col">Accuracy</th></tr></thead>
            <tbody>{rows}</tbody>
          </table>
          <p class="bench-note">Internal evaluation, 26 August 2026, using
          <a href="{MALAYMMLU_PAPER_URL}" target="_blank" rel="noopener">MalayMMLU</a> (UM &times; YTL AI Labs,
          Findings of EMNLP 2024), the full set of {MALAYMMLU['questions']} multiple-choice questions across
          22 Malaysian school subjects. Overall accuracy is across all questions, so it weights each category by
          its size.
          <a href="#malaymmlu">See how it compares</a> &middot; <a href="#local">Why size matters</a>.</p>
        </div>"""


def small_powerful_section():
    """Homepage section: the size story, with the hub page's size chart."""
    s, d = MODEL_SIZE, density_facts()
    runner_up = malaysian_runner_up()
    assert runner_up[0] == s["rival"], f"Runner-up is now {runner_up[0]}: update MODEL_SIZE"
    tiles = [
        (f"{s['ours_b']}B", "parameters, compact enough to host on-premise"),
        (f"{MALAYMMLU['overall']}%", "on MalayMMLU, the highest of the Malaysian-built models"),
        (d["ours"], "MalayMMLU points per billion parameters, the highest intelligence density in our comparison"),
        ("1 GPU", f"to host it: a single {GPU_GB} GB GPU holds the weights"),
    ]
    tiles_html = "".join(
        f'<div class="stat-tile"><p class="stat-num">{num}</p><p class="stat-label">{label}</p></div>'
        for num, label in tiles
    )
    return f"""
  <section id="small">
    <div class="container">
      <div class="section-head center">
        <span class="eyebrow">Intelligence density</span>
        <h2>The #1 Malaysian model, small enough to run in a school</h2>
        <p>{MALAYMMLU['model']}, our Bahasa Malaysia model fine-tuned on Sasbadi&rsquo;s curriculum content, scores {MALAYMMLU['overall']}% on
        MalayMMLU. At {s['ours_b']}B parameters it can be hosted on-premise, so student data stays in the school.
        It delivers the most MalayMMLU accuracy per parameter of any model in our comparison.</p>
      </div>
      <div class="stat-tiles">{tiles_html}</div>
      {size_chart()}
      <div class="small-actions">
        <a class="btn btn-primary" href="/merdeka-model-llm/#local">Why size matters</a>
        <a class="btn btn-ghost" href="/merdeka-model-llm/#malaymmlu">Full MalayMMLU comparison</a>
      </div>
      <p class="cmp-credit">Source: <a href="{PENDAKWAH_URL}" target="_blank" rel="noopener">Pendakwah Teknologi</a>,
      {PENDAKWAH_RETRIEVED}. Ours is an internal evaluation.
      GPU count is for the model weights alone.</p>
    </div>
  </section>"""


# ---------------------------------------------------------------------------
# HOME
# ---------------------------------------------------------------------------
def build_home():
    s = MODEL_SIZE
    art = '<img src="/assets/images/hero-rocket.webp" alt="Illustration of a rocket launching, representing Merdeka LLM\'s growth" width="420" height="336">'
    body = hero(
        "Malaysia's Sovereign AI",
        "Malaysia&rsquo;s AI for a Sovereign and Empowered Future",
        "Empowering Malaysia through AI sovereignty by Agmo Group: data, hosting, and ownership in Malaysian hands.",
        actions=JOIN_BTN + '<a class="btn btn-ghost" href="#small">Small and powerful</a>',
        art=art,
        badges="".join(f'<span class="badge">{b}</span>' for b in (
            f"{s['ours_b']}B parameters",
            f"{MALAYMMLU['overall']}% on MalayMMLU",
            "#1 Malaysian model",
            "Runs on one GPU",
        )),
    )
    body += small_powerful_section()
    body += f"""
  <section>
    <div class="container">
      <div class="section-head center">
        <span class="eyebrow">What is Merdeka LLM?</span>
        <h2>Built by Malaysians, for Malaysia</h2>
        <p>Merdeka LLM is Malaysia&rsquo;s AI Large Language Model designed to safeguard our digital future.
        Built entirely by Malaysians, hosted in Malaysian data centres, and trained on local data, it ensures
        that Malaysia&rsquo;s voice is at the forefront of AI development, powered by Agmo Group.</p>
      </div>
      <div class="grid grid-3">
        <div class="card">
          <div class="card-icon">{ICONS['train']}</div>
          <h3>LLM Training as a Service (TaaS)</h3>
          <p>In partnership with Phison&rsquo;s aiDAPTIV+ and SNS, we offer scalable LLM training as a service,
          helping businesses unlock the power of AI for their own needs, from tailored language models to
          data management solutions.</p>
        </div>
        <div class="card">
          <div class="card-icon">{ICONS['gig']}</div>
          <h3>LLM Gig Economy (Curatorship)</h3>
          <p>Malaysia&rsquo;s first LLM Gig Economy Platform empowers Malaysians to participate in our AI&rsquo;s
          growth through curated contributions, ensuring high-quality data inputs that keep Merdeka LLM relevant,
          accurate, and reliable.</p>
        </div>
        <div class="card">
          <div class="card-icon">{ICONS['shield']}</div>
          <h3>AI Sovereignty as a Service</h3>
          <p>We empower enterprises and governments to achieve AI sovereignty with secure infrastructure, skilled
          talent, custom data solutions, and seamless deployment, keeping organisations in control of their
          AI systems and data.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section-alt">
    <div class="container">
      <div class="section-head center">
        <span class="eyebrow">Why Merdeka LLM</span>
        <h2>Built here, for the way Malaysia works</h2>
      </div>
      <div class="grid grid-3">
        <div class="card"><span class="num">01</span><h3>Sovereignty Focused</h3><p>Data privacy and security, with 100% Malaysian hosting and infrastructure.</p></div>
        <div class="card"><span class="num">02</span><h3>Built for Malaysians</h3><p>Tailored for Malaysian languages, cultures, and sectors while creating opportunities for Malaysians to contribute to AI development as data curators.</p></div>
        <div class="card"><span class="num">03</span><h3>LLM Training as a Service</h3><p>Leverage our partnerships with Phison&rsquo;s aiDAPTIV+ and SNS to train your own AI models with the highest data security standards.</p></div>      </div>
    </div>
  </section>

  <section>
    <div class="container">
      <div class="section-head center">
        <span class="eyebrow">Mission &amp; Vision</span>
        <h2>Where we&rsquo;re headed</h2>
      </div>
      <div class="split">
        <div class="panel">
          <h3>Mission</h3>
          <p>To lead Malaysia into the next digital age with a sovereign AI solution that empowers our industries,
          strengthens our data privacy, promotes innovation, and creates new opportunities for Malaysians through
          AI contributions and LLM training services.</p>
        </div>
        <div class="panel">
          <h3>Vision</h3>
          <p>A Malaysia where AI innovation thrives in full autonomy, protecting national interests while delivering
          cutting-edge solutions for businesses, government, and society with contributions from everyday
          Malaysians and strategic partnerships with leading AI and data infrastructure providers.</p>
        </div>
      </div>
    </div>
  </section>
"""
    body += contact_section()
    html_str = page_shell(
        title="Merdeka LLM",
        description=DEFAULT_DESCRIPTION,
        path="/",
        body=body,
        active_nav=None,
    )
    write_page("/", html_str)


# ---------------------------------------------------------------------------
# WHY SOVEREIGNTY MATTERS
# ---------------------------------------------------------------------------
def build_sovereignty():
    body = hero(
        "AI Sovereignty as a Service",
        "AI that keeps your data in Malaysia",
        "Agmo Group builds AI for your business on local data and hosts it in Malaysia, so your data stays in "
        "the country and you stay within local rules such as the PDPA.",
        actions=JOIN_BTN,
    )
    body += f"""
  <section>
    <div class="container">
      <div class="grid grid-3">
        <div class="card">
          <div class="card-icon">{ICONS['train']}</div>
          <h3>Fine-tuned AI Models</h3>
          <p>Models trained on Malaysian legal, HR and industry data, such as Malaysia Legal LLM and Malaysia HR
          LLM, to automate policy drafting, compliance checks and document review.</p>
        </div>
        <div class="card">
          <div class="card-icon">{ICONS['channels']}</div>
          <h3>AI Deployment Across Channels</h3>
          <p>Flexible deployment options:<br><strong>Public</strong> - reach customers on Facebook Messenger and
          WhatsApp.<br><strong>Private</strong> - secure internal communication via Microsoft Teams and Slack.<br>
          <strong>Custom</strong> - mobile apps, websites, and chatbots.</p>
        </div>
        <div class="card">
          <div class="card-icon">{ICONS['server']}</div>
          <h3>Infrastructure Hosted in Malaysia</h3>
          <p>Everything runs on servers in Malaysia, so customer and company data never leaves the country.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section-alt">
    <div class="container">
      <div class="section-head center">
        <span class="eyebrow">Why Sovereignty Matters</span>
        <h2>The importance of AI sovereignty for Malaysia</h2>
      </div>
      <div class="grid grid-3">
        <div class="card">
          <span class="num">01</span>
          <h3>Protecting National Interests</h3>
          <p>When Malaysia runs its own models, sensitive data stays in the country and out of foreign control.</p>
        </div>
        <div class="card">
          <span class="num">02</span>
          <h3>Economic Independence</h3>
          <p><strong>Job Creation:</strong> supports the gig economy, letting Malaysians contribute directly to AI
          development while earning income.<br><strong>Innovation and Growth:</strong> local AI development fosters
          innovation and new business opportunities.<br><strong>Reduced Dependency:</strong> less reliance on
          foreign technology, more self-reliance.</p>
        </div>
        <div class="card">
          <span class="num">03</span>
          <h3>Data Ownership</h3>
          <p><strong>Resource Control:</strong> Malaysians should control their own data, ensuring it&rsquo;s used
          ethically and for the country&rsquo;s benefit.<br><strong>Economic Value:</strong> owning and managing
          data locally unlocks significant economic value across sectors.</p>
        </div>
      </div>
    </div>
  </section>
"""
    body += contact_section()
    html_str = page_shell(
        title="Why Sovereignty Matters",
        description="Why AI sovereignty matters for Malaysia: national interests, economic independence and data ownership.",
        path="/why-sovereignty-matters/",
        body=body,
        active_nav="/why-sovereignty-matters/",
    )
    write_page("/why-sovereignty-matters/", html_str)


# ---------------------------------------------------------------------------
# MERDEKA MODEL HUB
# ---------------------------------------------------------------------------
def build_model_hub():
    def hub(num, title, applications, automations, benefit, soon=False,
            anchor=None, partner=None, benchmark="", callout="", actions=""):
        # soon=True shows "Coming soon"; a string shows that label instead.
        pill = f'<span class="pill">{soon if isinstance(soon, str) else "Coming soon"}</span>' if soon else ""
        id_attr = f' id="{anchor}"' if anchor else ""
        partner_html = f'<p class="hub-partner">{partner}</p>' if partner else ""
        link_html = f'<div class="hub-actions">{actions}</div>' if actions else ""
        return f"""
      <div class="hub-card"{id_attr}>
        <div class="hub-card-head">
          <div class="hub-num">{num}</div>
          <h3>{title}</h3>
          {pill}
        </div>
        {partner_html}
        <div class="hub-grid">
          <div class="hub-field"><h5>Applications</h5><p>{applications}</p></div>
          <div class="hub-field"><h5>Automations</h5><p>{automations}</p></div>
          <div class="hub-field"><h5>Key Benefit</h5><p>{benefit}</p></div>
        </div>
        {benchmark}
        {callout}
        {link_html}
      </div>"""

    body = hero(
        "Merdeka Model Hub",
        "Our Model Hub",
        "Merdeka LLM is a family of domain-specialised models, each fine-tuned with a partner who knows the "
        "field. Here are its real-world applications across Malaysia&rsquo;s priority sectors. Hold quality "
        "data in your field? Partner with us on the next model.",
        actions=JOIN_BTN,
    )
    body += '<section><div class="container">'
    body += hub(
        "01", "&#127891; Education: MerdekaLLM-Sasbadi-27b",
        "Personalised learning, curriculum development, and AI-driven tutoring platforms in both Malay and English.",
        "Merdeka LLM can create personalised learning experiences for students across Malaysia, while aiding educators in curriculum planning and delivering digital education tools.",
        "Tailored learning experiences, enhanced educational tools, and efficient education delivery.",
        anchor="education",
        partner="Fine-tuned for Malaysian education in partnership with <strong>Sasbadi</strong>. Trained on formal "
        "Bahasa Malaysia curriculum content, so it also suits agencies and organisations that write in formal BM.",
        benchmark=malaymmlu_benchmark(),
        actions='<a class="btn btn-primary" href="/#contact">Ask about this model</a>',
    )
    body += hub(
        "02", "&#9878;&#65039; Legal",
        "Contract review automation, legal research assistance, document summarisation, and legal compliance checks.",
        "Merdeka LLM can automate tedious legal tasks such as document drafting, contract reviews, and legal research, ensuring compliance with Malaysian laws and regulations.",
        "Increased legal department productivity, reduced manual workload, and enhanced accuracy in legal operations.",
        soon="New version coming soon",
        anchor="legal",
        callout=data_partner_callout(
            "legal", "law firms, legal publishers and professional bodies with quality Malaysian legal content"),
        actions=DATA_PARTNER_BTN,
    )
    body += hub(
        "03", "&#128101; Human Resources (HR)",
        "Automated resume screening, employee onboarding, compliance training, and performance evaluations.",
        "HR teams can leverage Merdeka LLM to automate key tasks such as resume filtering, employee evaluations, and regulatory compliance training, streamlining recruitment and management.",
        "Efficient hiring processes, improved employee engagement, and better overall HR operations with reduced human bias.",
        soon="New version coming soon",
        anchor="hr",
        callout=data_partner_callout(
            "HR", "HR consultancies, payroll and HRMS providers, and training bodies with quality Malaysian HR content"),
        actions=DATA_PARTNER_BTN,
    )
    body += hub(
        "04", "&#128176; Finance",
        "Tax advisory, tax planning, and automated customer service solutions.",
        "Leverage Merdeka LLM to streamline customer interactions, enhance security, and provide predictive financial insights, all while ensuring compliance with local regulations.",
        "Optimised operations, secure financial analysis, and enhanced customer experiences.",
        soon=True,
        anchor="finance",
        callout=data_partner_callout(
            "finance", "banks, tax advisory firms and financial publishers with quality Malaysian finance content"),
        actions=DATA_PARTNER_BTN,
    )
    body += '</div></section>'
    body += local_hosting_section()
    body += malaymmlu_comparison()
    body += contact_section()
    html_str = page_shell(
        title="Merdeka Model Hub",
        description="Real-world applications of Merdeka LLM across Legal, HR, Education, and Finance, including MerdekaLLM-Sasbadi-27b: the #1 Malaysian model on MalayMMLU, small enough at 27B parameters to host on-premise in a school.",
        path="/merdeka-model-llm/",
        body=body,
        active_nav="/merdeka-model-llm/",
    )
    write_page("/merdeka-model-llm/", html_str)


# ---------------------------------------------------------------------------
# LLM TRAINING AS A SERVICE  (reconstructed — live page was 404)
# ---------------------------------------------------------------------------
def build_taas():
    body = hero(
        "LLM Training as a Service",
        "Train Your Own AI, Backed by Malaysian Infrastructure",
        "In partnership with Phison&rsquo;s aiDAPTIV+ and SNS, Merdeka LLM offers scalable LLM training as a "
        "service while helping Malaysian enterprises unlock the power of AI for their own needs, from tailored "
        "language models to data management solutions.",
        actions=JOIN_BTN,
    )
    body += f"""
  <section>
    <div class="container">
      <div class="grid grid-3">
        <div class="card">
          <div class="card-icon">{ICONS['train']}</div>
          <h3>Tailored Model Training</h3>
          <p>Train or fine-tune language models on your own organisation&rsquo;s data, with Malaysian context,
          languages, and compliance requirements built in from the start.</p>
        </div>
        <div class="card">
          <div class="card-icon">{ICONS['server']}</div>
          <h3>Secure, Local Infrastructure</h3>
          <p>Training runs on infrastructure hosted in Malaysia, in partnership with Phison&rsquo;s aiDAPTIV+ and
          SNS, keeping sensitive training data under Malaysian data-sovereignty standards throughout.</p>
        </div>
        <div class="card">
          <div class="card-icon">{ICONS['shield']}</div>
          <h3>Data Management Solutions</h3>
          <p>From data cleaning and curation to secure storage, we help enterprises get their data training-ready
          without sacrificing security or compliance.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section-alt">
    <div class="container">
      <div class="section-head center">
        <span class="eyebrow">Who it&rsquo;s for</span>
        <h2>Built for Malaysia&rsquo;s enterprises</h2>
        <p>Need a model for your industry, or a pipeline that keeps training data compliant? We bring the
        infrastructure, so you don&rsquo;t have to build it.</p>
      </div>
    </div>
  </section>
"""
    body += contact_section()
    html_str = page_shell(
        title="LLM Training as a Service",
        description="Scalable LLM training as a service, in partnership with Phison's aiDAPTIV+ and SNS using cutting-edge AI training for Malaysia's enterprises.",
        path="/llm-training-as-a-service/",
        body=body,
        active_nav="/llm-training-as-a-service/",
    )
    write_page("/llm-training-as-a-service/", html_str)


# ---------------------------------------------------------------------------
# LLM GIG ECONOMY
# ---------------------------------------------------------------------------
def build_gig_economy():
    body = hero(
        "LLM Gig Economy",
        "Contribution and Curatorship",
        "Merdeka LLM is more than a sovereign AI solution: it&rsquo;s a platform for Malaysians to actively "
        "contribute to AI development. Through curated contributions, individuals help ensure the quality of the "
        "LLM while earning income in the gig economy as data curators.",
        actions=JOIN_BTN,
    )
    body += """
  <section>
    <div class="container">
      <div class="section-head center">
        <span class="eyebrow">How it works</span>
        <h2>Become a curator in three steps</h2>
        <p>We&rsquo;re developing a platform that allows Malaysians to become curators: reviewing, refining,
        and approving data used to train the LLM. This ensures high-quality data and opens up new opportunities in
        the gig economy.</p>
      </div>
      <div class="steps">
        <div class="step"><div class="step-num">1</div><h3>Sign up</h3><p>Sign up as a contributor or curator.</p></div>
        <div class="step"><div class="step-num">2</div><h3>Contribute</h3><p>Participate in data contribution and curation tasks (e.g. reviewing, tagging, cleaning datasets).</p></div>
        <div class="step"><div class="step-num">3</div><h3>Get paid</h3><p>Get paid for your contributions.</p></div>
      </div>
    </div>
  </section>

  <section class="section-alt">
    <div class="container">
      <div class="section-head center">
        <span class="eyebrow">Key Benefits</span>
        <h2>Why join the LLM Gig Economy</h2>
      </div>
      <div class="grid grid-3">
        <div class="card"><h3>Ensuring Data Quality</h3><p>Prevent &ldquo;garbage in, garbage out&rdquo; by curating relevant, accurate data.</p></div>
        <div class="card"><h3>Income Opportunities</h3><p>Earn money by contributing to Malaysia&rsquo;s AI future.</p></div>
        <div class="card"><h3>National Contribution</h3><p>Be part of the team that ensures Malaysia&rsquo;s AI is built for local needs and contexts.</p></div>
      </div>
      <div class="cta-row">
        <a class="btn btn-primary" href="/contributor/">Join as Contributor</a>
        <a class="btn btn-ghost" href="/curator/">Join as Curator</a>
      </div>
    </div>
  </section>
"""
    body += contact_section()
    html_str = page_shell(
        title="LLM Gig Economy",
        description="Malaysia's first LLM Gig Economy Platform: contribute and curate data, ensure AI quality, and earn income.",
        path="/llm-gig-economy/",
        body=body,
        active_nav="/llm-gig-economy/",
    )
    write_page("/llm-gig-economy/", html_str)


# ---------------------------------------------------------------------------
# CURATOR
# ---------------------------------------------------------------------------
def build_curator():
    body = hero(
        "Curatorship",
        "Curate Data. Shape AI. Empower Malaysia.",
        "Curators uphold the quality and integrity of Merdeka LLM, making sure only the most accurate, relevant "
        "data shapes Malaysia&rsquo;s AI future. Take part in Malaysia&rsquo;s first AI Gig Economy Platform and "
        "earn while ensuring AI excellence.",
        actions=JOIN_BTN + ' <a class="btn btn-ghost" href="/contributor/">Become a Contributor instead</a>',
    )
    body += """
  <section>
    <div class="container">
      <div class="section-head center">
        <span class="eyebrow">What it means to be a Curator</span>
        <h2>The curator&rsquo;s role</h2>
        <p>Curators play an essential role in safeguarding the quality of data used in Merdeka LLM. As a curator,
        you&rsquo;ll refine, review, and validate data contributions, maintaining the high standards necessary for
        Malaysia&rsquo;s premier LLM, validating data entries, ensuring adherence to Malaysia&rsquo;s unique
        context, and helping prevent inaccuracies.</p>
      </div>
      <div class="steps">
        <div class="step"><div class="step-num">1</div><h3>Register as a Curator</h3><p>Sign up and set up your profile.</p></div>
        <div class="step"><div class="step-num">2</div><h3>Participate in Data Curation</h3><p>Review, clean, and approve datasets before they&rsquo;re used for LLM training.</p></div>
        <div class="step"><div class="step-num">3</div><h3>Earn as You Curate</h3><p>Receive payment for your quality assurance efforts.</p></div>
      </div>
    </div>
  </section>

  <section class="section-alt">
    <div class="container">
      <div class="section-head center">
        <span class="eyebrow">Benefits of Curatorship</span>
        <h2>Why become a curator</h2>
      </div>
      <div class="grid grid-3">
        <div class="card"><h3>Income Generation</h3><p>Earn from data privacy and security-conscious work, with 100% Malaysian hosting and infrastructure.</p></div>
        <div class="card"><h3>Flexible Working Hours</h3><p>Participate as a curator on your own schedule.</p></div>
        <div class="card"><h3>Play a Key Role in AI Quality</h3><p>By ensuring high-quality data, you contribute to an AI model that reflects Malaysia&rsquo;s needs and values.</p></div>
      </div>
    </div>
  </section>
"""
    body += contact_section()
    html_str = page_shell(
        title="Become a Curator",
        description="Become a Merdeka LLM curator: review, refine and validate the data that shapes Malaysia's sovereign AI, and earn as you go.",
        path="/curator/",
        body=body,
        active_nav=None,
    )
    write_page("/curator/", html_str)


# ---------------------------------------------------------------------------
# CONTRIBUTOR
# ---------------------------------------------------------------------------
def build_contributor():
    body = hero(
        "Contribution",
        "Shape Malaysia&rsquo;s AI Future. Your Contributions, Our Sovereignty.",
        "Join Merdeka LLM as a Contributor and take an active role in Malaysia&rsquo;s AI journey. By participating "
        "in data collection and curation, you ensure Merdeka LLM remains accurate, relevant, and truly Malaysian.",
        actions=JOIN_BTN + ' <a class="btn btn-ghost" href="/curator/">Become a Curator instead</a>',
    )
    body += """
  <section>
    <div class="container">
      <div class="section-head center">
        <span class="eyebrow">About Merdeka LLM Contributions</span>
        <h2>The role of a Contributor</h2>
        <p>Contributors are the backbone of Merdeka LLM, playing a crucial role in supplying and refining data that
        powers Malaysia&rsquo;s AI. As a contributor, you&rsquo;ll provide essential data, review its quality, and
        ensure it reflects Malaysia&rsquo;s unique cultural, linguistic, and contextual nuances.</p>
      </div>
      <div class="steps">
        <div class="step"><div class="step-num">1</div><h3>Sign Up</h3><p>Data privacy and security first, with 100% Malaysian hosting and infrastructure.</p></div>
        <div class="step"><div class="step-num">2</div><h3>Participate in Data Collection</h3><p>Engage in tasks like collecting, reviewing, and annotating datasets.</p></div>
        <div class="step"><div class="step-num">3</div><h3>Earn as You Contribute</h3><p>Your contributions help shape Malaysia&rsquo;s AI, and you&rsquo;ll receive income for your efforts.</p></div>
      </div>
    </div>
  </section>

  <section class="section-alt">
    <div class="container">
      <div class="section-head center">
        <span class="eyebrow">Key Benefits</span>
        <h2>Why become a Contributor</h2>
      </div>
      <div class="grid grid-3">
        <div class="card"><h3>Be a Pioneer</h3><p>Data privacy and security-conscious work, with 100% Malaysian hosting and infrastructure.</p></div>
        <div class="card"><h3>Earn Income</h3><p>Supplement your earnings while supporting national AI development.</p></div>
        <div class="card"><h3>Skill Development</h3><p>Gain experience in AI and data curation, opening doors to future opportunities.</p></div>
      </div>
    </div>
  </section>
"""
    body += contact_section()
    html_str = page_shell(
        title="Become a Contributor",
        description="Join Merdeka LLM as a Contributor: supply and refine the data that powers Malaysia's sovereign AI, and earn as you contribute.",
        path="/contributor/",
        body=body,
        active_nav=None,
    )
    write_page("/contributor/", html_str)


# ---------------------------------------------------------------------------
# LEGAL PAGES
# ---------------------------------------------------------------------------
def legal_page(title, path, updated, body_inner):
    body = f"""
  <section>
    <div class="container legal-body">
      <h1>{title}</h1>
      <p class="legal-updated">Last updated: {updated}</p>
      {body_inner}
    </div>
  </section>
"""
    html_str = page_shell(
        title=title,
        description=f"{title} for Merdeka LLM by Agmo Group.",
        path=path,
        body=body,
        active_nav=None,
    )
    write_page(path, html_str)


def build_legal():
    legal_page("Privacy Policy", "/privacy-policy/", "7 October 2026", f"""
      <p>Agmo Group (&ldquo;we&rdquo;, &ldquo;us&rdquo;) operates {SITE_LINK} (&ldquo;the Site&rdquo;). This
      Privacy Policy explains what information we collect through the Site, how we use it, and the choices you
      have.</p>
      <h2>Information we collect</h2>
      <p>When you use our contact form, we collect the details you submit: first and last name, email address,
      phone number, and the topic you select. We do not collect payment information through this Site.</p>
      <h2>How we use your information</h2>
      <p>We use the information you provide solely to respond to your enquiry and to follow up about Merdeka LLM,
      AI Sovereignty as a Service, LLM Training as a Service, or the LLM Gig Economy / Curatorship programme,
      depending on the topic you selected.</p>
      <h2>Sharing</h2>
      <p>We do not sell your personal data. Form submissions are processed by our form provider (Formspree) solely
      to deliver your enquiry to us, and are not used by them for any other purpose.</p>
      <h2>Your rights</h2>
      <p>You may ask us to access, correct, or delete the information you&rsquo;ve submitted at any time by
      emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
      <h2>Contact</h2>
      <p>Questions about this policy can be sent to <a href="mailto:{EMAIL}">{EMAIL}</a> or {PHONE}.</p>
    """)

    legal_page("Terms &amp; Conditions", "/terms-and-conditions/", "22 May 2026", f"""
      <p>These Terms &amp; Conditions (&ldquo;T&amp;C&rdquo;) govern your use of {SITE_LINK}, operated by Agmo
      Group. By using the Site, you agree to these terms.</p>
      <h2>Use of the Site</h2>
      <p>The Site provides information about Merdeka LLM, AI Sovereignty as a Service, LLM Training as a Service,
      and the LLM Gig Economy / Curatorship programme. Content is provided for informational purposes and may be
      updated as our services evolve.</p>
      <h2>Enquiries and engagements</h2>
      <p>Submitting the contact form does not create a binding commercial agreement. Specific commercial terms for
      LLM Training as a Service, curatorship, or contributor arrangements are agreed separately in writing.</p>
      <h2>Intellectual property</h2>
      <p>All content on this Site, including the Merdeka LLM name and branding, belongs to Agmo Group unless
      otherwise stated.</p>
      <h2>Changes</h2>
      <p>We may update these Terms from time to time; the &ldquo;last updated&rdquo; date above reflects the most
      recent revision.</p>
      <h2>Contact</h2>
      <p>Questions can be sent to <a href="mailto:{EMAIL}">{EMAIL}</a> or {PHONE}.</p>
    """)

    legal_page("Refund Policy", "/refund-policy/", "22 May 2026", f"""
      <p>This Refund Policy applies to paid engagements arranged through {SITE_LINK} with Agmo Group, such as LLM
      Training as a Service engagements.</p>
      <h2>Commercial services</h2>
      <p>Refunds for LLM Training as a Service or other paid engagements are governed by the specific commercial
      agreement signed for that engagement. Where no separate agreement specifies otherwise, refund requests are
      assessed case-by-case, based on work already performed.</p>
      <h2>Gig Economy payouts</h2>
      <p>Curator and contributor payouts are made for completed, approved work and are not refundable once paid.</p>
      <h2>How to request a refund</h2>
      <p>Email <a href="mailto:{EMAIL}">{EMAIL}</a> with your engagement details and the reason for your request.</p>
    """)

    legal_page("Accessibility Statement", "/accessibility-statement/", "22 May 2026", f"""
      <p>Agmo Group is working to make {SITE_LINK} accessible to people with disabilities.</p>
      <h2>Accessibility on this site</h2>
      <p>We aim to align this Site with WCAG 2.1 AA guidelines. This includes a semantic heading structure on every
      page, a skip-to-content link, keyboard-navigable menus and forms, visible focus states, alternative text on
      meaningful images, and colour combinations chosen to meet contrast requirements.</p>
      <h2>Requests, issues, and suggestions</h2>
      <p>If you find an accessibility issue on the Site, or need further assistance, please contact us:</p>
      <p>Agmo Group &middot; <a href="mailto:{EMAIL}">{EMAIL}</a> &middot; {PHONE}</p>
    """)


SITE_LINK = '<a href="/">merdekallm.com</a>'


# ---------------------------------------------------------------------------
# 404
# ---------------------------------------------------------------------------
def build_404():
    body = """
  <div class="error-page">
    <div class="code">404</div>
    <h1>This page isn&rsquo;t available</h1>
    <p>The page you&rsquo;re looking for may have moved. Try the homepage.</p>
    <a class="btn btn-primary" href="/">Go to Homepage</a>
  </div>
"""
    html_str = page_shell(
        title="Page Not Found",
        description="This page isn't available.",
        path="/404.html",
        body=body,
        active_nav=None,
        noindex=True,
    )
    out = os.path.join(PUBLISH_DIR, "404.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html_str)
    print("wrote 404.html")


# ---------------------------------------------------------------------------
# BLOG
# ---------------------------------------------------------------------------
def last_modified(path):
    """Date a source file last changed: today if it has uncommitted edits,
    otherwise its last commit date. None if git isn't available."""
    import datetime as dt
    rel = os.path.relpath(path, ROOT)
    try:
        dirty = subprocess.run(["git", "status", "--porcelain", "--", rel], cwd=ROOT,
                               capture_output=True, text=True, check=True).stdout.strip()
        if dirty:
            return dt.date.today().isoformat()
        return subprocess.run(["git", "log", "-1", "--format=%cs", "--", rel], cwd=ROOT,
                              capture_output=True, text=True, check=True).stdout.strip() or None
    except (OSError, subprocess.CalledProcessError):
        return None


def load_posts():
    posts = []
    for path in sorted(glob.glob(os.path.join(ROOT, "content-source", "*.md"))):
        slug = os.path.splitext(os.path.basename(path))[0]
        with open(path, encoding="utf-8") as f:
            raw = f.read()
        fm, body_md = parse_frontmatter(raw)
        first_para_match = re.search(r"<p>(.*?)</p>", markdown_to_html(body_md))
        excerpt = re.sub("<[^>]+>", "", first_para_match.group(1)) if first_para_match else ""
        posts.append({
            "slug": slug,
            "title": fm.get("title", slug),
            "author": fm.get("author", "Aik Keong Tan"),
            "date": fm.get("date", "2024-11-01"),
            "readtime": fm.get("readtime", "4 min read"),
            "modified": last_modified(path) or fm.get("date", "2024-11-01"),
            "body_html": markdown_to_html(body_md),
            "excerpt": (excerpt[:180] + "…") if len(excerpt) > 180 else excerpt,
        })
    return posts


def pretty_date(iso):
    import datetime as dt
    try:
        return dt.datetime.strptime(iso, "%Y-%m-%d").strftime("%b %-d, %Y")
    except Exception:
        try:
            return dt.datetime.strptime(iso, "%Y-%m-%d").strftime("%b %d, %Y").replace(" 0", " ")
        except Exception:
            return iso


def build_blog(posts):
    cards = []
    for p in posts:
        cards.append(f"""
        <a class="post-card" href="/post/{p['slug']}/">
          <div class="post-meta">{pretty_date(p['date'])} &middot; {p['readtime']}</div>
          <h3>{p['title']}</h3>
          <p>{p['excerpt']}</p>
        </a>""")
    body = hero(
        "Blog",
        "Insights on Malaysia&rsquo;s AI Journey",
        "Perspectives on AI sovereignty, governance, and Malaysia&rsquo;s growing generative AI landscape.",
    )
    body += f"""
  <section>
    <div class="container">
      <div class="post-list">
        {''.join(cards)}
      </div>
    </div>
  </section>
"""
    body += contact_section()
    html_str = page_shell(
        title="Blog",
        description="Insights on Malaysia's AI sovereignty, governance, and generative AI landscape from Merdeka LLM by Agmo Group.",
        path="/blog/",
        body=body,
        active_nav="/blog/",
    )
    write_page("/blog/", html_str)


def build_post(p):
    post_url = f"/post/{p['slug']}/"
    body = f"""
  <section>
    <div class="container post-article">
      <a class="back-link" href="/blog/">&larr; All Posts</a>
      <article>
        <h1>{p['title']}</h1>
        <div class="post-meta">
          <span itemscope itemtype="https://schema.org/Person">{p['author']}</span>
          &middot; <time datetime="{p['date']}">{pretty_date(p['date'])}</time>
          &middot; {p['readtime']}
        </div>
        <div class="post-body">
          {p['body_html']}
        </div>
      </article>
      <p class="mt-lg"><a class="back-link" href="/blog/">&larr; Back to all posts</a></p>
    </div>
  </section>
"""
    blog_posting = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "@id": f"{BASE_URL}{post_url}#article",
        "headline": p["title"],
        "description": p["excerpt"] or DEFAULT_DESCRIPTION,
        "datePublished": p["date"],
        "dateModified": p["date"],
        "author": {"@type": "Person", "name": p["author"]},
        "publisher": {"@id": f"{BASE_URL}/#organization"},
        "mainEntityOfPage": {"@type": "WebPage", "@id": f"{BASE_URL}{post_url}"},
        "image": OG_IMAGE,
        "url": f"{BASE_URL}{post_url}",
        "inLanguage": "en",
    }
    html_str = page_shell(
        title=p["title"],
        description=p["excerpt"] or DEFAULT_DESCRIPTION,
        path=post_url,
        body=body,
        active_nav="/blog/",
        page_type="article",
        breadcrumbs=[("Home", "/"), ("Blog", "/blog/"), (p["title"], post_url)],
        extra_jsonld=[blog_posting],
    )
    write_page(post_url, html_str)


STATIC_PATHS = [
    "/", "/why-sovereignty-matters/", "/merdeka-model-llm/",
    "/llm-training-as-a-service/", "/llm-gig-economy/", "/curator/",
    "/contributor/", "/blog/", "/privacy-policy/", "/terms-and-conditions/",
    "/refund-policy/", "/accessibility-statement/",
]


def build_sitemap(posts):
    import datetime as dt
    # Static page bodies all live in pages_content.py, so they share its date.
    # Template-only changes in build.py deliberately don't bump lastmod.
    static_date = last_modified(os.path.join(ROOT, "pages_content.py")) or dt.date.today().isoformat()
    lastmod = {u: static_date for u in STATIC_PATHS}
    for p in posts:
        lastmod[f"/post/{p['slug']}/"] = p["modified"]
    lastmod["/blog/"] = max([static_date] + [p["modified"] for p in posts])
    urls = list(STATIC_PATHS) + [f"/post/{p['slug']}/" for p in posts]
    # Real content images (favicon/decorative shapes excluded) — image sitemap
    # entries help these get (re-)indexed under the new domain for image search.
    page_images = {
        "/": [(f"{BASE_URL}/assets/images/hero-rocket.webp", "Merdeka LLM: rocket illustration representing Malaysia's AI growth")],
    }
    entries = []
    for u in urls:
        imgs = page_images.get(u, [])
        img_tags = "".join(
            f"\n    <image:image><image:loc>{src}</image:loc><image:title>{html.escape(title, quote=True)}</image:title></image:image>"
            for src, title in imgs
        )
        entries.append(f"  <url>\n    <loc>{BASE_URL}{u}</loc>\n    <lastmod>{lastmod[u]}</lastmod>{img_tags}\n  </url>")
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
        + "\n".join(entries) + "\n</urlset>\n"
    )
    with open(os.path.join(PUBLISH_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(xml)
    print("wrote sitemap.xml")


def build_llms_txt(posts):
    lines = [
        f"# {SITE_NAME}",
        "",
        "> Malaysia's sovereign AI Large Language Model and AI Sovereignty as a Service platform, built by "
        "Malaysians, hosted in Malaysian data centres, trained on local data. Powered by Agmo Group.",
        "",
        f"{SITE_NAME} by Agmo Group offers AI Sovereignty as a Service, LLM Training as a Service (with Phison's "
        "aiDAPTIV+ and SNS), and the LLM Gig Economy, a curatorship/contributor platform for Malaysians to help "
        "train Malaysia's own AI.",
        "",
        "## Pages",
        "",
        f"- [{SITE_NAME}]({BASE_URL}/): Malaysia's AI for a Sovereign and Empowered Future. Small and powerful: {MALAYMMLU['model']} has {MODEL_SIZE['ours_b']}B parameters, scores {MALAYMMLU['overall']}% on MalayMMLU (internal evaluation, the highest of the Malaysian-built models in our comparison) and runs on one GPU. Its intelligence density, {density_facts()['ours']} MalayMMLU points per billion total parameters, is the highest in our comparison",
        f"- [Why Sovereignty Matters]({BASE_URL}/why-sovereignty-matters/): AI that keeps your data in Malaysia, hosted on Malaysian infrastructure",
        f"- [Merdeka Model Hub]({BASE_URL}/merdeka-model-llm/): Real-world applications of Merdeka LLM across Legal, HR, Education, and Finance, including the education model MerdekaLLM-Sasbadi-27b (built with Sasbadi; {MALAYMMLU['overall']}% on MalayMMLU, internal evaluation, the highest of the Malaysian-built models in our comparison against the Pendakwah Teknologi leaderboard, at 27B parameters, so it can be hosted on-premise on one GPU; the highest intelligence density, or MalayMMLU accuracy per parameter, in our comparison). New versions of the Legal and HR models are coming soon; Merdeka LLM invites data partners in legal, HR and finance",
        f"- [LLM Training as a Service]({BASE_URL}/llm-training-as-a-service/): Scalable LLM training, in partnership with Phison's aiDAPTIV+ and SNS",
        f"- [LLM Gig Economy]({BASE_URL}/llm-gig-economy/): Contribution and curatorship platform for Malaysians",
        f"- [Become a Curator]({BASE_URL}/curator/): Review, refine, and validate data used to train Merdeka LLM",
        f"- [Become a Contributor]({BASE_URL}/contributor/): Supply and refine the data that powers Merdeka LLM",
        "",
        "## Blog",
        "",
    ]
    for p in posts:
        lines.append(f"- [{p['title']}]({BASE_URL}/post/{p['slug']}/): {p['excerpt']}")
    lines += [
        "",
        "## Legal",
        "",
        f"- [Privacy Policy]({BASE_URL}/privacy-policy/)",
        f"- [Terms & Conditions]({BASE_URL}/terms-and-conditions/)",
        f"- [Refund Policy]({BASE_URL}/refund-policy/)",
        f"- [Accessibility Statement]({BASE_URL}/accessibility-statement/)",
        "",
    ]
    with open(os.path.join(PUBLISH_DIR, "llms.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("wrote llms.txt")


# ---------------------------------------------------------------------------
def build_all():
    build_home()
    build_sovereignty()
    build_model_hub()
    build_taas()
    build_gig_economy()
    build_curator()
    build_contributor()
    build_legal()
    build_404()
    posts = load_posts()
    build_blog(posts)
    for p in posts:
        build_post(p)
    build_sitemap(posts)
    build_llms_txt(posts)
    print(f"\nBuilt {9 + len(posts)} pages ({len(posts)} blog posts).")
