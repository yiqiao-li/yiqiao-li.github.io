#!/usr/bin/env python3
"""Convert project SVG placeholders to JPG files."""

import sys
from pathlib import Path

# Add project root for imports
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
IMG_DIR = PROJECT_ROOT / "assets" / "img"

SVG_FILES = [
    "mllm_vru.svg",
    "vru_safety.svg",
    "curb_activity.svg",
    "cross_border_truck.svg",
    "inland_ports.svg",
    "lidar_freeway.svg",
    "truck_census.svg",
]


def main():
    try:
        import cairosvg
    except ImportError:
        print("Installing cairosvg...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "cairosvg", "-q"])
        import cairosvg

    for svg_name in SVG_FILES:
        svg_path = IMG_DIR / svg_name
        jpg_name = svg_name.replace(".svg", ".jpg")
        jpg_path = IMG_DIR / jpg_name

        if not svg_path.exists():
            print(f"Skipping {svg_name}: file not found")
            continue

        try:
            cairosvg.svg2png(
                url=str(svg_path),
                write_to=str(jpg_path.with_suffix(".png")),
                output_width=800,
            )
            # cairosvg doesn't do JPG directly; convert PNG to JPG via Pillow
            try:
                from PIL import Image
                png_path = jpg_path.with_suffix(".png")
                img = Image.open(png_path).convert("RGB")
                img.save(jpg_path, "JPEG", quality=90)
                png_path.unlink()
            except ImportError:
                print(f"  {svg_name} -> .png (run: pip install Pillow for JPG)")
                continue

            print(f"Converted: {svg_name} -> {jpg_name}")
        except Exception as e:
            print(f"Error converting {svg_name}: {e}")

    print("Done. Update project img fields from .svg to .jpg as needed.")


if __name__ == "__main__":
    main()
