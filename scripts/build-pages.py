import json
import html
import os

root = os.path.join(os.path.dirname(__file__), "..")
with open(os.path.join(root, "site-content.json"), encoding="utf-8") as f:
    data = json.load(f)

business = data["business"]
services = data["services"]
locations = data["locations"]
site_url = business["siteUrl"]


def esc(value):
    return html.escape(str(value), quote=True)


FORM_EMBED_SRC = "https://link.clicktitan.com/widget/form/FMUZz7UusRyIJeLnAGZI"
FORM_EMBED_ID = "FMUZz7UusRyIJeLnAGZI"

FAVICON_LINKS = """    <link rel="icon" href="/assets/favicon-32x32.png" type="image/png" sizes="32x32" />
    <link rel="apple-touch-icon" href="/assets/apple-touch-icon.png" />"""

GOOGLE_ANALYTICS = """    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-B34W90C26K"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', 'G-B34W90C26K');
    </script>"""


def render_form_embed(suffix="", extra_class="", title="Request service from Prestige Electric", height=719):
    iframe_id = f"inline-{FORM_EMBED_ID}{suffix}"
    classes = "site-form-embed"
    if extra_class:
        classes += f" {extra_class}"
    return f"""          <div class="{classes}" style="--form-embed-height: {height}px;">
            <iframe
              src="{FORM_EMBED_SRC}"
              id="{iframe_id}"
              title="{esc(title)}"
              width="100%"
              style="width:100%;min-height:{height}px;border:none;border-radius:8px;display:block;"
              scrolling="auto"
              referrerpolicy="no-referrer-when-downgrade"
            ></iframe>
          </div>"""


def page_shell(title, description, canonical, json_ld, body, page=""):
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
{GOOGLE_ANALYTICS}
    <title>{esc(title)}</title>
    <meta name="description" content="{esc(description)}" />
    <meta name="robots" content="index, follow" />
    <link rel="canonical" href="{esc(canonical)}" />
    <meta property="og:type" content="website" />
    <meta property="og:title" content="{esc(title)}" />
    <meta property="og:description" content="{esc(description)}" />
    <meta property="og:url" content="{esc(canonical)}" />
    <meta property="og:site_name" content="{esc(business['name'])}" />
    <meta property="og:locale" content="en_US" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="theme-color" content="#6fbd44" />
{FAVICON_LINKS}
    <link rel="stylesheet" href="/styles.css" />
    <script type="application/ld+json">{json.dumps(json_ld, indent=2)}</script>
  </head>
  <body data-page="{page}">
    <a class="skip-link" href="#main">Skip to content</a>
    <header data-site-header></header>
    <main id="main">{body}</main>
    <footer data-site-footer></footer>
    <script type="module" src="/main.js"></script>
  </body>
</html>"""


business_schema = {
    "@type": "Electrician",
    "@id": f"{site_url}/#business",
    "name": business["name"],
    "url": site_url,
    "telephone": "+18165489601",
    "email": business["email"],
    "address": {
        "@type": "PostalAddress",
        "addressLocality": business["address"]["addressLocality"],
        "addressRegion": business["address"]["addressRegion"],
        "postalCode": business["address"]["postalCode"],
        "addressCountry": business["address"]["addressCountry"],
    },
}

cta = f"""
      <section class="section quote-section page-cta" id="service-quote">
        <div class="container quote-grid">
          <div class="quote-panel">
            <p class="eyebrow">Get a free quote</p>
            <h2>Schedule service with {esc(business['name'])}.</h2>
            <p>Call or send a message to request electrical service anywhere in the Kansas City metro.</p>
            <div class="contact-stack">
              <a href="{business['phoneHref']}">{esc(business['phoneDisplay'])}</a>
              <a href="{business['emailHref']}">{esc(business['email'])}</a>
            </div>
          </div>
{render_form_embed(suffix="-cta", title="Request a free estimate from Prestige Electric")}
        </div>
      </section>"""


def render_service_cta(panel_heading, panel_text):
    return f"""
      <section class="section quote-section page-cta" id="service-quote">
        <div class="container quote-grid">
          <div class="quote-panel">
            <p class="eyebrow">Get a free quote</p>
            <h2>{esc(panel_heading)}</h2>
            <p>{esc(panel_text)}</p>
            <div class="contact-stack">
              <a href="{business['phoneHref']}">{esc(business['phoneDisplay'])}</a>
              <a href="{business['emailHref']}">{esc(business['email'])}</a>
            </div>
          </div>
{render_form_embed(suffix="-cta", title="Request a free estimate from Prestige Electric")}
        </div>
      </section>"""


def build_enhanced_service_graph(service, canonical):
    seo = service["seo"]
    area_served = [loc["displayName"] for loc in locations]
    graph = [
        {"@id": f"{site_url}/#business"},
        {
            "@type": "Service",
            "@id": f"{canonical}#service",
            "name": seo.get("serviceType", service["title"]),
            "serviceType": seo.get("serviceType", service["title"]),
            "url": canonical,
            "description": service["description"],
            "provider": {"@id": f"{site_url}/#business"},
            "areaServed": area_served,
        },
        {
            "@type": "BreadcrumbList",
            "@id": f"{canonical}#breadcrumb",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{site_url}/"},
                {"@type": "ListItem", "position": 2, "name": "Services", "item": f"{site_url}/#services"},
                {"@type": "ListItem", "position": 3, "name": service["title"], "item": canonical},
            ],
        },
    ]
    if service.get("faqs"):
        graph.append(
            {
                "@type": "FAQPage",
                "@id": f"{canonical}#faq",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": faq["question"],
                        "acceptedAnswer": {"@type": "Answer", "text": faq["answer"]},
                    }
                    for faq in service["faqs"]
                ],
            }
        )
    return graph


def build_legacy_service_graph(service, canonical):
    graph = [
        business_schema,
        {
            "@type": "Service",
            "name": service["title"],
            "description": service["description"],
            "provider": {"@id": f"{site_url}/#business"},
            "areaServed": [loc["displayName"] for loc in locations],
        },
    ]
    if service.get("faqs"):
        graph.append(
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": faq["question"],
                        "acceptedAnswer": {"@type": "Answer", "text": faq["answer"]},
                    }
                    for faq in service["faqs"]
                ],
            }
        )
    return graph


def get_intro_content(page):
    intro = page.get("intro", [])
    if isinstance(intro, dict):
        eyebrow = intro.get("eyebrow", intro.get("subheadline", ""))
        return eyebrow, intro.get("paragraphs", []), intro.get("image", {})
    return page.get("introEyebrow", page.get("introSubheadline", "")), intro if isinstance(intro, list) else [], {}


def render_enhanced_service_body(service):
    page = service["page"]
    seo = service["seo"]
    location_tags = "".join(
        f'<a class="tag-link" href="/locations/{loc["slug"]}.html">{esc(loc["displayName"])}</a>'
        for loc in locations
    )
    intro_eyebrow, intro_paragraphs, intro_image = get_intro_content(page)
    intro_eyebrow_html = f'<p class="eyebrow">{esc(intro_eyebrow)}</p>' if intro_eyebrow else ""
    intro_html = "".join(f"<p>{esc(paragraph)}</p>" for paragraph in intro_paragraphs)
    intro_image_html = ""
    if intro_image.get("src"):
        intro_image_html = (
            f'<figure class="service-intro-media"><img src="{esc(intro_image["src"])}" '
            f'alt="{esc(intro_image.get("alt", ""))}" '
            f'width="{esc(intro_image.get("width", 960))}" '
            f'height="{esc(intro_image.get("height", 640))}" loading="lazy" decoding="async" /></figure>'
        )
    symptoms_html = "".join(
        f'<article class="symptom-card"><h3>{esc(item["title"])}</h3><p>{esc(item["text"])}</p></article>'
        for item in page["symptoms"]["items"]
    )
    process_html = "".join(
        f'<article class="process-step"><span>{str(index + 1).zfill(2)}</span><h3>{esc(step["title"])}</h3><p>{esc(step["text"])}</p></article>'
        for index, step in enumerate(page["process"]["steps"])
    )
    why_bullets = "".join(f"<li>{esc(item)}</li>" for item in page["whyChoose"]["bullets"])
    why_paragraphs = "".join(f"<p>{esc(paragraph)}</p>" for paragraph in page["whyChoose"]["paragraphs"])
    license_note = ""
    if page["whyChoose"].get("licenseNote"):
        license_note = f'<p class="service-license-note">{esc(page["whyChoose"]["licenseNote"])}</p>'
    why_image = page["whyChoose"].get("image", {})
    why_image_html = ""
    if why_image.get("src"):
        why_image_html = (
            f'<figure class="service-why-media"><img src="{esc(why_image["src"])}" '
            f'alt="{esc(why_image.get("alt", ""))}" '
            f'width="{esc(why_image.get("width", 960))}" '
            f'height="{esc(why_image.get("height", 640))}" loading="lazy" decoding="async" /></figure>'
        )
    related_html = "".join(
        f'<article class="related-service-card"><h3><a href="/services/{esc(related["slug"])}.html">{esc(related["anchor"])}</a></h3><p>{esc(related["description"])}</p></article>'
        for related in page["relatedServices"]
    )
    faq_items = "".join(
        f'<details{" open" if index == 0 else ""}><summary>{esc(faq["question"])}</summary><p>{esc(faq["answer"])}</p></details>'
        for index, faq in enumerate(service["faqs"])
    )

    closing = page.get("closingCta", {})
    mid = page.get("midCta", {})
    hero_image = service.get("heroImage") or business.get("serviceHeroImage", "/assets/service-hero-electrical-kitchen.png")

    return f"""
      <div class="service-mobile-bar" data-service-mobile-bar hidden>
        <a class="btn btn-primary" href="{business['phoneHref']}">Call {esc(business['phone'])}</a>
        <a class="btn btn-secondary" href="#service-quote">Get a Quote</a>
      </div>
      <section class="page-hero section service-hero">
        <div class="service-hero-bg" aria-hidden="true">
          <img
            src="{esc(hero_image)}"
            alt=""
            width="1920"
            height="1080"
            fetchpriority="high"
            decoding="async"
          />
        </div>
        <div class="service-hero-overlay" aria-hidden="true"></div>
        <div class="container service-hero-content">
          <nav class="breadcrumbs" aria-label="Breadcrumb">
            <a href="/">Home</a><span aria-hidden="true">/</span>
            <a href="/#services">Services</a><span aria-hidden="true">/</span>
            <span aria-current="page">{esc(service['title'])}</span>
          </nav>
          <p class="eyebrow">Electrical services</p>
          <h1>{esc(seo['h1'])}</h1>
          <p class="page-lead">{esc(service['description'])}</p>
          <div class="hero-actions">
            <a class="btn btn-primary" href="#service-quote">Get a Free Quote</a>
            <a class="btn btn-secondary" href="{business['phoneHref']}">Call {esc(business['phone'])}</a>
          </div>
        </div>
      </section>
      <section class="section service-intro">
        <div class="container service-intro-grid">
          <div class="service-intro-copy">
            {intro_eyebrow_html}
            <div class="copy-stack service-prose">{intro_html}</div>
          </div>{intro_image_html}
        </div>
      </section>
      <section class="section service-symptoms">
        <div class="container">
          <div class="section-heading">
            <p class="eyebrow">{esc(page['symptoms'].get('eyebrow', 'Common signs'))}</p>
            <h2>{esc(page['symptoms']['heading'])}</h2>
            <p>{esc(page['symptoms']['intro'])}</p>
          </div>
          <div class="symptoms-grid">{symptoms_html}</div>
        </div>
      </section>
      <section class="section service-process">
        <div class="container">
          <div class="section-heading">
            <p class="eyebrow">{esc(page['process'].get('eyebrow', 'Our process'))}</p>
            <h2>{esc(page['process']['heading'])}</h2>
          </div>
          <div class="process-grid">{process_html}</div>
        </div>
      </section>
      <section class="section service-why">
        <div class="container service-why-grid">
          <div class="copy-stack service-prose">
            <p class="eyebrow">{esc(page['whyChoose'].get('eyebrow', 'Local electricians'))}</p>
            <h2>{esc(page['whyChoose']['heading'])}</h2>
            {why_paragraphs}
            {license_note}
            <ul class="check-list service-why-list">{why_bullets}</ul>
          </div>{why_image_html}
        </div>
      </section>
      <section class="section service-mid-cta">
        <div class="container service-mid-cta-inner">
          <div>
            <h2>{esc(mid['heading'])}</h2>
            <p>{esc(mid['text'])}</p>
          </div>
          <div class="hero-actions">
            <a class="btn btn-primary" href="{business['phoneHref']}">Call {esc(business['phone'])}</a>
            <a class="btn btn-secondary" href="#service-quote">Request a Quote</a>
          </div>
        </div>
      </section>
      <section class="section service-area-block">
        <div class="container">
          <div class="section-heading">
            <p class="eyebrow">Service area</p>
            <h2>{esc(page['serviceArea']['heading'])}</h2>
            <p>{esc(page['serviceArea']['paragraph'])}</p>
          </div>
          <div class="tag-list">{location_tags}</div>
        </div>
      </section>
      <section class="section service-related">
        <div class="container">
          <div class="section-heading">
            <p class="eyebrow">Related services</p>
            <h2>Other electrical services from Prestige Electric</h2>
          </div>
          <div class="related-services-grid">{related_html}</div>
        </div>
      </section>
      <section class="section faq" id="service-faq">
        <div class="container faq-grid">
          <div><p class="eyebrow">FAQ</p><h2>{esc(service['title'])} questions</h2></div>
          <div class="faq-list">{faq_items}</div>
        </div>
      </section>
      {render_service_cta(closing.get('heading', f"Schedule service with {business['name']}."), closing.get('text', 'Call or send a message to request electrical service anywhere in the Kansas City metro.'))}"""


def render_legacy_service_body(service):
    benefits = "".join(f"<li>{esc(item)}</li>" for item in service["benefits"])
    location_tags = "".join(
        f'<a class="tag-link" href="/locations/{loc["slug"]}.html">{esc(loc["displayName"])}</a>'
        for loc in locations
    )
    faq_items = "".join(
        f'<details{" open" if index == 0 else ""}><summary>{esc(faq["question"])}</summary><p>{esc(faq["answer"])}</p></details>'
        for index, faq in enumerate(service["faqs"])
    )
    return f"""
      <section class="page-hero section">
        <div class="container">
          <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><span>{esc(service['title'])}</span></nav>
          <p class="eyebrow">Electrical services</p>
          <h1>{esc(service['title'])} in the Kansas City Metro</h1>
          <p class="page-lead">{esc(service['description'])}</p>
          <div class="hero-actions">
            <a class="btn btn-primary" href="/#quote">Get a Free Quote</a>
            <a class="btn btn-secondary" href="{business['phoneHref']}">Call {esc(business['phone'])}</a>
          </div>
        </div>
      </section>
      <section class="section">
        <div class="container split">
          <div>
            <h2>Why choose {esc(business['name'])}?</h2>
            <ul class="check-list">{benefits}</ul>
          </div>
          <div class="copy-stack">
            <h3>Areas we serve</h3>
            <p>{esc(service['shortDescription'])}</p>
            <div class="tag-list">{location_tags}</div>
          </div>
        </div>
      </section>
      <section class="section faq">
        <div class="container faq-grid">
          <div><p class="eyebrow">FAQ</p><h2>{esc(service['title'])} questions</h2></div>
          <div class="faq-list">{faq_items}</div>
        </div>
      </section>{cta}"""


def render_location_cta(panel_heading, panel_text):
    return f"""
      <section class="section quote-section page-cta location-quote" id="location-quote">
        <div class="container quote-grid">
          <div class="quote-panel">
            <p class="eyebrow">Get a free quote</p>
            <h2>{esc(panel_heading)}</h2>
            <p>{esc(panel_text)}</p>
            <div class="contact-stack">
              <a href="{business['phoneHref']}">{esc(business['phoneDisplay'])}</a>
              <a href="{business['emailHref']}">{esc(business['email'])}</a>
            </div>
          </div>
{render_form_embed(suffix="-cta", title="Request a free estimate from Prestige Electric")}
        </div>
      </section>"""


def get_location_hero_image(location):
    page = location.get("page") or {}
    return page.get("heroImage") or business.get("locationHeroImage", "/assets/location-hero-kansas-city-skyline.png")


def render_location_hero(location, h1, lead, breadcrumbs_html, hero_eyebrow, trust_strip_html):
    hero_image = get_location_hero_image(location)
    return f"""
      <section class="page-hero section location-hero">
        <div class="location-hero-bg" aria-hidden="true">
          <img
            src="{esc(hero_image)}"
            alt=""
            width="1024"
            height="576"
            fetchpriority="high"
            decoding="async"
          />
        </div>
        <div class="location-hero-overlay" aria-hidden="true"></div>
        <div class="container location-hero-content">
          {breadcrumbs_html}
          <p class="eyebrow">{esc(hero_eyebrow)}</p>
          <h1>{esc(h1)}</h1>
          <p class="page-lead">{esc(lead)}</p>
          {trust_strip_html}
          <div class="hero-actions">
            <a class="btn btn-primary" href="{business['phoneHref']}">Call {esc(business['phone'])}</a>
            <a class="btn btn-secondary" href="#location-quote">Request a Quote</a>
          </div>
        </div>
      </section>"""


def build_enhanced_location_graph(location, canonical):
    seo = location["seo"]
    faqs = location.get("faqs", [])
    graph = [
        {"@id": f"{site_url}/#business"},
        {
            "@type": "WebPage",
            "@id": f"{canonical}#webpage",
            "name": seo["title"],
            "url": canonical,
            "description": seo["metaDescription"],
            "about": {
                "@type": "City",
                "name": location["name"],
                "addressRegion": location["state"],
            },
            "provider": {"@id": f"{site_url}/#business"},
        },
        {
            "@type": "Electrician",
            "@id": f"{canonical}#area-service",
            "name": business["name"],
            "url": canonical,
            "telephone": "+18165489601",
            "areaServed": {
                "@type": "City",
                "name": location["name"],
                "addressRegion": location["state"],
            },
            "parentOrganization": {"@id": f"{site_url}/#business"},
        },
        {
            "@type": "BreadcrumbList",
            "@id": f"{canonical}#breadcrumb",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{site_url}/"},
                {"@type": "ListItem", "position": 2, "name": "Locations", "item": f"{site_url}/#locations"},
                {"@type": "ListItem", "position": 3, "name": location["displayName"], "item": canonical},
            ],
        },
    ]
    if faqs:
        graph.append(
            {
                "@type": "FAQPage",
                "@id": f"{canonical}#faq",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": faq["question"],
                        "acceptedAnswer": {"@type": "Answer", "text": faq["answer"]},
                    }
                    for faq in faqs
                ],
            }
        )
    return graph


def render_enhanced_location_body(location):
    page = location["page"]
    seo = location["seo"]
    reviews = data.get("googleReviews", {})
    rating = reviews.get("rating", "")
    review_count = reviews.get("reviewCount", "")

    intro = page.get("intro", {})
    intro_eyebrow_html = f'<p class="eyebrow">{esc(intro.get("eyebrow", ""))}</p>' if intro.get("eyebrow") else ""
    intro_html = "".join(f"<p>{esc(paragraph)}</p>" for paragraph in intro.get("paragraphs", []))

    services_html = "".join(
        f'<article class="location-service-card"><h3><a href="/services/{esc(item["slug"])}.html">{esc(item["anchor"])}</a></h3><p>{esc(item["description"])}</p></article>'
        for item in page.get("services", [])
    )

    why = page.get("whyChoose", {})
    why_paragraphs = "".join(f"<p>{esc(paragraph)}</p>" for paragraph in why.get("paragraphs", []))
    why_bullets = "".join(f"<li>{esc(item)}</li>" for item in why.get("bullets", []))

    faq_items = "".join(
        f'<details{" open" if index == 0 else ""}><summary>{esc(faq["question"])}</summary><p>{esc(faq["answer"])}</p></details>'
        for index, faq in enumerate(location.get("faqs", []))
    )

    service_area = page.get("serviceArea", {})
    map_embed = service_area.get("mapEmbed")
    if not map_embed:
        map_embed = f"https://maps.google.com/maps?width=600&height=400&hl=en&q={location.get('mapQuery', location['name'])}&t=&z=11&ie=UTF8&iwloc=B&output=embed"
    maps_link = f"https://www.google.com/maps/search/?api=1&query={location.get('mapQuery', location['name']).replace('+', ' ')}"

    closing = page.get("closingCta", {})
    trust_rating = ""
    if rating and review_count:
        trust_rating = f'<span class="location-trust-badge">{esc(rating)} Google rating ({esc(review_count)} reviews)</span>'

    hero_eyebrow = page.get("heroEyebrow", f"{location['name']} electricians")
    services_section = page.get("servicesSection", {})
    services_eyebrow = services_section.get("eyebrow", f"Services in {location['name']}")
    services_heading = services_section.get(
        "heading", f"Electrical services we provide in {location['displayName']}"
    )
    services_intro = services_section.get(
        "intro",
        "Explore our core services below. Each links to a dedicated page with scope, process, and pricing details.",
    )
    faq_heading = page.get("faqHeading", f"{location['name']} electrician questions")
    map_link_label = page.get("mapLinkLabel", f"View {location['name']} on Google Maps")
    trust_strip_html = f"""
          <div class="location-trust-strip">
            <span class="location-trust-badge">Family-owned and operated</span>
            <span class="location-trust-badge">Licensed and insured</span>
            {trust_rating}
          </div>"""
    breadcrumbs_html = f"""
          <nav class="breadcrumbs" aria-label="Breadcrumb">
            <a href="/">Home</a><span aria-hidden="true">/</span>
            <a href="/#locations">Locations</a><span aria-hidden="true">/</span>
            <span aria-current="page">{esc(location['displayName'])}</span>
          </nav>"""
    hero_html = render_location_hero(
        location,
        seo["h1"],
        page.get("heroLead", location["description"]),
        breadcrumbs_html,
        hero_eyebrow,
        trust_strip_html,
    )

    return f"""
      <div class="location-mobile-bar" data-location-mobile-bar hidden>
        <a class="btn btn-primary" href="{business['phoneHref']}">Call {esc(business['phone'])}</a>
        <a class="btn btn-secondary" href="#location-quote">Get a Quote</a>
      </div>
      {hero_html}
      <section class="section location-intro">
        <div class="container">
          <div class="location-intro-copy">
            {intro_eyebrow_html}
            <div class="copy-stack location-prose">{intro_html}</div>
          </div>
        </div>
      </section>
      <section class="section location-services">
        <div class="container">
          <div class="section-heading">
            <p class="eyebrow">{esc(services_eyebrow)}</p>
            <h2>{esc(services_heading)}</h2>
            <p>{esc(services_intro)}</p>
          </div>
          <div class="location-services-grid">{services_html}</div>
        </div>
      </section>
      <section class="section location-why">
        <div class="container">
          <div class="section-heading">
            <p class="eyebrow">{esc(why.get('eyebrow', 'Local electricians'))}</p>
            <h2>{esc(why.get('heading', ''))}</h2>
          </div>
          <div class="copy-stack location-prose">
            {why_paragraphs}
            <ul class="check-list location-why-list">{why_bullets}</ul>
          </div>
        </div>
      </section>
      <section class="section location-map-block">
        <div class="container location-grid">
          <div class="location-copy">
            <p class="eyebrow">Service area</p>
            <h2>{esc(service_area.get('heading', ''))}</h2>
            <p>{esc(service_area.get('paragraph', ''))}</p>
            <p><a class="text-link map-link" href="{maps_link}" target="_blank" rel="noopener noreferrer">{esc(map_link_label)}</a></p>
          </div>
          <div class="map-embed">
            <iframe title="Map of {esc(location['displayName'])}" src="{esc(map_embed)}" width="600" height="400" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
          </div>
        </div>
      </section>
      <section class="section faq location-faq" id="location-faq">
        <div class="container faq-grid">
          <div><p class="eyebrow">FAQ</p><h2>{esc(faq_heading)}</h2></div>
          <div class="faq-list">{faq_items}</div>
        </div>
      </section>
      {render_location_cta(closing.get('heading', f"Schedule service in {location['displayName']}."), closing.get('text', 'Call or send a message to request electrical service in the Kansas City metro.'))}"""


def render_legacy_location_body(location, maps_link, map_embed, service_cards, differentiators):
    reviews = data.get("googleReviews", {})
    rating = reviews.get("rating", "")
    review_count = reviews.get("reviewCount", "")
    trust_rating = ""
    if rating and review_count:
        trust_rating = f'<span class="location-trust-badge">{esc(rating)} Google rating ({esc(review_count)} reviews)</span>'
    trust_strip_html = f"""
          <div class="location-trust-strip">
            <span class="location-trust-badge">Family-owned and operated</span>
            <span class="location-trust-badge">Licensed and insured</span>
            {trust_rating}
          </div>"""
    breadcrumbs_html = f"""
          <nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><span>{esc(location['displayName'])}</span></nav>"""
    hero_html = render_location_hero(
        location,
        f"Electrician in {location['displayName']}",
        location["description"],
        breadcrumbs_html,
        "Service area",
        trust_strip_html,
    )
    return f"""
      {hero_html}
      <section class="section">
        <div class="container split">
          <div>
            <h2>Electrical services in {esc(location['displayName'])}</h2>
            <div class="service-grid compact-grid">{service_cards}</div>
          </div>
          <div class="copy-stack">
            <h3>Local electrical contractor</h3>
            <p>{esc(business['about'])}</p>
            <ul class="check-list">{differentiators}</ul>
          </div>
        </div>
      </section>
      <section class="section location">
        <div class="container location-grid">
          <div class="location-copy">
            <h2>{esc(business['name'])} near {esc(location['displayName'])}</h2>
            <address class="location-nap">
              <strong>{esc(business['name'])}</strong><br />
              {esc(business['address']['addressLocality'])}, {esc(business['address']['addressRegion'])} {esc(business['address']['postalCode'])}<br />
              <a href="{business['phoneHref']}">{esc(business['phoneDisplay'])}</a><br />
              <a href="{business['emailHref']}">{esc(business['email'])}</a><br />
              <a class="text-link map-link" href="{maps_link}" target="_blank" rel="noopener noreferrer">View on Google Maps</a>
            </address>
          </div>
          <div class="map-embed">
            <iframe title="Map of {esc(location['displayName'])}" src="{map_embed}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
          </div>
        </div>
      </section>{render_location_cta(f"Schedule service in {location['displayName']}.", "Call or send a message to request electrical service in the Kansas City metro.")}"""


os.makedirs(os.path.join(root, "services"), exist_ok=True)
os.makedirs(os.path.join(root, "locations"), exist_ok=True)

for service in services:
    canonical = f"{site_url}/services/{service['slug']}.html"
    enhanced = service.get("seo") and service.get("page")

    if enhanced:
        graph = build_enhanced_service_graph(service, canonical)
        body = render_enhanced_service_body(service)
        page_title = service["seo"]["title"]
        meta_description = service["seo"]["metaDescription"]
        body_class = ' data-page="services" class="service-page-enhanced"'
        page_shell_body = page_shell(page_title, meta_description, canonical, {"@context": "https://schema.org", "@graph": graph}, body, "services")
        page_shell_body = page_shell_body.replace('<body data-page="services">', f'<body data-page="services" class="service-page-enhanced">')
    else:
        graph = build_legacy_service_graph(service, canonical)
        body = render_legacy_service_body(service)
        page_title = f"{service['title']} | {business['name']}"
        meta_description = service["shortDescription"]
        page_shell_body = page_shell(page_title, meta_description, canonical, {"@context": "https://schema.org", "@graph": graph}, body, "services")

    with open(os.path.join(root, "services", f"{service['slug']}.html"), "w", encoding="utf-8") as out:
        out.write(page_shell_body)

for location in locations:
    canonical = f"{site_url}/locations/{location['slug']}.html"
    map_embed = business["mapEmbedUrl"]
    if location.get("useBusinessMap"):
        maps_link = business["googleMapsUrl"]
    else:
        maps_link = f"https://www.google.com/maps/search/?api=1&query={location['mapQuery'].replace('+', ' ')}"

    enhanced = location.get("seo") and location.get("page")
    if enhanced:
        graph = build_enhanced_location_graph(location, canonical)
        body = render_enhanced_location_body(location)
        page_shell_body = page_shell(
            location["seo"]["title"],
            location["seo"]["metaDescription"],
            canonical,
            {"@context": "https://schema.org", "@graph": graph},
            body,
            "locations",
        )
        page_shell_body = page_shell_body.replace(
            '<body data-page="locations">',
            '<body data-page="locations" class="location-page-enhanced">',
        )
    else:
        graph = [
            business_schema,
            {
                "@type": "Electrician",
                "name": f"{business['name']} - {location['displayName']}",
                "description": location["description"],
                "areaServed": location["displayName"],
                "geo": {
                    "@type": "GeoCoordinates",
                    "latitude": location["geo"]["latitude"],
                    "longitude": location["geo"]["longitude"],
                },
            },
        ]
        service_cards = "".join(
            f'<article class="service-card"><a class="service-card-link" href="/services/{svc["slug"]}.html"><h3>{esc(svc["title"])}</h3><p>{esc(svc["shortDescription"])}</p><span class="service-card-cta">Learn more</span></a></article>'
            for svc in services
        )
        differentiators = "".join(f"<li>{esc(item['title'])}</li>" for item in business["differentiators"])
        body = render_legacy_location_body(location, maps_link, map_embed, service_cards, differentiators)
        page_shell_body = page_shell(
            f"Electrician in {location['displayName']} | {business['name']}",
            location["description"],
            canonical,
            {"@context": "https://schema.org", "@graph": graph},
            body,
            "locations",
        )

    with open(os.path.join(root, "locations", f"{location['slug']}.html"), "w", encoding="utf-8") as out:
        out.write(page_shell_body)

entries = [f"<url><loc>{site_url}/</loc><priority>1.0</priority></url>"]
entries.extend(f"<url><loc>{site_url}/services/{service['slug']}.html</loc><priority>0.8</priority></url>" for service in services)
entries.extend(f"<url><loc>{site_url}/locations/{location['slug']}.html</loc><priority>0.8</priority></url>" for location in locations)
legal_pages = [
    ("contact.html", "0.8"),
    ("our-work.html", "0.7"),
    ("sitemap.html", "0.5"),
    ("privacy-policy.html", "0.4"),
    ("terms-and-conditions.html", "0.4"),
]
entries.extend(f"<url><loc>{site_url}/{page}</loc><priority>{priority}</priority></url>" for page, priority in legal_pages)

with open(os.path.join(root, "sitemap.xml"), "w", encoding="utf-8") as out:
    out.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  ')
    out.write("\n  ".join(entries))
    out.write("\n</urlset>\n")

print(f"Generated {len(services)} service pages and {len(locations)} location pages")
