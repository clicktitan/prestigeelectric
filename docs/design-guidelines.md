# Electrician Website Design Guidelines

Use `docs/electrician-website-guidelines.json` as the authoritative design and build ruleset for this project. The JSON file was provided as the project guideline source and should be treated as a requirement document, not optional inspiration.

## How to use these guidelines

1. Read the JSON before designing or implementing any page, component, SEO metadata, form flow, or content.
2. Apply the highest-priority rules first when requirements conflict.
3. Do not invent business facts. Anything marked `PLACEHOLDER_*` in the JSON must be replaced with confirmed client data or left clearly flagged.
4. Before marking a page or feature complete, check it against the `qualityChecklist.items` array in the JSON.
5. Preserve the action-color rule: the accent color is reserved for conversion actions such as call buttons, request-service buttons, and approved offers.

## Critical product principles

- Make click-to-call visible and tappable above the fold on every page and viewport.
- Address customer anxiety in the hero with safety, trust, pricing, and urgency reassurance.
- Place trust badges high on the page: licensed/insured status, reviews, years in business, and BBB only if applicable.
- Design mobile-first for stressed, one-handed users with 48px minimum tap targets.
- Give every major service a dedicated, indexable page with unique, substantive copy.
- Combine persuasive plain-spoken copy with SEO structure, schema, and internal linking.

## Required business facts

Confirm these before launch and do not fabricate them:

- Business name
- Kansas and Missouri phone numbers
- Email and street address
- Hours and emergency-service availability
- Founding year
- License statement and insurance details
- BBB accreditation status
- Review count, average rating, and Google Business Profile URL
- Real testimonials, job details, technician names, and project photography

## Design-system defaults

| Token | Value | Role |
| --- | --- | --- |
| Primary | `#0B3D66` | Brand, headers, navigation |
| Primary dark | `#072A47` | Footer and primary hover states |
| Accent | `#F5A300` | CTAs only |
| Accent hover | `#D98C00` | CTA hover and active states |
| Neutral dark | `#1A1A1A` | Body text |
| Neutral mid | `#5A5A5A` | Secondary text |
| Neutral light | `#F4F6F8` | Alternating section backgrounds |
| Success | `#1E8E3E` | Form success and trust ticks |

Typography should use a legible sans-serif stack with fluid headings, body text no smaller than 16px on mobile, and generous line height.

## Page completion checklist

A page is not complete until it satisfies the JSON checklist, including:

- Header click-to-call and sticky mobile call/request bar.
- Hero value proposition, primary CTA, and trust badge row.
- Short server-handled request form with honeypot/rate-limit protection.
- Pricing-transparency promise using only claims the client can truthfully make.
- Named, job-specific testimonials from real reviews.
- Service-area block with map and truthful metro-area references.
- Unique title, meta description with phone number, canonical, OG/Twitter tags, and appropriate JSON-LD.
- Semantic HTML, one H1, descriptive image alt text, keyboard-accessible links and forms.
- Mobile testing for no horizontal scroll and minimum 48px tap targets.
- Performance targets: LCP under 2.5s, CLS under 0.1, INP under 200ms.

## Implementation note

This repository currently contains the guideline documentation only. When the website application is added, encode these rules in shared design tokens, reusable CTA/trust/form components, page templates, metadata helpers, schema helpers, and tests or checks where practical.
