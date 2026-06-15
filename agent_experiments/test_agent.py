import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.main import main as app_main

def main():
    print("Running Full Agent Execution Test...")
    print("This will execute the BrandIntelligenceAgent on drinklucent.com")
    print("Watch the console to see the LLM autonomously selecting tools.\n")
    
    # We can just call the main function from the application
    # Because it now uses the BrandIntelligenceAgent and prints traces!
    sys.argv = ["test_agent.py", "https://www.drinklucent.com/"]
    app_main()
    
    print("\nTest Completed: Check data/current/ for generated artifacts.")

if __name__ == "__main__":
    main()
