from ..ports.visual_extraction_port import ColorExtractorPort
from ..domain.models.visual_identity import ColorPalette, Typography
from typing import Tuple
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw
from sklearn.cluster import KMeans
import numpy as np
import json
from pathlib import Path
from urllib.parse import urlparse

class ColorExtractorAdapter(ColorExtractorPort):
    def extract_colors(self, url: str) -> Tuple[ColorPalette, Typography]:
        outputs_dir = Path("data")
        outputs_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. Take a screenshot & extract typography
        screenshot_path = outputs_dir / "screenshot.png"
        heading_font = None
        body_font = None
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            try:
                page.goto(url, wait_until="networkidle", timeout=30000)
                # Extract typography
                heading_font = page.evaluate("window.getComputedStyle(document.querySelector('h1, h2, h3') || document.body).fontFamily")
                body_font = page.evaluate("window.getComputedStyle(document.querySelector('p, span') || document.body).fontFamily")
            except Exception as e:
                print(f"Warning: Page load issue or timeout: {e}")
            page.screenshot(path=screenshot_path)
            browser.close()
            
        typography = Typography(heading_font=heading_font, body_font=body_font)
            
        # 2. Extract colors
        img = Image.open(screenshot_path)
        img = img.convert("RGB")
        img.thumbnail((200, 200)) # Resize for faster processing
        
        pixels = np.array(img).reshape(-1, 3)
        kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
        kmeans.fit(pixels)
        
        colors = kmeans.cluster_centers_.astype(int)
        
        # Sort by frequency
        labels = kmeans.labels_
        counts = np.bincount(labels)
        sorted_indices = np.argsort(counts)[::-1]
        sorted_colors = colors[sorted_indices]
        
        hex_colors = ["#{:02x}{:02x}{:02x}".format(c[0], c[1], c[2]) for c in sorted_colors]
        
        # Separate primary and secondary based on frequency
        primary = hex_colors[:2]
        secondary = hex_colors[2:5]
        
        # 3. Save to JSON
        colors_json_path = outputs_dir / "colors.json"
        with open(colors_json_path, "w") as f:
            json.dump({"primary": primary, "secondary": secondary, "typography": {"heading": heading_font, "body": body_font}}, f, indent=4)
            
        # 4. Generate Palette Visualization
        palette_path = outputs_dir / "palette.png"
        self._generate_palette_image(hex_colors, palette_path)
        
        # Clean up the raw screenshot as the task only specified palette output and crawler already saves its own.
        # Retain the screenshot instead of deleting it
        pass
            
        return ColorPalette(primary=primary, secondary=secondary), typography

    def _generate_palette_image(self, hex_colors: list[str], output_path: Path):
        swatch_size = 100
        img_width = swatch_size * len(hex_colors)
        img_height = swatch_size
        img = Image.new("RGB", (img_width, img_height))
        draw = ImageDraw.Draw(img)
        
        for i, hex_color in enumerate(hex_colors):
            h = hex_color.lstrip('#')
            rgb = tuple(int(h[j:j+2], 16) for j in (0, 2, 4))
            draw.rectangle(
                [i * swatch_size, 0, (i + 1) * swatch_size, swatch_size],
                fill=rgb
            )
        img.save(output_path)
