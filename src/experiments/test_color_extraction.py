import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.adapters.color_extractor_adapter import ColorExtractorAdapter

def test_colors():
    url = "https://veelapp.com/"
    print(f"Testing ColorExtractorAdapter with URL: {url}")
    
    adapter = ColorExtractorAdapter()
    result = adapter.extract_colors(url)
    
    print("\n--- Extracted Colors ---")
    print(f"Primary: {result.primary}")
    print(f"Secondary: {result.secondary}")
    
    print("\nCheck data/outputs for the colors json and palette image.")

if __name__ == "__main__":
    test_colors()
