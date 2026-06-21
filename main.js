const navToggle = document.querySelector(".nav-toggle");
const navLinks = document.querySelector("#navLinks");
const yearTarget = document.querySelector("[data-year]");
const quoteForm = document.querySelector("[data-quote-form]");
const formNote = document.querySelector("#formNote");

if (yearTarget) {
  yearTarget.textContent = new Date().getFullYear();
}

if (navToggle && navLinks) {
  navToggle.addEventListener("click", () => {
    const isOpen = navToggle.getAttribute("aria-expanded") === "true";
    navToggle.setAttribute("aria-expanded", String(!isOpen));
    navLinks.classList.toggle("is-open", !isOpen);
    document.body.classList.toggle("nav-open", !isOpen);
  });

  navLinks.addEventListener("click", (event) => {
    if (event.target instanceof HTMLAnchorElement) {
      navToggle.setAttribute("aria-expanded", "false");
      navLinks.classList.remove("is-open");
      document.body.classList.remove("nav-open");
    }
  });
}

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
      const icon = createElement("span", "service-icon", String(index + 1).padStart(2, "0"));
      icon.setAttribute("aria-hidden", "true");
      card.append(icon, createElement("h3", "", service.title), createElement("p", "", service.description));
      return card;
    }),
  );
};

const renderCities = (cities) => {
  const cityList = document.querySelector(".city-list");
  if (!cityList || !Array.isArray(cities) || cities.length === 0) return;

  cityList.replaceChildren(...cities.map((city) => createElement("li", "", city)));
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

const hydrateContent = async () => {
  try {
    const response = await fetch("/site-content.json");
    if (!response.ok) return;

    const data = await response.json();
    renderServices(data.services);
    renderCities(data.business?.serviceArea);
    renderFaq(data.faq);
  } catch {
    // The page includes static SEO content, so a JSON loading issue should not block the site.
  }
};

hydrateContent();

if (quoteForm && formNote) {
  quoteForm.addEventListener("submit", (event) => {
    event.preventDefault();

    if (!quoteForm.checkValidity()) {
      quoteForm.reportValidity();
      return;
    }

    const formData = new FormData(quoteForm);
    const name = formData.get("name")?.toString().trim() || "Website visitor";
    const phone = formData.get("phone")?.toString().trim() || "";
    const email = formData.get("email")?.toString().trim() || "";
    const message = formData.get("message")?.toString().trim() || "";

    const body = encodeURIComponent(
      `Name: ${name}\nPhone: ${phone}\nEmail: ${email}\n\nProject details:\n${message}`,
    );
    const subject = encodeURIComponent(`Electrical estimate request from ${name}`);
    const mailto = `mailto:info@prestigeelectricalcontractors.com?subject=${subject}&body=${body}`;

    formNote.innerHTML = `Your quote request is ready. <a href="${mailto}">Open your email app</a> or call <a href="tel:+18165489601">+1 (816) 548-9601</a>.`;
    quoteForm.querySelector("button")?.focus();
  });
}
