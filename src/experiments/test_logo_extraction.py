import sys
from pathlib import Path
import shutil

sys.path.append(str(Path(__file__).parent.parent.parent))

from src.adapters.logo_extractor_adapter import LogoExtractorAdapter

def test_logos():
    data_dir = Path("data")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    url = "https://veelapp.com/"
    print(f"Testing LogoExtractorAdapter with URL: {url}")
    
    adapter = LogoExtractorAdapter()
    result = adapter.extract_logos(url)
    
    print("\n--- Extracted Primary Logo ---")
    if not result:
        print("No logo candidates found.")
        return
        
    print(f"Selected logo URL/Path: {result.get('logo_url')}")
    print(f"Confidence score: {result.get('confidence')}")
    print("Ranking explanation:")
    for reason in result.get('reasoning', []):
        print(f"  - {reason}")
        
    print("\nCheck data/ for the downloaded file.")

if __name__ == "__main__":
    test_logos()
