# Prestige Electric Website

Static marketing website for Prestige Electric, a family owned electrician serving the Kansas City metro.

## What is included

- Homepage with about section, services, locations, FAQ, quote form, and Google Maps embed
- Dedicated service pages for each core offering
- Dedicated location pages for each city served
- SEO metadata, JSON-LD structured data, sitemap, and robots.txt
- Shared header/footer loaded from `site-content.json`
- Company logo and NAP information in the footer

## Business content source

Primary business details live in `site-content.json`, sourced from the onboarding survey.

## Run locally

```bash
python3 -m http.server 5173 --bind 127.0.0.1
```

Or with Vite when Node is installed:

```bash
npm install
npm run dev
```

## Regenerate service and location pages

After editing `site-content.json`:

```bash
python3 scripts/build-pages.py
```

## Gallery photos

To download photos from Google Drive, crop them to uniform squares, and update the See Our Work page:

```bash
python3 scripts/process-gallery.py
python3 scripts/build-pages.py
```

Place source photos in `assets/gallery-source/` and run with `--skip-download` if you are not using Drive.

## Build

```bash
npm run build
```

The production build is generated in `dist/`.

## Pages

- `/`
- `/our-work.html`
- `/services/service-upgrades.html`
- `/services/panel-replacements.html`
- `/services/hot-tubs.html`
- `/services/troubleshooting.html`
- `/locations/belton-mo.html`
- `/locations/lees-summit-mo.html`
- `/locations/overland-park-ks.html`
- `/locations/leawood-ks.html`
- `/locations/lenexa-ks.html`
- `/locations/olathe-ks.html`
