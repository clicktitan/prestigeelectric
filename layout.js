const getSiteContent = async () => {
  const response = await fetch("/site-content.json");
  if (!response.ok) throw new Error("Failed to load site content");
  return response.json();
};

const renderLogo = (
  business,
  { className = "brand-logo-img", width = 200, height = 56, loading = "" } = {},
) => {
  if (!business.logo) {
    return `<span class="brand-text">${business.name}</span>`;
  }

  const loadingAttr = loading ? ` loading="${loading}" decoding="async"` : "";
  return `<img class="${className}" src="${business.logo}" alt="${business.name} logo" width="${width}" height="${height}"${loadingAttr} />`;
};

const quoteHrefByPage = {
  home: "#quote",
  services: "#service-quote",
  locations: "#location-quote",
  contact: "#contact-form",
  "our-work": "#quote",
};

const getQuoteHref = (active) => quoteHrefByPage[active] ?? "/contact.html#contact-form";

const renderHeader = (business, services, locations, active = "") => {
  const serviceLinks = services.map((service) => ({
    href: `/services/${service.slug}.html`,
    label: service.title,
  }));

  const locationLinks = locations.map((location) => ({
    href: `/locations/${location.slug}.html`,
    label: location.displayName,
  }));

  const logoMarkup = renderLogo(business);

  const isHome = active === "home";
  const homePrefix = isHome ? "" : "/";

  return `
    <div class="topbar">
      <p>${business.hours}</p>
      <a href="${business.phoneHref}">Call ${business.phoneDisplay || business.phone}</a>
    </div>
    <nav class="nav" aria-label="Primary navigation">
      <a class="brand" href="${homePrefix}#top" aria-label="${business.name} home">
        ${logoMarkup}
      </a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="navLinks">
        <span class="sr-only">Toggle navigation</span>
        <span></span><span></span><span></span>
      </button>
      <div class="nav-links" id="navLinks">
        <a href="${homePrefix}#about"${active === "about" ? ' aria-current="page"' : ""}>About</a>
        <div class="nav-dropdown">
          <a href="${homePrefix}#services"${active === "services" ? ' aria-current="page"' : ""}>Services</a>
          <div class="nav-dropdown-panel" role="menu">
            ${serviceLinks.map((link) => `<a href="${link.href}" role="menuitem">${link.label}</a>`).join("")}
          </div>
        </div>
        <div class="nav-dropdown">
          <a href="${homePrefix}#locations"${active === "locations" ? ' aria-current="page"' : ""}>Locations</a>
          <div class="nav-dropdown-panel" role="menu">
            ${locationLinks.map((link) => `<a href="${link.href}" role="menuitem">${link.label}</a>`).join("")}
          </div>
        </div>
        <a href="/our-work.html"${active === "our-work" ? ' aria-current="page"' : ""}>See Our Work</a>
        <a href="/contact.html"${active === "contact" ? ' aria-current="page"' : ""}>Contact Us</a>
        <a class="nav-cta" href="${getQuoteHref(active)}">Get a Free Quote</a>
      </div>
    </nav>
  `;
};

const renderFooter = (business, services, locations) => {
  return `
    <div class="container footer-grid">
      <div>
        <a class="footer-brand" href="/#top" aria-label="${business.name} home">
          ${renderLogo(business, { className: "footer-brand-img", width: 180, height: 50, loading: "lazy" })}
        </a>
        <p>${business.about}</p>
        <a class="footer-social" href="${business.facebook}" target="_blank" rel="noopener noreferrer">Follow on Facebook</a>
      </div>
      <div class="footer-nap">
        <h2>Contact</h2>
        <address itemscope itemtype="https://schema.org/Electrician">
          <span itemprop="name">${business.name}</span><br />
          <span itemprop="address" itemscope itemtype="https://schema.org/PostalAddress">
            <span itemprop="addressLocality">${business.address.addressLocality}</span>,
            <span itemprop="addressRegion">${business.address.addressRegion}</span>
            <span itemprop="postalCode">${business.address.postalCode}</span>
          </span><br />
          <span>${business.hours}</span><br />
          <a itemprop="telephone" href="${business.phoneHref}">${business.phoneDisplay || business.phone}</a>
          <a itemprop="email" href="${business.emailHref}">${business.email}</a>
          <a class="footer-map-link" href="${business.googleMapsUrl}" target="_blank" rel="noopener noreferrer">View on Google Maps</a>
        </address>
      </div>
      <div>
        <h2>Services</h2>
        ${services.map((service) => `<a href="/services/${service.slug}.html">${service.title}</a>`).join("")}
      </div>
      <div>
        <h2>Locations</h2>
        ${locations.map((location) => `<a href="/locations/${location.slug}.html">${location.displayName}</a>`).join("")}
      </div>
    </div>
    <div class="container footer-bottom">
      <div class="footer-bottom-meta">
        <p>&copy; <span data-year></span> ${business.name}. All rights reserved.</p>
        <nav class="footer-legal" aria-label="Legal links">
          <a href="/sitemap.html">Sitemap</a>
          <a href="/privacy-policy.html">Privacy Policy</a>
          <a href="/terms-and-conditions.html">Terms and Conditions</a>
        </nav>
      </div>
      <div class="footer-bottom-end">
        <p class="footer-powered">Powered by <a href="https://clicktitan.com" target="_blank" rel="noopener noreferrer">ClickTitan</a></p>
      </div>
    </div>
  `;
};

export const initLayout = async (active = "") => {
  try {
    const data = await getSiteContent();
    const headerTarget = document.querySelector("[data-site-header]");
    const footerTarget = document.querySelector("[data-site-footer]");

    if (headerTarget) {
      headerTarget.className = "site-header";
      headerTarget.id = "top";
      headerTarget.innerHTML = renderHeader(data.business, data.services, data.locations, active);
    }

    if (footerTarget) {
      footerTarget.className = "site-footer";
      footerTarget.innerHTML = renderFooter(data.business, data.services, data.locations);
    }
  } catch {
    // Static fallbacks remain in HTML when JSON is unavailable.
  }
};
