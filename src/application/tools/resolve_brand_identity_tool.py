from typing import Dict, Any, Type
from pydantic import BaseModel, Field
from ddgs import DDGS
import json
from .base_tool import BrandTool

class ResolveBrandIdentityToolSchema(BaseModel):
    brand_query: str = Field(description="The brand name or query to resolve.")

class ResolveBrandIdentityTool(BrandTool):
    name = "resolve_brand_identity"
    description = """
    Dependency:
    - Requires: A brand name mentioned by the user where the exact URL is unknown.
    - Produces: Resolved brand URL (`website_url`), identity, and basic industry info.
    - Used by: crawl_website, competitor_discovery
    
    Rule: This tool MUST be called FIRST if the `website_url` is not already Present in the state.
    Do NOT guess or hallucinate the URL. Use this tool to ground it.
    """
    args_schema = ResolveBrandIdentityToolSchema

    def execute(self, state: Dict[str, Any], args: Dict[str, Any]) -> Dict[str, Any]:
        query = args.get("brand_query", "")
        print(f"[*] Tool executing: Resolving brand identity for '{query}' using Gemini exclusively...")
        
        url = None
        
        import os
        import time
        from urllib.parse import urlparse
        from langchain_google_genai import ChatGoogleGenerativeAI
        
        def get_root_domain(link: str) -> str:
            if not link.startswith("http"):
                link = "https://" + link
            parsed = urlparse(link)
            return f"{parsed.scheme}://{parsed.netloc}"
            
        SOCIAL_DOMAINS = ["instagram.com", "facebook.com", "twitter.com", "x.com", "linkedin.com", "tiktok.com", "youtube.com", "pinterest.com", "amazon.com", "wikipedia.org"]

        keys_str = os.getenv("GEMINI_API_KEY", "")
        api_keys = [k.strip() for k in keys_str.split(',') if k.strip()]
        
        prompt = f"What is the exact official primary website URL for the brand '{query}'? Respond ONLY with the https:// URL. Do not return social media links, Wikipedia, or generic stores. If you are not completely sure, respond with UNKNOWN."
        max_retries = max(3, len(api_keys) * 2) if api_keys else 3
        
        for attempt in range(max_retries):
            try:
                key_to_use = api_keys[attempt % len(api_keys)] if api_keys else None
                llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.0, api_key=key_to_use)
                llm_response = llm.invoke(prompt)
                
                candidate = llm_response.content.strip()
                if candidate and "http" in candidate and "UNKNOWN" not in candidate:
                    candidate_domain = urlparse(candidate).netloc.lower()
                    is_social = any(soc in candidate_domain for soc in SOCIAL_DOMAINS)
                    
                    if not is_social:
                        url = get_root_domain(candidate)
                        print(f"    Gemini resolved root URL: {url}")
                        break
                    else:
                        print(f"    Gemini suggested social/generic URL, retrying...")
                else:
                    print(f"    Gemini uncertain or failed: {candidate}")
                    break
            except Exception as e:
                error_msg = str(e).lower()
                if "429" in error_msg or "quota" in error_msg or "resource_exhausted" in error_msg:
                    print(f"    Rate limit hit in Resolver Tool! Switching keys and retrying...")
                    time.sleep(1)
                else:
                    print(f"    LLM Error in Tool: {e}")
                    break

        # Final Verification
        if url:
            resolution = {
                "brand_name": query,
                "official_url": url,
                "confidence": 0.9,
                "source": "gemini_knowledge"
            }
            return {
                "website_url": url,
                "resolved_brand_name": query,
                "resolved_url": url,
                "resolution_confidence": 0.9,
                "human_approved_url": False,
                "tool_message": f"Successfully resolved brand identity: {json.dumps(resolution)}. The website_url '{url}' is now in memory. Pausing for human validation."
            }
        else:
            return {"tool_message": "Could not confidently determine the official URL. Please ask the user to provide it directly."}
