import json
import os

root = os.path.join(os.path.dirname(__file__), "..")
content_path = os.path.join(os.path.dirname(__file__), "enhanced-location-content.json")
site_path = os.path.join(root, "site-content.json")

with open(content_path, encoding="utf-8") as f:
    enhanced = json.load(f)

with open(site_path, encoding="utf-8") as f:
    data = json.load(f)

updated = []
for location in data["locations"]:
    slug = location["slug"]
    if slug not in enhanced:
        continue
    payload = enhanced[slug]
    location["seo"] = payload["seo"]
    location["page"] = payload["page"]
    location["faqs"] = payload["faqs"]
    updated.append(slug)

with open(site_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")

print(f"Updated enhanced content for: {', '.join(updated)}")
