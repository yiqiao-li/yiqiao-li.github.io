#!/usr/bin/env python3
"""Convert project SVG placeholders to PNG files. Uses svglib + reportlab (pure Python, no Cairo)."""

import subprocess
import sys
from pathlib import Path

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

OUTPUT_WIDTH = 800


def ensure_deps():
    for pkg in ["svglib", "reportlab"]:
        try:
            if pkg == "svglib":
                __import__("svglib")
            else:
                __import__("reportlab")
        except ImportError:
            print(f"Installing {pkg}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"], capture_output=True)


def main():
    ensure_deps()

    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPM

    for svg_name in SVG_FILES:
        svg_path = IMG_DIR / svg_name
        png_name = svg_name.replace(".svg", ".png")
        png_path = IMG_DIR / png_name

        if not svg_path.exists():
            print(f"Skipping {svg_name}: file not found")
            continue

        try:
            drawing = svg2rlg(str(svg_path))
            if drawing is None:
                print(f"Error: could not parse {svg_name}")
                continue

            scale = OUTPUT_WIDTH / drawing.width
            drawing.width = OUTPUT_WIDTH
            drawing.height = int(drawing.height * scale)
            drawing.scale(scale, scale)

            renderPM.drawToFile(drawing, str(png_path), fmt="PNG")
            print(f"Converted: {svg_name} -> {png_name}")
        except Exception as e:
            print(f"Error converting {svg_name}: {e}")

    print("Done.")


if __name__ == "__main__":
    main()
