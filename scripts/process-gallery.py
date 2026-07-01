#!/usr/bin/env python3
"""Download gallery photos from Google Drive and process them into uniform square images."""

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = ROOT / "assets" / "gallery-source"
OUTPUT_DIR = ROOT / "assets" / "gallery"
SITE_CONTENT = ROOT / "site-content.json"
DRIVE_FOLDER_ID = "1_Q7DIbpggrhRhwEBmds4dZTLgchnfglA"
DRIVE_URL = f"https://drive.google.com/drive/folders/{DRIVE_FOLDER_ID}"
SQUARE_SIZE = 800
JPEG_QUALITY = 85
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".heic", ".heif", ".bmp", ".tiff"}


def download_drive_folder():
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    for child in SOURCE_DIR.iterdir():
        if child.is_file():
            child.unlink()
        elif child.is_dir():
            shutil.rmtree(child)

    cmd = [
        sys.executable,
        "-m",
        "gdown",
        "--folder",
        DRIVE_URL,
        "-O",
        str(SOURCE_DIR),
        "--remaining-ok",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        stderr = (result.stderr or result.stdout or "").strip()
        raise RuntimeError(stderr or "gdown failed to download the Google Drive folder.")


def collect_source_images():
    images = []
    for path in sorted(SOURCE_DIR.rglob("*")):
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS:
            images.append(path)
    return images


def make_alt_text(filename):
    stem = Path(filename).stem
    cleaned = re.sub(r"[_\-]+", " ", stem).strip()
    if re.fullmatch(r"(?i)(img|dsc|photo|image)?\s*\d+", cleaned.replace(" ", "")):
        return "Electrical project completed by Prestige Electric in the Kansas City metro"
    if len(cleaned) < 4 or cleaned.isdigit():
        return "Electrical project completed by Prestige Electric in the Kansas City metro"
    return f"{cleaned[0].upper()}{cleaned[1:]}"


def process_image(source_path, output_path):
    with Image.open(source_path) as img:
        img = ImageOps.exif_transpose(img)
        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")
        width, height = img.size
        side = min(width, height)
        left = (width - side) // 2
        top = (height - side) // 2
        cropped = img.crop((left, top, left + side, top + side))
        resized = cropped.resize((SQUARE_SIZE, SQUARE_SIZE), Image.Resampling.LANCZOS)
        resized.save(output_path, "JPEG", quality=JPEG_QUALITY, optimize=True)


def update_site_content(images):
    with open(SITE_CONTENT, encoding="utf-8") as handle:
        data = json.load(handle)

    gallery = data.setdefault("gallery", {})
    gallery.setdefault(
        "seo",
        {
            "title": "See Our Work | Prestige Electric",
            "metaDescription": "Browse electrical projects completed by Prestige Electric across the Kansas City metro, including panel upgrades, repairs, and wiring work.",
            "h1": "See Our Work",
            "intro": "Recent electrical projects from homes and businesses across Belton, Lee's Summit, Overland Park, and the greater Kansas City area.",
        },
    )
    gallery["images"] = images
    gallery["squareSize"] = SQUARE_SIZE

    with open(SITE_CONTENT, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def main():
    skip_download = "--skip-download" in sys.argv

    if not skip_download:
        try:
            download_drive_folder()
            print(f"Downloaded photos from Google Drive into {SOURCE_DIR}")
        except Exception as error:
            print(f"Drive download failed: {error}")
            if not collect_source_images():
                print(
                    "\nThe Google Drive folder must be shared as 'Anyone with the link' (Viewer), "
                    "or you can place photos in assets/gallery-source/ and rerun with --skip-download."
                )
                sys.exit(1)
            print("Using images already in assets/gallery-source/")

    source_images = collect_source_images()
    if not source_images:
        print("No images found to process.")
        sys.exit(1)

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    gallery_images = []
    for index, source_path in enumerate(source_images, start=1):
        filename = f"prestige-electric-work-{index:02d}.jpg"
        output_path = OUTPUT_DIR / filename
        process_image(source_path, output_path)
        gallery_images.append(
            {
                "src": f"/assets/gallery/{filename}",
                "alt": make_alt_text(source_path.name),
                "width": SQUARE_SIZE,
                "height": SQUARE_SIZE,
            }
        )
        print(f"Processed {source_path.name} -> {filename}")

    update_site_content(gallery_images)
    print(f"\nDone. {len(gallery_images)} square gallery images saved to assets/gallery/")
    print("Run: python3 scripts/build-pages.py")


if __name__ == "__main__":
    main()
