import { initLayout } from "./layout.js";

const QUOTE_HASHES = new Set([
  "#hero-quote",
  "#quote",
  "#service-quote",
  "#location-quote",
  "#contact-form",
]);

const getHeaderOffset = () => {
  const header = document.querySelector(".site-header");
  return header ? Math.ceil(header.getBoundingClientRect().height) + 12 : 96;
};

const closeMobileNav = () => {
  const navToggle = document.querySelector(".nav-toggle");
  const navLinks = document.querySelector("#navLinks");
  if (!navToggle || !navLinks) return;

  navToggle.setAttribute("aria-expanded", "false");
  navLinks.classList.remove("is-open");
  document.body.classList.remove("nav-open");
};

const scrollToHashTarget = (hash) => {
  if (!hash || !hash.startsWith("#") || hash.length < 2) return false;

  const target = document.querySelector(hash);
  if (!target) return false;

  const top = target.getBoundingClientRect().top + window.scrollY - getHeaderOffset();
  window.scrollTo({ top: Math.max(0, top), behavior: "smooth" });

  if (history.replaceState) {
    history.replaceState(null, "", hash);
  }

  return true;
};

const scrollToHashAfterNavClose = (hash) => {
  const wasNavOpen = document.body.classList.contains("nav-open");
  if (wasNavOpen) {
    closeMobileNav();
    window.setTimeout(() => scrollToHashTarget(hash), 120);
    return;
  }

  scrollToHashTarget(hash);
};

const initNavigation = () => {
  const navToggle = document.querySelector(".nav-toggle");
  const navLinks = document.querySelector("#navLinks");

  if (!navToggle || !navLinks) return;

  navToggle.addEventListener("click", () => {
    const isOpen = navToggle.getAttribute("aria-expanded") === "true";
    navToggle.setAttribute("aria-expanded", String(!isOpen));
    navLinks.classList.toggle("is-open", !isOpen);
    document.body.classList.toggle("nav-open", !isOpen);
  });

  navLinks.addEventListener("click", (event) => {
    const link = event.target.closest("a");
    if (!link || !navLinks.contains(link)) return;

    const href = link.getAttribute("href") || "";

    if (href.startsWith("#")) {
      event.preventDefault();
      scrollToHashAfterNavClose(href);
      return;
    }

    closeMobileNav();
  });
};

const initQuoteScroll = () => {
  document.addEventListener("click", (event) => {
    const link = event.target.closest("a");
    if (!link || link.closest("#navLinks")) return;

    const href = link.getAttribute("href") || "";
    if (!href.startsWith("#")) return;
    if (!QUOTE_HASHES.has(href) && !link.classList.contains("nav-cta")) return;

    event.preventDefault();
    scrollToHashTarget(href);
  });

  if (window.location.hash && QUOTE_HASHES.has(window.location.hash)) {
    window.setTimeout(() => scrollToHashTarget(window.location.hash), 150);
  }
};

const createElement = (tag, className, text) => {
  const element = document.createElement(tag);
  if (className) element.className = className;
  if (text) element.textContent = text;
  return element;
};

const renderServices = (services) => {
  const serviceGrid = document.querySelector("[data-service-grid]");
  if (!serviceGrid || !Array.isArray(services) || services.length === 0) return;

  serviceGrid.replaceChildren(
    ...services.map((service, index) => {
      const card = createElement("article", "service-card");
      const link = createElement("a", "service-card-link", "");
      link.href = `/services/${service.slug}.html`;

      const icon = createElement("span", "service-icon", String(index + 1).padStart(2, "0"));
      icon.setAttribute("aria-hidden", "true");
      link.append(icon, createElement("h3", "", service.title), createElement("p", "", service.shortDescription));
      link.append(createElement("span", "service-card-cta", "Learn more"));
      card.append(link);
      return card;
    }),
  );
};

const renderLocations = (locations) => {
  const locationGrid = document.querySelector("[data-location-grid]");
  if (!locationGrid || !Array.isArray(locations) || locations.length === 0) return;

  locationGrid.replaceChildren(
    ...locations.map((location) => {
      const card = createElement("article", "location-card");
      const link = createElement("a", "location-card-link", "");
      link.href = `/locations/${location.slug}.html`;
      link.append(
        createElement("h3", "", location.displayName),
        createElement("p", "", location.description),
        createElement("span", "location-card-cta", "View local page"),
      );
      card.append(link);
      return card;
    }),
  );
};

const renderDifferentiators = (items) => {
  const trustGrid = document.querySelector("[data-trust-grid]");
  if (!trustGrid || !Array.isArray(items) || items.length === 0) return;

  trustGrid.replaceChildren(
    ...items.map((item) => {
      const block = createElement("div", "");
      block.append(createElement("strong", "", item.title), createElement("span", "", item.description));
      return block;
    }),
  );
};

const renderStars = (rating) => {
  const stars = [];
  for (let index = 1; index <= 5; index += 1) {
    let className = "star";
    if (rating >= index) className += " filled";
    else if (rating >= index - 0.5) className += " partial";
    stars.push(`<span class="${className}" aria-hidden="true"></span>`);
  }
  return stars.join("");
};

const renderGoogleRating = (googleReviews) => {
  const ratingCard = document.querySelector("[data-google-rating]");
  if (!ratingCard || !googleReviews) return;

  const { rating, reviewCount, profileUrl } = googleReviews;
  ratingCard.innerHTML = `
    <div class="google-rating-badge">
      <span class="google-mark" aria-hidden="true">G</span>
      <span>Google Reviews</span>
    </div>
    <div class="google-rating-score" aria-label="${rating} out of 5 stars on Google">
      <span class="google-rating-number">${rating}</span>
      <div class="stars">${renderStars(rating)}</div>
    </div>
    <p class="google-rating-count">Based on ${reviewCount} Google reviews</p>
    <a class="btn btn-primary google-reviews-link" href="${profileUrl}" target="_blank" rel="noopener noreferrer">Read reviews on Google</a>
  `;
};

const renderTestimonials = (items, googleReviews) => {
  const testimonialsGrid = document.querySelector("[data-testimonials-grid]");
  if (!testimonialsGrid) return;

  if (!Array.isArray(items) || items.length === 0) {
    testimonialsGrid.replaceChildren();
    return;
  }

  testimonialsGrid.replaceChildren(
    ...items.map((item) => {
      const card = createElement("article", "testimonial-card");
      card.append(
        (() => {
          const header = createElement("div", "testimonial-card-header");
          header.innerHTML = `
            <div>
              <h3>${item.author}</h3>
              <p class="testimonial-source">Google review</p>
            </div>
            <div class="stars" aria-label="${item.rating} out of 5 stars">${renderStars(item.rating)}</div>
          `;
          return header;
        })(),
        createElement("p", "testimonial-text", item.text),
      );
      return card;
    }),
  );
};

const renderGallery = (gallery) => {
  const grid = document.querySelector("[data-gallery-grid]");
  const empty = document.querySelector("[data-gallery-empty]");
  if (!grid) return;

  const title = document.querySelector("[data-gallery-title]");
  const intro = document.querySelector("[data-gallery-intro]");
  if (gallery?.seo) {
    if (title && gallery.seo.h1) title.textContent = gallery.seo.h1;
    if (intro && gallery.seo.intro) intro.textContent = gallery.seo.intro;
  }

  const images = Array.isArray(gallery?.images) ? gallery.images : [];
  if (images.length === 0) {
    grid.replaceChildren();
    if (empty) empty.hidden = false;
    return;
  }

  if (empty) empty.hidden = true;
  grid.replaceChildren(
    ...images.map((image) => {
      const item = createElement("figure", "gallery-item");
      const img = document.createElement("img");
      img.src = image.src;
      img.alt = image.alt || "Electrical project completed by Prestige Electric";
      img.width = image.width || 800;
      img.height = image.height || 800;
      img.loading = "lazy";
      img.decoding = "async";
      item.append(img);
      return item;
    }),
  );
};

const renderFaq = (items) => {
  const faqList = document.querySelector(".faq-list");
  if (!faqList || !Array.isArray(items) || items.length === 0) return;

  faqList.replaceChildren(
    ...items.map((item, index) => {
      const details = document.createElement("details");
      if (index === 0) details.open = true;
      details.append(createElement("summary", "", item.question), createElement("p", "", item.answer));
      return details;
    }),
  );
};

const renderSitemapLists = (services, locations) => {
  const servicesList = document.querySelector("[data-sitemap-services]");
  const locationsList = document.querySelector("[data-sitemap-locations]");

  if (servicesList && Array.isArray(services)) {
    servicesList.replaceChildren(
      ...services.map((service) => {
        const item = createElement("li");
        const link = createElement("a", "", service.title);
        link.href = `/services/${service.slug}.html`;
        item.append(link);
        return item;
      }),
    );
  }

  if (locationsList && Array.isArray(locations)) {
    locationsList.replaceChildren(
      ...locations.map((location) => {
        const item = createElement("li");
        const link = createElement("a", "", location.displayName);
        link.href = `/locations/${location.slug}.html`;
        item.append(link);
        return item;
      }),
    );
  }
};

const hydrateContent = async () => {
  try {
    const response = await fetch("/site-content.json");
    if (!response.ok) return;

    const data = await response.json();
    renderServices(data.services);
    renderLocations(data.locations);
    renderGoogleRating(data.googleReviews);
    renderTestimonials(data.testimonials, data.googleReviews);
    renderDifferentiators(data.business?.differentiators);
    renderGallery(data.gallery);
    renderSitemapLists(data.services, data.locations);
    renderFaq(data.faq);

    document.querySelectorAll("[data-business-phone]").forEach((node) => {
      node.textContent = data.business.phoneDisplay || data.business.phone;
      if (node instanceof HTMLAnchorElement) node.href = data.business.phoneHref;
    });

    const callBarLink = document.querySelector("[data-site-call-bar] a");
    if (callBarLink && data.business?.phoneHref) {
      callBarLink.href = data.business.phoneHref;
    }

    document.querySelectorAll("[data-business-email]").forEach((node) => {
      node.textContent = data.business.email;
      if (node instanceof HTMLAnchorElement) node.href = data.business.emailHref;
    });

    document.querySelectorAll("[data-business-about]").forEach((node) => {
      node.textContent = data.business.about;
    });

    document.querySelectorAll("[data-about-section]").forEach((node) => {
      node.textContent = data.business.aboutSection || data.business.about;
    });
  } catch {
    // Static SEO content remains in HTML if JSON fails to load.
  }
};

const initYear = () => {
  document.querySelectorAll("[data-year]").forEach((node) => {
    node.textContent = new Date().getFullYear();
  });
};

const initImageLoading = () => {
  document.querySelectorAll("img:not([loading])").forEach((img) => {
    const isPriority =
      img.closest(".hero, .service-hero, .location-hero, .contact-hero") ||
      img.closest(".site-header .brand");

    if (isPriority) {
      img.fetchPriority = "high";
      img.decoding = "async";
      return;
    }

    img.loading = "lazy";
    img.decoding = "async";
  });
};

const loadScript = (src) =>
  new Promise((resolve, reject) => {
    if (document.querySelector(`script[src="${src}"]`)) {
      resolve();
      return;
    }

    const script = document.createElement("script");
    script.src = src;
    script.async = true;
    script.onload = resolve;
    script.onerror = reject;
    document.body.appendChild(script);
  });

const syncFormEmbedHeight = (iframe, height) => {
  if (!iframe || !height) return;

  const nextHeight = `${height}px`;
  const container = iframe.closest(".site-form-embed");
  iframe.style.height = nextHeight;
  iframe.style.minHeight = nextHeight;

  if (container) {
    container.style.minHeight = nextHeight;
    container.style.setProperty("--form-embed-height", nextHeight);
  }
};

const initGhlFormEmbeds = async () => {
  const iframes = document.querySelectorAll(".site-form-embed iframe");
  if (!iframes.length) return;

  try {
    await loadScript("https://cdn.jsdelivr.net/npm/iframe-resizer@4.3.11/js/iframeResizer.min.js");
  } catch {
    return;
  }

  if (typeof window.iFrameResize !== "function") return;

  window.iFrameResize(
    {
      checkOrigin: false,
      log: false,
      autoResize: true,
      sizeHeight: true,
      sizeWidth: false,
      warningTimeout: 10000,
      onResized: ({ iframe, height }) => {
        syncFormEmbedHeight(iframe, height);
      },
    },
    ".site-form-embed iframe",
  );
};

const initSiteCallBar = () => {
  if (document.querySelector("[data-site-call-bar]")) return;

  const phoneLink =
    document.querySelector("[data-business-phone]")?.getAttribute("href") ||
    document.querySelector('a[href^="tel:"]')?.getAttribute("href") ||
    "tel:+18165489601";

  const bar = document.createElement("div");
  bar.className = "site-call-bar";
  bar.setAttribute("data-site-call-bar", "");
  bar.innerHTML = `<a class="btn btn-primary site-call-bar-btn" href="${phoneLink}">Call Now</a>`;
  document.body.appendChild(bar);
};

const activePage = document.body.dataset.page || "";
await initLayout(activePage);
initImageLoading();
initNavigation();
initQuoteScroll();
initYear();
hydrateContent();
initSiteCallBar();
initGhlFormEmbeds();
