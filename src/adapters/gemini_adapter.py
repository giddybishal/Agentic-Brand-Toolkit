import os
import time
from typing import Type, TypeVar
from dotenv import load_dotenv
from google import genai
from google.genai import types

from ..ports.llm_port import LLMPort

T = TypeVar('T')

class GeminiAdapter(LLMPort):
    def __init__(self):
        load_dotenv()
        keys_str = os.getenv("GEMINI_API_KEY", "")
        self.api_keys = [k.strip() for k in keys_str.split(',') if k.strip()]
        if not self.api_keys:
            raise ValueError("GEMINI_API_KEY is not set in the environment.")
        
        self.current_key_idx = 0
        self.client = genai.Client(api_key=self.api_keys[self.current_key_idx])
        base_retries = int(os.getenv("MAX_RETRIES", "3"))
        self.max_retries = max(base_retries, len(self.api_keys) * 2)

    def generate_structured_data(self, prompt: str, schema: Type[T]) -> T:
        retries = 0
        while retries < self.max_retries:
            try:
                response = self.client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=schema,
                    ),
                )
                
                if hasattr(response, 'parsed') and response.parsed is not None:
                    return response.parsed
                    
                return schema.model_validate_json(response.text)
                
            except Exception as e:
                error_msg = str(e).lower()
                print(f"Gemini API error (attempt {retries + 1}/{self.max_retries}): {e}")
                
                if "429" in error_msg or "resource_exhausted" in error_msg or "quota" in error_msg:
                    self.current_key_idx = (self.current_key_idx + 1) % len(self.api_keys)
                    print(f"Rate limit hit! Switching to API key #{self.current_key_idx + 1}/{len(self.api_keys)}...")
                    self.client = genai.Client(api_key=self.api_keys[self.current_key_idx])
                    # Minimal sleep when switching keys
                    time.sleep(1)
                else:
                    time.sleep(2 ** retries)
                    
                retries += 1
                if retries >= self.max_retries:
                    raise
