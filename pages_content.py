"""Page content/body HTML for the Merdeka LLM static site."""
import os
import re
import glob
import html
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


def hero(eyebrow, title, lede, actions="", art=""):
    return f"""
  <section class="hero">
    <div class="container hero-grid">
      <div>
        <span class="eyebrow">{eyebrow}</span>
        <h1>{title}</h1>
        <p class="lede">{lede}</p>
        <div class="hero-actions">{actions}</div>
      </div>
      <div class="hero-art">{art}</div>
    </div>
  </section>"""


JOIN_BTN = '<a class="btn btn-primary" href="/#contact">Join the AI Revolution</a>'


# ---------------------------------------------------------------------------
# HOME
# ---------------------------------------------------------------------------
def build_home():
    art = '<img src="/assets/images/hero-rocket.gif" alt="Illustration of a rocket launching, representing Merdeka LLM\'s growth" width="420">'
    body = hero(
        "Malaysia's Sovereign AI",
        "Malaysia&rsquo;s AI for a Sovereign and Empowered Future",
        "Empowering Malaysia through AI sovereignty by Agmo Group — data, hosting, and ownership in Malaysian hands.",
        actions=JOIN_BTN,
        art=art,
    )
    body += f"""
  <section>
    <div class="container">
      <div class="section-head center">
        <span class="eyebrow">What is Merdeka LLM?</span>
        <h2>Built by Malaysians, for Malaysia</h2>
        <p>Merdeka LLM is Malaysia&rsquo;s AI Large Language Model designed to safeguard our digital future.
        Built entirely by Malaysians, hosted in Malaysian data centers, and trained on local data, it ensures
        that Malaysia&rsquo;s voice is at the forefront of AI development, powered by Agmo Group.</p>
      </div>
      <div class="grid grid-3">
        <div class="card">
          <div class="card-icon">{ICONS['train']}</div>
          <h3>LLM Training as a Service (TaaS)</h3>
          <p>In partnership with Phison&rsquo;s aiDAPTIV+ and SNS, we offer scalable LLM training as a service,
          helping businesses unlock the power of AI for their own needs &mdash; from tailored language models to
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
          talent, custom data solutions, and seamless deployment &mdash; keeping organizations in control of their
          AI systems and data.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="section-alt">
    <div class="container">
      <div class="section-head center">
        <span class="eyebrow">Key Highlights</span>
        <h2>Leading the AI academy world &mdash; without forgetting where we came from</h2>
      </div>
      <div class="grid grid-3">
        <div class="card"><span class="num">01</span><h3>Sovereignty Focused</h3><p>Data privacy and security, with 100% Malaysian hosting and infrastructure.</p></div>
        <div class="card"><span class="num">02</span><h3>Built for Malaysians</h3><p>Tailored for Malaysian languages, cultures, and sectors &mdash; creating opportunities for Malaysians to contribute to AI development as data curators.</p></div>
        <div class="card"><span class="num">03</span><h3>LLM Training as a Service</h3><p>Leverage our partnerships with Phison&rsquo;s aiDAPTIV+ and SNS to train your own AI models with the highest data security standards.</p></div>
        <div class="card"><span class="num">04</span><h3>State-of-the-Art AI</h3><p>High performance, efficiency, and scalability for real-world applications.</p></div>
      </div>
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
          cutting-edge solutions for businesses, government, and society &mdash; with contributions from everyday
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
        "Empower Your Business with Localized AI Solutions",
        "Agmo Group enables businesses to leverage AI solutions powered by locally sourced data and hosted "
        "within Malaysia&rsquo;s secure infrastructure &mdash; keeping your data within national borders, with "
        "enhanced security and compliance with local regulations.",
        actions=JOIN_BTN,
    )
    body += f"""
  <section>
    <div class="container">
      <div class="grid grid-3">
        <div class="card">
          <div class="card-icon">{ICONS['train']}</div>
          <h3>Finetuned AI Models</h3>
          <p>Tailored AI models built on Malaysian legal, HR, and industry-specific datasets &mdash; such as the
          Malaysia Legal LLM and Malaysia HR LLM &mdash; to automate processes like policy development, compliance,
          and document review.</p>
        </div>
        <div class="card">
          <div class="card-icon">{ICONS['channels']}</div>
          <h3>AI Deployment Across Channels</h3>
          <p>Flexible deployment options: <strong>Public</strong> &mdash; reach customers on Facebook Messenger and
          WhatsApp. <strong>Private</strong> &mdash; secure internal communication via Microsoft Teams and Slack.
          <strong>Custom</strong> &mdash; mobile apps, websites, and chatbots.</p>
        </div>
        <div class="card">
          <div class="card-icon">{ICONS['server']}</div>
          <h3>Infrastructure Hosted in Malaysia</h3>
          <p>Ensure data sovereignty with AI solutions self-hosted within Malaysia, safeguarding customer privacy
          and organizational data.</p>
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
          <p>By developing and maintaining our own AI models, Malaysia can safeguard its data from foreign control
          or misuse &mdash; keeping sensitive information within the country and protecting national security and
          privacy.</p>
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
        description="Why AI sovereignty matters for Malaysia — protecting national interests, economic independence, and data ownership.",
        path="/why-sovereignty-matters/",
        body=body,
        active_nav="/why-sovereignty-matters/",
    )
    write_page("/why-sovereignty-matters/", html_str)


# ---------------------------------------------------------------------------
# MERDEKA MODEL HUB
# ---------------------------------------------------------------------------
def build_model_hub():
    def hub(num, title, applications, automations, benefit, demo_url=None, model_url=None, soon=False):
        pill = '<span class="pill">Coming soon</span>' if soon else ""
        link_html = ""
        if demo_url or model_url:
            buttons = []
            if demo_url:
                buttons.append(f'<a class="btn btn-primary" href="{demo_url}" target="_blank" rel="noopener">Try the Demo</a>')
            if model_url:
                buttons.append(f'<a class="btn btn-ghost" href="{model_url}" target="_blank" rel="noopener">View Model Card on Hugging Face</a>')
            link_html = f'<div class="hub-actions">{"".join(buttons)}</div>'
        return f"""
      <div class="hub-card">
        <div class="hub-card-head">
          <div class="hub-num">{num}</div>
          <h3>{title}</h3>
          {pill}
        </div>
        <div class="hub-grid">
          <div class="hub-field"><h5>Applications</h5><p>{applications}</p></div>
          <div class="hub-field"><h5>Automations</h5><p>{automations}</p></div>
          <div class="hub-field"><h5>Key Benefit</h5><p>{benefit}</p></div>
        </div>
        {link_html}
      </div>"""

    body = hero(
        "Merdeka Model Hub",
        "Our Model Hub",
        "Real-world applications of Merdeka LLM across Malaysia&rsquo;s priority sectors.",
        actions=JOIN_BTN,
    )
    body += '<section><div class="container">'
    body += hub(
        "01", "&#9878;&#65039; Legal",
        "Contract review automation, legal research assistance, document summarization, and legal compliance checks.",
        "Merdeka LLM can automate tedious legal tasks such as document drafting, contract reviews, and legal research, ensuring compliance with Malaysian laws and regulations.",
        "Increased legal department productivity, reduced manual workload, and enhanced accuracy in legal operations.",
        demo_url="https://huggingface.co/spaces/Merdeka-LLM/merdeka-llm-lawyer-demo-chat-app",
        model_url="https://huggingface.co/Merdeka-LLM/merdeka-llm-lawyer-3b-128k-instruct",
    )
    body += hub(
        "02", "&#128101; Human Resources (HR)",
        "Automated resume screening, employee onboarding, compliance training, and performance evaluations.",
        "HR teams can leverage Merdeka LLM to automate key tasks such as resume filtering, employee evaluations, and regulatory compliance training, streamlining recruitment and management.",
        "Efficient hiring processes, improved employee engagement, and better overall HR operations with reduced human bias.",
        demo_url="https://huggingface.co/spaces/Merdeka-LLM/merdeka-llm-hr-demo-chat-app",
        model_url="https://huggingface.co/Merdeka-LLM/merdeka-llm-hr-3b-128k-instruct",
    )
    body += hub(
        "03", "&#127891; Education",
        "Personalized learning, curriculum development, and AI-driven tutoring platforms in both Malay and English.",
        "Merdeka LLM can create personalized learning experiences for students across Malaysia, while aiding educators in curriculum planning and delivering digital education tools.",
        "Tailored learning experiences, enhanced educational tools, and efficient education delivery.",
        soon=True,
    )
    body += hub(
        "04", "&#128176; Finance",
        "Tax advisory, tax planning, and automated customer service solutions.",
        "Leverage Merdeka LLM to streamline customer interactions, enhance security, and provide predictive financial insights, all while ensuring compliance with local regulations.",
        "Optimized operations, secure financial analysis, and enhanced customer experiences.",
        soon=True,
    )
    body += '</div></section>'
    body += contact_section()
    html_str = page_shell(
        title="Merdeka Model Hub",
        description="Real-world applications of Merdeka LLM across Legal, HR, Education, and Finance.",
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
        "service &mdash; helping Malaysian enterprises unlock the power of AI for their own needs, from tailored "
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
          <p>Train or fine-tune language models on your own organization&rsquo;s data, with Malaysian context,
          languages, and compliance requirements built in from the start.</p>
        </div>
        <div class="card">
          <div class="card-icon">{ICONS['server']}</div>
          <h3>Secure, Local Infrastructure</h3>
          <p>Training runs on infrastructure hosted in Malaysia, in partnership with Phison&rsquo;s aiDAPTIV+ and
          SNS &mdash; keeping sensitive training data under Malaysian data-sovereignty standards throughout.</p>
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
        <p>Whether you need a language model tailored to your industry, or a data management pipeline that keeps
        training data compliant and secure, our LLM Training as a Service gives Malaysian businesses a practical
        path to their own sovereign AI &mdash; without building infrastructure from scratch.</p>
      </div>
    </div>
  </section>
"""
    body += contact_section()
    html_str = page_shell(
        title="LLM Training as a Service",
        description="Scalable LLM training as a service, in partnership with Phison's aiDAPTIV+ and SNS — cutting-edge AI training for Malaysia's enterprises.",
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
        "Merdeka LLM is more than a sovereign AI solution &mdash; it&rsquo;s a platform for Malaysians to actively "
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
        <p>We&rsquo;re developing a platform that allows Malaysians to become curators &mdash; reviewing, refining,
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
        description="Malaysia's first LLM Gig Economy Platform — contribute and curate data, ensure AI quality, and earn income.",
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
        Malaysia&rsquo;s premier LLM &mdash; validating data entries, ensuring adherence to Malaysia&rsquo;s unique
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
        <div class="card"><h3>Income Generation</h3><p>Earn from data privacy- and security-conscious work, with 100% Malaysian hosting and infrastructure.</p></div>
        <div class="card"><h3>Flexible Working Hours</h3><p>Participate as a curator on your own schedule.</p></div>
        <div class="card"><h3>Play a Key Role in AI Quality</h3><p>By ensuring high-quality data, you contribute to an AI model that reflects Malaysia&rsquo;s needs and values.</p></div>
      </div>
    </div>
  </section>
"""
    body += contact_section()
    html_str = page_shell(
        title="Become a Curator",
        description="Become a Merdeka LLM curator — review, refine, and validate the data that shapes Malaysia's sovereign AI, and earn as you go.",
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
        description="Join Merdeka LLM as a Contributor — supply and refine the data that powers Malaysia's sovereign AI, and earn as you contribute.",
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
    legal_page("Privacy Policy", "/privacy-policy/", "22 May 2026", f"""
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
      <h2>What web accessibility is</h2>
      <p>An accessible site allows visitors with disabilities to browse the site with the same or a similar level
      of ease and enjoyment as other visitors, achieved through the capabilities of the system the site runs on and
      through assistive technologies.</p>
      <h2>Accessibility on this site</h2>
      <p>We aim to align this Site with WCAG 2.1 AA guidelines. This includes a semantic heading structure on every
      page, a skip-to-content link, keyboard-navigable menus and forms, visible focus states, alternative text on
      meaningful images, and color combinations chosen to meet contrast requirements.</p>
      <h2>Requests, issues, and suggestions</h2>
      <p>If you find an accessibility issue on the Site, or need further assistance, please contact us:</p>
      <p>Agmo Group &mdash; <a href="mailto:{EMAIL}">{EMAIL}</a> &mdash; {PHONE}</p>
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
    <p>The page you&rsquo;re looking for may have moved. Try the
    homepage, or explore Merdeka LLM below.</p>
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
    today = dt.date.today().isoformat()
    urls = list(STATIC_PATHS) + [f"/post/{p['slug']}/" for p in posts]
    # Real content images (favicon/decorative shapes excluded) — image sitemap
    # entries help these get (re-)indexed under the new domain for image search.
    page_images = {
        "/": [(f"{BASE_URL}/assets/images/hero-rocket.gif", "Merdeka LLM — rocket illustration representing Malaysia's AI growth")],
    }
    entries = []
    for u in urls:
        imgs = page_images.get(u, [])
        img_tags = "".join(
            f"\n    <image:image><image:loc>{src}</image:loc><image:title>{html.escape(title, quote=True)}</image:title></image:image>"
            for src, title in imgs
        )
        entries.append(f"  <url>\n    <loc>{BASE_URL}{u}</loc>\n    <lastmod>{today}</lastmod>{img_tags}\n  </url>")
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
        "Malaysians, hosted in Malaysian data centers, trained on local data. Powered by Agmo Group.",
        "",
        f"{SITE_NAME} by Agmo Group offers AI Sovereignty as a Service, LLM Training as a Service (with Phison's "
        "aiDAPTIV+ and SNS), and the LLM Gig Economy — a curatorship/contributor platform for Malaysians to help "
        "train Malaysia's own AI.",
        "",
        "## Pages",
        "",
        f"- [{SITE_NAME}]({BASE_URL}/): Malaysia's AI for a Sovereign and Empowered Future",
        f"- [Why Sovereignty Matters]({BASE_URL}/why-sovereignty-matters/): AI Sovereignty as a Service — localized, Malaysia-hosted AI solutions",
        f"- [Merdeka Model Hub]({BASE_URL}/merdeka-model-llm/): Real-world applications of Merdeka LLM across Legal, HR, Education, and Finance",
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
