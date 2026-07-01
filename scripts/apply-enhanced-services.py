import json
import os

root = os.path.join(os.path.dirname(__file__), "..")
content_path = os.path.join(os.path.dirname(__file__), "enhanced-service-content.json")
site_path = os.path.join(root, "site-content.json")

with open(content_path, encoding="utf-8") as f:
    enhanced = json.load(f)

with open(site_path, encoding="utf-8") as f:
    data = json.load(f)

slugs = set(enhanced.keys())
updated = []

for service in data["services"]:
    slug = service["slug"]
    if slug not in enhanced:
        continue
    payload = enhanced[slug]
    service["seo"] = payload["seo"]
    service["page"] = payload["page"]
    service["faqs"] = payload["faqs"]
    updated.append(slug)

with open(site_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")

print(f"Updated enhanced content for: {', '.join(updated)}")
