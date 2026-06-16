import json
import logging
from typing import Any, Dict

# Disable basic logging formatting to rely on our custom formatter
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("brand_agent")
logger.setLevel(logging.INFO)

def log_event(category: str, event_data: Dict[str, Any]):
    """
    Logs an event in a structured format.
    Categories: AGENT, TOOL, STATE, HITL, GRAPH
    """
    valid_categories = {"AGENT", "TOOL", "STATE", "HITL", "GRAPH"}
    category_upper = category.upper()
    if category_upper not in valid_categories:
        category_upper = "SYSTEM"

    # Format the log line
    lines = [f"[{category_upper}]"]
    for key, value in event_data.items():
        if isinstance(value, (dict, list)):
            try:
                # Summarize long lists or strings inside dicts
                val_str = json.dumps(value)
                if len(val_str) > 200:
                    val_str = val_str[:200] + "... [TRUNCATED]"
            except Exception:
                val_str = str(value)[:200]
        else:
            val_str = str(value)
            if len(val_str) > 200:
                val_str = val_str[:200] + "... [TRUNCATED]"
        
        lines.append(f"{key.capitalize()}: {val_str}")
        
    print("\n".join(lines))
    print("-" * 40)
