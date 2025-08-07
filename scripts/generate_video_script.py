#!/usr/bin/env python3
"""
Miss Gracy Baby Video Script Generator
Generates engaging video scripts using a live LLM from the internet.
"""

import json
import os
import sys
import requests
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

# --- Configuration for the Public LLM ---
# Using a public, instruction-tuned model from Hugging Face Spaces.
# This requires no API key but is subject to availability and rate limits.
LLM_API_URL = "https://huggingface.co/spaces/mistralai/Mixtral-8x7B-Instruct-v0.1/api/predict"

class VideoScriptGenerator:
    def __init__(self, config_path: Optional[str] = None):
        """
        Initializes the script generator.
        The config_path is kept for compatibility but is not used for the LLM call.
        """
        self.video_structure = self._load_video_structure()
        self.pillar_templates = self._load_pillar_templates()

    def _load_json_file(self, file_path: str, default: Dict) -> Dict:
        """Loads a JSON file with error handling."""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: {os.path.basename(file_path)} not found. Using default.", file=sys.stderr)
            return default
        except json.JSONDecodeError:
            print(f"Error: Could not decode {os.path.basename(file_path)}.", file=sys.stderr)
            return default

    def _load_video_structure(self) -> Dict:
        """Loads the video structure template."""
        return self._load_json_file(
            "prompt-templates/video-structure-template.json",
            {"sections": {}}
        )

    def _load_pillar_templates(self) -> Dict:
        """Loads content pillar templates."""
        return self._load_json_file(
            "prompt-templates/content-pillar-templates.json",
            {}
        )

    def _generate_prompt(self, pillar: str, category: str, subcategory: str, baby_age: str) -> str:
        """Generates a detailed, structured prompt for the LLM."""
        if not self.pillar_templates or pillar not in self.pillar_templates:
            # Fallback if templates are missing
            return f"Create a 2-minute YouTube video script about {subcategory} for a baby aged {baby_age}."

        pillar_data = self.pillar_templates[pillar]
        category_data = pillar_data.get("categories", {}).get(category, {})
        
        prompt = f"""
You are a creative scriptwriter for a YouTube channel about a baby named Gracy.
Your task is to generate a complete, engaging video script.

**Instructions:**
1.  The script must be for a baby named Gracy who is **{baby_age}**.
2.  The topic is **"{subcategory}"** within the broader theme of **"{pillar_data['name']}"**.
3.  The target audience is **{pillar_data['target_audience']}**.
4.  The tone should be warm, engaging, and authentic.
5.  Structure your response with the following clear headings: `[TITLE]`, `[HOOK]`, `[SETUP]`, `[MAIN CONTENT]`, `[EDUCATIONAL ELEMENT]`, and `[CONCLUSION]`.
6.  Do not add any other commentary or text outside of these sections.

Here is the content for each section:
-   **[TITLE]:** A catchy, SEO-friendly title for the video.
-   **[HOOK] (0-15 seconds):** A high-energy, attention-grabbing opening.
-   **[SETUP] (15-30 seconds):** Briefly explain the activity or what's about to happen.
-   **[MAIN CONTENT] (30 seconds - 3 minutes):** The core of the video. Describe the scenes, actions, and Gracy's reactions. Write this as a narrative.
-   **[EDUCATIONAL ELEMENT] (30 seconds):** A quick, valuable tip or insight for parents related to the activity.
-   **[CONCLUSION] (30 seconds):** A warm summary and a clear call-to-action (e.g., "subscribe," "comment below").

Begin the script now.
"""
        return prompt

    def _query_llm(self, prompt: str) -> str:
        """
        Sends the prompt to the public LLM API and returns the response.
        """
        print("Querying the LLM... This may take a moment.")
        payload = {
            "data": [
                prompt, # The prompt text
                None,   # No history needed
                0.9,    # Temperature
                1024,   # Max new tokens
                0.95,   # Top-p
                1.0,    # Repetition penalty
            ]
        }
        try:
            response = requests.post(LLM_API_URL, json=payload, timeout=120) # 120-second timeout
            response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx) 
            
            result = response.json()
            generated_text = result.get("data", [""])[0]
            
            if not generated_text:
                raise ValueError("LLM returned an empty response.")
                
            print("LLM query successful.")
            return generated_text

        except requests.exceptions.RequestException as e:
            print(f"Error querying LLM: {e}", file=sys.stderr)
            raise ConnectionError(f"Failed to connect to the LLM. Please check your internet connection. Error: {e}")
        except (ValueError, KeyError) as e:
            print(f"Error processing LLM response: {e}", file=sys.stderr)
            raise ValueError(f"Could not get a valid response from the LLM. It might be busy or down. Error: {e}")

    def _parse_llm_output(self, llm_text: str) -> Dict:
        """Parses the raw text from the LLM into a structured script dictionary."""
        print("Parsing LLM response...")
        script = {}
        # Regex to find all content between section markers (e.g., [HOOK]...[SETUP])
        pattern = r""\[(.*?)\](.*?)(?=\[|$)"""
        matches = re.findall(pattern, llm_text, re.DOTALL)

        if not matches:
            # If parsing fails, return the whole text as main content
            return {
                "title": "AI Generated Script",
                "main_content": {"content": llm_text.strip()}
            }

        for match in matches:
            section_title = match[0].strip().lower().replace(" ", "_")
            content = match[1].strip()
            
            if section_title == "title":
                script[section_title] = content
            else:
                script[section_title] = {"content": content}
        
        print("Parsing complete.")
        return script

    def generate_script(self, pillar: str, category: str, subcategory: str, baby_age: str) -> Dict:
        """
        Generates a complete video script by querying a live LLM.
        """
        prompt = self._generate_prompt(pillar, category, subcategory, baby_age)
        
        # Query the LLM
        llm_response_text = self._query_llm(prompt)
        
        # Parse the response
        structured_script = self._parse_llm_output(llm_response_text)
        
        return {
            "metadata": {
                "pillar": pillar,
                "category": category,
                "subcategory": subcategory,
                "baby_age": baby_age,
                "generated_at": datetime.now().isoformat(),
                "source": "Live LLM"
            },
            "script": structured_script
        }

if __name__ == '__main__':
    # Example of how to run this script directly for testing
    if len(sys.argv) < 4:
        print("Usage: python generate_video_script.py <pillar> <category> <subcategory> [baby_age]")
        sys.exit(1)
        
    pillar_arg = sys.argv[1]
    category_arg = sys.argv[2]
    subcategory_arg = sys.argv[3]
    baby_age_arg = sys.argv[4] if len(sys.argv) > 4 else "10 months"

    print(f"--- Generating Script for: {pillar_arg}/{category_arg}/{subcategory_arg} ---")
    generator = VideoScriptGenerator()
    try:
        final_script = generator.generate_script(pillar_arg, category_arg, subcategory_arg, baby_age_arg)
        print("\n--- Generated Script ---")
        print(json.dumps(final_script, indent=2))
        
        # Save to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated-scripts/video_script_{timestamp}.json"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(final_script, f, indent=2)
        print(f"\nScript saved to: {filename}")

    except (ConnectionError, ValueError) as e:
        print(f"\n--- Script Generation Failed ---", file=sys.stderr)
        print(e, file=sys.stderr)
        sys.exit(1)
