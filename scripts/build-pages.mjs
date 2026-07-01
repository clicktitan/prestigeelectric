import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, "..");
const data = JSON.parse(readFileSync(join(root, "site-content.json"), "utf8"));
const { business, services, locations } = data;
const siteUrl = business.siteUrl;

const esc = (value) =>
  String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");

const pageShell = ({ title, description, canonical, jsonLd, body, page = "" }) => `<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>${esc(title)}</title>
    <meta name="description" content="${esc(description)}" />
    <meta name="robots" content="index, follow" />
    <link rel="canonical" href="${esc(canonical)}" />
    <meta property="og:type" content="website" />
    <meta property="og:title" content="${esc(title)}" />
    <meta property="og:description" content="${esc(description)}" />
    <meta property="og:url" content="${esc(canonical)}" />
    <meta property="og:site_name" content="${esc(business.name)}" />
    <meta property="og:locale" content="en_US" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="theme-color" content="#6fbd44" />
    <link rel="stylesheet" href="/styles.css" />
    <script type="application/ld+json">${JSON.stringify(jsonLd, null, 2)}</script>
  </head>
  <body data-page="${page}">
    <a class="skip-link" href="#main">Skip to content</a>
    <header data-site-header></header>
    <main id="main">${body}</main>
    <footer data-site-footer></footer>
    <script type="module" src="/main.js"></script>
  </body>
</html>`;

const ctaSection = `
      <section class="section quote-section page-cta">
        <div class="container quote-grid">
          <div class="quote-panel">
            <p class="eyebrow">Get a free quote</p>
            <h2>Schedule service with ${esc(business.name)}.</h2>
            <p>Call or send a message to request electrical service anywhere in the Kansas City metro.</p>
            <div class="contact-stack">
              <a href="${business.phoneHref}">${esc(business.phoneDisplay)}</a>
              <a href="${business.emailHref}">${esc(business.email)}</a>
            </div>
          </div>
          <form class="quote-form" aria-label="Request a free estimate" data-quote-form>
            <div class="form-row"><label for="name">Full Name</label><input id="name" name="name" type="text" autocomplete="name" required /></div>
            <div class="form-row"><label for="phone">Phone *</label><input id="phone" name="phone" type="tel" autocomplete="tel" required /></div>
            <div class="form-row full"><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email" /></div>
            <div class="form-row full"><label for="message">Your Message</label><textarea id="message" name="message" rows="5" required></textarea></div>
            <label class="consent full"><input type="checkbox" required /><span>I agree to be contacted by ${esc(business.name)} about my request.</span></label>
            <p class="form-note full" id="formNote" aria-live="polite">Submit to prepare your quote request email.</p>
            <button class="btn btn-primary full" type="submit">Request Service Appointment</button>
          </form>
        </div>
      </section>`;

const businessSchema = {
  "@type": "Electrician",
  "@id": `${siteUrl}/#business`,
  name: business.name,
  url: siteUrl,
  telephone: "+18165489601",
  email: business.email,
  address: {
    "@type": "PostalAddress",
    addressLocality: business.address.addressLocality,
    addressRegion: business.address.addressRegion,
    postalCode: business.address.postalCode,
    addressCountry: business.address.addressCountry,
  },
};

mkdirSync(join(root, "services"), { recursive: true });
mkdirSync(join(root, "locations"), { recursive: true });

for (const service of services) {
  const canonical = `${siteUrl}/services/${service.slug}.html`;
  const jsonLd = {
    "@context": "https://schema.org",
    "@graph": [
      businessSchema,
      {
        "@type": "Service",
        name: service.title,
        description: service.description,
        provider: { "@id": `${siteUrl}/#business` },
        areaServed: locations.map((location) => location.displayName),
      },
      ...(service.faqs.length
        ? [
            {
              "@type": "FAQPage",
              mainEntity: service.faqs.map((faq) => ({
                "@type": "Question",
                name: faq.question,
                acceptedAnswer: { "@type": "Answer", text: faq.answer },
              })),
            },
          ]
        : []),
    ],
  };

  const body = `
      <section class="page-hero section">
        <div class="container">
          <nav class="breadcrumbs" aria-label="Breadcrumb">
            <a href="/">Home</a><span aria-hidden="true">/</span><span>${esc(service.title)}</span>
          </nav>
          <p class="eyebrow">Electrical services</p>
          <h1>${esc(service.title)} in the Kansas City Metro</h1>
          <p class="page-lead">${esc(service.description)}</p>
          <div class="hero-actions">
            <a class="btn btn-primary" href="/#quote">Get a Free Quote</a>
            <a class="btn btn-secondary" href="${business.phoneHref}">Call ${esc(business.phone)}</a>
          </div>
        </div>
      </section>
      <section class="section">
        <div class="container split">
          <div>
            <h2>Why choose ${esc(business.name)}?</h2>
            <ul class="check-list">
              ${service.benefits.map((benefit) => `<li>${esc(benefit)}</li>`).join("")}
            </ul>
          </div>
          <div class="copy-stack">
            <h3>Areas we serve</h3>
            <p>${esc(service.shortDescription)}</p>
            <div class="tag-list">
              ${locations.map((location) => `<a class="tag-link" href="/locations/${location.slug}.html">${esc(location.displayName)}</a>`).join("")}
            </div>
          </div>
        </div>
      </section>
      <section class="section faq">
        <div class="container faq-grid">
          <div>
            <p class="eyebrow">FAQ</p>
            <h2>${esc(service.title)} questions</h2>
          </div>
          <div class="faq-list">
            ${service.faqs
              .map(
                (faq, index) => `<details${index === 0 ? " open" : ""}><summary>${esc(faq.question)}</summary><p>${esc(faq.answer)}</p></details>`,
              )
              .join("")}
          </div>
        </div>
      </section>${ctaSection}`;

  writeFileSync(
    join(root, "services", `${service.slug}.html`),
    pageShell({
      title: `${service.title} | ${business.name}`,
      description: service.shortDescription,
      canonical,
      jsonLd,
      body,
      page: "services",
    }),
  );
}

for (const location of locations) {
  const canonical = `${siteUrl}/locations/${location.slug}.html`;
  const mapEmbed = `https://maps.google.com/maps?q=${location.mapQuery}&z=11&hl=en&output=embed`;
  const jsonLd = {
    "@context": "https://schema.org",
    "@graph": [
      businessSchema,
      {
        "@type": "Electrician",
        name: `${business.name} - ${location.displayName}`,
        description: location.description,
        areaServed: location.displayName,
        geo: {
          "@type": "GeoCoordinates",
          latitude: location.geo.latitude,
          longitude: location.geo.longitude,
        },
      },
    ],
  };

  const body = `
      <section class="page-hero section">
        <div class="container">
          <nav class="breadcrumbs" aria-label="Breadcrumb">
            <a href="/">Home</a><span aria-hidden="true">/</span><span>${esc(location.displayName)}</span>
          </nav>
          <p class="eyebrow">Service area</p>
          <h1>Electrician in ${esc(location.displayName)}</h1>
          <p class="page-lead">${esc(location.description)}</p>
          <div class="hero-actions">
            <a class="btn btn-primary" href="/#quote">Get a Free Quote</a>
            <a class="btn btn-secondary" href="${business.phoneHref}">Call ${esc(business.phone)}</a>
          </div>
        </div>
      </section>
      <section class="section">
        <div class="container split">
          <div>
            <h2>Electrical services in ${esc(location.displayName)}</h2>
            <div class="service-grid compact-grid">
              ${services
                .map(
                  (service) => `<article class="service-card"><a class="service-card-link" href="/services/${service.slug}.html"><h3>${esc(service.title)}</h3><p>${esc(service.shortDescription)}</p><span class="service-card-cta">Learn more</span></a></article>`,
                )
                .join("")}
            </div>
          </div>
          <div class="copy-stack">
            <h3>Local electrical contractor</h3>
            <p>${esc(business.about)}</p>
            <ul class="check-list">
              ${business.differentiators.map((item) => `<li>${esc(item.title)}</li>`).join("")}
            </ul>
          </div>
        </div>
      </section>
      <section class="section location">
        <div class="container location-grid">
          <div class="location-copy">
            <h2>${esc(business.name)} near ${esc(location.displayName)}</h2>
            <address class="location-nap">
              <strong>${esc(business.name)}</strong><br />
              ${esc(business.address.addressLocality)}, ${esc(business.address.addressRegion)} ${esc(business.address.postalCode)}<br />
              <a href="${business.phoneHref}">${esc(business.phoneDisplay)}</a><br />
              <a href="${business.emailHref}">${esc(business.email)}</a>
            </address>
          </div>
          <div class="map-embed">
            <iframe title="Map of ${esc(location.displayName)}" src="${mapEmbed}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
          </div>
        </div>
      </section>${ctaSection}`;

  writeFileSync(
    join(root, "locations", `${location.slug}.html`),
    pageShell({
      title: `Electrician in ${location.displayName} | ${business.name}`,
      description: location.description,
      canonical,
      jsonLd,
      body,
      page: "locations",
    }),
  );
}

const sitemapEntries = [
  `<url><loc>${siteUrl}/</loc><priority>1.0</priority></url>`,
  ...services.map((service) => `<url><loc>${siteUrl}/services/${service.slug}.html</loc><priority>0.8</priority></url>`),
  ...locations.map((location) => `<url><loc>${siteUrl}/locations/${location.slug}.html</loc><priority>0.8</priority></url>`),
];

writeFileSync(
  join(root, "sitemap.xml"),
  `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  ${sitemapEntries.join("\n  ")}\n</urlset>\n`,
);

console.log(`Generated ${services.length} service pages and ${locations.length} location pages.`);
